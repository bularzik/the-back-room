"""Builds src/packs for The Back Room (module id the-back-room) from tools/maps.json, journal.py, actors.py, matt.py.
Scenes whose maps are not in maps.json yet are skipped (with a note), so journals and actors build before the maps do."""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
from actors import build_monsters, build_npcs, uid, MOD
import journal, matt

ID, TITLE, VERSION = "the-back-room", "The Back Room", "2.0.0"
REPO = f"https://github.com/bularzik/{ID}"
PACK_ADV, PACK_BEST = ID, "back-room-bestiary"
ROOT, SRC = ".", "src/packs"
shutil.rmtree(SRC, ignore_errors=True)
for d in (PACK_ADV, PACK_BEST): os.makedirs(f"{SRC}/{d}", exist_ok=True)
maps = json.load(open("tools/maps.json")) if os.path.exists("tools/maps.json") else {}

monsters, npcs = build_monsters(), build_npcs()
allactors = {**monsters, **npcs}

# ---------- scenes: fixed rooms, The Cover, and the pool copies ----------
FIXED = {"backroom": "The Back Room", "common-room": "The Common Room", "corridor-between": "The Corridor Between",
         "hoard": "The Hoard", "cover-cavern": "The Cavern"}
POOL_NAMES = {"c1-stairwell": "Stairwell", "c2-stable": "Stable", "c3-inn-hallway": "Hallway", "c4-campfire": "Clearing",
              "c5-market": "Market Row", "c6-ferry": "Crossing", "c7-crossroads": "Crossroads", "c8-cellar": "Cellar"}
SCENE_KEYS = dict(FIXED)
for p, n in POOL_NAMES.items():
    for c in "abc": SCENE_KEYS[f"{p}-{c}"] = n          # bland, identical names on purpose (concealment)
scene_ids = {k: uid("scene", k) for k in SCENE_KEYS}
built = [k for k in SCENE_KEYS if k in maps or (k.rsplit("-", 1)[0] in maps and k.rsplit("-", 1)[1] in "abc" and k not in FIXED)]
def mapfor(k):
    """Pool copies share one map entry under the place key; a copy's own entry (if present) overrides it."""
    if k in maps: return maps[k]
    return maps[k.rsplit("-", 1)[0]]
missing = [k for k in SCENE_KEYS if k not in built]
if missing: print("  scenes not yet mapped (skipped):", ", ".join(sorted(set(m.rsplit('-', 1)[0] if m not in FIXED else m for m in missing))))

table_ids = {"pool": uid("table", "pool"), "cues": uid("table", "cues")}
F = {t: uid("folder", t) for t in ("JournalEntry", "Handouts", "Actor", "Actor-npc", "Scene", "Scene-pool", "Playlist", "RollTable")}

def L(kind, key, name=None):
    if kind == "actor":
        a = allactors[key]; return f"@UUID[Actor.{a.id}]{{{name or a.doc['name']}}}"
    if kind == "scene":
        return f"@UUID[Scene.{scene_ids[key]}]{{{name or SCENE_KEYS[key]}}}" if key in built else f"<em>{name or SCENE_KEYS[key]}</em>"
    if kind == "table": return f"@UUID[RollTable.{table_ids[key]}]{{{name or ('the Corridor Pool table' if key == 'pool' else 'the Cue table')}}}"
    raise KeyError(kind)

# ---------- journal ----------
journals, page_index, handout_ids = [], {}, {}
_entries = journal.build(L)
_entries[0][1].append(("Automation (Monk's Active Tile Triggers)", matt.GM_GUIDE, 2))
_split = []
for ename, pages in _entries:
    if ename.endswith("Handouts"):
        for p in pages: _split.append((p[0], [p], "Handouts"))
    else:
        _split.append((ename, [(p[0], p[1] + (f'<aside class="notable"><h4>Automation</h4><p>{matt.PAGE_NOTES[p[0]]}</p></aside>' if p[0] in matt.PAGE_NOTES else ""), *p[2:]) for p in pages], "JournalEntry"))
for ei, (ename, pages, fkey) in enumerate(_split):
    jid = uid("journal", ename); pdocs = []
    for pi, page in enumerate(pages):
        pname, html = page[0], page[1]; level = page[2] if len(page) > 2 else 1
        pid = uid(jid, pname); page_index[pname] = (jid, pid)
        pdocs.append({"_id": pid, "name": pname, "type": "text", "title": {"show": True, "level": level},
                      "text": {"format": 1, "content": html}, "sort": (pi + 1) * 100000,
                      "ownership": {"default": -1}, "flags": {}, "image": {}, "video": {}, "src": None, "system": {}})
    if fkey == "Handouts": handout_ids[ename] = f"JournalEntry.{jid}"
    journals.append({"_id": jid, "name": ename, "pages": pdocs, "folder": F[fkey], "sort": (ei + 1) * 100000,
                     "ownership": {"default": 0}, "flags": {}, "categories": []})

# ---------- actors ----------
def actor_doc(a, folder):
    d = json.loads(json.dumps(a.doc)); d["folder"] = folder
    for it in d["items"]: it.pop("_key", None)
    d.pop("_key", None); return d
adv_actors = [actor_doc(a, F["Actor"]) for a in monsters.values()] + [actor_doc(a, F["Actor-npc"]) for a in npcs.values()]

# ---------- roll tables ----------
def table(key, name, formula, desc, rows, img):
    tid = table_ids[key]; res = []
    for i, (lo, hi, text) in enumerate(rows):
        res.append({"_id": uid(tid, str(i)), "type": "text", "name": "", "description": text, "img": "icons/svg/d20-black.svg",
                    "weight": hi - lo + 1, "range": [lo, hi], "drawn": False, "flags": {}})
    return {"_id": tid, "name": name, "img": img, "description": desc, "results": res, "formula": formula,
            "replacement": True, "displayRoll": True, "folder": F["RollTable"], "sort": 0, "ownership": {"default": 0}, "flags": {}}
tables = [
    table("pool", "The Corridor Pool", "1d8", "<p>Which in-between place is behind the door. Reroll 8 before visit 5. Never the place just left.</p>", [
        (1, 1, "<strong>Stairwell.</strong> The steps go down and arrive one floor up."),
        (2, 2, "<strong>Stable.</strong> The horses face the wall. They are the party's own mounts, the ones they never bought."),
        (3, 3, "<strong>Hallway of inn doors.</strong> Every door has the same number. One is ajar."),
        (4, 4, "<strong>Campfire clearing.</strong> The fire gives no heat. A bedroll is already slept in, still warm."),
        (5, 5, "<strong>Market row at closing.</strong> Stalls shuttered by nobody. The potions are all red."),
        (6, 6, "<strong>Ferry crossing.</strong> A jetty, a lantern, no water and no ferry. The sound of a waterfall."),
        (7, 7, "<strong>Crossroads at dusk.</strong> Every arm of the signpost points the same way. The light never finishes going."),
        (8, 8, "<strong>Cellar</strong> (visit 5+ only). The back room from underneath. The provisions chest is breathing."),
    ], "icons/svg/door-exit.svg"),
    table("cues", "Corridor Cues (generic)", "1d6", "<p>Roll for a place-neutral cue in the 3–6 visit band, when the place's own cue has been used.</p>", [
        (1, 1, "Footsteps matching the party's own, a half-beat late."),
        (2, 2, "A chair creaks in an empty room."),
        (3, 3, "A door closes somewhere behind the party; all the doors are as they were."),
        (4, 4, "A figure at the end of the corridor, gone when looked at directly. It is wearing something one of the players' first characters wore."),
        (5, 5, "Someone says one character's name in the voice of the player who sits beside them."),
        (6, 6, "A half-page book, face down, where nobody left one."),
    ], "icons/svg/eye.svg"),
]

# ---------- playlists (v1 audio reused as placeholders until tools/audio.py is rerun for v2) ----------
def snd(name, file, repeat, vol, desc=""):
    return {"_id": uid("sound", file), "name": name, "path": f"{MOD}/audio/{file}.ogg", "repeat": repeat, "volume": vol,
            "description": desc, "fade": 1000 if repeat else None, "playing": False, "pausedTime": None, "sort": 0, "flags": {}}
playlists = [
    {"_id": uid("playlist", "amb"), "name": "Back Room: Ambience", "description": "Loops. Placeholder audio from v1 until the v2 loops are rendered.",
     "mode": -1, "fade": 1000, "sounds": [snd("Tavern, late", "ambience-tavern", True, .45), snd("Corridor hum", "ambience-corridor", True, .4),
                                           snd("Reading room, dawn", "ambience-reading-room", True, .4)],
     "folder": F["Playlist"], "sort": 100000, "ownership": {"default": 0}, "flags": {}, "playing": False},
    {"_id": uid("playlist", "sting"), "name": "Back Room: Stingers", "description": "One-shot cues used by the door tiles.", "mode": -1, "fade": None,
     "sounds": [snd("Door", "sting-door", False, .7), snd("The X", "sting-x-door", False, .7), snd("Footsteps, a half-beat late", "sting-footsteps", False, .7)],
     "folder": F["Playlist"], "sort": 200000, "ownership": {"default": 0}, "flags": {}, "playing": False},
]

# ---------- scenes ----------
NOTE_PAGES = {"A1": "The Evening", "A2": "The Evening", "A3": "The Night Event", "A4": "The Evening", "A5": "The Night Event",
              "B1": "The Room", "B2": "The Puzzle", "B3": "The Room", "B4": "The Room", "B5": "The Room",
              "C1": "The Trick", "C2": "The Trick", "C3": "The Trick", "C4": "The Trick", "C5": "The Trick", "C6": "The Setback & the Echo",
              "D1": "The Antagonist", "D2": "The Reading Room", "D3": "The Reading Room", "D4": "The Antagonist", "D5": "The Reading Room",
              "E1": "The Cavern", "E2": "The Six", "E3": "The Six", "E4": "The Six", "E5": "The Six"}
scenes = []
for i, key in enumerate(built):
    m = mapfor(key); sid = scene_ids[key]; is_pool = key not in FIXED
    walls = [{"_id": uid(sid, "w", str(j)), **w, "dir": 0, "threshold": {"light": None, "sight": None, "sound": None, "attenuation": False}, "flags": {}}
             for j, w in enumerate(m.get("walls", []))]
    lights = []
    for j, l in enumerate(m.get("lights", [])):
        lights.append({"_id": uid(sid, "l", str(j)), "x": int(l["x"]), "y": int(l["y"]), "rotation": 0, "walls": True, "vision": False, "hidden": False,
                       "config": {"dim": round(l["dim"]), "bright": round(l["bright"]), "color": l.get("color"), "alpha": l.get("alpha", .3), "angle": 360,
                                  "coloration": 1, "luminosity": .5, "attenuation": .5, "saturation": 0, "contrast": 0, "shadows": 0,
                                  "animation": {"type": l.get("anim"), "speed": 3, "intensity": 3, "reverse": False}, "darkness": {"min": 0, "max": 1}},
                       "flags": {}})
    notes = []
    for code, (x, y) in m.get("notes", {}).items():
        if code not in NOTE_PAGES or NOTE_PAGES[code] not in page_index: continue
        jid, pid = page_index[NOTE_PAGES[code]]
        notes.append({"_id": uid(sid, "n", code), "entryId": jid, "pageId": pid, "x": int(x), "y": int(y),
                      "texture": {"src": "icons/svg/book.svg", "tint": "#ffe9a8"}, "iconSize": 48, "text": code,
                      "fontSize": 28, "textAnchor": 1, "textColor": "#ffffff", "global": False, "flags": {}})
    sx, sy = m.get("start", [m["w"] // 2, m["h"] // 2])
    jref = page_index[NOTE_PAGES[list(m["notes"])[0]]][0] if m.get("notes") and list(m["notes"])[0] in NOTE_PAGES else None
    darkness = m.get("darkness", .7 if is_pool else .5)
    scenes.append({"_id": sid, "name": SCENE_KEYS[key], "navigation": not is_pool, "navOrder": i, "navName": "", "active": False,
                   "background": {"src": f"{MOD}/maps/{m['file']}"}, "foreground": None,
                   "thumb": f"{MOD}/maps/thumb-{m['file']}", "width": m["w"], "height": m["h"], "padding": 0,
                   "initial": {"x": int(sx), "y": int(sy), "scale": .7}, "backgroundColor": "#0b0a07",
                   "grid": {"type": 1, "size": 100, "style": "solidLines", "thickness": 1, "color": "#000000", "alpha": .12, "distance": 5, "units": "ft"},
                   "tokenVision": True, "fog": {"exploration": True, "reset": None, "overlay": None, "colors": {"explored": None, "unexplored": None}},
                   "environment": {"darknessLevel": darkness, "darknessLock": False, "globalLight": {"enabled": False}, "cycle": True},
                   "drawings": [], "tokens": [], "lights": lights, "notes": notes, "sounds": [], "regions": [], "tiles": [], "walls": walls,
                   "playlist": None, "playlistSound": None, "journal": jref, "journalEntryPage": None,
                   "weather": "", "folder": F["Scene-pool"] if is_pool else F["Scene"], "sort": (i + 1) * 100000, "ownership": {"default": 0}, "flags": {}})

ctx = {"scene_ids": {k: scene_ids[k] for k in built}, "rects": {k: mapfor(k).get("rects", {}) for k in built}, "handouts": handout_ids,
       "table_uuid": {k: f"RollTable.{v}" for k, v in table_ids.items()}}
tiles = matt.build_tiles(ctx)
for s, k in zip(scenes, built): s["tiles"] = tiles.get(k, [])

folders = [
    {"_id": F["JournalEntry"], "name": TITLE, "type": "JournalEntry", "color": "#27413b", "sorting": "a", "folder": None, "sort": 0, "flags": {}},
    {"_id": F["Handouts"], "name": "Handouts", "type": "JournalEntry", "color": "#3b6a5a", "sorting": "a", "folder": F["JournalEntry"], "sort": 0, "flags": {}},
    {"_id": F["Actor"], "name": "Back Room: The Cover", "type": "Actor", "color": "#7a2e24", "sorting": "a", "folder": None, "sort": 0, "flags": {}},
    {"_id": F["Actor-npc"], "name": "Back Room: People", "type": "Actor", "color": "#27413b", "sorting": "a", "folder": None, "sort": 0, "flags": {}},
    {"_id": F["Scene"], "name": TITLE, "type": "Scene", "color": "#27413b", "sorting": "m", "folder": None, "sort": 0, "flags": {}},
    {"_id": F["Scene-pool"], "name": "Corridors", "type": "Scene", "color": "#3b6a5a", "sorting": "m", "folder": F["Scene"], "sort": 0, "flags": {}},
    {"_id": F["Playlist"], "name": TITLE, "type": "Playlist", "color": "#27413b", "sorting": "m", "folder": None, "sort": 0, "flags": {}},
    {"_id": F["RollTable"], "name": TITLE, "type": "RollTable", "color": "#27413b", "sorting": "a", "folder": None, "sort": 0, "flags": {}},
]

adv_id = uid("adventure", ID)
adventure = {"_id": adv_id, "name": TITLE, "img": f"{MOD}/maps/cover.webp",
             "caption": "A liminal-horror adventure for 5th–8th level characters",
             "description": f"<p>The party beds down in the storeroom over a tavern kitchen and never leaves it. Stairwells, stables, corridors and campsites — all the back room, misremembered — and in there with them, their own first characters, who want the game to go on forever.</p><p><strong>Contents:</strong> {len(scenes)} scenes with walls, lights, notes and Monk's Active Tile Triggers automation; {len(adv_actors)} actors; {len(journals)} journal entries; 2 roll tables; 2 playlists.</p><p>Start with the journal <em>00. The Back Room: Adventure Overview</em>.</p>",
             "actors": adv_actors, "combats": [], "items": [], "scenes": scenes, "journal": journals, "tables": tables,
             "macros": [], "cards": [], "playlists": playlists, "folders": folders, "sort": 0, "flags": {}, "_key": f"!adventures!{adv_id}"}
json.dump(adventure, open(f"{SRC}/{PACK_ADV}/{PACK_ADV}.json", "w"), indent=1)
for k, a in allactors.items():
    d = json.loads(json.dumps(a.doc)); d["folder"] = None
    json.dump(d, open(f"{SRC}/{PACK_BEST}/{k}.json", "w"), indent=1)

# ---------- manifest ----------
manifest = {
    "id": ID, "title": TITLE,
    "description": "<p>A Backrooms-inspired liminal-horror adventure for D&amp;D 5e (2024 rules), levels 5–8: the party beds down in a tavern back room and never leaves it. Scenes, actors, journals, handouts, roll tables and ambient audio, with Monk's Active Tile Triggers automation.</p>",
    "version": VERSION, "url": REPO,
    "manifest": f"{REPO}/releases/latest/download/module.json",
    "download": f"{REPO}/releases/download/v{VERSION}/module.zip",
    "authors": [{"name": "Dan Bularzik"}, {"name": "Generated with Claude"}],
    "compatibility": {"minimum": "14", "verified": "14"},
    "relationships": {
        "systems": [{"id": "dnd5e", "type": "system", "compatibility": {"minimum": "5.0.0"}}],
        "requires": [{"id": "monks-active-tiles", "type": "module",
                      "manifest": "https://github.com/ironmonk108/monks-active-tiles/releases/latest/download/module.json",
                      "compatibility": {"minimum": "14.01"}, "reason": "Scene automation: random Corridor doors, fog resets, the X door, the Corridor Between loop, the Room 4 exit and GM controls."}]},
    "packs": [
        {"name": PACK_ADV, "label": f"{TITLE} (Adventure)", "path": f"packs/{PACK_ADV}", "type": "Adventure", "system": "dnd5e", "ownership": {"PLAYER": "NONE", "ASSISTANT": "OWNER"}},
        {"name": PACK_BEST, "label": f"{TITLE}: Bestiary", "path": f"packs/{PACK_BEST}", "type": "Actor", "system": "dnd5e", "ownership": {"PLAYER": "NONE", "ASSISTANT": "OWNER"}}],
    "packFolders": [{"name": TITLE, "sorting": "m", "color": "#27413b", "packs": [PACK_ADV, PACK_BEST]}],
    "languages": [], "esmodules": [], "styles": [],
}
json.dump(manifest, open(f"{ROOT}/module.json", "w"), indent=2)
print("sources written:", len(scenes), "scenes,", len(journals), "journals,", sum(len(j['pages']) for j in journals), "pages,", len(adv_actors), "actors")
