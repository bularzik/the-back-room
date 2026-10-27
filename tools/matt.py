"""Monk's Active Tile Triggers automation for The Back Room.

Primitives (design doc, "Automation"): random pool door (never the scene just left), visit counter whisper,
the X door, Room 3 segment doors and loop break, the Room 4 exit, the GM Reveal control, The Cover's door.

Each scene's maps.json entry supplies named rects (x, y, w, h in px). What each scene needs:
  pool copies  (c1-stairwell-a ...): door1, door2[, door3]  — the exits; arrive1.. matching — where tokens land
                                     one of the doors is also named in `xdoor` (e.g. "door2")
  backroom:        stairwell, loft          — the two ways out (Corridor doors); landing — arrival for Room 5
  common-room:     stairs                    — arrival; xdoor — the door that leads on (Corridor door otherwise)
  corridor-between: seg1..seg6 (far door of each segment), arrive1..arrive6 (just inside each segment), exit
  hoard:           doors (the glass double doors), arrive
  cover-cavern:    mouth (arrival), gap-dragon, gap-unicorn, gap-centaur, gap-troll, gap-roper, gap-owlbear, exit
Tiles whose rects are missing are skipped with a warning, so the build works before the maps do.
"""
from actors import uid, MOD

MATT = "monks-active-tiles"
AUD = f"{MOD}/audio"
TOKEN = {"id": "token", "name": "Triggering Token"}
PLAYERS = {"id": "players", "name": "Players"}
POOL = ["c1-stairwell", "c2-stable", "c3-inn-hallway", "c4-campfire", "c5-market", "c6-ferry", "c7-crossroads", "c8-cellar"]
COPIES = ("a", "b", "c")
ARRIVE = ["create", "enter"]   # a cross-scene teleport CREATES the token on the destination scene; "enter" alone never fires
BAND_MSG = ("<strong>Corridor entry.</strong> Tick the visit counter. Cue bands: 1–2 nothing · 3–4 sound · 5–6 glimpse "
            "(The Cover from a pool door in 3–6) · 7+ a Remnant. Apply the library step for this copy.")

class TB:
    """Tile builder for one scene."""
    def __init__(self, sid):
        self.sid = sid; self.tiles = []; self.n = 0
    def tid(self, key): return uid(self.sid, "tile", key)
    def tuuid(self, key): return f"Scene.{self.sid}.Tile.{self.tid(key)}"
    def tile(self, key, rect, actions=(), trigger="enter", img=None, hidden=False, active=True,
             restriction="player", controlled="all", pertoken=False, chance=100, name=None):
        x, y, w, h = rect
        acts = []
        for i, (a, data) in enumerate(actions):
            d = {"id": uid(self.tid(key), "a", str(i)), "action": a}
            if data is not None: d["data"] = data
            acts.append(d)
        self.n += 1
        self.tiles.append({
            "_id": self.tid(key), "x": int(x), "y": int(y), "width": int(w), "height": int(h),
            "texture": {"src": img, "anchorX": .5, "anchorY": .5, "scaleX": 1, "scaleY": 1, "tint": "#ffffff", "alphaThreshold": .75, "fit": "fill"},
            "elevation": 0, "sort": self.n, "rotation": 0, "alpha": 1, "hidden": hidden, "locked": False,
            "occlusion": {"mode": 0, "alpha": 0}, "restrictions": {"light": False, "weather": False},
            "flags": {MATT: {"name": name or key, "active": active, "trigger": trigger, "restriction": restriction,
                             "controlled": controlled, "pertoken": pertoken, "minrequired": 0, "chance": chance,
                             "vision": True, "fileindex": 0, "files": [], "actions": acts}}})
        return self

# ---------- action helpers ----------
def scroll(text, entity=TOKEN, to="trigger", dur=5):
    return ("scrollingtext", {"text": text, "entity": entity, "for": to, "duration": dur, "anchor": 0, "direction": 2})
def chat(text, to="gm", flavor="", speaker=None):
    return ("chatmessage", {"flavor": flavor, "text": text, "entity": speaker or "", "incharacter": False, "chatbubble": "false", "showto": to, "language": ""})
def sound(file, to="everyone", vol="0.8"):
    return ("playsound", {"audiofile": f"{AUD}/{file}.ogg", "audiofor": to, "volume": vol, "loop": False, "fade": 0.25, "scenerestrict": False, "prevent": False, "delay": False, "playlist": True})
def teleport(dest_uuids, entity=TOKEN, position="random", cross=True):
    """MATT takes one location {id, name} or a LIST of them, and picks one at random from a list."""
    if isinstance(dest_uuids, (list, tuple)):
        loc = [{"id": u, "name": "Destination"} for u in dest_uuids] if len(dest_uuids) != 1 else {"id": dest_uuids[0], "name": "Destination"}
    else:
        loc = {"id": dest_uuids, "name": "Destination"}
    return ("teleport", {"entity": entity, "location": loc, "position": position,
                         "remotesnap": True, "animatepan": cross, "triggerremote": cross, "deletesource": cross,
                         "preservesettings": True, "avoidtokens": True, "colour": ""})
def activate(uuids, state, collection="tiles"):
    return ("activate", {"entity": {"id": ",".join(uuids) if isinstance(uuids, list) else uuids, "name": "Targets"}, "collection": collection, "activate": state})
def deactivate_self(): return ("activate", {"entity": {"id": "tile", "name": "This Tile"}, "collection": "tiles", "activate": "deactivate"})
def showhide(uuid, state, collection="tiles"):
    return ("showhide", {"entity": {"id": uuid, "name": "Target"}, "collection": collection, "hidden": state, "fade": 0})
def delay(sec): return ("delay", {"delay": str(sec)})
def journal(uuid, to="everyone"):
    return ("openjournal", {"entity": {"id": uuid, "name": "Handout"}, "page": "", "subsection": "", "showto": to, "asimage": False, "permission": "OBSERVER", "enhanced": False})
def resetfog(): return ("resetfog", {"scene": {"id": "scene", "name": "This Scene"}, "for": "everyone"})
def rolltable(uuid, mode="gmroll"):
    return ("rolltable", {"rolltableid": uuid, "quantity": "1", "rollmode": mode, "chatmessage": True, "reset": True})

def build_tiles(ctx):
    """ctx: scene_ids {key: id}, rects {key: {name: [x,y,w,h]}}, handouts {name: uuid}, table_uuid {key: uuid}.
    The X door has one hidden twin per destination room (2, 3, 4); the GM control for the right stage swaps it in.
    Returns {scene_key: [tiles]}. Scenes absent from ctx are skipped."""
    S, R, H = ctx["scene_ids"], ctx["rects"], ctx.get("handouts", {})
    out, warnings = {}, []
    def rect(key, name):
        r = R.get(key, {}).get(name)
        if r is None: warnings.append(f"{key}: no rect '{name}'")
        return r
    present = lambda k: k in S

    # Pool copies present in the build, and their arrival tiles (the random-door destinations)
    pool_keys = [f"{p}-{c}" for p in POOL for c in COPIES if present(f"{p}-{c}")]
    builders = {k: TB(S[k]) for k in S}
    def arrivals(key):
        return [builders[key].tuuid(f"arrive{i}") for i in (1, 2, 3) if R.get(key, {}).get(f"arrive{i}")]
    arrive_uuids = {k: arrivals(k) for k in pool_keys}
    def pool_destinations(exclude_key):
        # every copy except the scene being left; the cellar only via the GM control (visit 5+)
        return [u for k in pool_keys if k != exclude_key and not k.startswith("c8-cellar") for u in arrive_uuids[k]]
    def corridor_door(tb, key, name, r, dests, xdoor=False):
        acts = [sound("sting-door"), teleport(dests)] if dests else [chat(f"No pool destinations built yet ({key}/{name}).")]
        tb.tile(name, r, acts, name=f"Pool door {name}" + (" (X-door slot)" if xdoor else ""))

    # ======================= THE CORRIDOR POOL =======================
    for key in pool_keys:
        tb = builders[key]
        for i in (1, 2, 3):
            r = rect(key, f"arrive{i}") if i < 3 else R.get(key, {}).get("arrive3")  # arrive3 is optional
            if r:
                tb.tile(f"arrive{i}", r, [resetfog(), chat(BAND_MSG), scroll("You don't remember this door.")], trigger=ARRIVE, active=True, pertoken=False, name=f"Arrival {i} (fog reset + visit whisper)")
        xd = R.get(key, {}).get("xdoor")
        for i in (1, 2, 3):
            r = rect(key, f"door{i}") if i < 3 else R.get(key, {}).get("door3")  # door3 is optional
            if r: corridor_door(tb, key, f"door{i}", r, pool_destinations(key), xdoor=(xd == f"door{i}"))
        # The X door: hidden/inactive twins of the xdoor slot, one per destination room; the matching GM control swaps one in.
        if xd and (r := rect(key, xd)):
            for stage, dkey, drect, label in (("2", "common-room", "stairs", "Room 2: The Common Room"),
                                              ("3", "corridor-between", "arrive1", "Room 3: The Corridor Between"),
                                              ("4", "hoard", "arrive", "Room 4: The Hoard")):
                dest = builders[dkey].tuuid(drect) if present(dkey) and R.get(dkey, {}).get(drect) else None
                tb.tile(f"xdoor{stage}", r, [sound("sting-x-door"), scroll("The X."), teleport(dest)] if dest else [chat(f"X door: {label} not built yet.")],
                        img=f"{MOD}/tiles/x-door.webp", hidden=True, active=False, name=f"The X Door → {label} (hidden until the GM reveals it)")
                tb.tile(f"gm-x{stage}", [0, 300 + 100 * int(stage), 100, 100],
                        [showhide(tb.tuuid(f"xdoor{stage}"), "show"), activate(tb.tuuid(f"xdoor{stage}"), "activate"), activate(tb.tuuid(xd), "deactivate"),
                         chat(f"The X has appeared on a door in this room. It leads to {label}.", to="gm")],
                        trigger="dblclick", img=f"{MOD}/tiles/gm-x.webp", hidden=True, restriction="all", controlled="gm", name=f"GM: Reveal the X door → {label}")
        cellar = [u for k in pool_keys if k.startswith("c8-cellar") for u in arrive_uuids[k]]
        if cellar and not key.startswith("c8-cellar"):
            tb.tile("gm-cellar", [0, 100, 100, 100], [teleport(cellar, entity=PLAYERS)], trigger="dblclick", img=f"{MOD}/tiles/gm-cellar.webp",
                    hidden=True, restriction="all", controlled="gm", name="GM: Next door → the Cellar (visit 5+)")
        if present("cover-cavern") and (m := rect("cover-cavern", "mouth")) and not key.startswith("c8-cellar"):
            tb.tile("gm-cover", [0, 200, 100, 100], [teleport(builders["cover-cavern"].tuuid("mouth"), entity=PLAYERS)], trigger="dblclick",
                    img=f"{MOD}/tiles/gm-cover.webp", hidden=True, restriction="all", controlled="gm", name="GM: Next door → The Cover (visits 3–6, once)")
        out[key] = tb.tiles

    # ======================= ROOM 1 / ROOM 5: THE BACK ROOM =======================
    if present("backroom"):
        tb = builders["backroom"]; key = "backroom"
        if (r := rect(key, "landing")): tb.tile("landing", r, [scroll("Dawn under the door.")], trigger=ARRIVE, active=True, name="Arrival (Room 5)")
        for name, text in (("stairwell", "Too many steps."), ("loft", "Hay, and under it, the sound of horses.")):
            if (r := rect(key, name)):
                tb.tile(name, r, [scroll(text), teleport(pool_destinations(None))] if pool_keys else [chat("Pool not built yet.")], name=f"Night door: {name} → Corridor pool")
        if "Handout: The Toothless Key" in H and (r := rect(key, "stone")):
            tb.tile("stone", r, [journal(H["Handout: The Toothless Key"], to="trigger"), chat("Someone pulled the key.", to="gm")], trigger="click", pertoken=True, name="The stone with the hilt (click)")
        tb.tile("gm-reveal", [0, 0, 100, 100], [chat("<strong>Reveal.</strong> Un-hide the pool copies' real names in the scene directory and keep the fog as it is. They never left.", to="gm")],
                trigger="dblclick", img=f"{MOD}/tiles/gm-reveal.webp", hidden=True, restriction="all", controlled="gm", name="GM: Reveal (Room 5)")
        out[key] = tb.tiles

    # ======================= ROOM 2: THE COMMON ROOM =======================
    if present("common-room"):
        tb = builders["common-room"]; key = "common-room"
        if (r := rect(key, "stairs")): tb.tile("stairs", r, [scroll("Nobody is looking at you.")], trigger=ARRIVE, active=True, pertoken=True, name="Arrival")
        if "Handout: The X Map" in H and (r := rect(key, "remnant")):
            tb.tile("remnant", r, [journal(H["Handout: The X Map"]), chat("The Remnant has handed over the map. The X door may now appear in the Corridors (GM: Reveal the X door, in any pool scene).", to="gm"), deactivate_self()],
                    trigger="click", name="The Remnant's table (click when the Signature is said)")
        if (r := rect(key, "xdoor")):
            tb.tile("xdoor", r, [sound("sting-door"), teleport(pool_destinations(None))] if pool_keys else [chat("Pool not built yet.")], name="Door → Corridor pool")
        out[key] = tb.tiles

    # ======================= ROOM 3: THE CORRIDOR BETWEEN =======================
    if present("corridor-between"):
        tb = builders["corridor-between"]; key = "corridor-between"
        for i in range(1, 7):
            if (r := rect(key, f"arrive{i}")): tb.tile(f"arrive{i}", r, [scroll("The same corridor.")] if i > 1 else [], trigger=ARRIVE, active=i > 1, name=f"Segment {i} arrival")
        for i in range(1, 7):
            if (r := rect(key, f"seg{i}")):
                nxt = tb.tuuid(f"arrive{min(i + 1, 6)}") if i < 6 else tb.tuuid("arrive1")
                tb.tile(f"seg{i}", r, [teleport(nxt, position="relative", cross=False), scroll("The same corridor, from the other end.")] +
                        ([chat("<strong>Second pass.</strong> The Echo steps out of the far door. Roll initiative.", to="gm")] if i == 2 else []),
                        name=f"Segment {i} far door → segment {min(i + 1, 6) if i < 6 else 1}")
        if (r := rect(key, "exit")):
            hoard = builders["hoard"].tuuid("arrive") if present("hoard") and rect("hoard", "arrive") else None
            tb.tile("exit", r, [sound("sting-door"), teleport(hoard)] if hoard else [chat("Room 4 not built yet.")], hidden=True, active=False, name="Exit → The Hoard (armed by Loop Break)")
            tb.tile("gm-break", [0, 0, 100, 100], [activate([tb.tuuid(f"seg{i}") for i in range(1, 7) if rect(key, f"seg{i}")], "deactivate"),
                                                    showhide(tb.tuuid("exit"), "show"), activate(tb.tuuid("exit"), "activate"),
                                                    chat("<strong>Loop broken.</strong> The next far door is the exit. Apply the Setback: one character's bond, ideal or named person is now different; tell the other players.", to="gm")],
                    trigger="dblclick", img=f"{MOD}/tiles/gm-break.webp", hidden=True, restriction="all", controlled="gm", name="GM: Loop Break (something was left behind)")
        out[key] = tb.tiles

    # ======================= ROOM 4: THE HOARD =======================
    if present("hoard"):
        tb = builders["hoard"]; key = "hoard"
        if (r := rect(key, "arrive")): tb.tile("arrive", r, [scroll("Dice on the table. Warm.")], trigger=ARRIVE, pertoken=True, name="Arrival through the glass doors")
        if (r := rect(key, "doors")):
            back = builders["backroom"].tuuid("landing") if present("backroom") and rect("backroom", "landing") else None
            tb.tile("doors", r, [sound("sting-door"), teleport(back)] if back else [chat("Room 1/5 not built yet.")], active=False, name="Exit → The Back Room, Again (armed by GM)")
            tb.tile("gm-exit", [0, 0, 100, 100], [activate(tb.tuuid("doors"), "activate"), chat("<strong>Round 3.</strong> The glass doors now lead back the way they came. Combat ends when a character walks through without looking back.", to="gm")],
                    trigger="dblclick", img=f"{MOD}/tiles/gm-exit.webp", hidden=True, restriction="all", controlled="gm", name="GM: Open the way back (top of round 3)")
        out[key] = tb.tiles

    # ======================= THE COVER =======================
    if present("cover-cavern"):
        tb = builders["cover-cavern"]; key = "cover-cavern"
        if (r := rect(key, "mouth")): tb.tile("mouth", r, [resetfog(), scroll("They are fighting nobody.")], trigger=ARRIVE, name="Arrival (cave mouth)")
        for mon in ("dragon", "unicorn", "centaur", "troll", "roper", "owlbear"):
            if (r := rect(key, f"gap-{mon}")):
                tb.tile(f"gap-{mon}", r, [chat(f"<strong>A gap was stepped into.</strong> The {mon} wakes — and only the {mon}. Roll its initiative; it acts right after the character that woke it.", to="gm"),
                                           scroll("It turns its head."), deactivate_self()], name=f"Gap: wakes the {mon} (once)")
        if (r := rect(key, "exit")):
            tb.tile("exit", r, [sound("sting-door"), chat("Nothing taken from the pile survives this door.", to="gm"), teleport(pool_destinations(None))] if pool_keys else [chat("Pool not built yet.")], name="Exit → Corridor pool")
        out[key] = tb.tiles

    for w in warnings: print("  matt:", w)
    return out

GM_GUIDE = """<h2>Automation with Monk's Active Tile Triggers</h2>
<p>This module requires <strong>Monk's Active Tile Triggers</strong> (MATT). Doors are tiles; walking onto one moves the token (and its owner's view) to another scene. Monster tokens never set them off. Every tile is named in its MATT settings, so you can find and adjust any of them from the Tiles layer.</p>
<h3>GM Controls</h3>
<p>Hidden <strong>GM control buttons</strong> sit in the top-left corner of scenes. Switch to the Tiles layer to see them, then double-click one from the Tokens layer to fire it.</p>
<table><thead><tr><th>Scene</th><th>Control</th><th>What it does</th></tr></thead><tbody>
<tr><td>Any pool scene</td><td>Reveal the X door</td><td>Swaps this scene's X-door slot from a pool door to the X door, which leads to the next fixed room. Fire it once the previous room's condition is met.</td></tr>
<tr><td>Any pool scene</td><td>Next door → the Cellar</td><td>Sends the party to a Cellar copy. The Cellar is never in the random pool; use this from visit 5.</td></tr>
<tr><td>Any pool scene</td><td>Next door → The Cover</td><td>Sends the party to the cavern. Once, at visits 3–6.</td></tr>
<tr><td>Corridor Between</td><td>Loop Break</td><td>Disarms the segment doors and reveals the exit to the Hoard. Fire it when something sincere is left behind.</td></tr>
<tr><td>The Hoard</td><td>Open the way back</td><td>Arms the glass doors as the exit to Room 5. Fire it at the top of round 3.</td></tr>
<tr><td>The Back Room</td><td>Reveal</td><td>A reminder to un-hide the pool copies' real names for the moment in Room 5.</td></tr>
</tbody></table>
<h3>Automatic Tiles</h3>
<table><thead><tr><th>Where</th><th>Trigger</th><th>Effect</th></tr></thead><tbody>
<tr><td>Pool scenes, each door</td><td>Enter</td><td>Door cue; the token is sent to a random arrival in any pool copy except this scene. Never the Cellar.</td></tr>
<tr><td>Pool scenes, each arrival</td><td>Enter</td><td>Fog is reset for everyone and the GM is whispered the visit-band reminder. <strong>Tick the visit counter by hand.</strong></td></tr>
<tr><td>Back Room, stairwell and loft</td><td>Enter</td><td>The night doors: into the pool. Visit 1.</td></tr>
<tr><td>Back Room, the stone</td><td>Click</td><td>Opens the Toothless Key handout for that player.</td></tr>
<tr><td>Common Room, the Remnant's table</td><td>Click (once)</td><td>Opens the X Map handout for everyone; reminds you the X door may now appear.</td></tr>
<tr><td>Corridor Between, each far door</td><td>Enter</td><td>Moves the token to the start of the next identical segment, same relative position. The second far door whispers the Echo reminder.</td></tr>
<tr><td>The Cover, each gap</td><td>Enter (once)</td><td>Whispers which monster wakes.</td></tr>
<tr><td>The Cover, exit</td><td>Enter</td><td>Back into the pool; nothing from the pile survives.</td></tr>
</tbody></table>
<p><strong>Tips.</strong> Cross-scene moves bring each token's owner along, so move the whole party before switching your own view. Pool copies are hidden from the navigation bar and share bland names on purpose; the Reveal moment in Room 5 is when to un-hide them. If a tile misfires, toggle its Active checkbox in its config.</p>"""

PAGE_NOTES = {
    "The Night Event": "Automated: the stairwell and loft doors send tokens into the Corridor pool; clicking the stone opens the key handout.",
    "The Puzzle": "Automated: click the Remnant's table when the Signature is said to hand out the X map; then use GM: Reveal the X door in whichever pool scene the party reaches next.",
    "The Trick": "Automated: each far door walks the party into the next identical segment. Fire GM: Loop Break when something is left behind; the next far door becomes the exit.",
    "The Antagonist": "Automated: fire GM: Open the way back at the top of round 3; the glass doors then send tokens to Room 5 with the fog kept.",
    "Rules for Every Place": "Automated: every pool door teleports to a random arrival in another copy; every arrival resets fog and whispers the visit-band reminder. The Cellar and The Cover are reached by GM controls.",
    "The Cavern": "Automated: each person-shaped gap whispers which monster wakes, once.",
}
