"""Adventure text for The Back Room. Each entry: (name, [(page_name, html, level)]). `L` resolves links at build time.
Source of truth: docs/the-back-room.md and docs/corridor-pool.md. GM text in <p>, read-aloud in <blockquote>."""

def box(t): return f'<blockquote class="read-aloud"><p><em>{t}</em></p></blockquote>'
def aside(title, body): return f'<aside class="notable"><h4>{title}</h4>{body}</aside>'
def ul(*items): return "<ul>" + "".join(f"<li>{i}</li>" for i in items) + "</ul>"
def ol(*items): return "<ol>" + "".join(f"<li>{i}</li>" for i in items) + "</ol>"
def P(*paras): return "".join(f"<p>{p}</p>" for p in paras)
def table(head, rows):
    h = "".join(f"<th>{c}</th>" for c in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table>"

def build(L):
    """L(kind, key) -> @UUID link string. kinds: actor, scene, table"""
    A = lambda k, n=None: L("actor", k, n)
    SC = lambda k, n=None: L("scene", k, n)
    TB = lambda k, n=None: L("table", k, n)

    entries = []

    # ------------------------------------------------------------------ 00 OVERVIEW
    entries.append(("00. The Back Room: Adventure Overview", [
        ("Introduction", "<h1>The Back Room</h1>" + P(
            "<em>The Back Room</em> is a liminal-horror adventure for four to five characters of 5th to 8th level, run over two or three sessions. The party meets in a tavern, played completely straight. They take the hook, buy provisions, and bed down in the storeroom over the kitchen before the dawn road. They never leave that room. The whole dungeon — stairwells, stables, corridors, campsites — is the storeroom, misremembered.",
            "The thing in there with them is not a monster. It is the first party: each player's first-ever D&D character, as the table misremembers them — overpowered, cooler than they were, one running joke swollen into a whole personality. These are the <strong>Remnants</strong>. They are not hostile. They want the game to keep going, forever, with the party in it.",
            "The message, in one line: <em>the places you are most comfortable are the ones you never finished leaving.</em>")
         + aside("Theme: Unfinished", P("One word, chosen first. Every room is something that was never finished — a story cut off, a character who never levelled, a campaign that died in the spring. 'Liminal' describes the dressing; 'unfinished' is the point. When you improvise a detail for a room, ask what in it was left undone."))
         + aside("Content Notes", P("Isolation, time loss, having one's memories quietly edited, a copy of a character, and a warm place that does not want anyone to leave. No gore. Talk with your players before you start about anything they'd rather fade to black."))),
        ("The Shape of It", "<h2>The Shape of It</h2>" + P(
            "The spine is a Five-Room Dungeon, but the five rooms are <em>destinations</em>, not neighbours. The party reaches each one by wandering the <strong>Corridors</strong>: a pool of eight in-between places behind random doors, where no door ever leads back. Five fixed beats threaded through an unfixed maze.")
         + table(["Beat", "Role", "Scene"], [
            ["1", "Entrance / Guardian", f"{SC('backroom')} — the storeroom over the kitchen; the barkeep as a gentle gate"],
            ["2", "Puzzle / Roleplay", f"{SC('common-room')} — every patron is a role; find the Remnant among them"],
            ["3", "Trick / Setback", f"{SC('corridor-between')} — the corridor takes something from the party"],
            ["4", "Climax", f"{SC('hoard')} — the first party, assembled, wants to finish the game"],
            ["5", "Reward / Revelation", f"{SC('backroom')} again — open the door or stay"]])
         + P("<strong>The central gimmick, escalating: misremembering.</strong> Early, the rooms are misremembered. Middle, the party's own past starts to be. Late, the party meets the misremembered versions of themselves and has to decide whether to leave them behind.",
             "<strong>Tone curve.</strong> Early rooms are off by one detail (comic, uncanny): the sword in the stone is a spoon. Middle rooms are wrong in ways that implicate the party: a barkeep who knows things the characters never said aloud. Late rooms stop pretending: the Remnants are in the room, and they are glad to see you."), 2),
        ("The Library Layer", "<h2>The Library Layer</h2>" + P(
            "The players at this table began playing D&D in the upstairs room of a library: a reading room with pointed arches, dark timber ribs, two tall stained-glass windows in arched bays, a stained-glass lantern in the ceiling, green-painted wainscoting, armchairs round a low table, and an inner glass-walled room with double wooden doors and bookshelves. That room is the memory the whole adventure is built on, so the dungeon gradually becomes it: one detail in Room 1, one more per Corridor visit, a step per segment in Room 3, and in Room 4 the Hoard <em>is</em> the reading room. It is the misremembering, surfacing.",
            "If your table did not start in a library, swap in the room where they did start — a basement, a kitchen table, a dorm lounge — and ladder its details the same way. The steps are in the Corridor rules.")
         + aside("Every book is a half-page book", P("Wherever the library layer puts a book or a shelf, every volume is one half-page long. This is a global rule, not a room's trope. Never explain it.")), 2),
        ("Goal & Progression", "<h2>Goal &amp; Progression</h2>" + P(
            "<strong>The stated goal</strong> arrives in Room 2: the Remnant hands the party a map with an X and says it marks the way out. It points at the Hoard. From then on the players can say what they are doing — follow the X — and the X pulls them through the Corridors.",
            "<strong>The real goal</strong> is discovered in Rooms 4–5: the way out was the door they came in by. The stated goal was the thing keeping them from it.",
            "<strong>Progression rule.</strong> Every Corridor scene has one door that can carry the X; the X moves between scenes when nobody looks at the map. The X door leads to the <em>next fixed room</em>, but it only appears once the party has done what the previous room required: found the Remnant in Room 2; left something behind in Room 3. All other doors are pool doors. Random doors for wandering, one scripted door for progress."), 2),
        ("Pacing", "<h2>Pacing (2–3 sessions)</h2>" + ul(
            "<strong>Session 1:</strong> Rooms 1–2 and two Corridors (visits 1–2).",
            "<strong>Session 2:</strong> three or four Corridors (visits 3–6, including The Cover and the glimpse), then Room 3.",
            "<strong>Session 3</strong> (or the back half of 2): a Corridor at visit 7+ with a Remnant in it, Room 4, Room 5.")
         + P("The Corridors are the pacing valve: add loops when the table is enjoying the dread, cut them when it isn't. Levels 5–8 is the right tier on purpose: past local nobodies, not yet legends. The characters are in a transition whether the players have noticed or not."), 2),
    ]))

    # ------------------------------------------------------------------ 01 RULES (players' journal)
    entries.append(("01. Rules of the Back Room", [
        ("The Four Rules", "<h1>Rules of the Back Room</h1>" + P("Four rules carry the theme. Read them to the players after Room 1; they go on the sheet, not in GM prose.")
         + ol("<strong>Misremembering.</strong> Each short rest taken in a Corridor rewrites one small backstory detail of one character — a sibling's name, the colour of the house, which god. The GM changes it on the sheet and tells only the <em>other</em> players. Track every change (who, what it was, what it is now): Room 5 needs the list.",
              "<strong>The Signature.</strong> A Remnant's one remembered thing auto-succeeds once per round, no roll, no save. Everything else about it is blank. A finished character has a whole sheet; an unfinished one has one line.",
              "<strong>No door leads back.</strong> Every door in the Corridors sends the party somewhere else in the pool, never to the place they left. The one scripted exception is the Room 4 exit. The visit counter escalates what is in there with them.",
              "<strong>Leaving something behind is the only way forward.</strong> Each transition out of a fixed room costs something the player chooses — an item set down, a slot spent on nothing, a story told once and never again. It breaks the Room 3 loop, it is what the Remnants are made of, and it is the choice in Room 5. Never gate it on a keyword; reward the first sincere sacrifice the table invents.")),
        ("The Corridors", "<h2>The Corridors</h2>" + P("The Corridors connect the five rooms and are where 'stuck' happens. Three rules run them.",
            "<strong>1. No door leads back.</strong> Every door the party uses sends them to a random Corridor scene from the pool, never the scene they left. In Foundry the door tiles do this; the GM only watches.",
            "<strong>2. Something is in here with you — by visit count.</strong> Track how many Corridor scenes the party has entered in total (the tiles count for you and whisper the band to the GM on each arrival).")
         + table(["Visits", "Cue", "Library layer"], [
            ["1–2", "Nothing. Furniture is wrong by one detail.", "A strip of green wainscoting on one wall."],
            ["3–4", "Sound: footsteps matching theirs, a half-beat late. A chair creaks in an empty room. (The Cover is reached from a pool door in this band or the next.)", "Doors become double wooden doors with glass panels; through one, bookshelves."],
            ["5–6", "Glimpse: a figure at the end of the corridor, gone when looked at directly. It is wearing something one of the players' first characters wore.", "A pointed arch; a stained-glass lantern-window on a landing; carpet on stone."],
            ["7+", "A Remnant is in the room. It is glad to see you. It does not attack.", "Timber ribs overhead. The room is half library now."]])
         + P("<strong>3. Rest costs memory, not hit points.</strong> Short rests work normally, but each one taken in a Corridor applies Rule 1 (Misremembering).",
             f"<strong>The pool (d8).</strong> Stairwell, stable, hallway of inn doors, campfire clearing, market row at closing, ferry crossing, crossroads at dusk, cellar (from visit 5 only). Roll on {TB('pool')} if the tiles are not doing it for you. One misremembered trope per place — never two; one is uncanny, two is a joke. The places are written up in <em>06. The Corridor Pool</em>."), 2),
        ("Remnants", "<h2>Remnants</h2>" + aside("GM prep (the one thing to do before session one)", P("Privately ask each player: <em>What was the first D&D character you ever played? Name, class, and the one thing everyone remembers about them.</em> Don't say why. Players with no answer get a fallback Remnant."))
         + P("<strong>Building a Remnant.</strong>") + ul(
            "Take the first character's class and build it at the party's level using the standard NPC approach, or a sidekick-style block if you'd rather keep it light.",
            "<strong>Max hit points.</strong> No rolling.",
            "<strong>The Signature.</strong> The one remembered thing becomes a feature that <em>always works</em>: once per round, it auto-succeeds, no roll, no save. The barbarian who was 'just really strong' always hits. The rogue who always rolled nat 20s on Stealth is simply not there until it chooses to be.",
            "<strong>Everything else is blank.</strong> The Remnant cannot answer any question about its past that isn't the Signature. It doesn't know its hometown. It knows it had a tragic backstory but not what it was.",
            "<strong>It never attacks first.</strong> It wants the game to continue; it will fight if that's what the party wants to do.",
            "<strong>It stands back up.</strong> At 0 HP it rises at the start of its next turn, in the pose it fell in, with full HP, and continues mid-sentence.",
            "<strong>It cannot leave a room through a door the party came through.</strong> That is the only hard limit on it, and it is the exit mechanic for Room 4.")
         + P(f"<strong>Fallback Remnants</strong> for players without an answer: {A('remnant-rogue')}, {A('remnant-barbarian')}, {A('remnant-wizard')}. A five-player table may need a fourth; build it from any trope the table laughs at.",
             "<strong>Using them.</strong> One Remnant appears in Room 2. One more surfaces in the Corridors at visit 7+. All of them are in Room 4. They are filed under People, never Monsters."), 2),
    ]))

    # ------------------------------------------------------------------ 02 ROOM 1
    entries.append(("02. Room 1: The Back Room", [
        ("The Evening", "<h1>Room 1: The Back Room</h1>" + P(
            f"Play the cliché straight and let the players relax into it. {A('stranger')} in the corner booth has a job (write it on the handout <em>The Job</em> before the session: an escort, a delivery, a missing person — whatever this table's campaign would open with). The party takes it, buys provisions, and {A('barkeep')} leads them <strong>up the stairs</strong> from the common room to the storeroom over the kitchen, where they can sleep before the dawn road.")
         + box("The barkeep goes up ahead of you with the lantern. A short landing at the top of the stairs, a door, and the storeroom: shelves of sacks and crocks, a cot for each of you already made up, one lantern on a hook, a small window over the yard. He sets the lantern down and tells you he'll have bread on at first light.")
         + P("Describe it in loving, mundane detail. Let them count the cots. In the window, one pane of coloured glass that was not there at supper. Nobody comments on it; the GM does not either.")
         + aside("Keyed areas", ul("<strong>A1. The landing.</strong> Top of the common-room stairs. The door to the storeroom.",
                                   "<strong>A2. The cots.</strong> One per character, along the left wall, blankets turned down.",
                                   "<strong>A3. The shelves.</strong> Provisions, with the party's receipts tucked under the crocks. Behind the far unit, a door nobody has noticed yet.",
                                   "<strong>A4. The window.</strong> Small, four panes. One of them is coloured.",
                                   "<strong>A5. The stone.</strong> In the corner by the chest: a stone with a hilt in it."))),
        ("The Night Event", "<h2>The Night Event (the Insomnia Rule)</h2>" + P("Someone wakes. Pick the character whose player is most likely to get up and look.")
         + box("The lantern is lit. Nobody lit it. The door to the landing is open a hand's width and the stairs beyond it are stone, going down — the stairs you came up, but too many of them, and no light at the bottom where the common room should be.")
         + P("Behind the shelves (A3), a second door nobody noticed: it opens into the <strong>hayloft</strong> over the stable, with a ladder down. This is how the storeroom connects to the yard; it also seeds the Stable in the Corridor pool, and it is the <em>riddle door</em> (see the Corridor Pool, Stable).",
             "<strong>The first anchor object.</strong> The stone in the corner (A5) has a hilt in it. Whoever pulls draws out a long iron key with no teeth. It opens nothing in the room. Keep it; it matters in Room 5. Give the handout <em>The Toothless Key</em>."), 2),
        ("The Guardian", "<h2>The Guardian Is Not a Fight</h2>" + P(
            f"{A('barkeep')} comes down the stone stairwell carrying a tray. He is kind. He tells them it's not morning yet and they should go back to bed; the road will be there tomorrow. He knows a detail about one character that the character has never told anyone — pick it from a sheet before the session. If pressed, he doesn't understand the question.",
            "The test here is only whether the party chooses the stairwell (or the loft ladder) over the cot. If they go back to sleep, they wake in Room 1 again, and the barkeep has set a second tray.",
            "<strong>Leaving.</strong> Whichever way they go — down the stairwell or down the loft ladder — the first door at the bottom is a Corridor door. Visit 1 begins."), 2),
    ]))

    # ------------------------------------------------------------------ 03 ROOM 2
    entries.append(("03. Room 2: The Common Room That Isn't", [
        ("The Room", "<h1>Room 2: The Common Room That Isn't</h1>" + box(
            "A tavern common room. The fire is lit, the tables are full, and nobody is looking at you. In every booth, a hooded stranger. The barmaid is walking a slow circle between the tables with a tray and has not arrived at one. A drunk by the hearth is telling a joke to nobody.")
         + P("Every patron is a <em>role</em>: a hooded stranger in every booth, a quest-giver who repeats the hook word for word, a barmaid who walks in a circle and never arrives, a drunk who says the same line no matter how many times you talk to him. Guards at the door say there's nothing to see here. There's a lot to see here.")
         + aside("Keyed areas", ul("<strong>B1. The booths.</strong> A hooded stranger in each, offering the job in the same words.",
                                   "<strong>B2. The bar.</strong> Nobody behind it. Tankards full. One is a different colour.",
                                   "<strong>B3. The hearth.</strong> The drunk, and his one line.",
                                   "<strong>B4. The door.</strong> Two guards. 'Nothing to see here.'",
                                   "<strong>B5. The stairs.</strong> Up to a landing that is not the landing they came down."))),
        ("The Puzzle", "<h2>The Puzzle</h2>" + P(
            "One patron is not a role. It is the first <strong>Remnant</strong>: one player's first character, misremembered. It doesn't know it's in a tavern. It thinks it's mid-adventure and the party are old companions. The puzzle is social: figure out which patron is real, and get it to say the thing everyone remembers it for (its Signature). When it does, the room goes quiet and every role turns to look at the party.",
            "<strong>Three clues</strong>, so the table can't miss it:") + ol(
            "The Remnant is the only patron who asks the party a question.",
            "It is the only one whose drink is a different colour.",
            "The player whose character it is will recognise it from the description before anyone else does — let that player sweat before they say so.")
         + P("<strong>Payoff.</strong> The Remnant gives them a map with an X. The X moves when nobody looks at it. It is pointing at the Corridors. Give the handout <em>The X Map</em>. From this moment the X door can appear in the Corridors (the GM's X-door tile)."), 2),
    ]))

    # ------------------------------------------------------------------ 04 ROOM 3
    entries.append(("04. Room 3: The Corridor Between", [
        ("The Trick", "<h1>Room 3: The Corridor Between</h1>" + box(
            "A corridor ten feet wide with a door at the far end. Torches lit ahead, dark behind. The door behind you is locked, and you can see the key for it hanging on a nail beside the far door.")
         + P("Two doors: the near one is locked and its key is behind the far one. The far one opens onto the same corridor, from the other end.",
             "<strong>The trick.</strong> Walking forward loops. In Foundry the loop is not a teleport: the map is a strip of identical segments and the party simply walks on (see Automation). Each pass is one step more library — ribs overhead, then the green paint, then the pointed arch at the far door — which reads as progress, and is: the corridor is going somewhere.",
             "<strong>Breaking it.</strong> The loop breaks on any sincere act of leaving something behind — a treasured item set down, a spell slot spent on nothing, a story a player tells about their first character and then agrees never to tell again. Don't gate it on a keyword; reward the first real sacrifice the table invents. When it breaks, the GM fires the Loop Break tile and the next far door is the exit.")
         + aside("Segments", P("<strong>C1–C6.</strong> Six identical segments in a line. Each far door is a tile that lets the party into the next segment. Segment dressing ladders the library: C1 plain; C2 a scratch on the wall at hip height and a dropped coin; C3 green wainscoting; C4 a glass double door with a bookshelf behind; C5 a pointed arch; C6 ribs overhead. Attentive players notice the scratch at the same height and the coin back on the floor."))),
        ("The Setback & the Echo", "<h2>The Setback</h2>" + P(
            "Whatever was left behind, a Remnant now has. And the corridor has taken something it wasn't offered: one character's bond, ideal, or a named person from their backstory is now subtly different, and only the other players notice. Apply Misremembering to one character now, chosen by the GM, and tell the others. This is the point where misremembering stops being about the rooms and starts being about the party.")
         + "<h2>The Echo</h2>" + P(
            f"On the second pass through the far door, a blank-faced copy of one character steps out of it: {A('echo')}. Pick the character who has left the least behind, if there's a choice. In this fight every attack repeats itself one round later in the same squares: the party must fight their own last turn. The Echo has the character's sheet with every number halved and no name. It stops when the loop breaks. This fight is mandatory, not conditional."), 2),
    ]))

    # ------------------------------------------------------------------ 05 ROOM 4
    entries.append(("05. Room 4: The Hoard", [
        ("The Reading Room", "<h1>Room 4: The Hoard</h1>" + box(
            "A dragon's hoard with no dragon. And the room is the upstairs reading room, fully arrived: pointed arches and dark timber ribs overhead, the stained-glass lantern in the ceiling, two tall stained-glass windows with dawn behind them, green wainscoting, armchairs. The hoard is the ring of armchairs round the low table, and on the table, where the coins should be, are dice — warm, as if they have just been rolled.")
         + P("The dark lord's tower, painted, hangs between the arches where a portrait would; it is the same size it has been from every window. At the far end, the inner glass-walled room with the double wooden doors: through the glass, bookshelves, and the Remnants, seated, waiting for the session to start.")
         + aside("Keyed areas", ul("<strong>D1. The glass doors.</strong> The party enters through them. They are the exit, later.",
                                   "<strong>D2. The armchairs.</strong> The hoard. Dice on the table, warm.",
                                   "<strong>D3. The portrait.</strong> The tower, between the arches.",
                                   "<strong>D4. The inner room.</strong> Bookshelves of half-page books. The Remnants.",
                                   "<strong>D5. The windows.</strong> Dawn. The same dawn as Room 5."))),
        ("The Antagonist", "<h2>The Antagonist's Motive</h2>" + P(
            "The Remnants are all here, the full first party. They have been waiting for the boss. They think the party <em>is</em> the boss, or the rescue, or the sequel — it changes mid-sentence. What they want is simple and sympathetic: for the session to not end. They were never given an ending; they are offering the party the same.")
         + "<h2>The Fight That Can't Be Won</h2>" + P(
            "Remnants have max HP and their Signature always works. Dropped to 0, a Remnant stands up at the start of its next turn in the same pose it fell in. Beating them rebuilds the room (the load-bearing boss, in reverse). Spell the stakes out at the top of round 3: the players should <em>understand</em> that winning is the loop.")
         + "<h2>How It Actually Ends</h2>" + P(
            "The glass double doors the party came in by (D1) now lead back the way they came — the first time in the adventure that's been true. Combat ends the moment a character walks through them without looking back. Remnants will not follow. They will call after the party by the players' real character names from Room 1, and then by the <em>first</em> characters' names, and then stop. The Room 4 Exit tile sends the party to Room 5."), 2),
    ]))

    # ------------------------------------------------------------------ 06 ROOM 5
    entries.append(("06. Room 5: The Back Room, Again", [
        ("Dawn", "<h1>Room 5: The Back Room, Again</h1>" + box(
            "The storeroom over the kitchen. Dawn light under the landing door, and through the small window — which is now, entirely, a stained-glass window — the colours of the reading room laid across the cots. The cots are made. The lantern is out. The stone in the corner has no hilt in it.")
         + P("This is the Room 1 scene with the fog <em>kept</em> and the same entry square: let Foundry tell them. The toothless key from Room 1 fits the door at the top of the stairs.",
             "<strong>The revelation.</strong> They never left. Say it plainly through the environment, not a monologue: provisions still on the shelf with the receipts the party paid for, the hooded stranger's voice rising from the common room below, ordinary morning noise, and under it, pages turning. Fire the GM <strong>Reveal</strong> tile now if you want the players to see the whole shape of it in the scene list.")),
        ("The Choice", "<h2>The Choice</h2>" + P("Open the door and leave, or stay. Make staying a real temptation, not a trap: the Remnants are audible through the loft door, laughing, and the back room is warm.")
         + ul("<strong>Leave.</strong> The job the stranger offered is real and ordinary. Each character permanently loses one misremembered thing (the detail that changed in Room 3 stays changed) and gains the level-up and a boon of the GM's choice tied to what they left behind in Room 3. The Remnants are gone; the players may say their first characters' names one last time if they want to.",
              "<strong>Stay.</strong> The campaign ends here, and it is allowed to be a good ending. Every session is session one. Tell the players that in those words.")
         + aside("The twist, for the GM only", P("The back room is still there, under every tavern the party ever starts in. Any future campaign at this table can open with the barkeep setting out a tray.")), 2),
    ]))

    # ------------------------------------------------------------------ 07 CORRIDOR POOL
    def place(num, key, name, trope, wrong, mapline, base, cues, dressing, extra=""):
        return (f"{num}. {name}", f"<h2>{num}. {name}</h2>" + P(f"Scene copies: {SC(key + '-a')}, {SC(key + '-b')}, {SC(key + '-c')}.",
                f"<strong>Trope.</strong> {trope}", f"<strong>Wrongness.</strong> {wrong}") + extra + P(f"<strong>Map.</strong> {mapline}", f"<strong>Library base step.</strong> {base}")
                + table(["Visits", "Cue"], cues) + P(f"<strong>Dressing line.</strong> {dressing}"), 2)
    entries.append(("07. The Corridor Pool", [
        ("Rules for Every Place", "<h1>The Corridor Pool</h1>" + P("Eight in-between places, one misremembered trope each. This is the spec the maps are built from; where it disagrees with anything else, it wins.")
         + ul("<strong>One trope, one wrongness.</strong> Never two — one is uncanny, two is a joke.",
              "<strong>Three copies.</strong> Each place is three Foundry scenes (A, B, C), same map, hidden from the navigation bar, all named with the place's bland name. Copy B is one step more library than A, copy C one more than B. The library steps are the only difference between copies; the wrongness is in all three.",
              "<strong>Every book is a half-page book.</strong>",
              "<strong>Entry doors.</strong> Each map has two or three doors. The random-door tile uses all of them as exits; arrivals are placed inside whichever door the tile chose, so a revisit can start from a different door. One door per scene is the X-door slot: a plain pool door until the progression condition is met, then the X appears on it and it leads to the next fixed room.",
              "<strong>Darkness</strong> 0.6–0.8 on every Corridor scene; one or two light sources at most. Small vision is part of the concealment.",
              "<strong>Size.</strong> 12×10 to 16×14 squares. Places to pass through, not explore.")
         + "<h3>The library steps</h3>" + table(["Step", "Detail"], [
            ["1", "A strip of green-painted wainscoting on one wall, chair-rail height."],
            ["2", "A door (or the door) is now a double wooden door with glass panels; through the glass, a bookshelf."],
            ["3", "A pointed arch where a square frame was; a small stained-glass lantern-window high in a wall; carpet over stone or dirt."],
            ["4", "Dark timber ribs overhead, meeting in a point. The room is half library now."]])
         + P("Copy A = the place's base step (0 for most). Copy B = base + 1. Copy C = base + 2. The generic cues (footsteps a half-beat late; a figure at the end of the corridor) apply anywhere; each place's own cues are below.")),
        place(1, "c1-stairwell", "Stairwell", "The dungeon stair; the inn's back stairs.",
              "The steps go <em>down</em> and arrive one floor <em>up</em>. Three flights, two landings; the party descends and comes out above where they started, every time.",
              "A stone stairwell in section-as-plan: three flights around a square well, two landings. Entry doors: bottom (arrival), top (arrival), one landing door. 14×10.",
              "0. (B = wainscoting on the landing walls; C = the landing door becomes the glass double door, bookshelf behind it.)",
              [["3–4", "A footstep on the flight above, matching the last step someone took."], ["5–6", "A figure on the landing above, gone when the party arrives there."], ["7+", "A Remnant sitting on a step, delighted."]],
              "One half-page book on each landing, face down, as if someone stepped out for a moment."),
        place(2, "c2-stable", "Stable", "The party's mounts; the stable behind the inn.",
              "The horses face the wall. They are the party's own mounts, saddled — the ones they never bought.",
              "Hayloft platform along one side (arrival from the loft door), ladder down, four stalls, a yard door, a tack-room door. Entry doors: loft door, yard door, tack door. 16×12.",
              "0.",
              [["3–4", "A horse shifts its weight; none of them has moved."], ["5–6", "A saddle on the rail that fits a character who has never ridden."], ["7+", "A Remnant brushing a horse that is facing the wall."]],
              "The mounts' names are on the stall doors, in the players' own handwriting.",
              aside("The loft door is the riddle door", P("This place is entered from the hayloft above; the ladder down is the door into the stalls. The hayloft door — the one behind the shelves in Room 1 and the loft door in every copy — speaks, as the two guards of the old riddle, one who always tells the truth and one who always lies. There is only one door. It cannot get the riddle right, contradicts itself mid-riddle, apologises, starts again. It opens the moment anyone tells it which guard it is; either answer works; it is grateful. (It is on the way in, not in the room, so it is not a second wrongness.)"))),
        place(3, "c3-inn-hallway", "Hallway of Inn Doors", "The inn's upstairs corridor of guest rooms.",
              "Identical doors, every one numbered with the same number. One is ajar: inside, a made cot with someone's pack on it. The inn has beds and nobody has ever slept in one — nobody here eats, sleeps, or was ever a child.",
              "A straight corridor, six doors a side, a window at one end, a stair-head at the other. Entry doors: the stair-head, the far-end door, the ajar room (it has a second door). 16×8.",
              "1 (inn corridors already have the wainscoting). B = glass double doors, C = pointed arches over them.",
              [["3–4", "A door closes somewhere behind the party; all the doors are as they were."], ["5–6", "Through the ajar door, the pack on the cot is one of theirs."], ["7+", "A Remnant in the ajar room, sitting on the cot, asking if this is their room."]],
              "The number on every door is the number of the room the players played in upstairs at the library, if they remember it; otherwise 2."),
        place(4, "c4-campfire", "Campfire Clearing", "The campsite; the one place every TTRPG assumes is safe.",
              "The fire gives no heat. A bedroll is already slept in, still warm. Anyone who rests here wakes at full hit points, every wound healed overnight — and Misremembering takes its due.",
              "A clearing ringed by trees, fire at the centre, three bedrolls, a log, a stream edge. 'Doors' are gaps in the trees: three paths out. 14×14.",
              "0. (B: the log is a bench with green wainscoting behind it, against a tree; C: a glass double door standing free between two trunks, a shelf behind it.)",
              [["3–4", "The fire crackles with the rhythm of someone's breathing."], ["5–6", "Figures dancing just outside the firelight who never look over (the dryads this table remembers)."], ["7+", "A Remnant sitting at the fire with its hands out, warming nothing."]],
              "The bedroll that is already slept in has a character's initials worked into the lining."),
        place(5, "c5-market", "Market Row at Closing", "The shopping trip; the potion seller.",
              "The stalls are being shuttered by nobody. The potion stall's labels are every one almost a word (HEALNG, MANNA, CURE LIHGT); the potions are all red.",
              "A short street of six stalls, awnings half down, a well, an arch at each end. Entry doors: the two arches and the back of one stall. 16×10.",
              "0.",
              [["3–4", "A shutter comes down on an empty stall as the party passes it."], ["5–6", "The stallholder's chair is warm."], ["7+", "A Remnant behind the potion stall, open for business, no idea what anything costs."]],
              "The potions work. Nobody can read which one they drank."),
        place(6, "c6-ferry", "Ferry Crossing", "The boatman; the river that must be crossed.",
              "A jetty, a lantern, no water and no ferry. The sound of a waterfall, close, with no waterfall. A bell on a post: ring it and it is answered from behind the party.",
              "A jetty running out over a dry riverbed, a boathouse, a path in through trees. Entry doors: the path, the boathouse door, the far end of the jetty (a door standing on the last plank). 16×12.",
              "0.",
              [["3–4", "The waterfall sound stops when someone speaks, resumes when they stop."], ["5–6", "A lantern on the far bank that was not lit."], ["7+", "A Remnant on the jetty with a pole, waiting for the water."]],
              "Under the jetty, where the water should be, a treasure chest. It has not been opened because nobody could get to it. It is right there."),
        place(7, "c7-crossroads", "Crossroads at Dusk", "The signpost; the road the party sets out on.",
              "Every arm of the signpost points the same way, to a town with the party's home town's name spelled almost right. The light never finishes going.",
              "Four roads meeting, a signpost, a milestone, a shrine, a verge with a stopped cart. 'Doors': the four roads. 16×16.",
              "0.",
              [["1–2 onward", "The roads are busy: every traveller is an adventuring party, not one farmer or merchant among them, all heading the way the arms point, and every party has its one member in the genre's impractical armour, whatever their race or number of legs. None of them stop."], ["3–4", "A party passes whose rear guard has a character's walk."], ["5–6", "A party passes going the other way; nobody looks."], ["7+", "A Remnant leaning on the signpost, waiting for its party, which is any party."]],
              "The milestone gives the distance to the town as a number that changes each time it is read, and is never smaller."),
        place(8, "c8-cellar", "Cellar", "The tavern cellar; the back room again.",
              "It is the back room — Room 1's storeroom — seen from the wrong angle: below it, the same shelves from underneath, the same cots' outlines in the boards overhead. The provisions chest is breathing. <strong>Appears from visit 5 only.</strong>",
              "A cellar the exact footprint of Room 1, casks, the chest, a trap in the ceiling (the storeroom floor), a coal chute, a stair. Entry doors: the stair, the chute, the ceiling trap (arrival only). 12×10.",
              "2 (the cellar's shelving is already library shelving, every book a half page). B = step 3, C = step 4: by copy C the cellar's ribs meet in a point.",
              [["5–6", "Footsteps overhead, in the storeroom, in the party's own rhythm."], ["7+", "A Remnant asleep on the chest, which is breathing in time with it."]],
              "The receipts for the party's provisions are nailed to a cask."),
    ]))

    # ------------------------------------------------------------------ 08 THE COVER
    entries.append(("08. The Cover (the Corridor fight)", [
        ("The Cavern", "<h1>The Cover</h1>" + P(
            f"The one honest fight, at Corridor visits 3–6. It is monsters, not Remnants — misremembered ones — and it is the payoff of the 'something is in here' escalation before the Remnant appears at visit 7+. Scene: {SC('cover-cavern')}, entered once, by the GM's scripted door at the visit of your choosing.",
            "The table's first Monster Manual had a cover: a red dragon, a unicorn, a centaur, a troll, a roper and an owlbear, all in one fight with adventurers in a dark, treasure-filled cavern. Monsters with no business being together, and the first treasure hoard these players ever saw.")
         + box("A pool door opens onto a cavern. Treasure heaped against the far wall, lit from a crack above. And in the middle of it, six monsters, mid-fight — a red dragon rearing, a unicorn with its horn lowered, a centaur drawing a bow, a troll mid-lunge, something like a stalagmite with its arms out, an owlbear — all perfectly still. They are fighting nobody. There are gaps in the picture the shape of people, and a dropped sword where one of them stood.")
         + P("The monsters do not acknowledge the party. They keep fighting nobody, as they have since 1977. (The rule is borrowed from a dryad encounter this table remembers: the thing in the room is busy, and the party has to decide whether to interrupt it.)",
             "<strong>Trigger: stepping into a gap.</strong> Each gap wakes one monster — the one that was fighting whoever stood there — and only that one. The rest keep posing. The party chooses how much of the cover to fight. Two or three is a hard fight for levels 5–8; all six is far beyond deadly, and the GM should let the tableau's stillness say so. Joining the picture is leaving-something-behind in reverse; and the theme, literally: the fight on the cover never ended, and you only have to finish the ones you start.")
         + aside("Keyed areas", ul("<strong>E1. The cave mouth.</strong> Arrival. The roper's gap (the thief).", "<strong>E2. The ledge.</strong> The centaur's gap (the archer).", "<strong>E3. The hoard.</strong> The dragon's gap (the fighter with the shield) and the treasure.", "<strong>E4. The chest.</strong> The troll's gap (the dwarf).", "<strong>E5. The back wall.</strong> The owlbear's gap (the cleric); the unicorn's gap (the elf) beside it."))),
        ("The Six", "<h2>The Six</h2>" + table(["Monster", "Misremembered as", "Build"], [
            [A("dragon"), "The size it was on the cover, about the owlbear's size. Everybody's first party beat a red dragon at level 3, somehow. It never got to grow.", "Red dragon wyrmling with a young red dragon's breath weapon"],
            [A("unicorn"), "On the monsters' side. It was in the Monster Manual, so it is a monster. It is confused about this.", "Unicorn; hostile; its healing goes to the other monsters"],
            [A("centaur"), "Has a bow but no arrows, and shoots anyway. They hit.", "Centaur trooper; ranged attacks need no ammunition"],
            [A("troll"), "Regenerates the way the table remembers, not the way the rules say: it stands up at the start of its turn in the pose it fell in.", "Troll; Regeneration replaced by the Remnant rule — fire or acid ends it"],
            [A("roper"), "The one nobody could draw properly; it looks like three different things from three angles.", "Roper, unchanged; describe it differently each round"],
            [A("owlbear"), "Just an owlbear. Something in here has to be.", "Owlbear, unchanged"]])
         + P("The treasure pile is real and quietly foreshadows Room 4: the Hoard has no dragon because the dragon is here, still frozen. Nothing taken from this pile survives the next Corridor door.",
             "The dryads themselves stay a glimpse cue, not a fight: at the campfire clearing, figures dancing just outside the firelight who never look over."), 2),
    ]))

    # ------------------------------------------------------------------ 09 CAST
    entries.append(("09. Cast", [
        ("People", "<h1>Cast</h1>" + P("Remnants are people, not monsters. File them accordingly and never give a player the stat block.") + ul(
            f"{A('barkeep')} — the gentle gate of Room 1; ordinary morning in Room 5.",
            f"{A('stranger')} — the hook, played straight; a role in every booth of Room 2.",
            f"{A('remnant-rogue')}, {A('remnant-barbarian')}, {A('remnant-wizard')} — the fallback Remnants.",
            f"{A('echo')} — Room 3's blank-faced copy; a placeholder to replace with the real halved sheet.")
         + "<h2>Monsters</h2>" + ul(f"{A('dragon')}, {A('unicorn')}, {A('centaur')}, {A('troll')}, {A('roper')}, {A('owlbear')} — The Cover.")),
    ]))

    # ------------------------------------------------------------------ 10 HANDOUTS (split into one entry per page by build.py)
    entries.append(("10. Handouts", [
        ("Handout: The Job", "<h2>The Job</h2>" + P("<em>GM: write the hook here before session one. An escort, a delivery, a missing person — whatever this table's campaign would open with. It is never a trick. Pay is fair. Directions are good.</em>")),
        ("Handout: The Toothless Key", "<h2>The Toothless Key</h2>" + P("A long iron key, drawn from a stone in the corner of the storeroom. It has a bow, a shank, and no teeth at all. It opens nothing in the room you found it in.", "<em>Keep it.</em>")),
        ("Handout: The X Map", "<h2>The X Map</h2>" + P("A map, drawn in a hand none of you recognise, of a place none of you have been. There is an X on it. The X marks the way out.", "<em>Do not look at the X for a moment. Now look again.</em>")),
        ("Handout: Rules of the Back Room", "<h2>Rules of the Back Room</h2>" + ol(
            "<strong>Misremembering.</strong> Each short rest in a Corridor rewrites one small thing about one of you. You will not be told which. The others will.",
            "<strong>The Signature.</strong> A Remnant's one remembered thing always works. Everything else about it is blank.",
            "<strong>No door leads back.</strong>",
            "<strong>Leaving something behind is the only way forward.</strong>")),
    ]))

    return entries
