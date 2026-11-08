"""Shared by both adventures: ambience and music (paths into the recommended audio modules), SoundBard banks, and the setup/removal macros."""
import json
IVAN, MG, AM, SFX = "ivan-duch-music-packs/audio", "michaelghelfi", "adventuremusic", "soundfxlibrary"
# One ambient loop per place; every scene (and its vista) plays its place's loop as its scene sound.
AMBIENCE = {   # key: (name, path or None for this module's own file, volume)
    "landing": ("The Stickit Inn, before the game (The Innkeeper)", f"{IVAN}/the-innkeeper-loop.ogg", .5),
    "backroom": ("Storeroom at night (town night)", f"{IVAN}/town-night-ambiance.ogg", .4),
    "common-room": ("The common room (peaceful tavern)", f"{IVAN}/ambiance-peaceful-tavern.ogg", .5),
    "corridor-between": ("The corridor hum", None, .4),
    "hoard": ("The reading room (Scholars of Mysterious Arts)", f"{IVAN}/scholars-of-mysterious-arts-loop.ogg", .45),
    "cover-cavern": ("The cavern", f"{MG}/ambience/SimpleCave.ogg", .5),
    "c1-stairwell": ("Stairwell: water dripping, echoing", f"{SFX}/Nature/Loops/Water Drips Echo/water-drips-echo-1.mp3", .45),
    "c2-stable": ("Stable: night outside the walls", f"{IVAN}/ambiance-the-grassland-night.ogg", .4),
    "c3-inn-hallway": ("Inn hallway: the taproom, far below", f"{IVAN}/peaceful-tavern-ambiance.ogg", .2),
    "c4-campfire": ("Campfire in the woods", f"{MG}/ambience/CampfireinWoods.ogg", .5),
    "c5-market": ("Market at closing", f"{SFX}/Town/Loops/Market/market-2.mp3", .3),
    "c6-ferry": ("Wind down a dry riverbed", f"{SFX}/Nature/Loops/Wind/wind-1.mp3", .4),
    "c7-crossroads": ("Crossroads at dusk (open fields)", f"{MG}/ambience/FieldsofOreskos.ogg", .45),
    "c8-cellar": ("Cellar: dripping", f"{SFX}/Nature/Loops/Water Drips/water-drips-1.mp3", .4),
}
MUSIC = [  # (key, name, path, repeat, volume)
    ("m-tavern", "Session 1: A Cozy Tavern", f"{IVAN}/a-cozy-tavern.ogg", True, .4),
    ("m-inn", "Session 1: The Inn", f"{MG}/music/TheInn.mp3", True, .4),
    ("m-eerie", "Corridors: Eerie Forest", f"{IVAN}/eerie-forest-loop.ogg", True, .35),
    ("m-mystery", "Corridors: Mystery", f"{IVAN}/mystery-aboard-the-mno-loop.ogg", True, .35),
    ("m-whispers", "Corridors, late: Whispers in the Cell", f"{IVAN}/whispers-in-the-cell.ogg", True, .35),
    ("m-cover", "The Cover: Dracona Mortis", f"{AM}/battles/DraconaMortis.mp3", True, .5),
    ("m-echo", "Room 3, the Echo: Haunted Mansion", f"{IVAN}/haunted-mansion.ogg", True, .4),
    ("m-hoard", "Room 4, the fight: It's All Led Up to This", f"{AM}/battles/ItsAllLedUpToThis.mp3", True, .5),
    ("m-dawn", "Room 5, dawn: Hope", f"{MG}/music/Hope.mp3", False, .45),
    ("m-last", "The Last Word: Sad Strings", f"{IVAN}/sad-strings.ogg", False, .45),
]
# SoundBard pads (StreamDeck-style panel; its banks are stored per browser, so a macro fills one for the GM)
OWN = "the-back-room/audio"
BANKS = {  # SoundBard banks: name -> pads (name, path under modules/, emoji, volume, loop); 12 pads per bank
    "The Back Room: Corridors": [
        ("Door, slowly", f"{SFX}/Misc/Single/Squeaky Door Open Slow/squeaky-door-open-slow-1.mp3", "🚪", .7, False),
        ("A door closes somewhere", f"{SFX}/Misc/Single/Door Close/door-close-1.mp3", "🔒", .6, False),
        ("Footsteps, a half-beat late", f"{OWN}/sting-footsteps.ogg", "👣", .7, False),
        ("The X", f"{OWN}/sting-x-door.ogg", "❌", .7, False),
        ("The lantern lights itself", f"{SFX}/Combat/Single/Spell Whoosh/spell-whoosh-1.mp3", "🏮", .5, False),
        ("Waterfall (stops when someone speaks)", f"{SFX}/Nature/Loops/Waterfall/waterfall-1.mp3", "🌊", .5, True),
        ("The ferry bell", f"{OWN}/sfx-ferry-bell.ogg", "🔔", .7, False),
        ("A horse shifts its weight", f"{SFX}/Creatures/Animals/Horse Whinny/horse-whinny-2.mp3", "🐴", .5, False),
        ("Pages turning", f"{OWN}/sfx-pages-turning.ogg", "📖", .7, False),
        ("Dice, warm, just rolled", f"{OWN}/sfx-dice-rolled.ogg", "🎲", .7, False),
        ("A monster wakes (The Cover)", f"{SFX}/Creatures/Monsters/Growl/growl-3.mp3", "🐉", .7, False),
        ("Cider, poured", f"{OWN}/sfx-cider-poured.ogg", "🍺", .7, False)],
    "The Back Room: People": [
        ("Remnants laughing, through the door", f"{OWN}/sfx-remnants-laughing.ogg", "😂", .4, False),
        ("POW! (Fred)", f"{SFX}/Combat/Single/Melee Hit/melee-hit-7.mp3", "💥", .8, False),
        ("Rorvik bursts in", f"{SFX}/Misc/Single/Impact/impact-2.mp3", "⏰", .8, False),
        ("Strider's arrow", f"{SFX}/Combat/Single/Arrow Fly-By/arrow-fly-by-1.mp3", "🏹", .7, False),
        ("Thon's rod clicks into a new shape", f"{SFX}/Combat/Single/Shield Hit/shield-hit-3.mp3", "🔧", .6, False),
        ("T. Morlock lands a vault", f"{SFX}/Combat/Single/Throw Hit/throw-hit-1.mp3", "🤸", .6, False)],
}
def soundbard_macro(banks): return SB_HEAD + json.dumps({b: [[n, f"modules/{p}", e, v, l] for n, p, e, v, l in pads] for b, pads in banks.items()}, ensure_ascii=False) + SB_TAIL
SB_HEAD = """// Fills SoundBard banks with this adventure's cues (SoundBard keeps banks per browser, so each GM who wants
// the pads runs this once). Re-running it refreshes the same banks.
if (!game.modules.get("soundbard")?.active) return ui.notifications.warn("Enable the SoundBard module first.");
const BANKS = """
SB_TAIL = """;
const data = foundry.utils.deepClone(game.settings.get("soundbard", "soundBank"));
const done = [];
for (const [name, pads] of Object.entries(BANKS)) {
  let bank = data.banks.find(b => b.name === name) ?? data.banks.find(b => !b.name && b.slots.every(s => !s.src));
  if (!bank) { ui.notifications.warn(`SoundBard has no empty bank left for "${name}"; clear one and run this again.`); continue; }
  bank.name = name;
  bank.slots.forEach((slot, i) => Object.assign(slot, pads[i] ? { name: pads[i][0], src: pads[i][1], emoji: pads[i][2], volume: pads[i][3], loop: pads[i][4] } : { name: "", src: "", emoji: "" }));
  done.push(bank);
}
await game.settings.set("soundbard", "soundBank", data);
if (done[0]) await game.settings.set("soundbard", "activeBank", done[0].id);
ui.notifications.info(`SoundBard: ${done.map(b => `bank ${b.id} "${b.name}"`).join(", ")}.`);"""
def remove_macro(pack, title): return REMOVE_TPL.replace("%PACK%", pack).replace("%TITLE%", title)
REMOVE_TPL = """// Deletes exactly the documents this adventure imported (matched by id against the adventure in the compendium).
// Your own documents are left alone. SoundBard banks the setup macro filled stay in SoundBard.
const pack = game.packs.get("the-back-room.%PACK%");
if (!pack) return ui.notifications.error("Enable The Back Room module first.");
const ok = await foundry.applications.api.DialogV2.confirm({ window: { title: "Remove %TITLE%" },
  content: "<p>Delete every scene, actor, journal, playlist, roll table, macro and folder this adventure imported? Your own documents are left alone.</p>" });
if (!ok) return;
const [adv] = await pack.getDocuments();
const types = { scenes: "Scene", actors: "Actor", journal: "JournalEntry", items: "Item", tables: "RollTable", macros: "Macro", playlists: "Playlist", cards: "Cards", folders: "Folder" };
const counts = [];
for (const [field, cls] of Object.entries(types)) {
  const ids = new Set(adv[field]?.map(d => d.id) ?? []);
  const found = game.collections.get(cls).filter(d => ids.has(d.id));
  if (cls === "Playlist") for (const p of found) if (p.playing) await p.stopAll();
  if (found.length) { await getDocumentClass(cls).deleteDocuments(found.map(d => d.id)); counts.push(`${found.length} ${cls}`); }
}
ui.notifications.info(`Removed: ${counts.join(", ") || "nothing (the adventure is not imported here)"}.`);"""
