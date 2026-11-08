"""GM text for The Back Room: The Unfinished Fight. Same people, maps and art as The Back Room; a different route.

Route: Room 1 (the night) -> Room 2 (Fred, the X Map) -> the Crossroads (Strider) -> the Cellar (Thon) -> the Stable
(T. Morlock) -> the Hoard (the ask) -> the Cover (three waves, with the Remnants) -> Room 5 (stay or go home).
No random doors, no misremembering, no Echo. Every door leads to one place, and back."""
import copy
from journal import box, P, ul, ol, aside, table, DIALOG as BASE_DIALOG

def step(n, title, body, use=None):
    out = f"<h3>{n}. {title}</h3>" + P(body)
    if use: out += aside("Use", ul(*use))
    return out

# ---------------- what the people say (base lines, with this adventure's own for the Remnants) ----------------
DIALOG = copy.deepcopy(BASE_DIALOG)
DIALOG.pop("echo", None)
DIALOG["barkeep"] = [l for l in DIALOG["barkeep"] if not l[0].startswith("Room 5")] + [
    ("Room 5, from downstairs", "Are they up yet? Bread's going hard. Tell them the wagon's in the yard.")]
DIALOG["remnant-fred"] = [
    ("Introducing himself", "FRED THE FIGHTER!"),
    ("Greeting the party", "There you are! Took your time. Ready for the next panel?"),
    ("His Signature, when he swings", "POW!"),
    ("Asked about his past", "Summer. Ink. A camp paper. Then… To be continued!"),
    ("Handing over the map", "The X is the way out. Everyone knows that. Follow it."),
    ("In the Hoard, the ask", "Last panel. We never drew it. Will you?"),
    ("In the Cover, wave 1", "Now THIS is a splash page!"),
    ("After wave 3", "We finished it. THE END. (He says the words as if he has never said them before.)"),
]
DIALOG["remnant-thon"] = [
    ("Greeting", "Ah, you'll want to see this. Everybody wants to see this."),
    ("In the Cellar, pressing buttons in order", "Button one, mace! (Click.) Button two, flaming blade! Hold on, I'll get there. They go in order."),
    ("Asked for the battering ram by name", "Button six! (Click. It is a battering ram.) Why didn't you say?"),
    ("Asked to cast a spell", "Spells? Yes, certainly, but have you seen button seven? It points north. Always. Even here. Especially here."),
    ("The Blank", "I knew a spell once. Started with an F. Doesn't matter. Button four."),
    ("In the Hoard, opening the door to the Cover", "Allow me. Button six."),
    ("After wave 3", "We finished it. (He looks at the rod as if he has only just noticed it is heavy.)"),
]
DIALOG["remnant-rorvik"] = [
    ("Every few minutes", "Is it my turn yet?"),
    ("Bursting into the Cover, round 2", "Sorry I'm late. What did I miss?"),
    ("Insulted", "Say that again. Go on. Say it with your sword out."),
    ("Asked about his adventures", "Adventures? I was there for all of them. Mostly. Sitting by the side. Waiting."),
    ("His Signature, first in initiative", "Me first. I've waited long enough."),
    ("After wave 3", "That was my turn. That was my turn, wasn't it?"),
]
DIALOG["remnant-morlock"] = [
    ("Introducing himself, from a rafter", "T. Morlock. Seventh level. Sixty thousand three hundred and eighty-one experience points. You can check."),
    ("Showing his sheet", "Every box filled in. Look: tightrope, one hundred percent. Climb walls, ninety-nine."),
    ("Asked to come down", "Why would I come down? Come up."),
    ("Asked what the T. stands for", "…It stands for T."),
    ("If anyone touches the leather bag", "Don't. Don't do that."),
    ("Walking into the stable wall", "Elishaf. (He is half through it.) Well? Come on."),
    ("After wave 3", "We finished it. Put that on the sheet. (He hands it to you. The T. still doesn't say.)"),
]
DIALOG["remnant-strider"] = [
    ("At the Crossroads, when they arrive", "You're lost. Don't argue. So am I. I've never had a map."),
    ("Reading the X Map", "That's two doors from here. (He points down the east road.)"),
    ("Asked who he is", "Strider will do. It's what everyone calls me."),
    ("Asked about his lineage", "(He tells it, earnestly, at length: a story every player at the table has read in a book. He does not notice.)"),
    ("Leaving the Crossroads", "Go on. I know the way now. I'll see you at the table."),
    ("His Signature, with the bow", "Hold still. (He doesn't miss.)"),
    ("After wave 3", "The road goes ever on. Not this one, though. This one's done."),
]

def build(L):
    A = lambda k, n=None: L("actor", k, n)
    SC = lambda k, n=None: L("scene", k, n)
    J = lambda k, n=None: L("journal", k, n)
    TB = lambda k, n=None: L("table", k, n)
    entries = []

    # ------------------------------------------------------------------ OVERVIEW
    entries.append(("00. The Unfinished Fight: Overview", [
        ("Introduction", "<h1>The Back Room: The Unfinished Fight</h1>" + P(
            "A three-session adventure for five 7th-level characters (it runs for 5th–8th). The party beds down in the back room of the Stickit Inn, and in the night the inn turns into somewhere else. On the way through it they meet the first party: each player's first-ever D&D character, the way the table remembers them. Those characters have one problem. On the cover of the 1977 Monster Manual there is a fight that was never finished, and they cannot finish it on their own.",
            "The adventure is a road with stops, not a maze. Every door goes to one place, and back. Each stop is a puzzle, a fight, or both; each one has a Remnant in it; and the last stop is a long, hard fight in three waves, with the Remnants at the party's side.")
         + aside("If you ran The Back Room", P("This is the same module, maps, people and art, with a different route. Gone: the random Corridor doors, Misremembering, the visit count, the X door and its GM controls, the Corridor Between and the Echo. New: a fixed route (Crossroads, Cellar, Stable), a puzzle and a Remnant at each stop, the Hoard's request, and the Cover as three back-to-back waves fought together with the Remnants. The Back Room's own journals, scenes and tiles are untouched; import one adventure or the other into a world, not both."))),
        ("The Route", "<h2>The Route</h2>" + table(["#", "Scene", "What happens", "Who"], [
            ["1", SC("backroom"), "The evening, the night, the stairs that are wrong.", A("barkeep")],
            ["2", SC("common-room"), "A room of roles. Find the real one. He hands over the X Map and the door unlocks.", A("remnant-fred")],
            ["3", SC("c7-crossroads"), "Every road comes back here, except one. Strider has never had a map.", A("remnant-strider")],
            ["4", SC("c8-cellar"), "A door that won't open, a rod with seven buttons, and the provisions chests are breathing.", A("remnant-thon")],
            ["5", SC("c2-stable"), "Two of the doors lead back to the hayloft. The way on is through the wall.", A("remnant-morlock")],
            ["6", SC("hoard"), "The first party, at their table. They ask.", "All five (Rorvik's chair is empty)"],
            ["7", SC("cover-cavern"), "The fight from the cover, in three waves, together.", "The six monsters; the five Remnants"],
            ["8", SC("backroom", "The Back Room, again"), "Dawn. Two doors: home, or the table.", "The Remnants, through the hayloft door"]])
         + P("<strong>Doors.</strong> A door with a tile beyond it moves the whole party, and makes the next scene the active one. Some of those doors start <em>locked</em>: they open when the story says (the Remnant in that scene does it), and you open them the ordinary Foundry way: click the door icon (or right-click it to unlock). Each scene's journal says which door, and when.")),
        ("Pacing", "<h2>Pacing</h2>" + ul(
            "<strong>Session 1:</strong> the Stickit Inn, Room 1, Room 2. End when the guards step aside and the door opens on a crossroads at dusk.",
            "<strong>Session 2:</strong> the Crossroads, the Cellar (one fight), the Stable, the Hoard. End on the ask, with the door to the Cover open.",
            "<strong>Session 3:</strong> the Cover, all three waves, then the goodbyes and Room 5. Long rest before it, none during it.")
         + P("The party can take short rests between stops in session 2, and should: the Cellar fight is meant to cost a little. They take a long rest in the Hoard before session 3 (the Remnants keep watch, and roll dice all night).")),
    ]))

    # ------------------------------------------------------------------ HOW TO RUN IT
    entries.append(("00b. How to Run It", [
        ("How to Run It", "<h1>How to Run It: Step by Step</h1>" + P("The whole adventure in order, with the Foundry pieces each step uses. Each scene's journal has the detail.")
         + "<h2>Three habits</h2>" + ol(
            "<strong>Doors move the party and switch the scene.</strong> The first character onto a door tile takes the whole party, and the new scene becomes active. Every door goes to one place; going back through it goes back.",
            "<strong>Locked doors open when a Remnant opens them.</strong> Room 2's door (Fred), the Cellar door (Thon), the Stable's east wall (T. Morlock), the Hoard's side door (the party says yes). You open each by clicking its door icon. Nothing else is hidden.",
            "<strong>People are already on the maps.</strong> Each Remnant is placed where the party meets them. In the Cover, the Remnants and the second and third waves' hangers-on are hidden tokens that the tiles reveal.")
         + "<h2>Before session 1</h2>"
         + step(1, "Check the modules", "Required: Monk's Enhanced Journal, Campaign Companion, Monk's Active Tile Triggers. Recommended for sound: Ivan Duch's Music Packs, Michael Ghelfi, SoundFx Library, Adventure Music, SoundBard; and Patrol, for the barmaid.")
         + step(2, "Read the route", "The overview, then the Hoard and the Cover journals: the end explains the beginning.", use=[J("00. The Unfinished Fight: Overview"), J("The Hoard"), J("The Cover")])
         + step(3, "Prepare the people", f"Read {J('The Remnants')}. Pick one secret detail from each character's backstory for {A('barkeep')} to know (Room 1). Decide who the latecomer is, if anyone.", use=[J("The Remnants"), "Each Remnant's Person page has their lines and links their actor."])
         + step(4, "Set the opening", "The scene <em>Welcome: The Stickit Inn</em> is active on import: it's what players see when they connect. Give out the handouts The Job and The Kettle Pass.", use=["Handouts: The Job, The Kettle Pass"])
         + "<h2>Session 1</h2>"
         + step(5, "The evening", "Play the inn straight in the common room (the vista is enough), then Bartleby leads them upstairs. Move everyone to Room 1 and activate it.", use=[SC("backroom"), J("Room 1: The Back Room")])
         + step(6, "Night falls", "When everyone has bedded down, double-click the GM control <em>Night falls</em> (top-left corner of the scene, on the Tiles layer). It lights the lantern, puts Bartleby on the stairs, opens the hayloft door that wasn't there, and arms the stairs and the hayloft door: both now lead down into Room 2.", use=["GM control: Night falls"])
         + step(7, "Room 2", "Roles, one line each. Fred is the real one. When he says his Signature, click his table (the tile under him): everyone gets the X Map, and the door's lock opens. If it doesn't, click the door icon yourself.", use=[SC("common-room"), J("Room 2: The Common Room That Isn't"), TB("jokes")])
         + "<h2>Session 2</h2>"
         + step(8, "The Crossroads", "Four roads out. North, south and west come back to the crossroads. East goes on. Strider reads the map and points east.", use=[SC("c7-crossroads"), J("The Crossroads")])
         + step(9, "The Cellar", "The fight. The east door won't open until Thon presses button six. When he does, click the door icon to open it; the chests stop.", use=[SC("c8-cellar"), J("The Cellar")])
         + step(10, "The Stable", "Two doors lead back up to the hayloft. When T. Morlock walks into the east wall, click the door icon there to open it: that is the hole he left.", use=[SC("c2-stable"), J("The Stable")])
         + step(11, "The Hoard", "The Remnants ask. When the party agrees, Thon opens the side door: click its door icon. End the session there, or go straight on.", use=[SC("hoard"), J("The Hoard")])
         + "<h2>Session 3</h2>"
         + step(12, "The Cover", "Three waves. The cave mouth tile wakes wave 1 and brings in the Remnants. Use the GM controls for Rorvik (top of round 2), wave 2 and wave 3.", use=[SC("cover-cavern"), J("The Cover"), "GM controls: Rorvik bursts in · Wave 2 wakes · Wave 3 wakes", "Music: The Cover"])
         + step(13, "Goodbyes", "After wave 3, the Remnants say goodbye, one by one, and each gives their own player something from the pile. Then the cave's back passage opens: it leads to Room 5.", use=[J("The Cover") + " (After the Fight)"])
         + step(14, "Room 5", "Dawn. Two doors: home, or the table. Each player chooses for their own character.", use=[J("Room 5: The Back Room, Again"), "Music: Room 5, dawn"])),
    ]))

    # ------------------------------------------------------------------ ROOM 1
    entries.append(("Room 1: The Back Room", [
        ("The Evening", "<h1>Room 1: The Back Room</h1>" + P(
            f"The Stickit Inn sits where the Kettle Pass road leaves the valley, and everyone for three days in any direction knows its cider. {A('stranger')} in the corner booth has a job: ride guard on a lamp-oil wagon over the Kettle Pass to Thistlecross — three days, forty gold each, half now, leaving at first light (the handout The Job). The party takes it, and {A('barkeep')} leads them up the stairs to the storeroom over the kitchen to sleep before the dawn road.")
         + aside("Why they're here", ol("<strong>It's on the road.</strong> The last bed and hot meal before three days of high road.",
                                       "<strong>The cider.</strong> Someone in the party has been promising the others a mug for weeks.",
                                       "<strong>The job brought them.</strong> Word went round: guards wanted for a wagon over the pass, ask at the Stickit Inn.",
                                       "<strong>They were passing through,</strong> and this is where night fell."))
         + box("The barkeep goes up ahead of you with the lantern. A short landing at the top of the stairs, a door, and the storeroom: shelves of sacks and crocks, a cot for each of you already made up, one lantern on a hook, a small window over the yard. He tells you he'll have bread on at first light, and a jug of the house cider for the road.")
         + P("Describe it in loving, mundane detail. Let them count the cots. The room has one door: the one they came in by. There is no other way out, and nothing to explore, which is the point: let them settle in, talk, and go to bed.")
         + aside("Keyed areas", ul("<strong>A1. The landing.</strong> Top of the stairs down to the common room.",
                                   "<strong>A2. The cots.</strong> One per character, blankets turned down.",
                                   "<strong>A3. The shelves.</strong> Provisions, the party's receipts tucked under the crocks. Behind the far unit, at night only, a door.",
                                   "<strong>A4. The window.</strong> Small, four panes.",
                                   "<strong>A5. The stone.</strong> In the corner by the chest: a stone with a hilt in it."))),
        ("The Latecomer", "<h2>The Latecomer</h2>" + P(
            "If a player arrives late, their character is the last guest of the night: Bartleby brings them up with a candle while the others are bedding down. If they arrive after night has fallen, they are the one who wakes.")
         + box("Footsteps on the stairs, and a second light. Bartleby comes up with a candle and someone behind him, travel-stained, apologising. 'One more for the road, if you'll have them.' The last cot, you notice, was already made up."), 2),
        ("Night Falls", "<h2>Night Falls</h2>" + P("When everyone is asleep, fire the GM control <strong>Night falls</strong>. Then pick the character whose player is most likely to get up and look: they wake.")
         + box("The lantern is lit. Nobody lit it. The door to the landing is open a hand's width, and the stairs beyond it are stone, going down, too many of them. And behind the shelves, where there was a wall at supper, there is a door.")
         + P("<strong>What the control did.</strong> Bartleby is now on the stairs (his token appears). The door behind the shelves (A3) is a real door now; it opens on the hayloft over the stable, and a ladder down. The stairs and the hayloft ladder now both lead to the same place: Room 2. Either way down is fine.",
             "<strong>The stone.</strong> Whoever pulls the hilt draws a long iron key with no teeth (handout: The Toothless Key). It opens nothing. Keep it: it opens the door home in Room 5.")
         + "<h3>Bartleby, on the stairs</h3>" + P(
            f"{A('barkeep')} comes up the stone stairs with a tray. He is kind. It's not morning yet, he says; go back to bed, the road will be there tomorrow. He knows one detail about one character that they have never told anyone (pick it before the session). He is not a fight and cannot be made into one.",
            "If they go back to sleep, they wake again in the dark, the lantern lit, and Bartleby has set a second tray. The way is down. Once anyone goes down the stairs or the ladder, the party is in Room 2."), 2),
    ]))

    # ------------------------------------------------------------------ ROOM 2
    entries.append(("Room 2: The Common Room That Isn't", [
        ("The Room", "<h1>Room 2: The Common Room That Isn't</h1>" + box(
            "The Stickit Inn's common room. The fire is lit, the tables are full, and nobody is looking at you. In every booth, a hooded stranger. The barmaid is walking a slow circle between the tables with a tray and has not arrived at one. A drunk by the hearth is telling a joke to nobody. Two guards stand in the door.")
         + P("Every patron is a <em>role</em>: a part in a scene, with one line, said the same way every time, whoever asks. The door out is locked, and the guards stand in it.")
         + aside("Keyed areas", ul("<strong>B1. The booths.</strong> A hooded stranger in each, offering the job in the same words.",
                                   "<strong>B2. The bar.</strong> Nobody behind it. Mugs of cider, every one pale gold. One is red.",
                                   f"<strong>B3. The hearth.</strong> The drunk: roll once on {TB('jokes')} the first time anyone talks to him; that joke is his line forever.",
                                   "<strong>B4. The door.</strong> Two guards. Locked.",
                                   "<strong>B5. The stairs.</strong> Up to a landing, a door, and the bottom of the same stairs. Every time."))
         + table(["Role", "Their line"], [
              ["A hooded stranger (every booth)", "“Lamp oil, over the Kettle Pass to Thistlecross. Three days. Forty a head, twenty tonight, the rest on delivery. We leave at first light.”"],
              ["The barmaid", "“Just coming, love.” (She never arrives. With the Patrol module she walks her circuit by herself.)"],
              ["The guards (B4)", "“Move along. Nothing to see here.” (Both together.)"],
              ["The merchant", "“Finest wares this side of the pass! Have a look!” (The table is empty.)"],
              ["The old man", "“In my day, the pass was a dangerous road.”"],
              ["The drunk (B3)", "His one joke (" + TB('jokes') + "), forever."]])),
        ("The Puzzle", "<h2>The Puzzle: Who Is Real?</h2>" + P(
            f"One patron is not a role: {A('remnant-fred')}, one player's first character (and quite possibly only ever a comic strip). He thinks it's mid-adventure and the party are his old companions. The puzzle is to find him and get him to say the thing everyone remembers him for: his Signature, <em>POW!</em>")
         + "<h3>Three clues</h3>" + ol("He is the only patron who asks the party a question (“Ready for the next panel?”).",
                                      "His cider is red; every other mug in the room is pale gold.",
                                      "The player whose character he is will recognise him first. Let them sweat before they say so.")
         + "<h3>Getting the Signature</h3>" + P("Anything that gets Fred to swing gets the POW: an arm-wrestle, a sparring bout, a dare, asking him to show how he fought the dragon, a fight with the guards. He never attacks the party. When the POW! hangs in the air in hand-lettered capitals, every role stops mid-line and turns to look at the party. Hold it for a beat.")
         + "<h3>The payoff</h3>" + P("Fred hands over a map with an X on it (handout: The X Map): “The X is the way out. Everyone knows that. Follow it.” <strong>Click Fred's table</strong> (the tile under him): it shows everyone the map and unlocks the door. The guards step aside together without a word. Fred stays: “See you at the table.”")
         + aside("If they force it", P("If the party fights its way past the guards or breaks the door, let them. Fred catches up at the Crossroads, out of breath: “You forgot this!”, and hands over the map there.")), 2),
    ]))

    # ------------------------------------------------------------------ CROSSROADS
    entries.append(("The Crossroads", [
        ("The Crossroads", "<h1>The Crossroads</h1>" + box(
            "The door opens on open country at dusk. A crossroads, a signpost, and long grass. Every arm of the signpost points the same way, north. The light is going, and it never finishes going. Someone is sitting at the foot of the signpost with his hood up.")
         + P(f"{A('remnant-strider')} has been here a long time. He is never lost; he just has never had a map. Four roads lead out: north, south (the way they came in), west and east.")
         + table(["Road", "Where it goes"], [
              ["North (where the signs point)", "Back to the crossroads. They walk a few minutes and come in again by the south road."],
              ["South", "Back to the crossroads. They come in by the north road."],
              ["West", "Back to the crossroads. They come in by the east road."],
              ["East", "On: a cellar door in a bank of earth. The Cellar."]])
         + P("<strong>The puzzle</strong> is only this: the signs lie and the roads loop. Let them try north first, everyone does. Show Strider the X Map and he reads it at a glance: “That's two doors from here.” He points east, and he is right (the Cellar door, then the Stable door, and the Hoard is through the next). The X on the map, when they look, is east.",
             "Strider does not come with them. “Go on. I know the way now. I'll see you at the table.”")
         + aside("Doors", P("The four roads are tiles at the map's edges (the free-standing door frames). North, south and west loop back here; east goes to the Cellar. The Cellar's way back out comes in on the east road."))),
    ]))

    # ------------------------------------------------------------------ CELLAR
    entries.append(("The Cellar", [
        ("The Cellar", "<h1>The Cellar</h1>" + box(
            "A cellar, low and dry, and you know it: it is the back room from underneath. The same shelves, the same crocks, upside down on the ceiling-beams. Four provisions chests stand in the middle of the floor, your receipts still tucked under the lids. They are breathing. At the far end, a door, and in front of it a wizard with a heavy black rod, pressing a button.")
         + P(f"{A('remnant-thon')} has been trying to open the east door for a long time. It has no handle and no lock; nothing opens it (Strength, thieves' tools, <em>knock</em>: it is not locked, it is just shut). His rod will, as a battering ram. The trouble is the order.")
         + "<h3>The rod</h3>" + P("Thon presses the buttons in order, one per press, one press on each of his turns, and names each one aloud: <strong>1</strong> mace, <strong>2</strong> flaming blade, <strong>3</strong> battleaxe, <strong>4</strong> spear, <strong>5</strong> ladder, <strong>6</strong> battering ram, <strong>7</strong> a pole that points north. He insists they go in order (“Hold on, I'll get there”). If anyone asks for the battering ram, or button six, by name, he grins, says “Button six!”, and presses it.",
            "So the door opens on his sixth turn by itself, or as soon as someone listens to the list and asks for the ram. A party that pays attention gets out in two rounds; one that doesn't fights for six.")
         + "<h3>The chests</h3>" + P(f"The first click wakes the {A('chest', 'Provisions Chests')} (four of them, already on the map). They fight until the door opens; then they stop where they are and are only chests again, and anyone stuck to one falls free. Thon will not fight them (“I'm busy”); he has a door to open.",
            "This is the adventure's only fight before the Cover. It should cost a spell slot or two and some hit points, not a life. Let the party short rest afterwards; Thon shows them every button again while they do.")
         + P("<strong>When the door opens</strong>, click its door icon to open it in Foundry. Beyond it is a ladder up, and the smell of hay. Thon stays: “See you at the table. Ask me about button seven.”")
         + aside("Doors", P("The door they came in by leads back to the Crossroads (by the east road). The east door is locked on the map until you open it; the tile behind it goes to the Stable."))),
    ]))

    # ------------------------------------------------------------------ STABLE
    entries.append(("The Stable", [
        ("The Stable", "<h1>The Stable</h1>" + box(
            "You come up the ladder into a hayloft, and look down into a stable. Horses in every stall, all of them facing the wall. They are your own mounts: the ones you never bought. High above, on a rafter, a halfling is sitting with his legs crossed, reading a sheet of paper.")
         + P(f"{A('remnant-morlock')} is twenty feet up (his token is at elevation 20). Below, the stable has three doors: the hayloft ladder they came up, the big doors at the south end, and a small door in the east wall.")
         + table(["Door", "Where it goes"], [
              ["The hayloft (north)", "Back down to the Cellar."],
              ["The south doors", "Out into the yard, round the side, up the outside ladder, and in through the hayloft. Every time."],
              ["The east door", "Locked, with no keyhole. It doesn't open. The way on is through the wall."]])
         + "<h3>Getting T. Morlock down</h3>" + P("He will not come down (“Why would I come down? Come up.”). Someone has to climb to him: the posts are smooth, Strength (Athletics) DC 15, or a rope, a spell, a familiar. Or ask to see his sheet: he lowers it on a string, then the string, then himself, because nobody ever asks to see it.",
            "When someone is up with him, or has read his sheet out loud (seventh level, every box filled in, climb walls ninety-nine percent), he drops twenty feet, lands on his feet, walks to the east wall, says “Elishaf”, and walks into it. There is a halfling-shaped hole. “Well? Come on.”")
         + P("<strong>When he goes through the wall,</strong> click the east door's icon to open it: that is the hole. It stays open for a minute; the tile behind it goes to the Hoard. He does not come through after them. He is already there when they arrive.")),
    ]))

    # ------------------------------------------------------------------ HOARD
    entries.append(("The Hoard", [
        ("The Room", "<h1>The Hoard</h1>" + box(
            "A reading room: two tall arched windows of stained glass, timber ribs across the ceiling, books to the beams. Armchairs round a low table, dice on the table, still warm. Beyond it, through glass double doors, a smaller room lined with shelves, and in it, people you know. Fred. Thon. Strider. T. Morlock on the back of a chair. One chair is empty, and someone has put a character sheet on it anyway.")
         + P("These are the Remnants, the first party, at their table. The empty chair is Rorvik's: he is late, as always. They are delighted to see the party, and they have been waiting a long time to ask them something.")
         + aside("Keyed areas", ul("<strong>D1. The glass doors</strong> (south): the way in, and back to the Stable.",
                                   "<strong>D2. The armchairs.</strong> Dice on the low table, warm, and a battered copy of the 1977 Monster Manual, face up.",
                                   "<strong>D3. The portrait.</strong> Between the arches: a party of five, painted badly, in a cave.",
                                   "<strong>D4. The inner room.</strong> The Remnants, at their own table. One chair empty, a character sheet on it.",
                                   "<strong>D5. The windows.</strong> Stained glass: a red dragon, a unicorn, an owlbear, all mid-fight.",
                                   "<strong>The side door</strong> (east wall): locked. It opens on the Cover."))),
        ("The Ask", "<h2>The Ask</h2>" + P("The Remnants explain, each in their own way, a line or two at a time. Let the players ask questions. The facts:")
         + ol("<strong>The fight on the cover was never finished.</strong> The six monsters on the 1977 Monster Manual: a dragon, a unicorn, a centaur, a troll, a roper, an owlbear. Every time the first party got to them, the session ended. It got late. Someone moved away. “To be continued!” says Fred.",
              "<strong>Unfinished things don't end.</strong> That is what the back room is: everything left unfinished at a table. It catches parties, and it caught this one.",
              "<strong>They can't finish it alone.</strong> They are the ones who didn't. They need a party that finishes things. They need this one.",
              "<strong>Finishing it is the way out.</strong> The X on the map is on the cavern. When the fight is over, the back room lets everyone go, if they want to go.",
              "<strong>There is a hoard.</strong> Behind the monsters, the treasure pile from the cover. Each Remnant will give their own player something from it.")
         + "<h3>Why the party should say yes</h3>" + ul(
              "<strong>It is the way home.</strong> The map, Strider and the Remnants all agree. Nothing else leads out.",
              "<strong>They won't be alone.</strong> The first party fights at their side.",
              "<strong>The treasure is real</strong> (After the Fight, in the Cover journal).",
              "<strong>It's the players' own first characters asking.</strong> Let each Remnant ask its own player, by name. That is the hook; play it straight.")
         + P("If the party refuses, the Remnants don't argue. They go back to their game, and the glass doors lead back the way the party came: Stable, Cellar, Crossroads, Common Room, and up the stairs to the back room, where Bartleby has set out a tray and it is still not morning. Every road comes back to this table. When they come back, the chairs are still there.")
         + "<h3>When they say yes</h3>" + P("Thon gets up: “Allow me. Button six.” The side door bursts open. <strong>Click the side door's icon</strong> to open it; the tile beyond goes to the Cover. If the table wants a long rest first, they take it here, and the Remnants keep watch, rolling dice all night.")),
    ]))

    # ------------------------------------------------------------------ COVER
    entries.append(("The Cover", [
        ("The Cavern", "<h1>The Cover</h1>" + box(
            "A dark cavern, and in it the picture from the cover of the Monster Manual, exactly as you remember it: a red dragon rearing over a pile of treasure, a unicorn, a centaur with a bow, a troll, a thing like a stump with tendrils, an owlbear. All frozen mid-fight. Fighting gaps: person-shaped spaces in the air where the adventurers stood. The gaps are your size. Behind you, the first party comes in, weapons out.")
         + P("The party and the Remnants fight the six monsters together, two at a time: three waves, back to back, no rest between them. Each wave is a hard fight on its own for a strong party of five. The point is not any one wave; it is all three, in a row, with what they have left.")
         + aside("Keyed areas", ul("<strong>E1. The cave mouth.</strong> Where the party and the Remnants come in. The roper's gap (the thief); the piercers on the ceiling above.", "<strong>E2. The ledge.</strong> The centaur's gap (the archer).",
                                   "<strong>E3. The hoard.</strong> The dragon's gap (the fighter with the shield), and the treasure.", "<strong>E4. The chest.</strong> The troll's gap (the dwarf).", "<strong>E5. The back wall.</strong> The owlbear's gap (the cleric); the unicorn's gap (the elf) beside it.",
                                   "<strong>The back passage</strong> (west side): the way out, once it is over."))),
        ("The Waves", "<h2>The Waves</h2>" + table(["Wave", "Monsters", "Wakes", "Its trick"], [
            ["1", f"{A('troll')}, {A('roper')}, six {A('piercer', 'Piercers')}", "The moment the party enters (the cave-mouth tile).", "The troll gets back up unless burned. The roper grapples from 60 feet and reels; the piercers drop on whoever it reels in."],
            ["2", f"{A('centaur')}, {A('unicorn')}, three {A('outrider', 'Outriders')}", "When wave 1's last monster drops: fire <em>GM: Wave 2 wakes</em>.", "Arrows from everywhere. The unicorn heals and shields the others, and can stand a downed monster back up: kill it first."],
            ["3", f"{A('owlbear')}, {A('dragon')}, two {A('cub', 'Owlbear Cubs')}", "When wave 2's last monster drops: fire <em>GM: Wave 3 wakes</em>.", "The dragon breathes on the most people it can catch, Remnants included. The owlbear grabs and holds."]])
         + P("<strong>Between waves.</strong> When a wave's last monster drops, the next pair takes one round to finish its 1977 pose and turn around. That round is the only breath the party gets: drink a potion, stand someone up, move. No short rest.",
             "<strong>The big six are visible from the start</strong>, frozen (their Still Fighting 1977 trait). Their hangers-on are hidden until their wave: the controls reveal them. Roll initiative once for the whole fight; add each wave's monsters when they wake, acting at the top of the next round.")
         + aside("If it goes badly", P("If two characters are down when wave 2 ends, wave 3 comes without the cubs (delete them from the scene). If the party is still fresh after wave 2, let the dragon open with its breath. Don't soften more than that: three hard fights in a row is the adventure.")), 2),
        ("The Remnants in the Fight", "<h2>The Remnants in the Fight</h2>" + P("The Remnants are allies, and you run them. They are the first party, not the heroes: the players' characters finish this fight. One rule keeps them in their place:")
         + ul("<strong>Once per wave, each Remnant uses its Signature, and it always works</strong> (on each Remnant's sheet: Fred's POW!, Thon's rod, Strider's arrow, T. Morlock's vault and backstab, Rorvik's Hothead).",
              "<strong>Every other turn, it Helps</strong> a character next to it (Advantage on that character's next attack or check), or Dodges. Describe it as the old party fighting the way it used to: shouting advice, a shield in the way.",
              "<strong>It never takes the last hit</strong> on a monster.",
              "<strong>It doesn't die.</strong> At 0 Hit Points it goes down, and stands up at the start of its next turn with half its Hit Points, mid-sentence. It has been in this fight before.")
         + "<h3>Rorvik</h3>" + P(f"{A('remnant-rorvik')} isn't there when wave 1 wakes. At the top of round 2, fire <em>GM: Rorvik bursts in</em>: he runs in through the cave mouth, sword out. “Sorry I'm late. What did I miss?” From then on he acts first every round.")
         + P("<strong>Speak for them.</strong> Each Remnant has a line for each wave on its Person page. Give each one a moment: the player whose first character it is should get to watch it do the thing everyone remembers.")),
        ("After the Fight", "<h2>After the Fight</h2>" + box("The dragon goes down onto the hoard, and the coins slide. The cavern is quiet. The gaps in the air are gone. The first party stands there, breathing hard, looking at each other as if they had just remembered something.")
         + P("<strong>The goodbyes.</strong> Each Remnant comes to its own player, one at a time, and says its last line (on its Person page): Fred's “We finished it. THE END.”, Strider's “This one's done.” Speak to the player, not the character. Then each one takes something from the pile and gives it to them:")
         + table(["From", "To their own player's character"], [
              [A("remnant-fred"), "A <em>+1 longsword</em> (or the character's own weapon, made +1). The POW! still appears when it crits."],
              [A("remnant-thon"), "A <em>wand of the war mage +1</em>. It has one button, and it is labelled."],
              [A("remnant-strider"), "A <em>cloak of elvenkind</em>, travel-stained."],
              [A("remnant-morlock"), "A <em>ring of protection</em>, from his own finger. And, if they ask, his sheet."],
              [A("remnant-rorvik"), "A <em>pair of boots of speed</em>. “You'll never be late.”"]])
         + P("<strong>The offer.</strong> Then the Remnants say what they came to say: the fight is done, and anyone can go home now. Or anyone can come with them. The table is still up there, and there's a chair for everyone. “Come on. Last panel. Or the first one.”",
             "<strong>The way out.</strong> The back passage (west side of the cavern) is open now. Its tile leads to Room 5: the back room, at dawn. The Remnants go ahead: they will be on the other side of the hayloft door.")
         + aside("If they flee mid-fight", P("The back passage is a way out at any time. A party that runs ends up in Room 5 having not finished it. Play Room 5 anyway: the Remnants are not behind the hayloft door, only the sound of a fight, still going.")), 2),
    ]))

    # ------------------------------------------------------------------ ROOM 5
    entries.append(("Room 5: The Back Room, Again", [
        ("Dawn", "<h1>Room 5: The Back Room, Again</h1>" + box(
            "The storeroom over the kitchen. Dawn light under the landing door, and through the small window, which is now a stained-glass window, the colours of the reading room laid across the cots. The cots are made. The lantern is out. The stone in the corner has no hilt in it.")
         + P("The same Room 1 scene. They never left. Downstairs, ordinary morning: Bartleby calling up that the bread's going hard, the stranger's voice asking if they're up. And from behind the hayloft door, the Remnants, laughing (SoundBard: <em>Remnants laughing, through the door</em>).")),
        ("The Choice", "<h2>The Choice</h2>" + ul(
              "<strong>The landing door: home.</strong> It is locked. The toothless key turns in it. Beyond: ordinary stairs, fourteen of them, and the common room in the morning.",
              "<strong>The hayloft door: the table.</strong> The Remnants, the low table, a chair for each character, dice still warm. “Oh, it's you. Go on through. They kept your seats.”")
         + "<h3>Making it a real choice</h3>" + ul(
              "<strong>Each player chooses for their own character.</strong> Not a party vote. The party can split.",
              "<strong>The price of going home:</strong> the Remnants are gone, and this time they said goodbye. The gifts from the pile come along.",
              "<strong>The gift of staying:</strong> the game never ends. Every session is session one, with the people you started with. Say so plainly. It is not a trick.",
              "<strong>Don't lean.</strong> No hint that one answer is right. Let the silence go on longer than is comfortable.",
              "<strong>Make it physical.</strong> Each player moves their token to a door.")
         + "<h3>If they go home</h3>" + box(
              "The key turns as if the lock had been waiting for it. The stairs are wooden, and there are fourteen of them; you count. Bartleby is behind the bar, wiping a mug that is already clean. “There they are. Bread's hot. Jug's by the door.”",
              "In the corner booth, the stranger has his hood down, checking the straps on a pack. “Wagon's in the yard,” he says. “If you're still coming.” Outside it is a cold, clear morning, and the road goes up into the hills one bend at a time.")
         + P("Each character who goes home gains a level, and keeps what the Remnants gave them.")
         + "<h3>If they stay</h3>" + box(
              "The hayloft is warm and full of lamplight, and there is a low table up here, and chairs round it, and the people you used to be already sitting down. There is a character sheet on your chair, and the name at the top is the one you almost gave them. Somebody says, “Right. Where were we?”, and nobody remembers, and it doesn't matter.")
         + P("The campaign ends here for that character, and it is allowed to be a good ending."), 2),
    ]))

    # ------------------------------------------------------------------ CAST, HANDOUTS
    entries.append(("Cast", [("Cast", "<h1>Cast</h1>" + table(["Who", "Where"], [
        [A("barkeep"), "Room 1 (the night stairs), Room 5 (from downstairs)"], [A("stranger"), "The Stickit Inn; every booth in Room 2"],
        [A("remnant-fred"), "Room 2; the Hoard; the Cover"], [A("remnant-strider"), "The Crossroads; the Hoard; the Cover"],
        [A("remnant-thon"), "The Cellar; the Hoard; the Cover"], [A("remnant-morlock"), "The Stable; the Hoard; the Cover"],
        [A("remnant-rorvik"), "The Cover, from round 2"],
        [A("remnant-rogue") + ", " + A("remnant-barbarian") + ", " + A("remnant-wizard"), "Fallbacks: a stand-in for any Remnant whose player can't make it, or for another table's first characters"]]))]))
    return entries
