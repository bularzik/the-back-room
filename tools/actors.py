"""dnd5e (2024 rules) actor builders for The Back Room."""
import hashlib, re

def slug(n): return re.sub(r"[^a-z0-9]+", "-", n.lower()).strip("-")

MOD = "modules/the-back-room"

def uid(*parts):
    h = hashlib.sha1("|".join(parts).encode()).hexdigest()
    alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    n = int(h, 16); out = ""
    for _ in range(16): out += alpha[n % 62]; n //= 62
    return out

SRC = {"revision": 1, "rules": "2024", "book": "The Back Room", "license": ""}
VIS = {"level": {}, "requireAttunement": False, "requireIdentification": False, "requireMagic": False}

def _act(aid, typ, act_type="action", act_value=None, extra=None, rng=None, target=None, name=""):
    a = {"_id": aid, "type": typ, "name": name, "sort": 0, "img": None, "flags": {},
         "activation": {"type": act_type, "value": act_value, "override": False, "condition": ""},
         "consumption": {"scaling": {"allowed": False}, "spellSlot": True, "targets": []},
         "description": {"chatFlavor": ""}, "duration": {"units": "inst", "concentration": False, "override": False},
         "effects": [], "range": rng or {"override": False, "units": "self"},
         "target": target or {"template": {"contiguous": False, "units": "ft", "type": ""},
                               "affects": {"choice": False, "type": ""}, "override": False, "prompt": True},
         "uses": {"spent": 0, "recovery": [], "max": ""}, "visibility": VIS}
    if extra: a.update(extra)
    return a

def dmg_part(n, d, types, bonus=""):
    return {"custom": {"enabled": False, "formula": ""}, "number": n, "denomination": d, "bonus": bonus,
            "types": types, "scaling": {"number": 1}}

def _item(actor_id, iid, name, typ, img, system, sort):
    return {"_id": iid, "name": name, "type": typ, "img": img, "system": system, "effects": [], "flags": {},
            "folder": None, "sort": sort, "ownership": {"default": 0},
            "_key": f"!actors.items!{actor_id}.{iid}"}

class Monster:
    def __init__(self, key, name, cr, size, ctype, align, ac, hp, hp_formula, abilities, speed,
                 token, senses=None, skills=None, saves=(), di=(), dr=(), dv=(), ci=(), languages="",
                 lang_values=(), swarm="", subtype="", bio="", disposition=-1, legact=0, legres=0,
                 ac_calc="natural", tsize=1, init_bonus=""):
        self.id = uid("actor", key); self.items = []; self.sort = 0
        timg = token if token.startswith("icons/") else f"{MOD}/tokens/{token}.webp"
        prof = 2 if cr < 5 else 3 if cr < 9 else 4 if cr < 13 else 5
        ab = {}
        for k, v in zip(["str", "dex", "con", "int", "wis", "cha"], abilities):
            ab[k] = {"value": v, "proficient": 1 if k in saves else 0, "bonuses": {"check": "", "save": ""}}
        sk = {}
        for k, lvl in (skills or {}).items(): sk[k] = {"value": lvl}
        mv = {"walk": 0, "units": "ft", "hover": False}
        mv.update(speed)
        self.doc = {
            "_id": self.id, "name": name, "type": "npc", "img": timg,
            "system": {
                "abilities": ab, "skills": sk,
                "attributes": {
                    "ac": {"calc": ac_calc, "flat": ac},
                    "hp": {"value": hp, "max": hp, "temp": None, "tempmax": None, "formula": hp_formula},
                    "init": {"ability": "", "bonus": init_bonus},
                    "movement": mv,
                    "senses": {"units": "ft", "special": "", "ranges": senses or {}},
                    "spellcasting": "int",
                },
                "details": {"biography": {"value": bio, "public": ""}, "alignment": align,
                            "type": {"value": ctype, "subtype": subtype, "swarm": swarm, "custom": ""},
                            "cr": cr, "habitat": {"value": [{"type": "planar", "subtype": "The Back Room"}], "custom": ""}},
                "resources": {"legact": {"max": legact, "spent": 0}, "legres": {"max": legres, "spent": 0},
                              "lair": {"value": False, "initiative": None, "inside": False}},
                "source": SRC,
                "traits": {"size": size,
                           "di": {"value": list(di), "custom": "", "bypasses": []},
                           "dr": {"value": list(dr), "custom": "", "bypasses": []},
                           "dv": {"value": list(dv), "custom": "", "bypasses": []},
                           "ci": {"value": list(ci), "custom": ""},
                           "languages": {"value": list(lang_values), "custom": languages}},
            },
            "prototypeToken": {"name": name, "displayName": 20, "actorLink": False, "disposition": disposition,
                               "displayBars": 20, "bar1": {"attribute": "attributes.hp"}, "width": tsize, "height": tsize,
                               "texture": {"src": timg, "scaleX": 1, "scaleY": 1},
                               "sight": {"enabled": False}, "appendNumber": True},
            "items": self.items, "effects": [], "folder": None, "sort": 0, "flags": {},
            "ownership": {"default": 0}, "_key": f"!actors!{self.id}",
        }

    def _next(self): self.sort += 100000; return self.sort

    def trait(self, name, html, img="icons/magic/symbols/question-stone-yellow.webp"):
        iid = uid(self.id, name)
        sysd = {"type": {"value": "monster", "subtype": ""}, "activities": {}, "uses": {"spent": 0, "recovery": [], "max": ""},
                "description": {"value": html, "chat": ""}, "identifier": slug(name),
                "source": SRC, "properties": ["trait"], "requirements": ""}
        self.items.append(_item(self.id, iid, name, "feat", img, sysd, self._next())); return self

    def attack(self, name, n, d, dtype, ability, kind="melee", reach=5, rng=None, extra_parts=(), note="",
               img="icons/creatures/claws/claw-curved-jagged-gray.webp", act_type="action", act_value=None):
        iid = uid(self.id, name); aid = uid(iid, "atk")
        act = _act(aid, "attack", act_type, act_value, {
            "attack": {"critical": {"threshold": None}, "flat": False, "type": {"value": kind, "classification": ""},
                       "ability": ability, "bonus": ""},
            "damage": {"critical": {"bonus": ""}, "includeBase": True, "parts": [dmg_part(*p) for p in extra_parts]}})
        desc = '<p class="feature">[[/attack extended]]. [[/damage average extended]].' + (f" {note}" if note else "") + "</p>"
        sysd = {"type": {"value": "natural", "baseItem": ""}, "activities": {aid: act},
                "uses": {"spent": 0, "recovery": [], "max": ""}, "description": {"value": desc, "chat": ""},
                "identifier": slug(name), "source": SRC, "quantity": 1, "equipped": True,
                "damage": {"base": {"number": n, "denomination": d, "types": [dtype], "custom": {"enabled": False},
                                    "scaling": {"number": 1}, "bonus": ""}},
                "properties": ["fin"] if ability == "dex" and kind == "melee" else [], "proficient": None,
                "range": {"value": rng[0] if rng else None, "long": rng[1] if rng else None, "reach": reach, "units": "ft"}}
        self.items.append(_item(self.id, iid, name, "weapon", img, sysd, self._next())); return self

    def save(self, name, ability, dc_from, parts, on_save, html, rng_ft=None, template=None, count="1",
             affects="creature", recharge=None, act_type="action", act_value=None, per_day=None,
             img="icons/magic/control/fear-fright-monster-grin-red-orange.webp"):
        iid = uid(self.id, name); aid = uid(iid, "save")
        rng = {"override": False, "units": "ft", "value": str(rng_ft)} if rng_ft else {"override": False, "units": "self"}
        tgt = {"template": {"contiguous": False, "units": "ft", "type": template[0] if template else "",
                            "size": str(template[1]) if template else ""},
               "affects": {"choice": False, "type": affects, "count": "" if template else count, "special": ""},
               "override": False, "prompt": True}
        act = _act(aid, "save", act_type, act_value, {
            "damage": {"parts": [dmg_part(*p) for p in parts], "onSave": on_save},
            "save": {"ability": [ability], "dc": {"calculation": dc_from, "formula": ""}}}, rng, tgt)
        uses = {"spent": 0, "recovery": [], "max": ""}
        if recharge: uses = {"spent": 0, "max": "1", "recovery": [{"period": "recharge", "formula": str(recharge), "type": "recoverAll"}]}
        if per_day: uses = {"spent": 0, "max": str(per_day), "recovery": [{"period": "day", "type": "recoverAll"}]}
        sysd = {"type": {"value": "monster", "subtype": ""}, "activities": {aid: act}, "uses": uses,
                "description": {"value": html, "chat": ""}, "identifier": slug(name),
                "source": SRC, "properties": [], "requirements": ""}
        self.items.append(_item(self.id, iid, name, "feat", img, sysd, self._next())); return self

    def utility(self, name, html, act_type="action", act_value=None, recharge=None, per_day=None,
                img="icons/magic/symbols/runes-star-orange-purple.webp"):
        iid = uid(self.id, name); aid = uid(iid, "use")
        act = _act(aid, "utility", act_type, act_value, {"roll": {"prompt": False, "visible": False}}, name="Use")
        uses = {"spent": 0, "recovery": [], "max": ""}
        if recharge: uses = {"spent": 0, "max": "1", "recovery": [{"period": "recharge", "formula": str(recharge), "type": "recoverAll"}]}
        if per_day: uses = {"spent": 0, "max": str(per_day), "recovery": [{"period": "day", "type": "recoverAll"}]}
        sysd = {"type": {"value": "monster", "subtype": ""}, "activities": {aid: act}, "uses": uses,
                "description": {"value": html, "chat": ""}, "identifier": slug(name),
                "source": SRC, "properties": [], "requirements": ""}
        self.items.append(_item(self.id, iid, name, "feat", img, sysd, self._next())); return self

M = "[[lookup @name lowercase]]{monster}"
def P(*paras): return "".join(f"<p>{x}</p>" for x in paras)


# Token art: tokens/token-<key>.webp, 512px round portraits generated with Draw Things (SD 1.5) and masked by tools/make_tokens.py.
TK = {k: f"token-{k}" for k in ("dragon", "unicorn", "centaur", "troll", "roper", "owlbear", "echo", "rogue", "barbarian", "wizard", "barkeep", "stranger",
                                "barmaid", "guard", "drunk", "merchant", "oldman",
                                "fred", "thon", "rorvik", "morlock", "strider")}

REMNANT_RULE = P("<strong>The Remnant Rule.</strong> When this creature drops to 0 Hit Points it does not die. At the start of its next turn it stands up in the pose it fell in, with all its Hit Points, and continues mid-sentence. The only way to be rid of it is to leave the room by a door it did not come through; it cannot follow.")

def build_monsters():
    """The Cover: the six monsters of the 1977 Monster Manual cover, misremembered (design doc, Encounters)."""
    out = {}

    # ---------- Red Dragon (wyrmling with a young dragon's breath) ----------
    m = Monster("cover-dragon", "Red Dragon (The Cover)", 6, "med", "dragon", "Chaotic Evil", 17, 75, "10d8 + 30",
                (19, 10, 17, 12, 11, 15), {"walk": 30, "climb": 30, "fly": 60}, TK["dragon"],
                senses={"blindsight": 10, "darkvision": 60}, skills={"prc": 2, "ste": 1}, saves=("dex", "wis"), di=("fire",),
                languages="Draconic", lang_values=("draconic",), subtype="chromatic",
                bio=P("The size it was on the cover: about the owlbear's size. Everybody's first party beat a red dragon at level 3, somehow. It never got to grow, so it is a wyrmling. Its breath, however, is the breath the table remembers.",
                      "<strong>Tableau.</strong> Rearing over the hoard, wings half open, jaw wide at nothing. It wakes only if a character steps into the gap in front of it, where the fighter with the shield stood."))
    m.trait("Still Fighting 1977", P(f"The {M} is frozen mid-battle and has the Incapacitated condition until a creature enters the person-shaped gap it is fighting. When it wakes, roll its Initiative; it acts immediately after the creature that woke it."))
    m.utility("Multiattack", P(f"The {M} makes two Rend attacks."), img="icons/skills/melee/strike-weapons-orange.webp")
    m.attack("Rend", 1, 10, "slashing", "str", extra_parts=[(1, 6, ["fire"])], img="icons/creatures/claws/claw-curved-jagged-gray.webp")
    m.save("Fire Breath (Young)", "dex", "con", [(16, 6, ["fire"])], "half",
           P(f"<em>Dexterity Saving Throw:</em> each creature in a 30-foot Cone. <em>Failure:</em> [[/damage average]] damage. <em>Success:</em> Half damage.",
             "The breath of a young dragon in a wyrmling's body. The first time it is used, every player at the table should recognise the number."),
           template=("cone", 30), recharge=5, img="icons/magic/fire/beam-jet-stream-embers.webp")
    out["dragon"] = m

    # ---------- Unicorn (hostile; its healing goes to the other monsters) ----------
    m = Monster("cover-unicorn", "Unicorn (The Cover)", 5, "lg", "celestial", "Lawful Good", 12, 97, "13d10 + 26",
                (18, 14, 15, 11, 17, 16), {"walk": 50}, TK["unicorn"], senses={"darkvision": 60}, di=("poison",),
                ci=("charmed", "paralyzed", "poisoned"), languages="Celestial, Elvish, Sylvan; telepathy 60 ft.",
                lang_values=("celestial", "elvish", "sylvan"), tsize=2,
                bio=P("On the monsters' side. It was in the Monster Manual, so it is a monster. It is confused about this, and its confusion does not slow it down.",
                      "<strong>Tableau.</strong> Rearing beside the troll, horn lowered at the gap where the elf stood."))
    m.trait("Still Fighting 1977", P(f"The {M} is frozen mid-battle and has the Incapacitated condition until a creature enters the gap it is fighting."))
    m.trait("Wrong Side", P(f"The {M}'s Healing Touch and Shimmering Shield can target only the other five monsters of the Cover. It will not heal a character under any circumstances, and does not understand why anyone would ask."))
    m.utility("Multiattack", P(f"The {M} makes one Hooves attack and one Radiant Horn attack."), img="icons/skills/melee/strike-weapons-orange.webp")
    m.attack("Hooves", 2, 6, "bludgeoning", "str", img="icons/creatures/mammals/horse-hooves-blue.webp")
    m.attack("Radiant Horn", 1, 8, "piercing", "str", extra_parts=[(2, 8, ["radiant"])], img="icons/magic/light/beam-rays-yellow.webp")
    m.utility("Healing Touch", P(f"The {M} touches one other monster of the Cover, which regains [[/heal 2d8+2]] Hit Points."), per_day=3, img="icons/magic/life/heart-cross-green.webp")
    m.utility("Shimmering Shield", P(f"The {M} grants one other monster of the Cover within 60 feet a +2 bonus to Armor Class until the start of the unicorn's next turn."), act_type="bonus", per_day=3, img="icons/magic/defensive/shield-barrier-glowing-blue.webp")
    m.utility("Charge", P(f"If the {M} moves at least 20 feet straight toward a target and then hits it with Radiant Horn, the target takes an extra [[/damage 2d8 piercing]] and must succeed on a DC 15 Strength saving throw or have the Prone condition."), img="icons/skills/movement/arrow-upward-yellow.webp")
    out["unicorn"] = m

    # ---------- Centaur (a bow with no arrows; it hits anyway) ----------
    m = Monster("cover-centaur", "Centaur (The Cover)", 2, "lg", "fey", "Neutral Good", 16, 45, "6d10 + 12",
                (18, 14, 14, 9, 13, 11), {"walk": 50}, TK["centaur"], skills={"ath": 1, "prc": 1, "sur": 1},
                languages="Elvish, Sylvan", lang_values=("elvish", "sylvan"), tsize=2,
                bio=P("Has a bow but no arrows, and shoots anyway. They hit. Nobody at the table ever tracked ammunition and the centaur is the proof.",
                      "<strong>Tableau.</strong> Drawing an empty bow at the gap on the ledge where the archer stood."))
    m.trait("Still Fighting 1977", P(f"The {M} is frozen mid-battle and has the Incapacitated condition until a creature enters the gap it is fighting."))
    m.trait("Nobody Tracked Arrows", P(f"The {M}'s Longbow needs no ammunition and ignores the Disadvantage normally imposed by Long Range. If a character asks what it is shooting, the answer is <em>arrows</em>, and there are none."))
    m.utility("Multiattack", P(f"The {M} makes two attacks, using Pike or Longbow in any combination."), img="icons/skills/melee/strike-weapons-orange.webp")
    m.attack("Pike", 1, 10, "piercing", "str", reach=10, img="icons/weapons/polearms/spear-simple-engraved.webp")
    m.attack("Longbow", 1, 8, "piercing", "dex", kind="ranged", reach=None, rng=(150, 600), img="icons/weapons/bows/longbow-recurve-leather-brown.webp")
    m.utility("Trampling Charge", P(f"If the {M} moves at least 20 feet straight toward a target and then hits it with Pike, the target must succeed on a DC 14 Strength saving throw or have the Prone condition. The centaur can then make one Hooves attack ([[/damage 2d6+4 bludgeoning]]) against it as a Bonus Action."), img="icons/skills/movement/arrow-upward-yellow.webp")
    out["centaur"] = m

    # ---------- Troll (regenerates the way the table remembers) ----------
    m = Monster("cover-troll", "Troll (The Cover)", 5, "lg", "giant", "Chaotic Evil", 15, 84, "8d10 + 40",
                (18, 13, 20, 7, 9, 7), {"walk": 30}, TK["troll"], senses={"darkvision": 60}, skills={"prc": 1},
                languages="Giant", lang_values=("giant",), tsize=2,
                bio=P("Regenerates the way the table remembers, not the way the rules say: it stands up at the start of its turn in the pose it fell in. This is the Remnant rule, previewed. Fire or acid still ends it, because everybody remembers that part.",
                      "<strong>Tableau.</strong> Mid-lunge at the gap by the treasure chest, where the dwarf stood."))
    m.trait("Still Fighting 1977", P(f"The {M} is frozen mid-battle and has the Incapacitated condition until a creature enters the gap it is fighting."))
    m.trait("Stands Back Up (Remnant Rule)", P(f"When the {M} drops to 0 Hit Points it does not die unless the damage that dropped it included Fire or Acid damage. At the start of its next turn it stands up in the pose it fell in with all its Hit Points. It has no other regeneration."))
    m.utility("Multiattack", P(f"The {M} makes three attacks: one Bite and two Claw attacks."), img="icons/skills/melee/strike-weapons-orange.webp")
    m.attack("Bite", 1, 6, "piercing", "str", img="icons/creatures/abilities/mouth-teeth-long-red.webp")
    m.attack("Claw", 2, 6, "slashing", "str", img="icons/creatures/claws/claw-curved-jagged-gray.webp")
    out["troll"] = m

    # ---------- Roper (looks like three different things from three angles) ----------
    m = Monster("cover-roper", "Roper (The Cover)", 5, "lg", "aberration", "Neutral Evil", 20, 93, "11d10 + 33",
                (18, 8, 17, 7, 16, 6), {"walk": 10, "climb": 20}, TK["roper"], senses={"darkvision": 60},
                skills={"prc": 3, "ste": 2}, languages="Deep Speech", lang_values=("deep",), tsize=2,
                bio=P("The one nobody could draw properly. It looks like three different things from three angles: a stalagmite, a rotted stump, a face. Describe it differently each round and never correct yourself.",
                      "<strong>Tableau.</strong> Tendrils out toward the gap at the cave mouth, where the thief was sneaking in."))
    m.trait("Still Fighting 1977", P(f"The {M} is frozen mid-battle and has the Incapacitated condition until a creature enters the gap it is fighting."))
    m.trait("False Appearance", P(f"If the {M} is motionless at the start of combat, it has Advantage on its Initiative roll. Moreover, if a creature hasn't observed it move or act, that creature must succeed on a DC 20 Intelligence (Investigation) check to discern that it is animate."))
    m.trait("Spider Climb", P(f"The {M} can climb difficult surfaces, including along ceilings, without needing to make an ability check."))
    m.utility("Multiattack", P(f"The {M} makes two Tendril attacks, uses Reel, and makes one Bite attack."), img="icons/skills/melee/strike-weapons-orange.webp")
    m.attack("Bite", 4, 8, "piercing", "str", img="icons/creatures/abilities/mouth-teeth-long-red.webp")
    m.attack("Tendril", 1, 4, "bludgeoning", "str", reach=60, note="If the target is Large or smaller, it has the Grappled condition (escape DC 14) and the Poisoned condition until the grapple ends. The roper has six tendrils; each can grapple one creature.", img="icons/creatures/tentacles/tentacle-earth-green.webp")
    m.utility("Reel", P(f"The {M} pulls each creature Grappled by it up to 30 feet straight toward it."), act_type="bonus", img="icons/skills/movement/arrow-upward-yellow.webp")
    out["roper"] = m

    # ---------- Owlbear (just an owlbear) ----------
    m = Monster("cover-owlbear", "Owlbear (The Cover)", 3, "lg", "monstrosity", "Unaligned", 13, 59, "7d10 + 21",
                (20, 12, 17, 3, 12, 7), {"walk": 40, "climb": 40}, TK["owlbear"], senses={"darkvision": 60}, skills={"prc": 1}, tsize=2,
                bio=P("Just an owlbear. Something in here has to be.",
                      "<strong>Tableau.</strong> Rearing at the back of the cavern over the gap where the cleric stood, mace raised."))
    m.trait("Still Fighting 1977", P(f"The {M} is frozen mid-battle and has the Incapacitated condition until a creature enters the gap it is fighting."))
    m.utility("Multiattack", P(f"The {M} makes two Rend attacks."), img="icons/skills/melee/strike-weapons-orange.webp")
    m.attack("Rend", 2, 8, "slashing", "str", img="icons/creatures/claws/claw-curved-jagged-gray.webp")
    out["owlbear"] = m

    # ---------- The Echo (Room 3) ----------
    m = Monster("echo", "The Echo", 3, "med", "undead", "Unaligned", 13, 40, "9d8",
                (12, 12, 12, 8, 10, 6), {"walk": 30}, TK["echo"], senses={"darkvision": 60}, di=("poison",), ci=("charmed", "frightened", "poisoned"),
                bio=P("A blank-faced copy of one character: the one with the fewest Misremembering changes so far (the corridor has taken the least from them). It steps out of the far door on the second pass through the Corridor Between. It has that character's sheet with every number halved and no name.",
                      "<strong>Running it.</strong> This block is a 5th-level adventurer halved and plays as written; or run the macro <em>The Back Room: make the Echo of a character</em> to make a halved copy of a real character. It acts right after the copied character. The full procedure is on the Room 3 journal, The Echo. It stops the moment the loop breaks."))
    m.trait("Halved", P("The Echo's statistics are the mirrored character's with every number halved (Hit Points, Armor Class, attack bonuses, damage, save DCs). As written, it is a 5th-level adventurer halved."))
    m.trait("Your Own Last Turn", P("The Echo acts immediately after the character it copies. On round 1 it does nothing. From round 2, on its turn it repeats that character's previous turn: it moves to the square they started that turn in and takes the same actions at the same squares, with every number halved, against whatever is in those squares now. It copies everything, including healing, dodging and doing nothing. If the party goes through the far door, it steps out of the next far door at the start of the following round."))
    m.trait("Unfinished", P("The Echo cannot be reduced below 1 Hit Point while the Corridor Between is looping. When the loop breaks it stops where it stands, and is not there a moment later."))
    m.attack("Repeated Strike", 1, 8, "str", "str", note="Uses the mirrored character's main weapon damage, halved.", img="icons/weapons/swords/sword-guard-steel.webp")
    out["echo"] = m
    return out

def build_npcs():
    """Remnants are NPCs, never monsters (design doc). Three fallbacks, the barkeep, the hooded stranger."""
    out = {}

    def remnant(key, name, cls, token, ac, hp, hpf, abil, sig_name, sig_html, blank_html, bio, size="med", subtype=None, align="Unaligned", senses=None, speed=None):
        m = Monster(key, name, 5, size, "humanoid", align, ac, hp, hpf, abil, speed or {"walk": 30}, TK[token], senses=senses,
                    disposition=0, ac_calc="flat", languages="Common", lang_values=("common",), subtype=subtype or cls,
                    bio=P(bio, "<strong>Remnant.</strong> Max Hit Points, never rolled. It never attacks first. It cannot answer any question about its past that is not its Signature. It cannot leave a room by a door the party came through."))
        m.trait("Signature: " + sig_name, P(sig_html), img="icons/magic/symbols/runes-star-orange-purple.webp")
        m.trait("The Blank", P(blank_html), img="icons/magic/symbols/question-stone-yellow.webp")
        m.trait("Stands Back Up", REMNANT_RULE, img="icons/magic/life/heart-cross-green.webp")
        m.trait("Cannot Follow", P("It cannot leave a room through a door the party came through. That is the only hard limit on it, and it is the exit mechanic for Room 4."))
        return m

    m = remnant("remnant-rogue", "Raven Nightshade", "rogue", "rogue", 15, 44, "8d8 + 8", (10, 18, 12, 12, 10, 14),
                "Sneak Attack, Always", "Once per round the Remnant's Sneak Attack applies, no roll and no conditions: its weapon attack hits and deals [[/damage 1d6+4 piercing]] plus [[/damage 3d6 piercing]], even in plain sight, even if the target is watching it.",
                "Cannot say what the tragedy was. Gets upset when asked. If pressed three times it goes quiet and looks at the player whose first character it is not.",
                "The Rogue With a Tragic Past: a hooded figure in dark leathers who says 'it's complicated' a great deal. Everyone at the table has played this character, or sat next to someone who did.")
    m.attack("Dagger", 1, 4, "piercing", "dex", rng=(20, 60), img="icons/weapons/daggers/dagger-simple-gray.webp")
    out["remnant-rogue"] = m

    m = remnant("remnant-barbarian", "Grukk Skullsplitter", "barbarian", "barbarian", 14, 65, "10d12", (20, 12, 16, 6, 8, 8),
                "Just Strong", "Every Strength check and Strength saving throw the Remnant makes is an automatic success. Once per round, one Greataxe attack hits without a roll for [[/damage 1d12+5 slashing]].",
                "Its name is the only thing it remembers about itself, and it says it often, in the third person. Ask where it is from, who it travelled with or why it fights, and it says its name again, louder.",
                "The Barbarian Who Is Just Strong: enormous, cheerful, and holding a greataxe that is bigger than the rules allow. It is not angry. It has never been angry. It was just strong.")
    m.attack("Greataxe", 1, 12, "slashing", "str", img="icons/weapons/axes/axe-double-engraved.webp")
    out["remnant-barbarian"] = m

    m = remnant("remnant-wizard", "Mordecai the Magnificent", "wizard", "wizard", 12, 38, "8d6 + 8", (8, 14, 12, 18, 10, 12),
                "One Fireball, Forever", "The Remnant can cast <em>fireball</em> at will. It always hits every target in the 20-foot-radius Sphere for [[/damage 8d6 fire]]; there is no saving throw. It has no other spells, and it will tell you otherwise.",
                "Has no other spells prepared and insists it does. If asked to cast anything else it begins the gestures, frowns, and casts fireball.",
                "The Wizard Who Misread the Spell: robes, a staff, a spellbook with one page in it. The page is very well thumbed.")
    m.attack("Staff", 1, 6, "bludgeoning", "str", img="icons/weapons/staves/staff-simple.webp")
    out["remnant-wizard"] = m

    # ---- This table's Remnants: the five players' first characters, as they remember them (or don't) ----
    m = remnant("remnant-fred", "Fred the Fighter", "fighter", "fred", 17, 58, "9d10 + 9", (17, 12, 13, 9, 10, 13),
                "POW!", "Once per round, one of Fred's Longsword attacks hits without a roll and deals maximum damage ([[/damage 12 slashing]]), and the hit appears in the air above the target in hand-lettered capitals: <em>POW!</em>, <em>KRAK!</em>, <em>THWACK!</em> Everyone present can read it. It fades by the end of the round.",
                "He cannot say whether anyone ever played him. What he remembers is being drawn: four panels at a time, one summer, in a camp newspaper, until the strip stopped mid-story. He speaks in short lines, as if he has to fit inside a speech balloon, and every so often he finishes a thought with 'To be continued!' and waits, a little hopefully, for next week.",
                "A square-jawed fighter in a winged helmet and chain mail, outlined in ink a shade heavier than everything around him, so he always looks slightly in front of the room. He introduces himself the way the strip's title panel did: 'FRED THE FIGHTER!' His player may not remember playing him. That is the point: he may only ever have been a comic strip, and he is here anyway.")
    m.attack("Longsword", 1, 8, "slashing", "str", img="icons/weapons/swords/sword-guard-steel.webp")
    out["remnant-fred"] = m

    m = remnant("remnant-thon", "Thon", "wizard", "thon", 14, 49, "9d8 + 9", (10, 14, 12, 18, 13, 11),
                "The Rod of Lordly Might", "Thon carries a heavy black rod studded with buttons, and once per round he presses one and it is exactly the right tool: a mace, a flaming blade, a battleaxe, a spear that extends to 50 feet, a ladder, a battering ram, a pole that points north. Whatever he uses it for that round succeeds without a roll. As a weapon it hits for [[/damage 1d8+4 bludgeoning]] plus [[/damage 2d6 fire]]; as a ram it opens any door that is not one the party came through; as a ladder or a pole it gets him anywhere he can see.",
                "He remembers every button on the rod, the order they go in, and the faint click each one makes. He does not remember a single spell. Asked to cast one, he explains button six instead, at length, delighted.",
                "A half-elf wizard in faded robes who has stopped pretending to be interested in magic. Everything he has to say is about the rod: the gadgetry, the satisfying mechanisms, what it can turn into. He will show it to anyone who stands still.", subtype="half-elf")
    m.attack("Rod of Lordly Might", 1, 8, "bludgeoning", "int", img="icons/weapons/maces/mace-round-ornate-purple.webp")
    out["remnant-thon"] = m

    m = remnant("remnant-rorvik", "Rorvik", "magic-user thief", "rorvik", 15, 52, "8d8 + 16", (14, 17, 14, 15, 9, 12),
                "Hothead", "Rorvik always acts first, in every round, before anyone rolls initiative. Once per round his first Longsword attack hits without a roll, and a crackle of half-remembered magic runs down the blade: [[/damage 1d8+3 slashing]] plus [[/damage 3d6 force]]. He can then slip away up to his Speed without provoking Opportunity Attacks: a thief's exit from a fight he started.",
                "Nobody remembers his adventures, and neither does he: his player was usually the one running the game, so Rorvik spent most of his life waiting for a turn. He asks, every few minutes, whether it is his turn yet. He cannot let an insult go: anyone who mocks him has his complete attention, and the Remnant rule that it never attacks first does not survive being called a coward.",
                "A half-elven magic-user and thief with a longsword he was never strictly allowed to carry, a short fuse, and the restless energy of someone who has been sitting on the side of the table for forty years.", subtype="half-elf")
    m.trait("Sorry I'm Late", P("In the Hoard, Rorvik is not there when the fight begins. At the top of round 2 the inner room's double doors bang open and he strides in, longsword out: 'Sorry I'm late. What did I miss?' From then on Hothead applies as normal: he acts first, every round, as if he had been there all along."))
    m.attack("Longsword", 1, 8, "slashing", "dex", img="icons/weapons/swords/sword-guard-purple.webp")
    out["remnant-rorvik"] = m

    # Built from the player's original character sheet (AD&D, 7th level, 60,381 XP), converted to 5e: abilities as written,
    # hit dice d6 at maximum, AC from leather +1, ring of protection +3 and Dex 18.
    m = remnant("remnant-morlock", "T. Morlock", "thief-acrobat", "morlock", 17, 63, "7d6 + 21", (17, 18, 17, 16, 18, 12),
                "Thief-Acrobat", "Once per round, one acrobatic move succeeds without a roll (his sheet says tightrope 100%, and he means it): a tumble through an enemy's space, a pole vault of nine and a half feet onto a table or a balcony, a run along a rail or a rope, a fall of up to twenty feet landed on his feet. None of it provokes Opportunity Attacks. The first hit he makes after a move like that in the same round is a backstab: triple damage dice.",
                "He has his character sheet, and he will show it to you: seventh level, sixty thousand three hundred and eighty-one experience points, every box filled in, the paper soft and scorched in one corner. The name line says only <em>T. Morlock</em>. Nobody knows what the T. stands for, and he gets quieter each time someone asks.",
                "A halfling thief-acrobat in leather armour, eighty-eight years old, four foot eight, blond, blue-eyed, upper class, and (Comeliness 18) the handsomest halfling anyone has ever seen. Always slightly higher up than everyone else: on the bar, on a rafter, on someone's shoulders. His deity is his dagger, and his holy symbol is a silver dagger. His secondary skill is carpet making; he will tell you about it. On the sheet, next to <em>Jewelry</em>, it says <em>I hope so</em>.",
                size="sm", subtype="halfling", align="Neutral Evil", senses={"darkvision": 30})
    m.trait("Elishaf", P("Twice a day he says <em>elishaf</em> and walks through a wall, as the spell <em>passwall</em>, into the space beyond. It never carries him out of a room through a wall the party has left by: the Remnant rule still holds."))
    m.trait("Rings", P("A ring of invisibility (he turns invisible as an action until he attacks, once per round of his choosing) and a ring of chameleon power (Advantage on Dexterity (Stealth) checks; he blends into any crowd, booth or bookshelf). His ring of protection +3 is already in his AC."))
    m.trait("The Leather Bag", P("He carries a leather bag with a sapphire in it worth eleven thousand eight hundred gold pieces, and the sapphire has a demon in it. He will not open the bag and does not like it being touched. Nobody at the table remembers what happens if it is opened, so nothing does, unless you want it to."))
    m.attack("Short Sword +1", 1, 6, "piercing", "dex", img="icons/weapons/swords/shortsword-guard-brass.webp")
    m.attack("Dagger of Wounding", 1, 4, "piercing", "dex", rng=(20, 60), note="A creature hit loses 1 extra Hit Point at the start of each of its turns until it or an ally uses an action to staunch the wound.", img="icons/weapons/daggers/dagger-curved-steel.webp")
    m.attack("Shortbow (silver arrows)", 1, 6, "piercing", "dex", kind="ranged", reach=None, rng=(80, 320), img="icons/weapons/bows/shortbow-recurve.webp")
    out["remnant-morlock"] = m

    m = remnant("remnant-strider", "Strider", "ranger", "strider", 15, 60, "8d10 + 16", (14, 17, 14, 11, 15, 12),
                "Knows the Way", "Strider is never lost. In the Corridors he knows which door leads where, and if asked the GM tells him the truth (he will offer to lead; where he leads is always toward the Hoard). Once per round one of his Longsword or Longbow attacks hits without a roll for [[/damage 1d8+3 slashing]] plus [[/damage 2d6 slashing]].",
                "Everything about him past the name and the cloak belongs to somebody else's story. Ask about his lineage and he tells it, earnestly, and it is a story the whole table has read in a book. He does not notice.",
                "A weathered ranger in a travel-stained cloak who sits with his back to the wall and his hood up, watching the door. His player built him straight out of a beloved novel at the time and named him Strider, and he has been walking ever since.")
    m.attack("Longsword", 1, 8, "slashing", "dex", img="icons/weapons/swords/sword-guard-brown.webp")
    m.attack("Longbow", 1, 8, "piercing", "dex", kind="ranged", reach=None, rng=(150, 600), img="icons/weapons/bows/longbow-recurve-leather-brown.webp")
    out["remnant-strider"] = m

    m = Monster("barkeep", "Bartleby Stickit", 0, "med", "humanoid", "Neutral", 10, 9, "2d8", (12, 10, 11, 10, 14, 15), {"walk": 30}, TK["barkeep"],
                disposition=1, ac_calc="flat", languages="Common", lang_values=("common",), subtype="human",
                bio=P("Bartleby Stickit, Bart to his friends (which is everyone who has drunk his cider twice). Keeper of the Stickit Inn, as his father was. Kind. Tired in a way that is not unhappy. He pours the house cider with a heavy hand, led the party up the stairs with a lantern and showed them the cots, and in the night he comes down the wrong stairwell with a tray.",
                      "<strong>Room 1.</strong> He tells them it is not morning yet and they should go back to bed; the road will be there tomorrow. He knows one detail about one character that the character has never told anyone. If pressed about it he does not understand the question.",
                      "<strong>Room 5.</strong> His voice from the common room below is the sound of ordinary morning."))
    m.trait("Not a Fight", P("Bartleby never attacks and cannot be made to. If attacked he sets the tray down, says 'well', and goes back up the stairs. He will have set a second tray by morning."))
    m.trait("He Knows", P("Once, in Room 1, he mentions one detail from a character's backstory that the player has never said aloud at the table: pick it from the sheet before the session. With nothing on the sheet to use, he asks after the character by the name the player almost gave them."))
    m.trait("Formerly a Scrivener", P("Asked whether he used to be a scrivener, he nods: 'But I'm not any more.' Asked why, or asked to write, copy, check or witness anything at all: 'I would prefer not to.' He says it pleasantly, every time, and goes back to wiping the mug."))
    out["barkeep"] = m

    m = Monster("stranger", "Kael Shadowmere", 0, "med", "humanoid", "Neutral", 11, 13, "3d8", (10, 12, 11, 13, 12, 14), {"walk": 30}, TK["stranger"],
                disposition=0, ac_calc="flat", languages="Common", lang_values=("common",), subtype="human",
                bio=P("A hooded stranger in the corner booth of the Stickit Inn, with a job and an untouched mug of cider. He gives his name as Kael Shadowmere, as if anyone could keep a straight face. Play it completely straight: the job is real, the pay is fair, the directions are good.",
                      "<strong>Room 2.</strong> There is a hooded stranger in every booth, and every one of them is a role, repeating the hook word for word. None of them is the Remnant.",
                      "<strong>Room 5.</strong> The stranger's voice rises from the common room below, asking Bart whether the party is up yet. The job is still there."))
    m.trait("The Hook", P("The stranger offers a plain, ordinary job: ride guard on a wagon of lamp oil over the Kettle Pass to Thistlecross, three days, forty gold a head, half tonight, leaving at first light (the handout <em>The Job</em>). It is never a trick, and if the party leaves at the end, it is still there to be done."))
    out["stranger"] = m

    # ---- Room 2's roles: patrons of the Common Room That Isn't. Each has one line, said the same way every time. ----
    ROLE_RULE = P("<strong>A Role.</strong> This is not a person; it is a part in a scene. It says its one line, word for word, whoever asks and whatever they ask, and does nothing else. It cannot be persuaded, frightened or charmed out of it. If attacked it does not fight back: it says its line again, a little quieter. When Fred says his Signature, every role stops mid-line and turns to look at the party.")
    roles = [
        ("role-barmaid", "The Barmaid", "barmaid", (10, 12, 10, 10, 10, 12), "\u201cJust coming, love.\u201d She never arrives. Step into her path and she walks round you, still smiling, still coming.",
         "A barmaid in an apron, a tray of full cider mugs on one hand, walking a slow circle between the tables. She has been walking it all night."),
        ("role-guard", "Inn Guard", "guard", (13, 11, 12, 10, 10, 10), "\u201cMove along. Nothing to see here.\u201d (Both guards say it together. Ask what they are guarding: \u201cNothing to see here.\u201d)",
         "One of two guards at the Common Room's door, leather jerkin, short spear. Before Fred's Signature they stand in the doorway; after it, they step aside together without a word."),
        ("role-drunk", "The Drunk", "drunk", (10, 8, 12, 10, 8, 12), "His one joke: roll once on the table <em>The Drunk's Joke</em>, then tell that same joke, word for word and with the same pause, forever. Nobody else laughs.",
         "A drunk in an armchair by the hearth, telling a joke to nobody, and laughing at the end of it."),
        ("role-merchant", "The Merchant", "merchant", (10, 10, 10, 12, 10, 14), "\u201cFinest wares this side of the pass! Have a look!\u201d There is nothing on the table.",
         "A travelling merchant at a table, fur-trimmed coat, hands spread over the goods he does not have."),
        ("role-oldman", "The Old Man", "oldman", (8, 8, 10, 12, 12, 10), "\u201cIn my day, the pass was a dangerous road.\u201d Ask how: \u201cIn my day, the pass was a dangerous road.\u201d",
         "A very old man at a table near the wall, a wool shawl round his shoulders, looking at a window that isn't there."),
    ]
    for key, name, tok, abil, line, bio in roles:
        m = Monster(key, name, 0, "med", "humanoid", "Unaligned", 10, 4, "1d8", abil, {"walk": 30}, TK[tok],
                    disposition=0, ac_calc="flat", languages="Common", lang_values=("common",), subtype="human",
                    bio=P(bio, "<strong>Room 2, the Common Room That Isn't.</strong> Every patron is a role, and so is this one. Its line: " + line))
        m.trait("A Role", ROLE_RULE)
        m.trait("Its Line", P(line))
        if key == "role-guard":
            m.attack("Spear", 1, 6, "piercing", "str", img="icons/weapons/polearms/spear-simple-engraved.webp")
        out[key] = m
    return out
