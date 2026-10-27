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


# Token art is not drawn yet: every actor uses a Foundry core icon until tools/tokens.py is rewritten for v2.
TK = {"dragon": "icons/creatures/reptiles/dragon-winged-red.webp", "unicorn": "icons/creatures/mammals/horse-unicorn-white.webp",
      "centaur": "icons/creatures/mammals/horse-brown.webp", "troll": "icons/creatures/magical/humanoid-giant-ogre-green.webp",
      "roper": "icons/creatures/tentacles/tentacles-suctioncups-pink.webp", "owlbear": "icons/creatures/mammals/bear-paw-print-brown.webp",
      "echo": "icons/svg/mystery-man.svg", "rogue": "icons/svg/mystery-man.svg", "barbarian": "icons/svg/mystery-man.svg",
      "wizard": "icons/svg/mystery-man.svg", "barkeep": "icons/svg/mystery-man.svg", "stranger": "icons/svg/mystery-man.svg"}

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
                bio=P("A blank-faced copy of one character: the one who has left the least behind, if there is a choice. It steps out of the far door on the second pass through the Corridor Between. It has that character's sheet with every number halved and no name.",
                      "<strong>Running it.</strong> Replace this placeholder with the real sheet: copy the character's actor, halve every number, blank the name. The two traits below are the rules that matter. It stops the moment the loop breaks."))
    m.trait("Halved", P("The Echo's statistics are the mirrored character's with every number halved (Hit Points, Armor Class bonus from Dexterity, attack bonuses, damage, save DCs). The block above is a placeholder for a 5th-level character."))
    m.trait("Fight Your Own Last Turn", P("In this fight every attack a character makes repeats itself one round later in the same squares, made by the Echo with the same numbers. Note each character's attack and the squares it covered; on the Echo's next turn it makes those attacks from where that character was standing. Moving is how you dodge yourself."))
    m.trait("Unfinished", P("The Echo cannot be reduced below 1 Hit Point while the Corridor Between is looping. When the loop breaks it stops where it stands, and is not there a moment later."))
    m.attack("Repeated Strike", 1, 8, "str", "str", note="Uses the mirrored character's main weapon damage, halved.", img="icons/weapons/swords/sword-guard-steel.webp")
    out["echo"] = m
    return out

def build_npcs():
    """Remnants are NPCs, never monsters (design doc). Three fallbacks, the barkeep, the hooded stranger."""
    out = {}

    def remnant(key, name, cls, token, ac, hp, hpf, abil, sig_name, sig_html, blank_html, bio):
        m = Monster(key, name, 5, "med", "humanoid", "Unaligned", ac, hp, hpf, abil, {"walk": 30}, TK[token],
                    disposition=0, ac_calc="flat", languages="Common", lang_values=("common",), subtype=cls,
                    bio=P(bio, "<strong>Remnant.</strong> Max Hit Points, never rolled. It never attacks first. It cannot answer any question about its past that is not its Signature. It cannot leave a room by a door the party came through."))
        m.trait("Signature: " + sig_name, P(sig_html), img="icons/magic/symbols/runes-star-orange-purple.webp")
        m.trait("The Blank", P(blank_html), img="icons/magic/symbols/question-stone-yellow.webp")
        m.trait("Stands Back Up", REMNANT_RULE, img="icons/magic/life/heart-cross-green.webp")
        m.trait("Cannot Follow", P("It cannot leave a room through a door the party came through. That is the only hard limit on it, and it is the exit mechanic for Room 4."))
        return m

    m = remnant("remnant-rogue", "The Rogue With a Tragic Past", "rogue", "rogue", 15, 44, "8d8 + 8", (10, 18, 12, 12, 10, 14),
                "Sneak Attack, Always", "Once per round the Remnant's Sneak Attack applies, no roll and no conditions: its weapon attack hits and deals [[/damage 1d6+4 piercing]] plus [[/damage 3d6 piercing]], even in plain sight, even if the target is watching it.",
                "Cannot say what the tragedy was. Gets upset when asked. If pressed three times it goes quiet and looks at the player whose first character it is not.",
                "A hooded figure in dark leathers who says 'it's complicated' a great deal. Everyone at the table has played this character, or sat next to someone who did.")
    m.attack("Dagger", 1, 4, "piercing", "dex", rng=(20, 60), img="icons/weapons/daggers/dagger-simple-gray.webp")
    out["remnant-rogue"] = m

    m = remnant("remnant-barbarian", "The Barbarian Who Is Just Strong", "barbarian", "barbarian", 14, 65, "10d12", (20, 12, 16, 6, 8, 8),
                "Just Strong", "Every Strength check and Strength saving throw the Remnant makes is an automatic success. Once per round, one Greataxe attack hits without a roll for [[/damage 1d12+5 slashing]].",
                "Has no name. Answers to any name given, and keeps it. The first name a character uses for it is its name for the rest of the adventure; write it on the token.",
                "Enormous, cheerful, and holding a greataxe that is bigger than the rules allow. It is not angry. It has never been angry. It was just strong.")
    m.attack("Greataxe", 1, 12, "slashing", "str", img="icons/weapons/axes/axe-double-engraved.webp")
    out["remnant-barbarian"] = m

    m = remnant("remnant-wizard", "The Wizard Who Misread the Spell", "wizard", "wizard", 12, 38, "8d6 + 8", (8, 14, 12, 18, 10, 12),
                "One Fireball, Forever", "The Remnant can cast <em>fireball</em> at will. It always hits every target in the 20-foot-radius Sphere for [[/damage 8d6 fire]]; there is no saving throw. It has no other spells, and it will tell you otherwise.",
                "Has no other spells prepared and insists it does. If asked to cast anything else it begins the gestures, frowns, and casts fireball.",
                "Robes, a staff, a spellbook with one page in it. The page is very well thumbed.")
    m.attack("Staff", 1, 6, "bludgeoning", "str", img="icons/weapons/staves/staff-simple.webp")
    out["remnant-wizard"] = m

    m = Monster("barkeep", "The Barkeep", 0, "med", "humanoid", "Neutral", 10, 9, "2d8", (12, 10, 11, 10, 14, 15), {"walk": 30}, TK["barkeep"],
                disposition=1, ac_calc="flat", languages="Common", lang_values=("common",), subtype="human",
                bio=P("Kind. Tired in a way that is not unhappy. He led the party up the stairs with a lantern and showed them the cots, and in the night he comes down the wrong stairwell with a tray.",
                      "<strong>Room 1.</strong> He tells them it is not morning yet and they should go back to bed; the road will be there tomorrow. He knows one detail about one character that the character has never told anyone. If pressed about it he does not understand the question.",
                      "<strong>Room 5.</strong> His voice from the common room below is the sound of ordinary morning."))
    m.trait("Not a Fight", P("The Barkeep never attacks and cannot be made to. If attacked he sets the tray down, says 'well', and goes back up the stairs. He will have set a second tray by morning."))
    m.trait("He Knows", P("Once, in Room 1, he mentions one detail from a character's backstory that the player has never said aloud at the table. The GM picks it from the character sheet before the session."))
    out["barkeep"] = m

    m = Monster("stranger", "The Hooded Stranger", 0, "med", "humanoid", "Neutral", 11, 13, "3d8", (10, 12, 11, 13, 12, 14), {"walk": 30}, TK["stranger"],
                disposition=0, ac_calc="flat", languages="Common", lang_values=("common",), subtype="human",
                bio=P("A hooded stranger in the corner booth with a job. Play it completely straight: the job is real, the pay is fair, the directions are good.",
                      "<strong>Room 2.</strong> There is a hooded stranger in every booth, and every one of them is a role, repeating the hook word for word. None of them is the Remnant.",
                      "<strong>Room 5.</strong> The stranger's voice rises from the common room below, asking the barkeep whether the party is up yet. The job is still there."))
    m.trait("The Hook", P("The stranger offers a plain, ordinary job: an escort, a delivery, a missing person, whatever this table's campaign would open with. The GM writes it on the handout <em>The Job</em> before session one. It is never a trick."))
    out["stranger"] = m
    return out
