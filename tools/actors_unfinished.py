"""Actors for The Back Room: The Unfinished Fight (the second adventure in the module).

The Cover is fought in three waves, two of the cover's monsters at a time plus their hangers-on, by the party and the
Remnants together. These are the Cover's own versions, built for that fight (not Monster Manual stat blocks): each wave
is a High encounter for five strong 7th-level characters (budgeted as 8th level, about 9,000-10,000 XP), and the waves
come back to back. The Remnants fight alongside, but mostly Help (see the Cover journal), so they are not in the budget.

Also: the Provisions Chests in the Cellar (a pressure fight while Thon finds the right button), and edits that turn the
original Remnant NPCs into allies for this adventure.
"""
from actors import Monster, P, M, TK, build_npcs

WAVE = {1: "Wave 1", 2: "Wave 2", 3: "Wave 3"}

def frozen(m, wave):
    m.trait("Still Fighting 1977", P(f"Until {WAVE[wave].lower()} wakes, the {M} is frozen mid-battle in its pose from the cover and has the Incapacitated condition; nothing harms it. "
                                     f"{'It wakes the moment the party enters the cavern.' if wave == 1 else 'It wakes when the last monster of the wave before it drops: it finishes its 1977 pose, turns its head, and joins the fight at the top of the next round.'}"))
    return m

def multi(m, html): return m.utility("Multiattack", P(html), img="icons/skills/melee/strike-weapons-orange.webp")

def build_waves():
    out = {}
    # ======================= WAVE 1: the troll and the roper (+ piercers) =======================
    m = Monster("uf-troll", "Troll (The Cover)", 9, "lg", "giant", "Chaotic Evil", 16, 168, "16d10 + 80",
                (20, 13, 20, 7, 9, 7), {"walk": 30}, TK["troll"], senses={"darkvision": 60}, skills={"prc": 1},
                languages="Giant", lang_values=("giant",), tsize=2,
                bio=P("The troll from the cover, mid-lunge at the gap by the treasure chest where the dwarf stood. It has been lunging since 1977. It regenerates the way every table remembers trolls: it gets back up, unless you burn it.",
                      "<strong>Wave 1.</strong> Wakes when the party enters the cavern."))
    frozen(m, 1)
    m.trait("Gets Back Up", P(f"When the {M} drops to 0 Hit Points it falls prone and does not die, unless the damage that dropped it included Fire or Acid damage, or a creature uses an action to burn it while it is down (a torch counts). At the start of its next turn it stands up with half its Hit Points. Everybody at the table knows about the fire; let them remember it."))
    multi(m, f"The {M} makes three attacks: one Bite and two Claw attacks.")
    m.attack("Bite", 2, 6, "piercing", "str", img="icons/creatures/abilities/mouth-teeth-long-red.webp")
    m.attack("Claw", 2, 8, "slashing", "str", img="icons/creatures/claws/claw-curved-jagged-gray.webp")
    m.save("Hurl the Chest", "dex", "con", [(4, 10, ["bludgeoning"])], "half",
           P(f"The {M} heaves the treasure chest it was fighting over at a point it can see within 60 feet. <em>Dexterity Saving Throw:</em> each creature in a 10-foot-radius Sphere centred on that point. <em>Failure:</em> [[/damage average]] damage and the Prone condition. <em>Success:</em> Half damage. Coins everywhere. None of them are worth anything once they leave the cavern."),
           rng_ft=60, template=("sphere", 10), recharge=5, img="icons/skills/melee/strike-weapons-orange.webp")
    out["troll"] = m

    m = Monster("uf-roper", "Roper (The Cover)", 8, "lg", "aberration", "Neutral Evil", 20, 147, "14d10 + 70",
                (18, 8, 20, 7, 16, 6), {"walk": 10, "climb": 20}, TK["roper"], senses={"darkvision": 60},
                skills={"prc": 3, "ste": 2}, languages="Deep Speech", lang_values=("deep",), tsize=2,
                bio=P("The one nobody could draw properly. It looks like three different things from three angles: a stalagmite, a rotted stump, a face. Describe it differently each round and never correct yourself.",
                      "<strong>Wave 1.</strong> Its tendrils were reaching for the gap at the cave mouth, where the thief was sneaking in. The piercers on the ceiling above it were never on the cover, but everyone remembers them being there."))
    frozen(m, 1)
    m.trait("Three Things at Once", P(f"Attack rolls against the {M} can't have Advantage: whichever side you come at it from, it is something else."))
    m.trait("Spider Climb", P(f"The {M} can climb difficult surfaces, including along ceilings, without needing to make an ability check."))
    multi(m, f"The {M} makes four Tendril attacks, uses Reel, and makes one Bite attack.")
    m.attack("Bite", 4, 8, "piercing", "str", img="icons/creatures/abilities/mouth-teeth-long-red.webp")
    m.attack("Tendril", 1, 6, "bludgeoning", "str", reach=60, note="If the target is Large or smaller, it has the Grappled condition (escape DC 15) and the Poisoned condition until the grapple ends. The roper has six tendrils; each can grapple one creature. A tendril has AC 20 and 10 Hit Points; destroying one ends its grapple and doesn't hurt the roper.", img="icons/creatures/tentacles/tentacle-earth-green.webp")
    m.utility("Reel", P(f"The {M} pulls each creature Grappled by it up to 30 feet straight toward it."), act_type="bonus", img="icons/skills/movement/arrow-upward-yellow.webp")
    out["roper"] = m

    m = Monster("uf-piercer", "Piercer (The Cover)", 0.5, "sm", "monstrosity", "Unaligned", 15, 22, "4d6 + 8",
                (10, 13, 14, 1, 7, 3), {"walk": 5, "climb": 5}, TK["roper"], senses={"blindsight": 30, "darkvision": 60}, skills={"ste": 3},
                bio=P("A stalactite that is not a stalactite. Six of them hang over the roper. They were never on the cover; the table put them there."), tsize=1)
    m.trait("Spider Climb", P(f"The {M} can climb difficult surfaces, including along ceilings, without needing to make an ability check."))
    m.save("Drop", "dex", "con", [(4, 6, ["piercing"])], "half",
           P(f"Once, while on the ceiling, the {M} drops onto a creature directly below it. <em>Dexterity Saving Throw:</em> DC 12. <em>Failure:</em> [[/damage average]] damage. <em>Success:</em> Half damage. Either way the piercer is now on the floor, Prone, and fights with its Bite."),
           count="1", per_day=1, img="icons/weapons/polearms/spear-simple-engraved.webp")
    m.attack("Bite", 1, 6, "piercing", "dex", img="icons/creatures/abilities/mouth-teeth-long-red.webp")
    out["piercer"] = m

    # ======================= WAVE 2: the centaur and the unicorn (+ outriders) =======================
    m = Monster("uf-centaur", "Centaur Captain (The Cover)", 8, "lg", "fey", "Neutral Good", 17, 152, "16d10 + 64",
                (20, 18, 18, 10, 14, 14), {"walk": 50}, TK["centaur"], skills={"ath": 1, "prc": 1, "sur": 1},
                languages="Elvish, Sylvan", lang_values=("elvish", "sylvan"), tsize=2,
                bio=P("Draws an empty bow at the ledge where the archer stood, and hits. Nobody at the table ever tracked ammunition, and the centaur is the proof. The outriders came with it because a centaur is never alone in anyone's memory.",
                      "<strong>Wave 2.</strong> Wakes when the last monster of wave 1 drops."))
    frozen(m, 2)
    m.trait("Nobody Tracked Arrows", P(f"The {M}'s Longbow needs no ammunition and ignores the Disadvantage normally imposed by Long Range. If a character asks what it is shooting, the answer is <em>arrows</em>, and there are none."))
    multi(m, f"The {M} makes three attacks, using Pike or Longbow in any combination.")
    m.attack("Pike", 2, 8, "piercing", "str", reach=10, img="icons/weapons/polearms/spear-simple-engraved.webp")
    m.attack("Longbow", 2, 8, "piercing", "dex", kind="ranged", reach=None, rng=(150, 600), img="icons/weapons/bows/longbow-recurve-leather-brown.webp")
    m.utility("Trampling Charge", P(f"If the {M} moves at least 20 feet straight toward a target and then hits it with Pike, the target must succeed on a DC 16 Strength saving throw or have the Prone condition. The captain can then make one Hooves attack ([[/damage 2d6+5 bludgeoning]]) against it as a Bonus Action."), img="icons/skills/movement/arrow-upward-yellow.webp")
    m.utility("Sound the Horn", P(f"Each Centaur Outrider that can hear the {M} can use its Reaction to make one Pike or Longbow attack."), act_type="bonus", recharge=5, img="icons/magic/symbols/runes-star-orange-purple.webp")
    out["centaur"] = m

    m = Monster("uf-outrider", "Centaur Outrider (The Cover)", 2, "lg", "fey", "Neutral Good", 16, 45, "6d10 + 12",
                (18, 14, 14, 9, 13, 11), {"walk": 50}, TK["centaur"], skills={"ath": 1, "prc": 1},
                languages="Elvish, Sylvan", lang_values=("elvish", "sylvan"), tsize=2,
                bio=P("One of the captain's outriders. Not on the cover. Remembered there anyway."))
    m.trait("Nobody Tracked Arrows", P(f"The {M}'s Longbow needs no ammunition and ignores the Disadvantage normally imposed by Long Range."))
    multi(m, f"The {M} makes two attacks, using Pike or Longbow in any combination.")
    m.attack("Pike", 1, 10, "piercing", "str", reach=10, img="icons/weapons/polearms/spear-simple-engraved.webp")
    m.attack("Longbow", 1, 8, "piercing", "dex", kind="ranged", reach=None, rng=(150, 600), img="icons/weapons/bows/longbow-recurve-leather-brown.webp")
    out["outrider"] = m

    m = Monster("uf-unicorn", "Unicorn (The Cover)", 7, "lg", "celestial", "Lawful Good", 15, 136, "16d10 + 48",
                (18, 14, 16, 11, 17, 16), {"walk": 50}, TK["unicorn"], senses={"darkvision": 60}, di=("poison",),
                ci=("charmed", "paralyzed", "poisoned"), languages="Celestial, Elvish, Sylvan; telepathy 60 ft.",
                lang_values=("celestial", "elvish", "sylvan"), tsize=2,
                bio=P("On the monsters' side. It was in the Monster Manual, so it is a monster. It is confused about this, and its confusion does not slow it down. Kill it first or the wave never ends: it keeps the others standing.",
                      "<strong>Wave 2.</strong> Rearing beside the troll, horn lowered at the gap where the elf stood."))
    frozen(m, 2)
    m.trait("Wrong Side", P(f"The {M}'s Healing Touch and Shimmering Shield can target only monsters of the Cover. It will not heal a character or a Remnant under any circumstances, and does not understand why anyone would ask."))
    multi(m, f"The {M} makes one Hooves attack and one Radiant Horn attack.")
    m.attack("Hooves", 2, 6, "bludgeoning", "str", img="icons/creatures/mammals/horse-hooves-blue.webp")
    m.attack("Radiant Horn", 1, 8, "piercing", "str", extra_parts=[(2, 8, ["radiant"])], img="icons/magic/light/beam-rays-yellow.webp")
    m.utility("Healing Touch", P(f"The {M} touches one other monster of the Cover within 5 feet, which regains [[/heal 4d8+4]] Hit Points. If that monster has 0 Hit Points (including a troll that is down), it stands up."), recharge=5, img="icons/magic/life/heart-cross-green.webp")
    m.utility("Shimmering Shield", P(f"The {M} grants one other monster of the Cover within 60 feet a +2 bonus to Armor Class until the start of the unicorn's next turn."), act_type="bonus", img="icons/magic/defensive/shield-barrier-glowing-blue.webp")
    m.utility("Charge", P(f"If the {M} moves at least 20 feet straight toward a target and then hits it with Radiant Horn, the target takes an extra [[/damage 2d8 piercing]] and must succeed on a DC 15 Strength saving throw or have the Prone condition."), img="icons/skills/movement/arrow-upward-yellow.webp")
    out["unicorn"] = m

    # ======================= WAVE 3: the owlbear and the red dragon (+ cubs) =======================
    m = Monster("uf-owlbear", "Owlbear (The Cover)", 7, "lg", "monstrosity", "Unaligned", 15, 168, "16d10 + 80",
                (22, 12, 20, 3, 12, 7), {"walk": 40, "climb": 40}, TK["owlbear"], senses={"darkvision": 60}, skills={"prc": 1}, tsize=2,
                bio=P("Just an owlbear. Something in here has to be. It has had a long time to get bigger, and the cubs are its own.",
                      "<strong>Wave 3.</strong> Rearing at the back of the cavern over the gap where the cleric stood, mace raised."))
    frozen(m, 3)
    multi(m, f"The {M} makes two Rend attacks. If both hit the same Large or smaller target, the target has the Grappled condition (escape DC 17) and takes [[/damage 2d8 bludgeoning]] at the start of each of its turns while grappled.")
    m.attack("Rend", 2, 8, "slashing", "str", img="icons/creatures/claws/claw-curved-jagged-gray.webp")
    m.utility("Screech", P(f"Each creature within 30 feet of the {M} that can hear it must succeed on a DC 16 Wisdom saving throw or have the Frightened condition until the end of its next turn."), recharge=5, img="icons/magic/control/fear-fright-monster-grin-red-orange.webp")
    out["owlbear"] = m

    m = Monster("uf-cub", "Owlbear Cub (The Cover)", 2, "med", "monstrosity", "Unaligned", 13, 45, "6d8 + 18",
                (17, 12, 16, 3, 12, 7), {"walk": 40, "climb": 30}, TK["owlbear"], senses={"darkvision": 60}, tsize=1,
                bio=P("Not on the cover. Somebody at the table drew them in the margin, once."))
    multi(m, f"The {M} makes two Rend attacks.")
    m.attack("Rend", 1, 8, "slashing", "str", img="icons/creatures/claws/claw-curved-jagged-gray.webp")
    out["cub"] = m

    m = Monster("uf-dragon", "Red Dragon (The Cover)", 10, "lg", "dragon", "Chaotic Evil", 18, 178, "17d10 + 85",
                (23, 10, 21, 14, 11, 19), {"walk": 40, "climb": 40, "fly": 80}, TK["dragon"],
                senses={"blindsight": 30, "darkvision": 120}, skills={"prc": 2, "ste": 1}, saves=("dex", "wis"), di=("fire",),
                languages="Common, Draconic", lang_values=("common", "draconic"), subtype="chromatic", tsize=2,
                bio=P("On the cover it was the size of the owlbear, rearing over the hoard. It has had since 1977 to grow, and it has. This is the last thing between the party and the end of the fight.",
                      "<strong>Wave 3.</strong> Wakes with the owlbear. Its first breath goes at the most people it can catch, Remnants included."))
    frozen(m, 3)
    m.trait("The Last Monster", P(f"The {M} does not flee and cannot be frightened or charmed while any other monster of the Cover is still standing. When it is the last one, it speaks once, in Common: <em>“You came back.”</em>"))
    multi(m, f"The {M} makes three Rend attacks. It can replace one of them with a use of Fire Breath if it is available.")
    m.attack("Rend", 2, 10, "slashing", "str", reach=10, extra_parts=[(1, 6, ["fire"])], img="icons/creatures/claws/claw-curved-jagged-gray.webp")
    m.save("Fire Breath", "dex", "con", [(16, 6, ["fire"])], "half",
           P(f"<em>Dexterity Saving Throw:</em> DC 17, each creature in a 30-foot Cone. <em>Failure:</em> [[/damage average]] damage. <em>Success:</em> Half damage."),
           template=("cone", 30), recharge=5, img="icons/magic/fire/beam-jet-stream-embers.webp")
    m.utility("Wing Gust", P(f"The {M} beats its wings. Each creature within 10 feet of it must succeed on a DC 18 Strength saving throw or be pushed 15 feet away and have the Prone condition. The dragon can then fly up to half its Fly Speed."), act_type="bonus", recharge=5, img="icons/skills/movement/arrow-upward-yellow.webp")
    out["dragon"] = m

    # ======================= THE CELLAR: the breathing provisions chests =======================
    m = Monster("uf-chest", "Provisions Chest", 4, "med", "monstrosity", "Neutral", 13, 75, "10d8 + 30",
                (17, 12, 16, 5, 13, 8), {"walk": 15}, "icons/svg/chest.svg", senses={"darkvision": 60}, skills={"ste": 5},
                ci=("prone",), subtype="shapechanger",
                bio=P("The party's own provisions chest, from the storeroom upstairs, receipts still tucked under the lid. Four of them. They are breathing.",
                      "<strong>The Cellar.</strong> They wake when anyone touches one, or when Thon presses his first button (the click). They stop, and are only chests, the moment the cellar door opens."))
    m.trait("Adhesive", P(f"The {M} adheres to anything that touches it. A Large or smaller creature adhered to it has the Grappled condition (escape DC 14). Ability checks made to escape this grapple have Disadvantage."))
    m.trait("False Appearance", P(f"While the {M} is motionless, it is indistinguishable from an ordinary provisions chest."))
    m.trait("Only a Chest", P(f"When the cellar door opens, every {M} stops where it is and is an ordinary chest again. Anyone it was holding falls free."))
    multi(m, f"The {M} makes one Pseudopod attack and one Bite attack.")
    m.attack("Pseudopod", 1, 8, "bludgeoning", "str", note="The target is stuck to the chest (see Adhesive).", img="icons/creatures/tentacles/tentacle-earth-green.webp")
    m.attack("Bite", 1, 8, "piercing", "str", extra_parts=[(2, 8, ["acid"])], img="icons/creatures/abilities/mouth-teeth-long-red.webp")
    out["chest"] = m
    return out

# ---------- the Remnants as allies ----------
ALLY_RULE = P("<strong>Allies in the Cover.</strong> In the Cover the Remnant fights on the party's side, on its own initiative. Once per wave it uses its Signature, and the Signature always works. The rest of its turns it takes the Help action for a character next to it (that character has Advantage on its next attack roll or check), or Dodges. It never steals a kill. If it drops to 0 Hit Points it does not die: at the start of its next turn it stands up with half its Hit Points, mid-sentence. It has been in this fight before.")
REMOVE_TRAITS = {"Cannot Follow", "Stands Back Up", "Sorry I'm Late"}
VARIANT_TRAITS = {
    "remnant-rorvik": [("Sorry I'm Late", P("In the Cover, Rorvik is not there when wave 1 wakes. At the top of round 2 he comes in through the cave mouth at a run, longsword out: <em>“Sorry I'm late. What did I miss?”</em> From then on Hothead applies as normal: he acts first, every round, as if he had been there all along."))],
    "remnant-thon": [("The Buttons, in Order", P("Thon presses the rod's buttons in order, one per press, and names each one: <strong>1</strong> mace, <strong>2</strong> flaming blade, <strong>3</strong> battleaxe, <strong>4</strong> spear, <strong>5</strong> ladder, <strong>6</strong> battering ram, <strong>7</strong> a pole that points north. He insists on showing them in order, every time, unless someone asks for one by name: then he grins, says its number, and presses it. As the battering ram, it opens any door."))],
    "remnant-strider": [("Knows the Way (The Unfinished Fight)", P("Strider has been at the Crossroads a long time, because he has never had a map. Show him the X Map and he reads it at a glance: <em>“That's two doors from here.”</em> He points down the east road, and he is right."))],
}
VARIANT_BIO = P("<strong>Remnant.</strong> One of the first party: a player's first-ever character, as the table remembers them. Max Hit Points, never rolled. It never attacks first. It cannot answer any question about its past that is not its Signature. In this adventure it wants one thing: to finish the fight on the cover of the Monster Manual, which the first party never did.")

def build_allies():
    """The original NPCs (Bartleby, Kael, the Remnants, the fallbacks, the Room 2 roles), with the Remnants turned into
    the party's allies for the Cover. The Echo is not in this adventure."""
    npcs = build_npcs()
    npcs.pop("echo", None)
    for key, m in npcs.items():
        if not key.startswith("remnant-"): continue
        bio = m.doc["system"]["details"]["biography"]
        bio["value"] = bio["value"].split("<p><strong>Remnant.</strong>")[0] + VARIANT_BIO
        m.items[:] = [it for it in m.items if it["name"] not in REMOVE_TRAITS]
        m.trait("Ally in the Cover", ALLY_RULE, img="icons/magic/life/heart-cross-green.webp")
        for name, html in VARIANT_TRAITS.get(key, []): m.trait(name, html)
        m.doc["prototypeToken"]["disposition"] = 1   # friendly
    return npcs
