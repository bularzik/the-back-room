"""Builds src/packs/the-back-room-unfinished: the second Adventure in the module, The Back Room: The Unfinished Fight.
Same maps, art, people and audio as The Back Room; a fixed route, its own journals, tiles and Cover monsters.
Every document id is salted, so both adventures can sit in one compendium folder without clashing.
Run after tools/build.py (which writes module.json, listing both packs)."""
import json, math, os, shutil, sys
sys.path.insert(0, os.path.dirname(__file__))
import actors
_base_uid = actors.uid
def uid(*parts): return _base_uid("unfinished", *parts)
actors.uid = uid                      # every actor/item id made from here on is salted
import matt; matt.uid = uid           # and every tile/action id
from actors import MOD
import journal as base_journal
import journal_unfinished as journal, matt_unfinished
from actors_unfinished import build_waves, build_allies
from sound import IVAN, MG, AM, SFX, AMBIENCE, BANKS, soundbard_macro, remove_macro

ID = "the-back-room"
PACK, TITLE = "the-back-room-unfinished", "The Back Room: The Unfinished Fight"
ROOT, SRC = ".", "src/packs"
shutil.rmtree(f"{SRC}/{PACK}", ignore_errors=True)
os.makedirs(f"{SRC}/{PACK}", exist_ok=True)
maps = json.load(open("tools/maps.json"))

monsters, npcs = build_waves(), build_allies()
allactors = {**monsters, **npcs}

# ---------- scenes: the route, in order ----------
ROUTE = {"backroom": "1. The Back Room", "common-room": "2. The Common Room That Isn't", "c7-crossroads": "3. The Crossroads",
         "c8-cellar": "4. The Cellar", "c2-stable": "5. The Stable", "hoard": "6. The Hoard", "cover-cavern": "7. The Cover"}
NAV_NAME = {"backroom": "Upstairs", "common-room": "Downstairs", "c7-crossroads": "A Crossroads", "c8-cellar": "A Cellar",
            "c2-stable": "A Stable", "hoard": "A Room", "cover-cavern": "A Cave"}
scene_ids = {k: uid("scene", k) for k in ROUTE}
VISTAS = {"backroom": "The Back Room", "common-room": "The Common Room", "c7-crossroads": "The Crossroads", "c8-cellar": "The Cellar",
          "c2-stable": "The Stable", "hoard": "The Hoard", "cover-cavern": "The Cover"}
vista_id = lambda key: uid("scene", "vista-" + key)
vista_src = lambda key: f"{MOD}/vistas/{key}.webp"
def vista_box(key): return (f'<aside class="notable"><h4>Vista</h4><p>On arrival, show the players @UUID[Scene.{vista_id(key)}]{{the vista}} '
                            f'(a painted view of the place, no grid), then pull them to the map.</p></aside>')
# Doors this adventure changes on the shared maps: (scene, name) -> (wall coords, door type, state). 1 = door, 2 = secret; state 0 closed, 2 locked.
DOORS = {("backroom", "loft"): ([1100, 400, 1100, 500], 2, 0),        # hidden until night: the party never sees it before then
         ("backroom", "stairwell"): ([600, 900, 500, 900], 1, 0),
         ("common-room", "xdoor"): ([100, 700, 100, 600], 1, 2),      # Fred's Signature unlocks it
         ("c8-cellar", "door2"): ([1100, 200, 1100, 300], 1, 2),      # Thon's button six
         ("c2-stable", "door3"): ([1500, 600, 1500, 700], 1, 2),      # T. Morlock, through the wall
         ("hoard", "side"): ([1400, 650, 1400, 750], 1, 2)}           # the party says yes

table_ids = {"jokes": uid("table", "jokes")}
F = {t: uid("folder", t) for t in ("JournalEntry", "Handouts", "Actor", "Actor-npc", "Scene", "Scene-vista", "Playlist", "RollTable")}
TABLE_REMNANTS = ("remnant-fred", "remnant-thon", "remnant-rorvik", "remnant-morlock", "remnant-strider")
FALLBACK_REMNANTS = ("remnant-rogue", "remnant-barbarian", "remnant-wizard")
PERSON_KEYS = ("barkeep", "stranger", *TABLE_REMNANTS, *FALLBACK_REMNANTS)
npc_name = lambda key: allactors[key].doc["name"]
def L(kind, key, name=None):
    if kind == "actor":
        if key in PERSON_KEYS: return f"@UUID[JournalEntry.{uid('journal', npc_name(key))}]{{{name or npc_name(key)}}}"
        a = allactors[key]; return f"@UUID[Actor.{a.id}]{{{name or a.doc['name']}}}"
    if kind == "scene": return f"@UUID[Scene.{scene_ids[key]}]{{{name or ROUTE[key]}}}"
    if kind == "table": return f"@UUID[RollTable.{table_ids[key]}]{{{name or 'the Drunk’s Joke table'}}}"
    if kind == "journal": return f"@UUID[JournalEntry.{uid('journal', key)}]{{{name or key}}}"
    raise KeyError(kind)

# ---------- journals ----------
MEJ, CC = "monks-enhanced-journal", "mej-campaign-companion"
MEJ_DEFAULTS = {"person": {"relationships": {}, "attributes": {}}, "place": {"relationships": {}, "attributes": {}},
                "quest": {"rewards": {}, "objectives": {}, "seen": False, "status": "inactive"},
                "encounter": {"items": {}, "actors": {}, "dcs": {}}, "organization": {"relationships": {}}, "journalentry": {}}
journals, page_index, handout_ids = [], {}, {}
jid_of = lambda name: uid("journal", name)
def mej_entry(name, mtype, html, folder, data=None, ownership=0, sort=0, session=None, src=None):
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
                "image": {}, "video": {}, "src": src, "system": {}}
        eflags = {MEJ: {"pagetype": mtype, "img": src or f"modules/monks-enhanced-journal/assets/{mtype}.png"}}
    page_index[name] = (jid, pid)
    journals.append({"_id": jid, "name": name, "pages": [page], "folder": folder, "sort": sort, "ownership": {"default": ownership}, "flags": eflags, "categories": []})
    return jid
def rel(name, relationship="", role=None):
    r = {"id": jid_of(name), "uuid": f"JournalEntry.{jid_of(name)}", "relationship": relationship, "hidden": False}
    if role: r["role"] = role
    return r
def rels(*rows): return {r["id"]: r for r in rows}
def actor_ref(key, **extra):
    a = allactors[key]; return {"id": a.id, "uuid": f"Actor.{a.id}", "name": a.doc["name"], "img": a.doc["img"], **extra}
def join_pages(pages): return "".join(p[1] + (f'<aside class="notable"><h4>Automation</h4><p>{matt_unfinished.PAGE_NOTES[p[0]]}</p></aside>' if p[0] in matt_unfinished.PAGE_NOTES else "") for p in pages)

E = dict(journal.build(L))
S = 0
def nxt():
    global S; S += 100000; return S
mej_entry("00. The Unfinished Fight: Overview", "journalentry", join_pages(E["00. The Unfinished Fight: Overview"]), F["JournalEntry"], sort=nxt())
mej_entry("How to Run It: Step by Step", "journalentry", join_pages(E["00b. How to Run It"]), F["JournalEntry"], sort=nxt())
mej_entry("01. Automation (Monk's Active Tile Triggers)", "journalentry", matt_unfinished.GM_GUIDE, F["JournalEntry"], sort=nxt())
PLACES = [  # (journal name, vista key, size, people)
    ("Room 1: The Back Room", "backroom", "12×10 squares, upstairs", ["barkeep"]),
    ("Room 2: The Common Room That Isn't", "common-room", "16×12 squares", ["stranger", "remnant-fred"]),
    ("The Crossroads", "c7-crossroads", "16×16 squares, open country", ["remnant-strider"]),
    ("The Cellar", "c8-cellar", "12×10 squares", ["remnant-thon"]),
    ("The Stable", "c2-stable", "16×12 squares, a hayloft above", ["remnant-morlock"]),
    ("The Hoard", "hoard", "16×14 squares", ["remnant-fred", "remnant-thon", "remnant-morlock", "remnant-strider"]),
    ("Room 5: The Back Room, Again", "backroom", "12×10 squares, the same room", ["barkeep", "stranger"])]
for name, vk, size, people in PLACES:
    mej_entry(name, "place", vista_box(vk) + join_pages(E[name]), F["JournalEntry"], sort=nxt(), src=vista_src(vk),
              data={"attributes": {"size": size, "inhabitants": ", ".join(npc_name(p) for p in people)},
                    "relationships": rels(*[rel(npc_name(p), role="here") for p in people])})
    if name == "The Hoard":   # the Cover follows the Hoard
        mej_entry("The Cover", "encounter", vista_box("cover-cavern") + join_pages(E["The Cover"]), F["JournalEntry"], sort=nxt(), src=vista_src("cover-cavern"),
                  data={"actors": {allactors[k].id: actor_ref(k, quantity=str(q), hidden=False) for k, q in
                                   (("troll", 1), ("roper", 1), ("piercer", 6), ("centaur", 1), ("unicorn", 1), ("outrider", 3), ("owlbear", 1), ("cub", 2), ("dragon", 1))}})
PEOPLE = {"barkeep": ("Innkeeper of the Stickit Inn", {"profession": "Innkeeper", "voice": "Kind, tired in a way that is not unhappy", "faction": "The Stickit Inn"}, "The Stickit Inn"),
          "stranger": ("The hooded stranger in the corner booth", {"profession": "Quest-giver", "voice": "The hook, word for word", "faction": "Every booth"}, "The Stickit Inn, corner booth"),
          "remnant-fred": ("Fighter, possibly only ever a comic strip", {"profession": "Fighter (a player's first character)", "voice": "Short lines, as if in a speech balloon.", "faction": "The Remnants"}, "Room 2, the Hoard, the Cover"),
          "remnant-strider": ("Ranger out of a beloved novel", {"profession": "Ranger (a player's first character)", "voice": "Low, earnest.", "faction": "The Remnants"}, "The Crossroads, the Hoard, the Cover"),
          "remnant-thon": ("Half-elf wizard with a Rod of Lordly Might", {"profession": "Wizard (a player's first character)", "voice": "Delighted, about the rod. Only the rod.", "faction": "The Remnants"}, "The Cellar, the Hoard, the Cover"),
          "remnant-morlock": ("Halfling thief-acrobat, 7th level", {"profession": "Thief-acrobat (a player's first character)", "voice": "Proud of his sheet. Quiet about the T.", "faction": "The Remnants"}, "The Stable, the Hoard, the Cover"),
          "remnant-rorvik": ("Half-elven magic-user and thief", {"profession": "Magic-user/thief (a player's first character)", "voice": "Hot-headed. 'Is it my turn yet?'", "faction": "The Remnants"}, "The Cover, from round 2"),
          "remnant-rogue": ("Fallback: The Rogue With a Tragic Past", {"profession": "Rogue (someone's first character)", "voice": "'It's complicated.'", "faction": "The Remnants"}, "Fallback"),
          "remnant-barbarian": ("Fallback: The Barbarian Who Is Just Strong", {"profession": "Barbarian (someone's first character)", "voice": "Cheerful. Has never been angry.", "faction": "The Remnants"}, "Fallback"),
          "remnant-wizard": ("Fallback: The Wizard Who Misread the Spell", {"profession": "Wizard (someone's first character)", "voice": "Insists.", "faction": "The Remnants"}, "Fallback")}
place_people = {name: [npc_name(p) for p in people] for name, _, _, people in PLACES}
for key, (role, attrs, where) in PEOPLE.items():
    a = allactors[key]; name = npc_name(key)
    data = {"attributes": attrs, "actor": actor_ref(key), "role": role, "location": where,
            "relationships": rels(*[rel(pn, role="appears here") for pn, ppl in place_people.items() if name in ppl],
                                  *([rel("The Remnants", relationship="member")] if attrs["faction"] == "The Remnants" else []))}
    says = journal.DIALOG.get(key, [])
    quote = lambda line: line if line.startswith("(") else "“" + line + "”"
    says_html = ("<h2>Things They Say</h2>" + base_journal.ul(*["<strong>" + when + ".</strong> " + quote(line) for when, line in says])) if says else ""
    mej_entry(name, "person", a.doc["system"]["details"]["biography"]["value"] + says_html, F["JournalEntry"], sort=nxt(), data=data, src=a.doc["img"])
mej_entry("The Remnants", "organization", base_journal.P(
    "The first party: each player's first-ever D&D character, as the table remembers them. They are not hostile. They have been trying to finish one fight since 1977: the one on the cover of the Monster Manual. They can't do it without the party.",
    "This table's five: Fred the Fighter (Room 2), Strider (the Crossroads), Thon (the Cellar), T. Morlock (the Stable), and Rorvik, who is late. The three fallbacks stand in for a Remnant whose player can't make it, or for another table's first characters.")
    + "<h3>Rules</h3>" + base_journal.ul("Max Hit Points, never rolled.", "The Signature always works.", "It never attacks first.", "In the Cover: Signature once per wave, otherwise Help. At 0 Hit Points it stands back up next turn.")
    + "<h3>For another table</h3>" + base_journal.P("Ask each player privately: <em>What was the first D&D character you ever played? Name, class, and the one thing everyone remembers about them.</em> Don't say why. That one thing is the Signature. Put them at the stops in any order; give the latecomer's character Rorvik's entrance."),
    F["JournalEntry"], sort=nxt(), data={"relationships": rels(*[rel(npc_name(k), relationship="member") for k in (*TABLE_REMNANTS, *FALLBACK_REMNANTS)])})
mej_entry("Finish the Fight", "quest", base_journal.P("The Remnants' request: finish the fight on the cover of the 1977 Monster Manual, the one the first party never finished. It is the way out."),
    F["JournalEntry"], sort=nxt(), data={"status": "inactive", "objectives": {uid("obj", str(i)): {"id": uid("obj", str(i)), "content": c, "available": i == 0, "status": False, "done": 0, "required": ""}
        for i, c in enumerate(["Find the real one among the roles in the common room, and get the map.", "Find the road at the crossroads.", "Get through the cellar door.",
                               "Find the way through the stable.", "Hear the Remnants out.", "Finish the fight: all three waves.", "Go home, or stay."])}})
mej_entry("Cast", "journalentry", join_pages(E["Cast"]), F["JournalEntry"], sort=nxt())
# Handouts: the original adventure's four, with their pictures
def soft_L(kind, key, name=None):
    try: return L(kind, key, name)
    except KeyError: return f"<em>{name or key}</em>"
base_entries = dict(base_journal.build(soft_L))
HANDOUT_IMG = {"Handout: The Job": "handout-the-job", "Handout: The Toothless Key": "handout-toothless-key", "Handout: The X Map": "handout-x-map"}
for pname, html, *_ in base_entries["10. Handouts"]:
    if pname == "Handout: The X Map":
        html = "<h2>The X Map</h2>" + base_journal.P("A map, drawn in a hand none of you recognise, of a place none of you have been: a crossroads, a cellar, a stable, a room full of books, and beyond it a cave. There is an X on the cave.", "<em>The X marks the way out.</em>")
    img = f"handouts/{HANDOUT_IMG[pname]}.webp" if pname in HANDOUT_IMG else None
    src = f"modules/{ID}/{img}" if img and os.path.exists(f"{ROOT}/{img}") else None
    if src: html = f'<p class="handout-picture"><img src="{src}" alt="{pname[9:]}" style="max-width:100%;height:auto"></p>' + html   # MEJ shows src only on the Picture tab
    handout_ids[pname] = f"JournalEntry.{mej_entry(pname, 'journalentry', html, F['Handouts'], sort=nxt(), src=src)}"
# Campaign Companion: portal, timeline, sessions
PORTAL_ID, TIMELINE_ID = uid("journal", "campaign-portal"), uid("journal", "campaign-timeline")
journals.append({"_id": PORTAL_ID, "name": TITLE, "folder": F["JournalEntry"], "sort": 0, "ownership": {"default": 0}, "categories": [], "flags": {CC: {"campaignPortal": True}},
                 "pages": [{"_id": uid(PORTAL_ID, "page"), "name": TITLE, "type": f"{CC}.campaign", "title": {"show": False, "level": 1}, "text": {"format": 1, "content": ""},
                            "sort": 100000, "ownership": {"default": -1}, "flags": {CC: {"campaignPortal": True}, MEJ: {"type": "campaign"}}, "image": {}, "video": {}, "src": None, "system": {}}]})
journals.append({"_id": TIMELINE_ID, "name": f"{TITLE} — Timeline", "folder": F["JournalEntry"], "sort": 50000, "ownership": {"default": 0}, "categories": [], "pages": [],
                 "flags": {CC: {"timeline": {"timepoints": []}}, "core": {"sheetClass": f"{CC}.TimelineJournalSheet"}}})
SESSIONS = [("Session 1", "The Stickit Inn, Room 1, Room 2. Night falls (GM control) once everyone is asleep. Fred is the real one in the common room; click his table when he says POW! End when the door opens on a crossroads at dusk."),
            ("Session 2", "The Crossroads (Strider reads the map: east), the Cellar (the chests fight until Thon presses button six; open the door), the Stable (T. Morlock walks through the east wall; open the door), the Hoard (the ask). End on the yes, with the side door open. Long rest in the Hoard."),
            ("Session 3", "The Cover, three waves back to back. Rorvik at the top of round 2 (GM control); wave 2 and wave 3 controls when the wave before falls. Remnants: Signature once per wave, otherwise Help. Then the goodbyes and gifts, the back passage, Room 5: home or the table.")]
for i, (name, plan) in enumerate(SESSIONS):
    mej_entry(name, "session", "<p></p>", F["JournalEntry"], sort=nxt(), session={"number": i + 1, "gmNotes": f"<p>{plan}</p>"})

# ---------- actors ----------
def actor_doc(a, folder):
    d = json.loads(json.dumps(a.doc)); d["folder"] = folder
    for it in d["items"]: it.pop("_key", None)
    d.pop("_key", None); return d
adv_actors = [actor_doc(a, F["Actor"]) for a in monsters.values()] + [actor_doc(a, F["Actor-npc"]) for a in npcs.values()]

# ---------- table, playlists, macros ----------
tid = table_ids["jokes"]
tables = [{"_id": tid, "name": "The Drunk's Joke", "img": "icons/consumables/drinks/alcohol-beer-stein-wooden-metal-brown.webp",
           "description": "<p>Room 2, the hearth (B3). Roll once, the first time anyone talks to the drunk. That is his only line from then on, word for word, however many times anyone speaks to him. Nobody else in the room laughs.</p>",
           "results": [{"_id": uid(tid, str(i)), "type": "text", "name": "", "description": joke, "img": "icons/svg/d20-black.svg", "weight": 1, "range": [i + 1, i + 1], "drawn": False, "flags": {}}
                       for i, joke in enumerate(base_journal.DRUNK_JOKES)],
           "formula": f"1d{len(base_journal.DRUNK_JOKES)}", "replacement": True, "displayRoll": True, "folder": F["RollTable"], "sort": 0, "ownership": {"default": 0}, "flags": {}}]
def snd(name, file, repeat, vol):
    return {"_id": uid("sound", file), "name": name, "path": f"{MOD}/audio/{file}.ogg", "repeat": repeat, "volume": vol,
            "description": "", "fade": 1000 if repeat else None, "playing": False, "pausedTime": None, "sort": 0, "flags": {}}
def xsnd(key, name, path, repeat, vol):
    return {"_id": uid("sound", key), "name": name, "path": f"modules/{path}", "repeat": repeat, "volume": vol,
            "description": "", "fade": 1500 if repeat else None, "playing": False, "pausedTime": None, "sort": 0, "flags": {}}
AMB_KEYS = ["landing", *ROUTE]
amb_id = lambda k: uid("sound", "amb-" + k)
MUSIC = [("m-tavern", "Session 1: A Cozy Tavern", f"{IVAN}/a-cozy-tavern.ogg", True, .4),
         ("m-eerie", "On the road: Eerie Forest", f"{IVAN}/eerie-forest-loop.ogg", True, .35),
         ("m-mystery", "On the road: Mystery", f"{IVAN}/mystery-aboard-the-mno-loop.ogg", True, .35),
         ("m-cellar", "The Cellar, the fight: It's All Led Up to This", f"{AM}/battles/ItsAllLedUpToThis.mp3", True, .5),
         ("m-hoard", "The Hoard: Scholars of Mysterious Arts", f"{IVAN}/scholars-of-mysterious-arts-loop.ogg", True, .4),
         ("m-cover", "The Cover: Dracona Mortis", f"{AM}/battles/DraconaMortis.mp3", True, .5),
         ("m-goodbye", "After the fight: Sad Strings", f"{IVAN}/sad-strings.ogg", False, .45),
         ("m-dawn", "Room 5, dawn: Hope", f"{MG}/music/Hope.mp3", False, .45)]
playlists = [
    {"_id": uid("playlist", "amb"), "name": "Unfinished Fight: Ambience", "description": "One loop per place; each scene and its vista plays its own as the scene sound.",
     "mode": -1, "fade": 1500, "sounds": [xsnd("amb-" + k, AMBIENCE[k][0], AMBIENCE[k][1], True, AMBIENCE[k][2]) for k in AMB_KEYS],
     "folder": F["Playlist"], "sort": 100000, "ownership": {"default": 0}, "flags": {}, "playing": False},
    {"_id": uid("playlist", "music"), "name": "Unfinished Fight: Music", "description": "Music for the beats that need it. Play by hand.",
     "mode": -1, "fade": 2000, "sounds": [xsnd(k, n, p, r, v) for k, n, p, r, v in MUSIC], "folder": F["Playlist"], "sort": 150000, "ownership": {"default": 0}, "flags": {}, "playing": False},
    {"_id": uid("playlist", "sting"), "name": "Unfinished Fight: Stingers", "description": "One-shot cues (also on the SoundBard pads).", "mode": -1, "fade": None,
     "sounds": [snd("Door", "sting-door", False, .7), snd("The X", "sting-x-door", False, .7), snd("Dice, warm, just rolled", "sfx-dice-rolled", False, .7),
                snd("Cider, poured", "sfx-cider-poured", False, .7), snd("Remnants laughing, through the door", "sfx-remnants-laughing", False, .4)],
     "folder": F["Playlist"], "sort": 200000, "ownership": {"default": 0}, "flags": {}, "playing": False}]
macros = [{"_id": uid("macro", "soundbard"), "name": "The Unfinished Fight: set up SoundBard", "type": "script", "scope": "global", "author": None,
           "img": "icons/tools/instruments/drum-hand-tan.webp", "command": soundbard_macro(BANKS), "folder": None, "sort": 0, "ownership": {"default": 0}, "flags": {}},
          {"_id": uid("macro", "remove"), "name": "The Unfinished Fight: remove the adventure from this world", "type": "script", "scope": "global", "author": None,
           "img": "icons/svg/trash.svg", "command": remove_macro(PACK, TITLE), "folder": None, "sort": 100, "ownership": {"default": 0}, "flags": {}}]

# ---------- tokens placed in the scenes (top-left px; 100 px = 5 ft) ----------
# (actor key, x, y, hidden, token name or None, tag for the tiles or None, elevation in ft)
SCENE_TOKENS = {
    "backroom": [("barkeep", 600, 700, True, None, "bartleby", 0)],
    "common-room": [("remnant-fred", 550, 575, False, None, None, 0),
                    ("stranger", 300, 200, False, "A hooded stranger", None, 0), ("stranger", 300, 900, False, "A hooded stranger", None, 0),
                    ("stranger", 950, 1000, False, "A hooded stranger", None, 0),
                    ("role-barmaid", 800, 700, False, None, None, 0), ("role-guard", 200, 500, False, None, None, 0), ("role-guard", 200, 700, False, None, None, 0),
                    ("role-drunk", 880, 250, False, None, None, 0), ("role-merchant", 1000, 750, False, None, None, 0), ("role-oldman", 420, 1000, False, None, None, 0)],
    "c7-crossroads": [("remnant-strider", 650, 600, False, None, "strider", 0)],
    "c8-cellar": [("remnant-thon", 900, 300, False, None, "thon", 0),
                  ("chest", 500, 400, False, None, None, 0), ("chest", 650, 550, False, None, None, 0), ("chest", 450, 650, False, None, None, 0), ("chest", 750, 350, False, None, None, 0)],
    "c2-stable": [("remnant-morlock", 1100, 600, False, None, "morlock", 20)],
    "hoard": [("remnant-fred", 400, 170, False, None, None, 0), ("remnant-thon", 500, 170, False, None, None, 0),
              ("remnant-morlock", 330, 240, False, None, None, 0), ("remnant-strider", 550, 240, False, None, None, 0)],
    "cover-cavern": [("troll", 650, 350, False, None, None, 0), ("roper", 750, 950, False, None, None, 0),
                     *[("piercer", x, y, False, None, None, 15) for x, y in ((700, 850), (950, 950), (600, 850), (950, 1050), (900, 1150), (500, 800))],
                     ("centaur", 900, 750, False, None, None, 0), ("unicorn", 600, 600, False, None, None, 0),
                     *[("outrider", x, y, True, None, f"outrider{i}", 0) for i, (x, y) in enumerate(((1200, 750), (1400, 700), (1400, 500)))],
                     ("owlbear", 1000, 350, False, None, None, 0), ("dragon", 800, 200, False, None, None, 0),
                     *[("cub", x, y, True, None, f"cub{i}", 0) for i, (x, y) in enumerate(((1350, 400), (1300, 600)))],
                     ("remnant-fred", 800, 1150, True, None, "fred", 0), ("remnant-thon", 1100, 1100, True, None, "thon", 0),
                     ("remnant-strider", 800, 1250, True, None, "strider", 0), ("remnant-morlock", 1100, 1200, True, None, "morlock", 0),
                     ("remnant-rorvik", 1000, 1300, True, None, "rorvik", 0)],
}
PROTO_ONLY = ("randomImg", "appendNumber", "prependAdjective")
token_uuids = {}
def scene_tokens(key, sid):
    out = []
    for n, (akey, x, y, hidden, name, tag, elev) in enumerate(SCENE_TOKENS.get(key, [])):
        a = allactors[akey]; proto = {k: v for k, v in json.loads(json.dumps(a.doc["prototypeToken"])).items() if k not in PROTO_ONLY}
        tid = uid(sid, "token", str(n))
        if tag: token_uuids.setdefault(key, {})[tag] = f"Scene.{sid}.Token.{tid}"
        out.append({**proto, "_id": tid, "name": name or proto.get("name") or a.doc["name"], "actorId": a.id, "actorLink": False,
                    "x": int(x), "y": int(y), "elevation": elev, "rotation": 0, "hidden": bool(hidden), "locked": False, "alpha": 1,
                    "flags": {"patrol": {"enablePatrol": True}} if (key, akey) == ("common-room", "role-barmaid") else {}})
    return out
_cx, _cy, _rx, _ry = 745, 810, 200, 130   # the barmaid's circuit (same as The Back Room)
BARMAID_LOOP = [round(v) for a in range(8) for v in (_cx + _rx * math.cos(a * math.pi / 4 + math.pi / 8), _cy + _ry * math.sin(a * math.pi / 4 + math.pi / 8))]
def scene_regions(key, sid):
    if key != "common-room": return []
    return [{"_id": uid(sid, "region", "barmaid"), "name": "The barmaid's circuit", "color": "#c9a227", "shapes": [{"type": "polygon", "points": BARMAID_LOOP, "hole": False}],
             "elevation": {"bottom": None, "top": None, "topInclusive": False}, "behaviors": [], "visibility": 0, "highlightMode": "shapes",
             "displayMeasurements": False, "hidden": False, "locked": False, "flags": {ID: {"patrol": "The Barmaid"}}}]

NOTE_PAGES = {**{f"A{i}": "Room 1: The Back Room" for i in range(1, 6)}, **{f"B{i}": "Room 2: The Common Room That Isn't" for i in range(1, 6)},
              **{f"D{i}": "The Hoard" for i in range(1, 6)}, **{f"E{i}": "The Cover" for i in range(1, 6)}}
SCENE_JOURNAL = {"backroom": "Room 1: The Back Room", "common-room": "Room 2: The Common Room That Isn't", "c7-crossroads": "The Crossroads",
                 "c8-cellar": "The Cellar", "c2-stable": "The Stable", "hoard": "The Hoard", "cover-cavern": "The Cover"}
wall_uuids, scenes = {}, []
door_at = {(k, tuple(c)): (n, t, st) for (k, n), (c, t, st) in DOORS.items()}
for i, key in enumerate(ROUTE):
    m = maps[key]; sid = scene_ids[key]
    walls = []
    for j, w in enumerate(m.get("walls", [])):
        w = dict(w); wid = uid(sid, "w", str(j))
        if (key, tuple(w["c"])) in door_at:
            n, t, st = door_at[(key, tuple(w["c"]))]; w["door"], w["ds"] = t, st; wall_uuids[(key, n)] = f"Scene.{sid}.Wall.{wid}"
        walls.append({"_id": wid, **w, "dir": 0, "threshold": {"light": None, "sight": None, "sound": None, "attenuation": False}, "flags": {}})
    lights = [{"_id": uid(sid, "l", str(j)), "x": int(l["x"]), "y": int(l["y"]), "rotation": 0, "walls": True, "vision": False, "hidden": False,
               "config": {"dim": round(l["dim"]), "bright": round(l["bright"]), "color": l.get("color"), "alpha": l.get("alpha", .3), "angle": 360,
                          "coloration": 1, "luminosity": .5, "attenuation": .5, "saturation": 0, "contrast": 0, "shadows": 0,
                          "animation": {"type": l.get("anim"), "speed": 3, "intensity": 3, "reverse": False}, "darkness": {"min": 0, "max": 1}}, "flags": {}}
              for j, l in enumerate(m.get("lights", []))]
    notes = []
    for code, (x, y) in m.get("notes", {}).items():
        if code not in NOTE_PAGES: continue
        jid, pid = page_index[NOTE_PAGES[code]]
        notes.append({"_id": uid(sid, "n", code), "entryId": jid, "pageId": pid, "x": int(x), "y": int(y), "texture": {"src": "icons/svg/book.svg", "tint": "#ffe9a8"},
                      "iconSize": 48, "text": code, "fontSize": 28, "textAnchor": 1, "textColor": "#ffffff", "global": False, "flags": {}})
    sx, sy = m.get("start", [m["w"] // 2, m["h"] // 2])
    scenes.append({"_id": sid, "name": ROUTE[key], "navigation": True, "navOrder": i, "navName": NAV_NAME[key], "active": False,
                   "background": {"src": f"{MOD}/maps/{m['file']}"}, "foreground": None, "thumb": f"{MOD}/maps/thumb-{m['file']}", "width": m["w"], "height": m["h"], "padding": 0,
                   "initial": {"x": int(sx), "y": int(sy), "scale": .7}, "backgroundColor": "#0b0a07",
                   "grid": {"type": 1, "size": 100, "style": "solidLines", "thickness": 1, "color": "#000000", "alpha": .12, "distance": 5, "units": "ft"},
                   "tokenVision": True, "fog": {"exploration": True, "reset": None, "overlay": None, "colors": {"explored": None, "unexplored": None}},
                   "environment": {"darknessLevel": round(m.get("darkness", .5) * .5, 2), "darknessLock": False, "globalLight": {"enabled": False}, "cycle": True},
                   "drawings": [], "tokens": scene_tokens(key, sid), "lights": lights, "notes": notes, "sounds": [], "regions": scene_regions(key, sid), "tiles": [], "walls": walls,
                   "playlist": uid("playlist", "amb"), "playlistSound": amb_id(key), "journal": page_index[SCENE_JOURNAL[key]][0], "journalEntryPage": None,
                   "weather": "", "folder": F["Scene"], "sort": (i + 1) * 100000, "ownership": {"default": 0}, "flags": {}})
missing = [k for k in DOORS if k not in wall_uuids]
assert not missing, f"doors not found on the maps: {missing}"
GRIDLESS = {"grid": {"type": 0, "size": 100, "style": "solidLines", "thickness": 1, "color": "#000000", "alpha": 0, "distance": 5, "units": "ft"},
            "tokenVision": False, "fog": {"exploration": False, "reset": None, "overlay": None, "colors": {"explored": None, "unexplored": None}},
            "environment": {"darknessLevel": 0, "darknessLock": True, "globalLight": {"enabled": True}, "cycle": False},
            "drawings": [], "tokens": [], "lights": [], "notes": [], "sounds": [], "regions": [], "tiles": [], "walls": [], "padding": 0, "foreground": None,
            "backgroundColor": "#0b0a07", "journal": None, "journalEntryPage": None, "weather": "", "ownership": {"default": 0}, "flags": {}, "playlist": uid("playlist", "amb")}
scenes.append({**GRIDLESS, "_id": uid("scene", "landing"), "name": "Welcome: The Stickit Inn", "navigation": True, "navOrder": -1, "navName": "The Stickit Inn", "active": True,
               "background": {"src": f"{MOD}/vistas/landing.webp"}, "thumb": f"{MOD}/vistas/landing.webp", "width": 1920, "height": 1280,
               "initial": {"x": 960, "y": 640, "scale": .5}, "playlistSound": amb_id("landing"), "folder": F["Scene"], "sort": 0})
for vi, (vk, vname) in enumerate(VISTAS.items()):
    scenes.append({**GRIDLESS, "_id": vista_id(vk), "name": f"Vista: {vname}", "navigation": False, "navOrder": 0, "navName": NAV_NAME[vk], "active": False,
                   "background": {"src": vista_src(vk)}, "thumb": vista_src(vk), "width": 1536, "height": 1024, "initial": {"x": 768, "y": 512, "scale": .6},
                   "playlistSound": amb_id(vk), "folder": F["Scene-vista"], "sort": (vi + 1) * 100000})

ctx = {"scene_ids": scene_ids, "rects": {k: maps[k].get("rects", {}) for k in ROUTE}, "handouts": handout_ids, "walls": wall_uuids, "tokens": token_uuids}
tiles = matt_unfinished.build_tiles(ctx)
for s in scenes:
    for k, sid in scene_ids.items():
        if s["_id"] == sid: s["tiles"] = tiles.get(k, [])

folders = [
    {"_id": F["JournalEntry"], "name": TITLE, "type": "JournalEntry", "color": "#5a2e27", "sorting": "m", "folder": None, "sort": 0,
     "flags": {CC: {"campaign": {"ownershipDefault": "none", "defaultTimelineId": TIMELINE_ID}}}},
    {"_id": F["Handouts"], "name": "Handouts", "type": "JournalEntry", "color": "#7a4a3b", "sorting": "a", "folder": F["JournalEntry"], "sort": 0, "flags": {}},
    {"_id": F["Actor"], "name": "Unfinished Fight: The Cover", "type": "Actor", "color": "#7a2e24", "sorting": "a", "folder": None, "sort": 0, "flags": {}},
    {"_id": F["Actor-npc"], "name": "Unfinished Fight: People", "type": "Actor", "color": "#5a2e27", "sorting": "a", "folder": None, "sort": 0, "flags": {}},
    {"_id": F["Scene"], "name": TITLE, "type": "Scene", "color": "#5a2e27", "sorting": "m", "folder": None, "sort": 0, "flags": {}},
    {"_id": F["Scene-vista"], "name": "Vistas", "type": "Scene", "color": "#6a4e2b", "sorting": "m", "folder": F["Scene"], "sort": 0, "flags": {}},
    {"_id": F["Playlist"], "name": TITLE, "type": "Playlist", "color": "#5a2e27", "sorting": "m", "folder": None, "sort": 0, "flags": {}},
    {"_id": F["RollTable"], "name": TITLE, "type": "RollTable", "color": "#5a2e27", "sorting": "a", "folder": None, "sort": 0, "flags": {}},
]
adv_id = uid("adventure", PACK)
adventure = {"_id": adv_id, "name": TITLE, "img": f"{MOD}/vistas/cover-cavern.webp",
             "caption": "The fight on the cover, finished at last. For five 7th-level characters.",
             "description": f"<p>The party beds down in the back room of the Stickit Inn, and in the night the inn turns into somewhere else. On the road through it they meet the first party, each player's first-ever character, and the first party has one thing to ask: help us finish the fight on the cover of the 1977 Monster Manual. Three sessions: a road of puzzles and one fight, then the Cover in three waves, fought together.</p><p><strong>Contents:</strong> {len(scenes)} scenes; {len(adv_actors)} actors; {len(journals)} journal entries; Monk's Active Tile Triggers automation. Shares its maps, art and audio with <em>The Back Room</em>; import one or the other into a world.</p><p>Start with the journal <em>00. The Unfinished Fight: Overview</em>.</p>",
             "actors": adv_actors, "combats": [], "items": [], "scenes": scenes, "journal": journals, "tables": tables,
             "macros": macros, "cards": [], "playlists": playlists, "folders": folders, "sort": 100, "flags": {}, "_key": f"!adventures!{adv_id}"}
json.dump(adventure, open(f"{SRC}/{PACK}/{PACK}.json", "w"), indent=1)
ntiles = sum(len(s["tiles"]) for s in scenes)
print(f"{TITLE}: {len(scenes)} scenes, {ntiles} tiles, {len(journals)} journals, {len(adv_actors)} actors")
