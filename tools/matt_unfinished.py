"""Monk's Active Tile Triggers for The Back Room: The Unfinished Fight.

A fixed route: every door tile goes to one place, and going back through goes back. Locked doors (Room 2's, the Cellar's,
the Stable's east door, the Hoard's side door) are ordinary Foundry doors the GM opens when a Remnant opens them; their
tiles sit on the far side of the door, so nobody reaches them until the door is open.

ctx: scene_ids {key: id}, rects {key: {name: [x,y,w,h]}}, handouts {name: uuid}, walls {(key, name): uuid},
tokens {key: {tag: uuid}}. Returns {scene_key: [tiles]}.
"""
from matt import TB, scroll, chat, sound, party_teleport, teleport, activate, showhide, journal, deactivate_self, ARRIVE, PLAYERS, MOD, OPEN_EXITS

def changedoor(wall_uuid, type="nothing", state="nothing"):
    """MATT 'Change Door' (actions.js, MATT 14.01): type door/secret/toggle; state open/closed/lock/toggle; 'nothing' leaves a
    property alone. Every key must be present: a missing one is applied as undefined."""
    state = {"locked": "lock"}.get(state, state)
    return ("changedoor", {"entity": {"id": wall_uuid, "name": "Door"}, "type": type, "state": state,
                           "movement": "nothing", "light": "nothing", "sight": "nothing", "sound": "nothing"})

def loop(dest_uuid, text):
    """A same-scene 'road that comes back': the whole party walks out and comes in again elsewhere on this map."""
    return [scroll(text), teleport(dest_uuid, entity=PLAYERS, cross=False)]

# Door tiles sit BEYOND the door they belong to (rects here override maps.json's, which were in front of the doors).
# No tile may touch x=0 or y=0: MATT never fires for a token whose final x or y is 0 (tested in Foundry 14.369, MATT 14.01).
RECTS = {
    "backroom": {"stairwell": [500, 900, 100, 100], "loft": [1100, 400, 100, 100]},
    "common-room": {"xdoor": [100, 600, 100, 100]},   # in front of the locked door (the map has no room beyond it); off until Fred's table
    "c7-crossroads": {"door1": [650, 100, 300, 100], "arrive1": [700, 250, 100, 100], "land-north": [600, 250, 400, 150], "land-south": [600, 1250, 400, 150],
                      "land-east": [1100, 650, 250, 300], "west": [100, 650, 100, 300]},
    "c8-cellar": {"door1": [200, 900, 100, 100], "door2": [1100, 200, 100, 100]},
    "c2-stable": {"land-loft": [700, 200, 300, 100], "door1": [800, 100, 100, 100], "door2": [750, 1100, 100, 100], "door3": [1500, 600, 100, 100]},
    "hoard": {"doors": [750, 1300, 100, 100], "side": [1400, 650, 100, 100]},
}

def build_tiles(ctx):
    S, H, W, T = ctx["scene_ids"], ctx.get("handouts", {}), ctx["walls"], ctx["tokens"]
    R = {k: {**ctx["rects"].get(k, {}), **RECTS.get(k, {})} for k in S}
    B = {k: TB(S[k]) for k in S}
    out, warnings = {}, []
    def rect(key, name):
        r = R.get(key, {}).get(name)
        if r is None: warnings.append(f"{key}: no rect '{name}'")
        return r
    dest = lambda key, name: B[key].tuuid(name)
    gm = dict(trigger="dblclick", hidden=True, restriction="all", controlled="gm")

    # ---------------- ROOM 1 / ROOM 5: the back room ----------------
    k, tb = "backroom", B["backroom"]
    tb.tile("stairwell", rect(k, "stairwell"), [scroll("Too many steps."), *party_teleport(dest("common-room", "stairs"))], active=False,
            name="Night: the stairs → Room 2 (armed by Night falls)")
    tb.tile("loft", rect(k, "loft"), [scroll("Hay, and a ladder down."), *party_teleport(dest("common-room", "stairs"))], active=False,
            name="Night: the hayloft door → Room 2 (armed by Night falls)")
    # Room 5 arrival locks the stairs door for the toothless key. (A change-door action on another scene does nothing, so
    # it lives here. If the GM drops tokens on the landing in session 1 it locks too, harmlessly: Night falls unlocks it.)
    tb.tile("landing", rect(k, "landing"), [scroll("Dawn under the door."), changedoor(W[(k, "stairwell")], state="locked")], trigger=ARRIVE, name="Arrival (Room 5): locks the stairs door")
    if "Handout: The Toothless Key" in H and (r := rect(k, "stone")):
        tb.tile("stone", r, [journal(H["Handout: The Toothless Key"], to="trigger"), chat("Someone pulled the key.", to="gm"), deactivate_self()], trigger="click", name="The stone with the hilt (click)")
    tb.tile("gm-night", [0, 0, 100, 100], [
        activate([tb.tuuid("stairwell"), tb.tuuid("loft")], "activate"),
        changedoor(W[(k, "loft")], type="door", state="closed"), changedoor(W[(k, "stairwell")], state="closed"),
        showhide(T[k]["bartleby"], "show", collection="tokens"),
        chat("<strong>Night falls.</strong> The lantern is lit; Bartleby is on the stairs; the hayloft door behind the shelves is a real door now. The stairs and the hayloft both lead down to Room 2.", to="gm")],
        img=f"{MOD}/tiles/gm-night.webp", name="GM: Night falls", **gm)
    out[k] = tb.tiles

    # ---------------- ROOM 2: the common room that isn't ----------------
    k, tb = "common-room", B["common-room"]
    tb.tile("stairs", rect(k, "stairs"), [scroll("Nobody is looking at you.")], trigger=ARRIVE, name="Arrival")
    acts = [journal(H["Handout: The X Map"])] if "Handout: The X Map" in H else []
    tb.tile("remnant", rect(k, "remnant"), acts + [changedoor(W[(k, "xdoor")], state="closed"), activate([tb.tuuid("xdoor")], "activate"),
            chat("<strong>POW!</strong> Fred has handed over the X Map and the door is unlocked (if it isn't, right-click its door icon). The guards step aside.", to="gm"), deactivate_self()],
            trigger="click", name="Fred's table (click when he says his Signature)")
    tb.tile("xdoor", rect(k, "xdoor"), [sound("sting-door"), *party_teleport(dest("c7-crossroads", "arrive2"))], active=False, name="The door → the Crossroads (armed by Fred's table)")
    tb.tile("gm-door", [0, 0, 100, 100], [changedoor(W[(k, "xdoor")], state="open"), activate([tb.tuuid("xdoor")], "activate"),
            chat("The door is open and leads to the Crossroads. (Fred catches up there with the map: read it out, or show them the X Map handout.)", to="gm")],
            img=f"{MOD}/tiles/gm-door.webp", name="GM: The door opens anyway (they forced it)", **gm)
    out[k] = tb.tiles

    # ---------------- THE CROSSROADS ----------------
    k, tb = "c7-crossroads", B["c7-crossroads"]
    for n, text in (("arrive1", "The light never finishes going."), ("arrive2", "Every sign points north."), ("arrive3", "Dusk, still.")):
        tb.tile(n, rect(k, n), [scroll(text)], trigger=ARRIVE, name=f"Arrival ({n})")
    for n in ("land-north", "land-south", "land-east"): tb.tile(n, rect(k, n), [], active=False, name=f"Landing ({n}): where the looping roads come back in")
    side = OPEN_EXITS[k]
    tb.tile("door1", rect(k, "door1"), loop(tb.tuuid("land-south"), "…and back to the crossroads."), img=f"{MOD}/tiles/exit-door-{side['door1']}.webp", fit="contain", name="North road → loops back (in from the south)")
    tb.tile("door2", rect(k, "door2"), loop(tb.tuuid("land-north"), "…and back to the crossroads."), img=f"{MOD}/tiles/exit-door-{side['door2']}.webp", fit="contain", name="South road → loops back (in from the north)")
    tb.tile("west", rect(k, "west"), loop(tb.tuuid("land-east"), "…and back to the crossroads."), img=f"{MOD}/tiles/exit-door-left.webp", fit="contain", name="West road → loops back (in from the east)")
    tb.tile("door3", rect(k, "door3"), [sound("sting-door"), *party_teleport(dest("c8-cellar", "arrive1"))], img=f"{MOD}/tiles/exit-door-{side['door3']}.webp", fit="contain", name="East road → the Cellar")
    out[k] = tb.tiles

    # ---------------- THE CELLAR ----------------
    k, tb = "c8-cellar", B["c8-cellar"]
    tb.tile("arrive1", rect(k, "arrive1"), [scroll("The back room, from underneath.")], trigger=ARRIVE, name="Arrival from the Crossroads")
    tb.tile("arrive2", rect(k, "arrive2"), [scroll("The door stands open.")], trigger=ARRIVE, name="Arrival from the Stable")
    tb.tile("door1", rect(k, "door1"), [sound("sting-door"), *party_teleport(dest("c7-crossroads", "arrive3"))], name="The way in → back to the Crossroads (east road)")
    tb.tile("door2", rect(k, "door2"), [sound("sting-door"), *party_teleport(dest("c2-stable", "arrive1"))], name="Beyond the east door (locked until Thon's button six) → the Stable")
    out[k] = tb.tiles

    # ---------------- THE STABLE ----------------
    k, tb = "c2-stable", B["c2-stable"]
    tb.tile("arrive1", rect(k, "arrive1"), [scroll("Every horse faces the wall.")], trigger=ARRIVE, name="Arrival (the hayloft)")
    tb.tile("arrive3", rect(k, "arrive3"), [scroll("Hay, and horses.")], trigger=ARRIVE, name="Arrival from the Hoard")
    tb.tile("door1", rect(k, "door1"), [sound("sting-door"), *party_teleport(dest("c8-cellar", "arrive2"))], name="The hayloft ladder → back to the Cellar")
    tb.tile("land-loft", rect(k, "land-loft"), [], active=False, name="Landing: where the south doors come back in (the hayloft)")
    tb.tile("door2", rect(k, "door2"), loop(tb.tuuid("land-loft"), "Round the yard, up the ladder, in at the hayloft."), name="South doors → loops back to the hayloft")
    tb.tile("door3", rect(k, "door3"), [sound("sting-door"), *party_teleport(dest("hoard", "arrive"))], name="Through the east wall (opened by T. Morlock) → the Hoard")
    out[k] = tb.tiles

    # ---------------- THE HOARD ----------------
    k, tb = "hoard", B["hoard"]
    tb.tile("arrive", rect(k, "arrive"), [scroll("Dice on the table. Warm.")], trigger=ARRIVE, name="Arrival")
    tb.tile("doors", rect(k, "doors"), [sound("sting-door"), *party_teleport(dest("c2-stable", "arrive3"))], name="Glass doors → back to the Stable")
    tb.tile("side", rect(k, "side"), [sound("sting-x-door"), *party_teleport(dest("cover-cavern", "mouth"))], name="Side door (opened when the party says yes) → the Cover")
    out[k] = tb.tiles

    # ---------------- THE COVER ----------------
    k, tb = "cover-cavern", B["cover-cavern"]
    allies = [T[k][t] for t in ("fred", "thon", "strider", "morlock")]
    tb.tile("mouth", rect(k, "mouth"), [*[showhide(u, "show", collection="tokens") for u in allies],
            chat("<strong>Wave 1 wakes:</strong> the troll, the roper and the piercers. The Remnants are in, behind the party (Rorvik comes at the top of round 2: GM: Rorvik). Roll initiative for everyone.", to="gm"),
            scroll("They turn their heads."), deactivate_self()], trigger=ARRIVE, name="Arrival: wave 1 wakes, the Remnants come in (once)")
    tb.tile("gm-rorvik", [0, 0, 100, 100], [showhide(T[k]["rorvik"], "show", collection="tokens"),
            chat("<strong>Rorvik bursts in:</strong> “Sorry I'm late. What did I miss?” He acts first, every round, from now on.", to="gm")],
            img=f"{MOD}/tiles/gm-rorvik.webp", name="GM: Rorvik bursts in (top of round 2)", **gm)
    tb.tile("gm-wave2", [0, 100, 100, 100], [*[showhide(T[k][f"outrider{i}"], "show", collection="tokens") for i in range(3)],
            chat("<strong>Wave 2 wakes</strong> at the top of the next round: the centaur captain, the unicorn and three outriders. Kill the unicorn first or it keeps the others standing.", to="gm")],
            img=f"{MOD}/tiles/gm-wave2.webp", name="GM: Wave 2 wakes", **gm)
    tb.tile("gm-wave3", [0, 200, 100, 100], [*[showhide(T[k][f"cub{i}"], "show", collection="tokens") for i in range(2)],
            chat("<strong>Wave 3 wakes</strong> at the top of the next round: the owlbear, two cubs, and the red dragon. Its first breath goes where the most people are.", to="gm")],
            img=f"{MOD}/tiles/gm-wave3.webp", name="GM: Wave 3 wakes", **gm)
    br = B["backroom"]
    tb.tile("exit", rect(k, "exit"), [activate([br.tuuid("stairwell"), br.tuuid("loft")], "deactivate"),
            sound("sting-door"), *party_teleport(br.tuuid("landing"))], name="The back passage → Room 5 (the back room at dawn; locks its door for the key)")
    out[k] = tb.tiles

    for w in warnings: print("  matt (unfinished):", w)
    return out

GM_GUIDE = """<h2>Automation with Monk's Active Tile Triggers</h2>
<p>Doors are tiles. Walking onto one moves the whole party (every player character's token on the scene) to the next scene, and makes that scene active. Every door goes to one place; going back through it goes back. Monster and NPC tokens never set doors off.</p>
<h3>Locked doors</h3>
<p>Four doors start locked, with their tiles on the far side: <strong>Room 2's door</strong> (Fred's table unlocks it), the <strong>Cellar's east door</strong> (Thon's button six), the <strong>Stable's east door</strong> (T. Morlock walks through the wall), and the <strong>Hoard's side door</strong> (the party says yes). Open each the ordinary way: click its door icon; right-click to unlock first if needed.</p>
<h3>GM controls</h3>
<p>Hidden buttons in the top-left corner of a scene. Switch to the Tiles layer to see them; double-click one to fire it.</p>
<table><thead><tr><th>Scene</th><th>Control</th><th>What it does</th></tr></thead><tbody>
<tr><td>Room 2</td><td>The door opens anyway</td><td>Only if the party forces its way out without Fred: opens the door and arms it.</td></tr>
<tr><td>Room 1</td><td>Night falls</td><td>Shows Bartleby on the stairs, turns the secret door behind the shelves into a real door, and arms the stairs and the hayloft door: both lead to Room 2.</td></tr>
<tr><td>The Cover</td><td>Rorvik bursts in</td><td>Shows Rorvik at the cave mouth. Top of round 2 of wave 1.</td></tr>
<tr><td>The Cover</td><td>Wave 2 wakes</td><td>Shows the three outriders; reminder in chat. When wave 1's last monster drops.</td></tr>
<tr><td>The Cover</td><td>Wave 3 wakes</td><td>Shows the two owlbear cubs; reminder in chat. When wave 2's last monster drops.</td></tr>
</tbody></table>
<h3>Automatic tiles</h3>
<table><thead><tr><th>Where</th><th>Trigger</th><th>Effect</th></tr></thead><tbody>
<tr><td>Room 1, the stone</td><td>Click (once)</td><td>Opens the Toothless Key handout for that player.</td></tr>
<tr><td>Room 2, Fred's table</td><td>Click (once)</td><td>Shows everyone the X Map and unlocks the door.</td></tr>
<tr><td>The Crossroads, north, south and west roads</td><td>Enter</td><td>The party walks out and comes back in by the opposite road.</td></tr>
<tr><td>The Stable, south doors</td><td>Enter</td><td>The party comes back in at the hayloft.</td></tr>
<tr><td>The Cover, the cave mouth</td><td>Arrival (once)</td><td>Shows Fred, Thon, Strider and T. Morlock behind the party; whispers that wave 1 wakes.</td></tr>
<tr><td>The Cover, the back passage</td><td>Enter</td><td>Turns off Room 1's night doors, locks its stairs door (the toothless key opens it), and takes the party to Room 5.</td></tr>
</tbody></table>"""

PAGE_NOTES = {
    "Night Falls": "Automated: GM: Night falls (top-left of the scene) shows Bartleby, opens the hayloft door and arms both ways down to Room 2. The stone opens the Toothless Key handout when clicked.",
    "The Puzzle": "Automated: click Fred's table when he says his Signature: everyone sees the X Map, and the door unlocks.",
    "The Crossroads": "Automated: the north, south and west roads loop the party back to the crossroads; the east road goes to the Cellar.",
    "The Cellar": "Open the east door yourself (click its door icon) when Thon presses button six; the tile beyond it goes to the Stable.",
    "The Stable": "Open the east door yourself when T. Morlock walks through the wall; the tile beyond it goes to the Hoard. The south doors loop back to the hayloft.",
    "The Ask": "Open the side door yourself when the party says yes; the tile beyond it goes to the Cover.",
    "The Waves": "Automated: arriving wakes wave 1 and shows the Remnants. GM controls: Rorvik bursts in, Wave 2 wakes, Wave 3 wakes.",
    "After the Fight": "Automated: the back passage turns off Room 1's night doors, locks its stairs door, and takes the party to Room 5.",
}
