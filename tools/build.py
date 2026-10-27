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

# ---------- journal: Monk's Enhanced Journal entries + Campaign Companion sessions ----------
# Every entry is ONE text page carrying MEJ's type flag (the shape MEJ and the companion create themselves):
#   page.type "text", page.flags["monks-enhanced-journal"] = {type, ...per-type defaults, ...data}; the entry carries
#   {pagetype, img}. Sessions are the companion's native page type with system.recap/gmNotes.
MEJ, CC = "monks-enhanced-journal", "mej-campaign-companion"
MEJ_DEFAULTS = {"person": {"relationships": {}, "attributes": {}}, "place": {"relationships": {}, "attributes": {}},
                "quest": {"rewards": {}, "objectives": {}, "seen": False, "status": "inactive"},
                "encounter": {"items": {}, "actors": {}, "dcs": {}}, "organization": {"relationships": {}}, "journalentry": {}}
journals, page_index, handout_ids = [], {}, {}
jid_of = lambda name: uid("journal", name)
def mej_entry(name, mtype, html, folder, data=None, ownership=0, sort=0, session=None):
    jid = jid_of(name); pid = uid(jid, "page")
    if session:
        page = {"_id": pid, "name": name, "type": f"{CC}.session", "title": {"show": False, "level": 1}, "text": {"format": 1, "content": ""},
                "system": {"recap": html, "gmNotes": session.pop("gmNotes", "")}, "sort": 100000, "ownership": {"default": -1},
                "flags": {CC: {"session": {"sessionNumber": session.get("number"), "campaignDate": None, "attendees": [], "secrets": [], "autoTimepoint": False}},
                          MEJ: {"type": "session"}}, "image": {}, "video": {}, "src": None}
        eflags = {MEJ: {"pagetype": "session"}}
    else:
        page = {"_id": pid, "name": name, "type": "text", "title": {"show": False, "level": 1}, "text": {"format": 1, "content": html},
                "sort": 100000, "ownership": {"default": -1}, "flags": {MEJ: {"type": mtype, **MEJ_DEFAULTS.get(mtype, {}), **(data or {})}},
                "image": {}, "video": {}, "src": None, "system": {}}
        eflags = {MEJ: {"pagetype": mtype, "img": f"modules/monks-enhanced-journal/assets/{mtype}.png"}}
    page_index[name] = (jid, pid)
    journals.append({"_id": jid, "name": name, "pages": [page], "folder": folder, "sort": sort, "ownership": {"default": ownership}, "flags": eflags, "categories": []})
    return jid
def rel(name, relationship="", hidden=False, role=None):
    """A relationship row to another journal entry (MEJ keys them by the other entry's id)."""
    r = {"id": jid_of(name), "uuid": f"JournalEntry.{jid_of(name)}", "relationship": relationship, "hidden": hidden}
    if role: r["role"] = role
    return r
def rels(*rows): return {r["id"]: r for r in rows}
def actor_ref(key, **extra):
    a = allactors[key]; return {"id": a.id, "uuid": f"Actor.{a.id}", "name": a.doc["name"], "img": a.doc["img"], **extra}
def join_pages(pages): return "".join(p[1] + (f'<aside class="notable"><h4>Automation</h4><p>{matt.PAGE_NOTES[p[0]]}</p></aside>' if p[0] in matt.PAGE_NOTES else "") for p in pages)

_entries = dict(journal.build(L))
S = 0
def nxt():
    global S; S += 100000; return S
# Guides and rules
mej_entry("00. The Back Room: Adventure Overview", "journalentry", join_pages(_entries["00. The Back Room: Adventure Overview"]), F["JournalEntry"], sort=nxt())
mej_entry("01. Rules of the Back Room", "journalentry", join_pages(_entries["01. Rules of the Back Room"]), F["JournalEntry"], sort=nxt())
mej_entry("02. Automation (Monk's Active Tile Triggers)", "journalentry", matt.GM_GUIDE, F["JournalEntry"], sort=nxt())
# The five rooms as Places; the people in them as townsfolk
ROOM_PEOPLE = {"Room 1: The Back Room": ["The Barkeep", "The Hooded Stranger"], "Room 2: The Common Room That Isn't": ["The Hooded Stranger", "The Rogue With a Tragic Past"],
               "Room 3: The Corridor Between": ["The Echo"], "Room 4: The Hoard": ["The Rogue With a Tragic Past", "The Barbarian Who Is Just Strong", "The Wizard Who Misread the Spell"],
               "Room 5: The Back Room, Again": ["The Barkeep", "The Hooded Stranger"]}
ROOM_SIZE = {"Room 1: The Back Room": "12×10 squares, upstairs", "Room 2: The Common Room That Isn't": "16×12 squares", "Room 3: The Corridor Between": "6 segments of 8×2 squares",
             "Room 4: The Hoard": "16×14 squares", "Room 5: The Back Room, Again": "12×10 squares, the same room"}
for old in ["02. Room 1: The Back Room", "03. Room 2: The Common Room That Isn't", "04. Room 3: The Corridor Between", "05. Room 4: The Hoard", "06. Room 5: The Back Room, Again"]:
    name = old[4:]
    mej_entry(name, "place", join_pages(_entries[old]), F["JournalEntry"], sort=nxt(),
              data={"attributes": {"size": ROOM_SIZE[name], "inhabitants": ", ".join(ROOM_PEOPLE[name])},
                    "relationships": rels(*[rel(pn, role="in this room") for pn in ROOM_PEOPLE[name]])})
# The Corridor pool: the rules as a journal entry, each place as a Place
pool_pages = _entries["07. The Corridor Pool"]
mej_entry("The Corridor Pool: rules for every place", "journalentry", pool_pages[0][1], F["JournalEntry"], sort=nxt())
POOL_PLACE = {}
for pname, html, *_ in pool_pages[1:]:
    name = "Corridor: " + pname.split(". ", 1)[1]
    key = {"Stairwell": "c1-stairwell", "Stable": "c2-stable", "Hallway of Inn Doors": "c3-inn-hallway", "Campfire Clearing": "c4-campfire", "Market Row at Closing": "c5-market",
           "Ferry Crossing": "c6-ferry", "Crossroads at Dusk": "c7-crossroads", "Cellar": "c8-cellar"}[pname.split(". ", 1)[1]]
    POOL_PLACE[key] = name
    mej_entry(name, "place", html, F["JournalEntry"], sort=nxt(), data={"attributes": {"size": "one Dungeondraft map, three scene copies", "inhabitants": "nobody, until visit 7"}})
# The Cover as an Encounter with its six monsters
mej_entry("The Cover", "encounter", join_pages(_entries["08. The Cover (the Corridor fight)"]), F["JournalEntry"], sort=nxt(),
          data={"actors": {allactors[k].id: actor_ref(k, quantity="1", hidden=False) for k in ("dragon", "unicorn", "centaur", "troll", "roper", "owlbear")}})
# People: one Person per NPC, linked to its actor; the Remnants also belong to the organization
PEOPLE = {"barkeep": ("The Barkeep", {"profession": "Tavern keeper", "voice": "Kind, tired in a way that is not unhappy", "faction": "The tavern"}),
          "stranger": ("The Hooded Stranger", {"profession": "Quest-giver", "voice": "The hook, word for word", "faction": "Every booth"}),
          "remnant-rogue": ("The Rogue With a Tragic Past", {"profession": "Rogue (someone's first character)", "voice": "'It's complicated.'", "faction": "The Remnants"}),
          "remnant-barbarian": ("The Barbarian Who Is Just Strong", {"profession": "Barbarian (someone's first character)", "voice": "Cheerful. Has never been angry.", "faction": "The Remnants"}),
          "remnant-wizard": ("The Wizard Who Misread the Spell", {"profession": "Wizard (someone's first character)", "voice": "Insists.", "faction": "The Remnants"}),
          "echo": ("The Echo", {"profession": "A copy", "voice": "None", "faction": "The Corridor Between"})}
for key, (name, attrs) in PEOPLE.items():
    a = allactors[key]; rooms = [rn for rn, ppl in ROOM_PEOPLE.items() if name in ppl]
    data = {"attributes": attrs, "actor": actor_ref(key), "relationships": rels(*[rel(rn, role="appears here") for rn in rooms], *([rel("The Remnants", relationship="member")] if attrs["faction"] == "The Remnants" else []))}
    mej_entry(name, "person", a.doc["system"]["details"]["biography"]["value"], F["JournalEntry"], sort=nxt(), data=data)
mej_entry("The Remnants", "organization", journal.P(
    "The first party: each player's first-ever D&D character, as the table misremembers them — overpowered, cooler than they were, one running joke swollen into a whole personality. They are not hostile. They want the game to keep going, forever, with the party in it.",
    "One appears in Room 2. One more surfaces in the Corridors at visit 7+. All of them are in Room 4. The three listed here are the fallbacks; the real ones are built from the players' answers to the one question asked before session one.")
    + "<h3>Rules</h3>" + journal.ul("Max hit points, never rolled.", "The Signature always works, once per round.", "Everything else is blank.", "It never attacks first.", "At 0 HP it stands back up in the pose it fell in.", "It cannot leave a room through a door the party came through."),
    F["JournalEntry"], sort=nxt(), data={"relationships": rels(*[rel(n, relationship="member") for n in ("The Rogue With a Tragic Past", "The Barbarian Who Is Just Strong", "The Wizard Who Misread the Spell")])})
# The stated goal as a Quest
mej_entry("Follow the X", "quest", journal.P("The map the Remnant hands over in Room 2 has an X on it. The X marks the way out. It moves when nobody looks at it. It points at the Hoard.",
    "The real goal, discovered in Rooms 4–5: the way out was the door they came in by. The stated goal was the thing keeping them from it."),
    F["JournalEntry"], sort=nxt(), data={"status": "inactive", "objectives": {uid("obj", str(i)): {"id": uid("obj", str(i)), "content": c, "available": i == 0, "status": False, "done": 0, "required": ""}
        for i, c in enumerate(["Find the Remnant among the roles in the common room and get it to say its Signature.", "Follow the X through the Corridors.",
                               "Leave something behind in the Corridor Between.", "Reach the Hoard.", "Go back the way you came in, without looking back."])}})
# Cast index (plain)
mej_entry("Cast", "journalentry", join_pages(_entries["09. Cast"]), F["JournalEntry"], sort=nxt())
# Handouts
for pname, html, *_ in _entries["10. Handouts"]:
    jid = mej_entry(pname, "journalentry", html, F["Handouts"], sort=nxt()); handout_ids[pname] = f"JournalEntry.{jid}"
# Campaign Companion structure: the campaign's portal entry and its default timeline (what createCampaign() makes)
PORTAL_ID, TIMELINE_ID = uid("journal", "campaign-portal"), uid("journal", "campaign-timeline")
journals.append({"_id": PORTAL_ID, "name": TITLE, "folder": F["JournalEntry"], "sort": 0, "ownership": {"default": 0}, "categories": [],
                 "flags": {CC: {"campaignPortal": True}},   # no MEJ pagetype flag: the companion's guard reads it as a stray campaign page and refuses the entry
                 "pages": [{"_id": uid(PORTAL_ID, "page"), "name": TITLE, "type": f"{CC}.campaign", "title": {"show": False, "level": 1}, "text": {"format": 1, "content": ""},
                            "sort": 100000, "ownership": {"default": -1}, "flags": {CC: {"campaignPortal": True}, MEJ: {"type": "campaign"}}, "image": {}, "video": {}, "src": None, "system": {}}]})
journals.append({"_id": TIMELINE_ID, "name": f"{TITLE} — Timeline", "folder": F["JournalEntry"], "sort": 50000, "ownership": {"default": 0}, "categories": [], "pages": [],
                 "flags": {CC: {"timeline": {"timepoints": []}}, "core": {"sheetClass": f"{CC}.TimelineJournalSheet"}}})
# Sessions (Campaign Companion): recap is the players' shared text, GM notes carry the plan
SESSIONS = [("Session 1: The Tavern", "Rooms 1–2 and two Corridors (visits 1–2). Ask each player, privately and before play, for their first character's name, class and the one thing everyone remembers. Play the tavern straight. End on the X map."),
            ("Session 2: The Corridors", "Three or four Corridors (visits 3–6, including The Cover and the glimpse), then Room 3. Track every Misremembering change: who, what it was, what it is now."),
            ("Session 3: The Hoard", "A Corridor at visit 7+ with a Remnant in it, Room 4, Room 5. Spell the stakes out at the top of round 3. Make staying a real temptation.")]
for i, (name, plan) in enumerate(SESSIONS):
    mej_entry(name, "session", "<p></p>", F["JournalEntry"], sort=nxt(), ownership=2, session={"number": i + 1, "gmNotes": f"<p>{plan}</p>"})

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
NOTE_PAGES = {**{f"A{i}": "Room 1: The Back Room" for i in range(1, 6)}, **{f"B{i}": "Room 2: The Common Room That Isn't" for i in range(1, 6)},
              **{f"C{i}": "Room 3: The Corridor Between" for i in range(1, 7)}, **{f"D{i}": "Room 4: The Hoard" for i in range(1, 6)}, **{f"E{i}": "The Cover" for i in range(1, 6)}}
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
    jref = page_index[NOTE_PAGES[list(m["notes"])[0]]][0] if m.get("notes") and list(m["notes"])[0] in NOTE_PAGES else (page_index[POOL_PLACE[key.rsplit("-", 1)[0]]][0] if is_pool else None)
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
    {"_id": F["JournalEntry"], "name": TITLE, "type": "JournalEntry", "color": "#27413b", "sorting": "m", "folder": None, "sort": 0,
     "flags": {CC: {"campaign": {"ownershipDefault": "none", "defaultTimelineId": TIMELINE_ID}}}},   # a Campaign Companion campaign; the companion adds the portal and timeline
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
             "description": f"<p>The party beds down in the storeroom over a tavern kitchen and never leaves it. Stairwells, stables, corridors and campsites — all the back room, misremembered — and in there with them, their own first characters, who want the game to go on forever.</p><p><strong>Contents:</strong> {len(scenes)} scenes with walls, lights, notes and Monk's Active Tile Triggers automation; {len(adv_actors)} actors; {len(journals)} journal entries; 2 roll tables; 2 playlists.</p><p>Start with the journal <em>00. The Back Room: Adventure Overview</em>; the journal folder is a Campaign Companion campaign with three prepared Sessions.</p>",
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
        "requires": [{"id": "monks-enhanced-journal", "type": "module",
                      "manifest": "https://github.com/ironmonk108/monks-enhanced-journal/releases/latest/download/module.json",
                      "compatibility": {"minimum": "14.01"}, "reason": "Every journal entry is an Enhanced Journal Place, Person, Encounter, Organization or Quest."},
                     {"id": "mej-campaign-companion", "type": "module",
                      "manifest": "https://github.com/bularzik/mej-campaign-companion/releases/latest/download/module.json",
                      "compatibility": {"minimum": "0.26.0"}, "reason": "The adventure's journal folder is a campaign with three Session pages."},
                     {"id": "monks-active-tiles", "type": "module",
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
