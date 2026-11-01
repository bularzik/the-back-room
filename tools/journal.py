"""Adventure text for The Back Room. Each entry: (name, [(page_name, html, level)]). `L` resolves links at build time.
Source of truth: docs/the-back-room.md and docs/corridor-pool.md. GM text in <p>, read-aloud in <blockquote>."""

def box(*ts): return '<blockquote class="read-aloud">' + "".join(f"<p><em>{t}</em></p>" for t in ts) + "</blockquote>"
# Misremembering: what one short rest in the Corridors rewrites. (detail, how it shifts)
MISREMEMBERING = [
    ("A sibling's name", "It drifts by a sound or two (Tomas is Thomas now), or a brother has become a sister."),
    ("The door of the house they grew up in", "A different colour. They will describe it the new way without noticing."),
    ("Which god they pray to", "The same prayers and the same holy days, addressed to a neighbouring god's name."),
    ("Their mentor's fate", "Alive where they died, retired where they vanished, or the other way round."),
    ("Their hometown", "One syllable off, or it stands on a river now instead of the coast."),
    ("A scar", "On the other side of the body, or from a different wound with a different story."),
    ("A favourite food or drink", "Now Stickit cider, which they had never tasted before last night."),
    ("A parent's trade", "The baker was a chandler; the soldier was a ferryman."),
    ("How they met one other party member", "Their version now starts somewhere else, and the other player's version no longer matches."),
    ("An heirloom on their sheet", "A slightly different object: the locket is a ring, the dagger has a different pommel."),
    ("A rival", "Same name, but the grudge has turned around: the rival now owes them."),
    ("Their age", "A year or two off, and their birthday falls in a different season."),
    ("A language they speak", "Swapped for a related one. Let them find out when another player mentions it."),
    ("Their ideal", "Reworded so that it means a little less."),
    ("Their bond", "The person they protect is now someone else from their own story."),
    ("A fear", "Now something from the Corridors: stairs that do not end, doors with the same number, a fire that gives no heat."),
    ("A childhood pet or mount", "The same name, a different animal."),
    ("Why they became an adventurer", "Now simply: because the others were going."),
    ("Their first adventure", "It now took place in the upstairs room of a library."),
    ("Their name", "One letter of the spelling, or a nickname the others have always used and they have never heard."),
]

# The drunk by the hearth in Room 2: one joke, rolled once, then the same line forever.
DRUNK_JOKES = [
    "A wizard, a fighter and a thief walk into a tavern. The barkeep says, ‘Is this some kind of quest?’ And the wizard says— <em>(He laughs so hard he never says what the wizard says.)</em>",
    "How many adventurers does it take to light a lantern? <em>(Beat.)</em> None. It lights itself.",
    "Fellow walks into an inn and asks for a room. Innkeeper says, ‘All we’ve got is the back room.’ Fellow says, ‘I’ll take it.’ Innkeeper says, ‘You already did.’",
    "Knock knock. <em>(He waits. If nobody says ‘Who’s there?’, he goes on waiting. If someone does:)</em> Me. Still.",
    "Did you hear about the barmaid? She’s been bringing me this drink since Tuesday. <em>(He raises an empty hand.)</em>",
    "What do you call a door that always opens onto somewhere else? <em>(Beat.)</em> A door.",
    "I told the hooded stranger a joke once. Now he’s in every booth. Went over very well.",
    "Ten rats walk into a cellar. Farmer pays for them. Ten rats walk into a cellar.",
    "What’s the difference between a stairwell and a staircase? <em>(Beat.)</em> One of them goes up. <em>(He looks over at the stairs for a long time.)</em>",
    "Why did the halfling cross the high wire? To get to the far post. <em>(Beat.)</em> Which one’s the far post?",
    "How do you know you’ve been at the Stickit too long? The cider tastes like the first time. Every time.",
    "Best thing about this inn? Nobody ever leaves a bad word about it. <em>(Beat.)</em> Nobody ever leaves.",
]

# Lines for each NPC's Person page: (when, line). Use them, change them, ignore them.
DIALOG = {
    "barkeep": [
        ("Pouring", "House cider. Pressed in the yard, served cold. Goes down like water and gets up like a mule."),
        ("Showing them upstairs", "Cot each, made up fresh. Bread on at first light, and a jug for the road. Mind the third step; it's been the third step since my father's day."),
        ("The night, on the stone stairs", "Not morning yet. Back to bed, now. The road'll be there tomorrow. It always is."),
        ("He knows (pick the detail before the session)", "Your mother still keeps the lamp in the window, doesn't she? The blue one."),
        ("If pressed about how he knows", "Know what, love? Drink your milk."),
        ("If they go back to sleep", "There we are. I'll set another tray."),
        ("Room 5, from downstairs", "Are they up yet? Bread's going hard. Tell them the wagon's in the yard."),
    ],
    "stranger": [
        ("The hook", "Lamp oil, over the Kettle Pass to Thistlecross. Three days. Forty a head, twenty tonight, the rest on delivery. We leave at first light."),
        ("Asked if it's dangerous", "It's a road. Roads have weather. That's the whole of it."),
        ("Asked his name", "Kael Shadowmere. (He does not smile. Nobody ever believes him.)"),
        ("Asked why he's hooded", "It's cold in the booth."),
        ("Room 2, every booth, word for word", "Lamp oil, over the Kettle Pass to Thistlecross. Three days. Forty a head…"),
        ("Room 5, from downstairs", "Are they up yet, Barnaby? We've a pass to cross."),
    ],
    "remnant-fred": [
        ("Introducing himself", "FRED THE FIGHTER!"),
        ("Greeting the party", "There you are! Took your time. Ready for the next panel?"),
        ("Sizing them up", "Four of you. Good. Fits the frame."),
        ("His Signature, when he swings", "POW!"),
        ("Asked about his past", "Summer. Ink. A camp paper. Then… To be continued!"),
        ("Handing over the map", "The X is the way out. Everyone knows that. Next week, we follow it."),
        ("Room 4, as they reach the glass doors", "Hey. Hey! There's still a panel left. Same time next week?"),
    ],
    "remnant-thon": [
        ("Greeting", "Ah, you'll want to see this. Everybody wants to see this."),
        ("Showing off the rod", "Button one, mace. Button two, flaming blade. Button three, and this is the good one, listen for the click…"),
        ("Asked to cast a spell", "Spells? Yes, certainly, but have you seen button six? It points north. Always. Even here. Especially here."),
        ("His Signature", "Hold on. (Click.) There. Ladder."),
        ("The Blank", "I knew a spell once. Started with an F. Doesn't matter. Button four."),
        ("Room 4, pleading", "Stay. I haven't shown you button seven. Nobody's ever seen button seven."),
    ],
    "remnant-rorvik": [
        ("Every few minutes", "Is it my turn yet?"),
        ("Arriving in the Hoard, round 2", "Sorry I'm late. What did I miss?"),
        ("Insulted", "Say that again. Go on. Say it with your sword out."),
        ("Asked about his adventures", "Adventures? I was there for all of them. Mostly. Sitting by the side. Waiting."),
        ("His Signature, first in initiative", "Me first. I've waited long enough."),
        ("Room 4, as they leave", "You're leaving? I only just got here!"),
    ],
    "remnant-morlock": [
        ("Introducing himself, from somewhere high up", "T. Morlock. Seventh level. Sixty thousand three hundred and eighty-one experience points. You can check."),
        ("Showing his sheet", "Every box filled in. Look: tightrope, one hundred percent."),
        ("Asked what the T. stands for", "…It stands for T."),
        ("About carpet making", "Nobody asks about the carpets. Warp, weft, a proper knot. It's very calming."),
        ("If anyone touches the leather bag", "Don't. Don't do that."),
        ("Passing through a wall", "Elishaf."),
        ("Room 4, from a rafter", "Stay. I'll teach you the high wire. It's easy, once you stop looking for the far post."),
    ],
    "remnant-strider": [
        ("First sighting, visit 7+", "You're lost. Don't argue. I know these halls."),
        ("Offering to lead", "This way. Every door goes somewhere. Only one goes where you're going."),
        ("Asked who he is", "Strider will do. It's what everyone calls me."),
        ("Asked about his lineage", "(He tells it, earnestly, at length: a story every player at the table has read in a book. He does not notice.)"),
        ("His Signature, with the bow", "Hold still. (He doesn't miss.)"),
        ("Room 4, quietly, as they reach the doors", "I've walked a long way to sit at this table. Stay a while. The road can wait."),
    ],
    "remnant-rogue": [
        ("Greeting", "Don't ask. It's complicated."),
        ("Asked about the tragedy", "It's… complicated."),
        ("Asked three times", "(Goes quiet, and looks at a player whose character it isn't.)"),
        ("Room 4", "Nobody leaves. That's the one thing I'm sure of."),
    ],
    "remnant-barbarian": [
        ("Greeting", "GRUKK SKULLSPLITTER!"),
        ("Asked anything about its past", "Grukk Skullsplitter. (Louder.) GRUKK SKULLSPLITTER."),
        ("Happily", "Grukk not angry. Grukk never angry. Grukk just strong."),
        ("Room 4", "Stay! Grukk carry you. Grukk carry everyone."),
    ],
    "remnant-wizard": [
        ("Greeting", "Mordecai the Magnificent. Master of the arcane. All of it."),
        ("Asked to cast anything else", "Certainly. (Gestures. Frowns.) Fireball."),
        ("Showing the spellbook", "Very rare tome. One page, but what a page."),
        ("Room 4", "Don't go. I've prepared something special. (It is a fireball.)"),
    ],
    "echo": [
        ("It does not speak", "It mouths whatever the character it copies said on their last turn, a moment late, without a sound."),
        ("When the loop breaks", "Nothing. It is just not there any more."),
    ],
}

# The half-page books: (band, title, text). Each is a player handout and a row of the Half-page Books table.
HALF_PAGE_BOOKS = [
    ("anywhere", "The Journal of Aldous Penhallow, Adventurer (Fourth Day)",
     "<em>Fourth day in the round room. No doors, no windows, and in the middle a marble statue of a fat king. Brannoc tried to dig under it and Wren tried to pray to it. Nothing worked. This morning Pell found a silver spoon on the floor beside the plinth, right where we have walked a hundred times, and said, very quietly, “What if.” The marble tastes faintly of almonds. We have eaten the left foot. There is a draught now from under the king, and Pell thinks if we keep going until</em>"),
    ("anywhere", "A Field Guide to the Creatures of the Region",
     "<em>RAT. Common. Found in cellars. Will attack if cornered, and frequently when not. A farmer in the next village will pay for ten of them. He will always need ten more.</em>"),
    ("anywhere", "On the Proper Keeping of Inns",
     "<em>A good inn offers a fire, a bed and a fair meal. The traveller should know that a free night is never free: someone will knock before dawn. Do not answer to your name. Pour the cider first and ask questions after, because once the cider is poured</em>"),
    ("anywhere", "Stairs, and Where They Go",
     "<em>Every stair goes up or down. It is the first thing a child learns about stairs and the last thing an old man forgets. If you count the steps going up, count them again coming down, and get a different number, you have not miscounted. Go back to the landing where the book lay face down and</em>"),
    ("visit 3+", "A Short Guide to Tracking in Difficult Country",
     "<em>Every trail tells you three things: who passed, how long ago, and whether they meant to come back. These tracks are yours. They are a day old. They go in, and they</em>"),
    ("visit 3+", "The Art of the High Wire",
     "<em>The rope does not care how good you are; it cares where your weight is. Look at the far post, never at your feet. Anyone who has crossed once will tell you the middle is not the hard part. The hard part is the moment you notice there is no far post, and you</em>"),
    ("visit 3+", "Rods and Their Configurations",
     "<em>Press the first stud: a mace. The second: an axe. The third: a ladder fifty feet long, which is more ladder than most problems need. There are six studs. Someone has labelled the fourth in a hand you almost recognise. The label says</em>"),
    ("visit 5+", "The Adventures of Fred the Fighter, No. 3",
     "<em>Panel one: Fred, winged helmet, sword raised. “POW!” Panel two: the troll falls over. Panel three: Fred grins out at the reader. “Same time next week?”</em> (The fourth panel is ruled in pencil and was never drawn.)"),
    ("visit 5+", "A Letter, Folded Into a Book",
     "<em>Sorry I’m late. Got turned round on the stairs, the stable had one horse too many, and I’m fairly sure I walked through the same market twice. Start without me. Save me a chair. I’ll be there before the</em>"),
    ("visit 5+", "Rules for the Reading Room",
     "<em>Quiet, please. No food at the tables. Roll dice on the felt, not the wood; the wood remembers. The room closes at nine. The room closes at nine. If you are still here when the room closes, push your chair in for whoever</em>"),
    ("visit 5+", "Recipe: Stickit Cider",
     "<em>Take apples from the old trees behind the inn, the sour ones nobody eats. Press them on the first cold night. Leave the barrel in the back room for one winter and do not open the door to check on it, however many times you hear</em>"),
    ("the Hoard only", "(Untitled)",
     "A clean title page, and under it one line: <em>“For the ones who kept the chairs warm.”</em> The rest of the page is blank."),
]

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
    J = lambda k, n=None: L("journal", k, n)
    TB = lambda k, n=None: L("table", k, n)

    entries = []

    # ------------------------------------------------------------------ 00 OVERVIEW
    entries.append(("00. The Back Room: Adventure Overview", [
        ("Introduction", "<h1>The Back Room</h1>" + P(
            "<em>The Back Room</em> is a liminal-horror adventure for four to five characters of 5th to 8th level, run over two or three sessions. The party meets at the Stickit Inn, a roadside tavern famous for its cider, played completely straight. They take the hook, buy provisions, and bed down in the storeroom over the kitchen before the dawn road. They never leave that room. The whole dungeon — stairwells, stables, corridors, campsites — is the storeroom, misremembered.",
            "The thing in there with them is not a monster. It is the first party: each player's first-ever D&D character, as the table misremembers them — overpowered, cooler than they were, one running joke swollen into a whole personality. These are the <strong>Remnants</strong>. They are not hostile. They want the game to keep going, forever, with the party in it.",
            "The message, in one line: <em>the places you are most comfortable are the ones you never finished leaving.</em>")
         + aside("Theme: Unfinished", P("One word, chosen first. Every room is something that was never finished — a story cut off, a character who never levelled, a campaign that died in the spring. 'Liminal' describes the dressing; 'unfinished' is the point. When you improvise a detail for a room, ask what in it was left undone."))
         + aside("Content Notes", P("Isolation, time loss, having one's memories quietly edited, a copy of a character, and a warm place that does not want anyone to leave. No gore. Talk with your players before you start about anything they'd rather fade to black."))),
        ("Sound", "<h2>Sound</h2>" + P(
            "<strong>Automatic.</strong> Every scene and vista has an ambient loop as its scene sound (playlist <em>Back Room: Ambience</em>): it starts when you activate the scene and stops when you leave. The Corridor copies share their place's loop. The landing scene comes in already active, so after importing click <em>Activate</em> on it once to start its music. The door tiles play their own stingers.",
            "<strong>By hand.</strong> <em>Back Room: Music</em> has a track for each beat that wants one (Session 1 tavern, the Corridors, The Cover, the Echo, the Hoard fight, dawn, the Last Word); most of the adventure is better with ambience alone. Run the macro <em>The Back Room: set up SoundBard</em> once per GM browser to fill a SoundBard bank with the cues: the door, a door closing somewhere, footsteps a half-beat late, the X, the lantern lighting itself, the waterfall that stops when someone speaks, a horse, the Remnants laughing through the door, Fred's POW!, Rorvik bursting in, a monster waking, Strider's arrow.",
            "The ambience and music come from four audio modules this one recommends (Ivan Duch's Music Packs, Michael Ghelfi Studios Audio Pack, SoundFx Library, Adventure Music); without them those sounds are silent and everything else works.")),
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
         + aside("Every book is a half-page book", P("Wherever the library layer puts a book or a shelf, every volume is one half-page long. This is a global rule, not a room's trope. Never explain it.", f"When a player opens one, roll on {TB('books', 'the Half-page Books table')} (or pick): each result links to a short handout to show them. Books 1–4 fit anywhere, 5–7 from visit 3 (each nods to one of the Remnants), 8–11 from visit 5, and 12 belongs on the shelves of the Hoard's inner room.")), 2),
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


    # ------------------------------------------------------------------ 00b HOW TO RUN IT
    def step(n, title, *paras, use=None):
        body = f"<h3>{n}. {title}</h3>" + P(*paras)
        return body + (aside("Use", ul(*use)) if use else "")
    entries.append(("00b. How to Run It", [
        ("How to Run It", "<h1>How to Run It: Step by Step</h1>" + P(
            "The whole adventure in the order you run it, with the Foundry pieces each step uses. The room journals have the detail; this is the thread through them. Each session also has a Session page (Campaign Companion) with the same plan in one paragraph.")
         + "<h2>Three habits for the whole adventure</h2>" + ol(
            "<strong>Doors move the party; you activate the scene.</strong> Walking onto a door tile moves the tokens and their players' view to the new scene. Then right-click that scene in the Scenes sidebar and choose <em>Activate</em>, so its ambience starts and it is the scene everyone sees.",
            "<strong>GM controls are hidden tiles.</strong> They sit in the top-left corner of a scene. Switch to the Tiles layer to see them; double-click one (from the Tokens layer) to fire it. The full list is in " + J("02. Automation (Monk's Active Tile Triggers)", "02. Automation") + ".",
            "<strong>Keep a tally sheet</strong> with three lists: the <em>visit count</em> (every Corridor scene entered, including repeats); <em>Misremembering</em> changes (who, what it was, what it is now); and <em>what each character left behind</em> in Room 3. Rooms 4 and 5 use all three.")
         + "<h2>Before the first session</h2>"
         + step(1, "Check the modules",
            "Required: Monk's Enhanced Journal, Campaign Companion, Monk's Active Tile Triggers. Recommended for sound: Ivan Duch's Music Packs, Michael Ghelfi, SoundFx Library, Adventure Music, and SoundBard. Without the sound packs the adventure runs silent but works.")
         + step(2, "Read three journals",
            "The overview, the rules (they are the theme: Misremembering, the Signature, no door leads back, leaving something behind), and the automation table.",
            use=[J("00. The Back Room: Adventure Overview"), J("01. Rules of the Back Room"), J("02. Automation (Monk's Active Tile Triggers)")])
         + step(3, "Prepare the people",
            f"Read {J('The Remnants')} and swap in your own table's first characters if this isn't the original table. For {A('barkeep')}, pick one secret detail from each character's backstory (Room 1, The Guardian). Decide which player is the latecomer, if any.",
            use=[J("The Remnants"), J("Cast"), "Each Remnant's Person page links its actor."])
         + step(4, "Set up sound",
            "Run the macro <em>The Back Room: set up SoundBard</em> once (Macro Directory: the folder icon at the left end of the hotbar). It fills two SoundBard banks: Corridors and People. The playlists Back Room: Music and Back Room: Stingers are there for anything else.",
            use=["Macro: The Back Room: set up SoundBard", "Playlists: Back Room: Ambience, Music, Stingers"])
         + step(5, "Set the opening",
            "Make the landing scene active and click <em>Activate</em> on it once so its music starts. Place the player tokens on the cots in The Back Room scene, out of sight until you need them.",
            use=["Scene: Welcome: The Stickit Inn (navigation: The Stickit Inn)", SC("backroom") + " (navigation: Upstairs)"])
         + "<h2>Session 1: Rooms 1–2, Corridor visits 1–2</h2>"
         + step(6, "While players arrive",
            "The landing scene is up and the Stickit Inn's music is playing. Nothing to do.",
            use=["Scene: Welcome: The Stickit Inn"])
         + step(7, "The evening at the Stickit Inn",
            f"Narrate the inn and the job, played completely straight: {A('stranger')} in the corner booth, three days to Thistlecross, forty gold. Show the handout. If you want a picture on screen, activate the vista of the common room for a moment. Start the music track <em>Session 1: A Cozy Tavern</em>.",
            use=[J("Room 1: The Back Room") + " (The Evening)", J("Handout: The Job"), "Scene: Vista: The Common Room (optional)"])
         + step(8, "Upstairs to the back room",
            f"Activate {SC('backroom')} and read the boxed text. If a player is late, run The Latecomer: their character arrives last, with Barnaby and a candle.",
            use=[SC("backroom"), J("Room 1: The Back Room") + " (The Latecomer)", J("Barnaby Stickit")])
         + step(9, "The night event",
            "Someone wakes; the lantern is lit. The stone in the corner has a hilt in it: when a player clicks the stone, that player gets the Toothless Key handout automatically. Barnaby comes down the stone stairs with a tray and asks them to go back to bed (The Guardian is not a fight).",
            use=[J("Room 1: The Back Room") + " (The Night Event, The Guardian)", J("Handout: The Toothless Key") + " (opens itself from the stone)", "SoundBard: The lantern lights itself"])
         + step(10, "Into the Corridors (visit 1)",
            "When a token steps onto the stairwell or the hayloft door, it is sent to a random Corridor scene. Activate that scene. Open the matching Corridor journal and use its visit-band cue (nothing yet at visits 1–2). Tick visit 1.",
            use=[J("The Corridor Pool: rules for every place"), "The Corridor journal for wherever they landed (Stairwell, Stable, Hallway, Clearing, Market Row, Crossing, Crossroads)", TB("pool") + " if you'd rather choose by roll"])
         + step(11, "Visit 2, and the way to Room 2",
            "Any door sends them somewhere else in the pool; tick visit 2. When you are ready for Room 2, double-click <em>GM: Reveal the X door → Room 2</em> in the scene they are in: the X appears on one door. Walking through it takes them to the Common Room.",
            use=["GM control (any Corridor scene): Reveal the X door → Room 2"])
         + step(12, "Room 2: the Common Room That Isn't",
            f"Activate {SC('common-room')}. Every patron is a role. Roll the drunk's joke once and repeat it forever. One patron is real: {A('remnant-fred')}. When he says his Signature, click his table: everyone gets the X Map. End the session on the map.",
            use=[SC("common-room"), J("Room 2: The Common Room That Isn't"), TB("jokes"), J("Fred the Fighter"), J("Handout: The X Map") + " (opens itself from Fred's table)", "SoundBard: POW! (Fred)"])
         + "<h2>Session 2: Corridor visits 3–6, Room 3</h2>"
         + step(13, "Back into the Corridors",
            "The common room's far door leads into the pool. Every arrival resets the fog and whispers you the band. Visits 3–4: sound (footsteps a half-beat late). Visits 5–6: a glimpse. Use each place's own cue first, then the generic table. Books on a shelf are half-page books. Each short rest in a Corridor costs a Misremembering.",
            use=["The Corridor journal for each place", TB("cues"), TB("books"), TB("misremember"), "SoundBard: Corridors bank", "Music: Corridors: Eerie Forest / Mystery"])
         + step(14, "The Cover (once, at visits 3–6)",
            "When the table needs a real fight, double-click <em>GM: Next door → The Cover</em> instead of letting them roll a door. The six monsters are frozen; stepping into a person-shaped gap wakes one (the tile whispers which). The cave's exit puts them back in the pool; nothing from the treasure pile survives it.",
            use=["GM control (any Corridor scene): Next door → The Cover", SC("cover-cavern"), J("The Cover"), "Music: The Cover: Dracona Mortis", "SoundBard: A monster wakes"])
         + step(15, "The Cellar (optional, visit 5+)",
            "The Cellar is never a random destination. From visit 5, use <em>GM: Next door → the Cellar</em> when you want it.",
            use=["GM control: Next door → the Cellar", J("Corridor: Cellar")])
         + step(16, "The way to Room 3",
            "Once they have the X Map, double-click <em>GM: Reveal the X door → Room 3</em> in the scene they are in. The X door takes them to the Corridor Between.",
            use=["GM control (any Corridor scene): Reveal the X door → Room 3"])
         + step(17, "Room 3: the Corridor Between",
            f"Activate {SC('corridor-between')}. Walking forward loops through six identical segments. Teach the rule with the clue ladder, one clue per pass. On the second pass {A('echo')} steps out of the far door (the tile reminds you). When someone sincerely leaves something behind, double-click <em>GM: Loop Break</em>, apply the Setback (one Misremembering), and ask whether anyone else wants to leave something too. Write down who left what. End the session here if you like: the next far door leads back into the Corridors.",
            use=[SC("corridor-between"), J("Room 3: The Corridor Between") + " (The Trick, Leaving Something Behind, The Setback &amp; the Echo)", J("The Echo"), "Macro: The Back Room: make the Echo of a character", TB("misremember"), "GM control: Loop Break"])
         + "<h2>Session 3: visit 7+, Room 4, Room 5</h2>"
         + step(18, "A Corridor at visit 7+",
            f"The far door of Room 3 puts them back in the pool, now at visit 7 or more: a Remnant is in the room. Place {A('remnant-strider')}'s token in this scene. He is not hostile; he wants the game to go on.",
            use=["The Corridor journal for the place", J("Strider"), J("The Remnants"), "SoundBard: Strider's arrow"])
         + step(19, "The way to Room 4",
            "Double-click <em>GM: Reveal the X door → Room 4</em>. The X door takes them to the Hoard.",
            use=["GM control (any Corridor scene): Reveal the X door → Room 4"])
         + step(20, "Room 4: the Hoard",
            f"Activate {SC('hoard')}. The reading room, fully arrived; the Remnants are waiting in the inner room. The fight starts when someone makes it start. Rorvik's chair is empty: at the top of round 2 he bursts in (“Sorry I'm late. What did I miss?”). The Remnants can't be beaten: they stand back up. At the top of round 3, spell out the stakes and double-click <em>GM: Open the way back</em>: the glass doors they came in by now lead out. Combat ends when a character walks through them without looking back.",
            use=[SC("hoard"), J("Room 4: The Hoard"), J("Fred the Fighter") + ", " + J("Thon") + ", " + J("Rorvik") + ", " + J("T. Morlock") + ", " + J("Strider"), J("Half-page Book 12: (Untitled)") + " (on the inner room's shelves)", "Music: It's All Led Up to This", "SoundBard: People bank (Rorvik bursts in)", "GM control: Open the way back"])
         + step(21, "Room 5: the Back Room, again",
            "The glass doors bring them back to The Back Room with the fog kept: they never left. The toothless key opens the door at the top of the stairs. Double-click <em>GM: Reveal</em> if you want to un-hide the Corridor scenes' real names. Offer the choice: leave or stay. Use the tally: the Misremembering list and what each of them left behind.",
            use=[SC("backroom"), J("Room 5: The Back Room, Again") + " (Dawn, The Choice: the landing door leaves, the hayloft door stays)", "GM control: Reveal (Room 5)", "Music: Room 5, dawn: Hope", "SoundBard: Remnants laughing, through the door"])
         + step(22, "The Last Word",
            "Out of character, after the choice: stop the ambience, start <em>The Last Word: Sad Strings</em> (Playlists: Back Room: Music), let it play a few bars, then put the dice down and read the closing to the players. Then stop.",
            use=[J("Room 5: The Back Room, Again") + " (The Last Word)", "Music: The Last Word: Sad Strings"])
         + "<h2>Afterwards</h2>" + P("To clear the adventure out of a world, run the macro <em>The Back Room: remove the adventure from this world</em>. It asks first, then deletes exactly what the adventure imported, itself included, and leaves your own documents alone."), 1),
    ]))

    # ------------------------------------------------------------------ 01 RULES (players' journal)
    entries.append(("01. Rules of the Back Room", [
        ("The Four Rules", "<h1>Rules of the Back Room</h1>" + P("Four rules carry the theme. They are for you, not the players: each one is discovered at the table — the first rewritten detail, the first door that opens on somewhere else, the first thing left behind. Say the rule aloud only after the table has met it.")
         + ol(f"<strong>Misremembering.</strong> Each short rest taken in a Corridor rewrites one small backstory detail of one character — a sibling's name, the colour of the house, which god. The GM changes it on the sheet and tells only the <em>other</em> players. Roll on {TB('misremember')} for what changes, or pick. Track every change (who, what it was, what it is now): Room 5 needs the list.",
              "<strong>The Signature.</strong> A Remnant's one remembered thing auto-succeeds once per round, no roll, no save. Everything else about it is blank. A finished character has a whole sheet; an unfinished one has one line.",
              "<strong>No door leads back.</strong> Every door in the Corridors sends the party somewhere else in the pool, never to the place they left. The one scripted exception is the Room 4 exit. The visit counter escalates what is in there with them.",
              "<strong>Leaving something behind is the only way forward.</strong> Something the player chooses and does not get back: an item set down, a slot spent on nothing, a story told once and never again. It is required once, to break the Room 3 loop; it is what the Remnants are made of; and it is the choice in Room 5. Never gate it on a keyword; reward the first sincere sacrifice the table invents. What counts, what doesn't, and the clues that teach it are in <em>Room 3: Leaving Something Behind</em>.")),
        ("The Corridors", "<h2>The Corridors</h2>" + P("The Corridors connect the five rooms and are where 'stuck' happens. Three rules run them.",
            "<strong>1. No door leads back.</strong> Every door the party uses sends them to a random Corridor scene from the pool, never the scene they left. In Foundry the door tiles do this; the GM only watches.",
            "<strong>2. Something is in here with you — by visit count.</strong> Track how many Corridor scenes the party has entered in total (keep a tally; on each arrival the tiles reset the fog and whisper you the band reminder, but they do not count).")
         + table(["Visits", "Cue", "Library layer"], [
            ["1–2", "Nothing. Furniture is wrong by one detail.", "A strip of green wainscoting on one wall."],
            ["3–4", "Sound: footsteps matching theirs, a half-beat late. A chair creaks in an empty room. (The Cover is reached from a pool door in this band or the next.)", "Doors become double wooden doors with glass panels; through one, bookshelves."],
            ["5–6", "Glimpse: a figure at the end of the corridor, gone when looked at directly. It is wearing something one of the players' first characters wore.", "A pointed arch; a stained-glass lantern-window on a landing; carpet on stone."],
            ["7+", "A Remnant is in the room. It is glad to see you. It does not attack.", "Timber ribs overhead. The room is half library now."]])
         + P("<strong>3. Rest costs memory, not hit points.</strong> Short rests work normally, but each one taken in a Corridor applies Rule 1 (Misremembering).",
             f"<strong>The pool (d8).</strong> Stairwell, stable, hallway of inn doors, campfire clearing, market row at closing, ferry crossing, crossroads at dusk, cellar (from visit 5 only). Roll on {TB('pool')} if the tiles are not doing it for you. One misremembered trope per place — never two; one is uncanny, two is a joke. The places are written up in <em>06. The Corridor Pool</em>."), 2),
        ("Remnants", "<h2>Remnants</h2>" + aside("GM prep (done for this table)", P("Each player was asked privately: <em>What was the first D&D character you ever played? Name, class, and the one thing everyone remembers about them.</em> Their answers are the five Remnants below. For a different table, ask the same question, don't say why, and rebuild the five from the answers; a player with no answer gets a fallback Remnant."))
         + P("<strong>Building a Remnant.</strong>") + ul(
            "Take the first character's class and build it at the party's level using the standard NPC approach, or a sidekick-style block if you'd rather keep it light.",
            "<strong>Max hit points.</strong> No rolling.",
            "<strong>The Signature.</strong> The one remembered thing becomes a feature that <em>always works</em>: once per round, it auto-succeeds, no roll, no save. The barbarian who was 'just really strong' always hits. The rogue who always rolled nat 20s on Stealth is simply not there until it chooses to be.",
            "<strong>Everything else is blank.</strong> The Remnant cannot answer any question about its past that isn't the Signature. It doesn't know its hometown. It knows it had a tragic backstory but not what it was.",
            "<strong>It never attacks first.</strong> It wants the game to continue; it will fight if that's what the party wants to do.",
            "<strong>It stands back up.</strong> At 0 HP it rises at the start of its next turn, in the pose it fell in, with full HP, and continues mid-sentence.",
            "<strong>It cannot leave a room through a door the party came through.</strong> That is the only hard limit on it, and it is the exit mechanic for Room 4.")
         + P("<strong>This table's Remnants.</strong>") + ul(
            f"{A('remnant-fred')}: his player isn't sure he ever played him; he was certainly a comic strip in a summer-camp newspaper, briefly. <em>Signature:</em> POW! (one hit a round lands, at maximum, lettered in the air). He is the Remnant in <strong>Room 2</strong>: the player who doesn't remember playing him is the one who will recognise him.",
            f"{A('remnant-thon')}: half-elf wizard with a Rod of Lordly Might. <em>Signature:</em> the rod is always the right tool. He remembers every button and no spells.",
            f"{A('remnant-rorvik')}: half-elven magic-user and thief, longsword, a hothead. <em>Signature:</em> always acts first. His player usually ran the game, so nobody remembers his adventures, including him.",
            f"{A('remnant-morlock')}: halfling thief-acrobat, 7th level. <em>Signature:</em> every acrobatic move works. He has his character sheet; nobody knows what the T. stands for.",
            f"{A('remnant-strider')}: a ranger built out of a beloved novel. <em>Signature:</em> knows the way. He is the Remnant who surfaces in a <strong>Corridor at visit 7+</strong>, and he offers to lead (always toward the Hoard).")
         + P(f"<strong>Fallback Remnants</strong> for a player who misses a session, or for another table: {A('remnant-rogue')}, {A('remnant-barbarian')}, {A('remnant-wizard')}.",
             "<strong>Using them.</strong> Fred appears in Room 2. Strider surfaces in the Corridors at visit 7+. All five are in Room 4. They are filed under People, never Monsters."), 2),
    ]))

    # ------------------------------------------------------------------ 02 ROOM 1
    entries.append(("02. Room 1: The Back Room", [
        ("The Evening", "<h1>Room 1: The Back Room</h1>" + P(
            "The Stickit Inn sits where the Kettle Pass road leaves the valley, and everyone for three days in any direction knows its cider: pressed in the yard, served cold in clay mugs, stronger than it tastes.",
            f"Play the cliché straight and let the players relax into it. {A('stranger')} in the corner booth has a job: ride guard on a lamp-oil wagon over the Kettle Pass to Thistlecross — three days, forty gold each, half now, leaving at first light (the handout <em>The Job</em> has the terms; swap in your own hook if your campaign already has one). The party takes it, buys provisions, and {A('barkeep')} leads them <strong>up the stairs</strong> from the common room to the storeroom over the kitchen, where they can sleep before the dawn road.")
         + aside("Why they're here", P("The adventure never says, on purpose: <em>you all meet in a tavern</em> is the oldest opening in the game, and playing it straight lets the players relax. If your table wants a reason, pick one (or roll a d4):")
            + ol("<strong>It's on the road.</strong> The inn sits where the Kettle Pass road leaves the valley: the last bed and hot meal before three days of high road. Anyone going over the pass stops here.",
                 "<strong>The cider.</strong> Everyone for three days in any direction knows the Stickit's cider. Someone in the party has been promising the others a mug for weeks.",
                 "<strong>The job brought them.</strong> Word has gone round the nearby towns: guards wanted for a wagon over the pass, ask at the Stickit Inn. They came to answer it.",
                 "<strong>Your own campaign.</strong> They are passing through on the way to wherever they were already going, and this is where night falls.")
            + P("For a table that started playing together long ago, the cliché is the point: this is how the first party met, too.", "What the party already knows about the road is in the handout <em>The Kettle Pass</em>: give it to them before the session, or let Barnaby and the stranger hand it out a line at a time."))
         + box("The barkeep goes up ahead of you with the lantern. A short landing at the top of the stairs, a door, and the storeroom: shelves of sacks and crocks, a cot for each of you already made up, one lantern on a hook, a small window over the yard. He sets the lantern down and tells you he'll have bread on at first light, and a jug of the house cider for the road.")
         + P("Describe it in loving, mundane detail. Let them count the cots. In the window, one pane of coloured glass that was not there at supper. Nobody comments on it; the GM does not either.")
         + aside("Keyed areas", ul("<strong>A1. The landing.</strong> Top of the common-room stairs. The door to the storeroom.",
                                   "<strong>A2. The cots.</strong> One per character, along the left wall, blankets turned down.",
                                   "<strong>A3. The shelves.</strong> Provisions, with the party's receipts tucked under the crocks. Behind the far unit, a door nobody has noticed yet.",
                                   "<strong>A4. The window.</strong> Small, four panes. One of them is coloured.",
                                   "<strong>A5. The stone.</strong> In the corner by the chest: a stone with a hilt in it."))),
        ("The Latecomer", "<h2>The Latecomer</h2>" + P(
            f"At this table one player usually arrives late (the player whose first character is {A('remnant-rorvik')}), and session one will be no different. Plan for it rather than around it: their character is the last guest of the night at the Stickit Inn, and the rest of the party meets them in the back room.")
         + box("Footsteps on the stairs, and a second light. Barnaby comes up with a candle and someone behind him, travel-stained, apologising. 'One more for the road, if you'll have them. Came in on the last of the light.' The last cot, you notice, was already made up.")
         + P("Run the introductions by lantern light, in character, as the others are bedding down; the newcomer has heard about the job from the stranger downstairs and is in. If the player arrives after the night event has begun, they are the one who wakes: they arrive in the dark, Barnaby is not with them, and the lantern is already lit. A late arrival is the best possible way into this adventure."), 2),
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
            "The Stickit Inn's common room. The fire is lit, the tables are full, and nobody is looking at you. In every booth, a hooded stranger. The barmaid is walking a slow circle between the tables with a tray and has not arrived at one. A drunk by the hearth is telling a joke to nobody.")
         + P("Every patron is a <em>role</em>: a hooded stranger in every booth, a quest-giver who repeats the hook word for word, a barmaid who walks in a circle and never arrives, a drunk who says the same line no matter how many times you talk to him. Guards at the door say there's nothing to see here. There's a lot to see here.")
         + aside("Keyed areas", ul("<strong>B1. The booths.</strong> A hooded stranger in each, offering the job in the same words.",
                                   "<strong>B2. The bar.</strong> Nobody behind it. Mugs of the house cider, full, every one the same pale gold. One is a different colour.",
                                   f"<strong>B3. The hearth.</strong> The drunk, and his one line: roll on {TB('jokes')} the first time anyone talks to him, then tell that same joke, word for word and with the same pause, every time after.",
                                   "<strong>B4. The door.</strong> Two guards. 'Nothing to see here.'",
                                   "<strong>B5. The stairs.</strong> Up to a landing that is not the landing they came down."))),
        ("The Puzzle", "<h2>The Puzzle</h2>" + P(
            f"One patron is not a role. It is the first <strong>Remnant</strong>, {A('remnant-fred')}: one player's first character, misremembered (and possibly never played at all; he was certainly a comic strip). It doesn't know it's in a tavern. It thinks it's mid-adventure and the party are old companions. The puzzle is social: figure out which patron is real, and get it to say the thing everyone remembers it for (its Signature). When it does, the room goes quiet and every role turns to look at the party.",
            "<strong>Three clues</strong>, so the table can't miss it:") + ol(
            "The Remnant is the only patron who asks the party a question.",
            "It is the only one whose cider is a different colour: red as wine, where every other mug in the room is pale gold.",
            "The player whose character it is will recognise it from the description before anyone else does — let that player sweat before they say so.")
         + P("<strong>Payoff.</strong> The Remnant gives them a map with an X. The X moves when nobody looks at it. It is pointing at the Corridors. Give the handout <em>The X Map</em>. From this moment the X door can appear in the Corridors (the GM's X-door tile)."), 2),
    ]))

    # ------------------------------------------------------------------ 04 ROOM 3
    entries.append(("04. Room 3: The Corridor Between", [
        ("The Trick", "<h1>Room 3: The Corridor Between</h1>" + box(
            "A corridor ten feet wide with a door at the far end. Torches lit ahead, dark behind. The door behind you is locked, and you can see the key for it hanging on a nail beside the far door.")
         + P("Two doors: the near one is locked and its key is behind the far one. The far one opens onto the same corridor, from the other end.",
             "<strong>The trick.</strong> Walking forward loops. In Foundry the loop is not a teleport: the map is a strip of identical segments and the party simply walks on (see Automation). Each pass is one step more library — ribs overhead, then the green paint, then the pointed arch at the far door — which reads as progress, and is: the corridor is going somewhere.",
             "<strong>Breaking it.</strong> The loop breaks on any sincere act of leaving something behind — a treasured item set down, a spell slot spent on nothing, a story a player tells about their first character and then agrees never to tell again. Don't gate it on a keyword; reward the first real sacrifice the table invents. When it breaks, the GM fires the Loop Break tile and the next far door is the exit. What counts, what doesn't, and how the table works it out are on the next page.")
         + aside("Segments", P("<strong>C1–C6.</strong> Six identical segments in a line. Each far door is a tile that lets the party into the next segment. Segment dressing ladders the library: C1 plain; C2 a scratch on the wall at hip height and a dropped coin; C3 green wainscoting; C4 a glass double door with a bookshelf behind; C5 a pointed arch; C6 ribs overhead. Attentive players notice the scratch at the same height and the coin back on the floor."))),
        ("Leaving Something Behind", "<h2>Leaving Something Behind</h2>" + P(
            "This is the one thing the adventure asks of the players, and it should feel like a choice, not a password. Here is how to judge it, and how they find out.")
         + "<h3>The test</h3>" + P("It counts when all three are true. When in doubt, ask the player one question: <em>“Is that for good?”</em> If the answer is yes, and it costs them to say it, it counts.")
         + ol("<strong>Chosen.</strong> The player decides, for their own character. Nobody can leave something behind on someone else's behalf.",
              "<strong>It costs.</strong> The character, or the player, will miss it. It is something they would otherwise use, carry, or tell.",
              "<strong>It stays.</strong> It is left in the corridor, and nobody goes back for it or gets it back later.")
         + "<h3>Counts</h3>" + ul(
              "<strong>A thing that matters.</strong> A named weapon, a holy symbol, an attuned magic item, a backstory keepsake (the ring, the letter, the father's sword), a real share of the party's gold. Set down on the floor and walked away from.",
              "<strong>Power spent on nothing.</strong> A spell slot of the character's highest level, or a once-a-day feature (Rage, Channel Divinity, Wild Shape, a Ki or Sorcery pool), spent into the empty corridor with no target and no effect. The player says aloud what they are giving up.",
              "<strong>A story told once.</strong> A player tells the table a real memory of their first character, or of an old session, and agrees never to tell it again. (The GM can keep it; it turns up in Room 4.)",
              "<strong>Part of who they are.</strong> A title, a vow, a nickname, a backstory detail. The player picks it and lets it go; apply it like Misremembering, except they chose it.")
         + "<h3>Doesn't count</h3>" + ul(
              "<strong>Junk.</strong> A torch, a copper piece, a ration, a rock. The corridor gives it back: it is lying on the floor of the next segment, in the same spot, like the coin.",
              "<strong>Anything taken back.</strong> Picked up again, fetched with Mage Hand, recovered later by any means. If they go back for it, the loop resumes.",
              "<strong>Loopholes.</strong> An illusion of an item, a conjured or summoned object, a decoy, a “loan”. The corridor is not fooled, and neither is anyone at the table.",
              "<strong>Resources spent for a reason.</strong> A spell cast at the Echo, a potion drunk to heal, a feature used to scout. That is play, not leaving.",
              "<strong>Someone else's sacrifice.</strong> An NPC's belongings, a familiar dismissed on another character's say-so, another player's item.",
              "<strong>Hit points or blood.</strong> Bodies heal. The Back Room does not take what comes back on its own; rests cost memory here, not hit points.")
         + "<h3>When it breaks</h3>" + P(
              "The first sincere act is enough: fire Loop Break. Then pause before anyone opens the far door. The corridor is quiet; the torches behind them have gone out. Ask whether anyone else wants to leave something too. Nobody has to, but each character who does gets the Room 5 boon tied to what they left. (The Echo, if it was fighting, vanished when the loop broke.) Note who left what: the Remnants in Room 4 have every one of those things, and Room 5 asks about them again.")
         + "<h3>How the players figure it out</h3>" + P(
              "Never tell them the rule. Let the corridor teach it, one clue per pass through the far door, and stop as soon as someone tries something.")
         + table(["Pass", "Clue"], [
              ["1", "Nothing but the loop. Let them test it: walk back, try the locked door, check for secret doors. Each segment is a little more library, which reads as progress."],
              ["2", "The scratch at hip height and the dropped coin are back, exactly as they were. Anything they dropped or used as a marker is back too. The corridor returns what nobody wanted. The Echo steps out of the far door: a copy of the character the corridor has taken least from, with no name and nothing in its hands."],
              ["3", "By the far door, a row of hooks that wasn't there before, each holding something a stranger left: a child's wooden sword, a wedding ring on a string, a folded letter with the wax unbroken, a dice bag. None of it can be taken; a hand passes through. One hook is empty for each character. (Narrate it; the hooks are not on the map.)"],
              ["4", "A voice through the far door, warm and familiar (a Remnant, though they don't know it yet): <em>“Everybody leaves something. That's how we got in here.”</em> Then laughter, and nothing."],
              ["5+", "Each character remembers, in their own way, a rule from childhood: nothing goes through for free. Tell each player privately what their character half-remembers paying to get past something once (a toll bridge, a ferry, a lost tooth under a pillow). If they still have not tried anything, let the Echo take a thing from the character it copies, and break the loop on that — the corridor has taken its due, and that character gets no boon in Room 5."],
         ])
         + aside("Things that seed it earlier", ul(
              "The Ferry crossing in the Corridors: a jetty with no water and no ferry, the toll post empty. People expect to pay the ferryman.",
              "The half-page book <em>On the Proper Keeping of Inns</em>: a free night is never free.",
              "Fred in Room 2 wears things that are not his: a ring, a scarf, a holy symbol from some other party. He doesn't know where they came from.",
              "The Remnants themselves are the answer, seen backwards: they are what people left behind."))),
        ("The Setback & the Echo", "<h2>The Setback</h2>" + P(
            f"Whatever was left behind, a Remnant now has. And the corridor has taken something it wasn't offered: one character's bond, ideal, or a named person from their backstory is now subtly different, and only the other players notice. Apply Misremembering to one character now, chosen by the GM, and tell the others ({TB('misremember')}: use 4, 11, 14 or 15, or reroll until one comes up). This is the point where misremembering stops being about the rooms and starts being about the party.")
         + "<h2>The Echo</h2>" + P(
            f"On the second pass through the far door, a blank-faced copy of one character steps out of it: {A('echo')}. It is that character with nothing given up and nothing left: a sheet with every number halved and no name. It is the fight that tells the table the corridor wants something from them.")
         + "<h3>Who it copies</h3>" + P(
            "The character the corridor has taken the least from. Look at your tally: the character with the <strong>fewest Misremembering changes</strong> so far. If that is a tie, pick among them the one whose player has held on hardest (the one who refused a rest, kept every item, never told a story about their past). Anyone who has already left something behind in this room is never chosen.")
         + "<h3>Setting it up in Foundry</h3>" + ol(
            "Before the session (or at the table), run the macro <em>The Back Room: make the Echo of a character</em> and pick the character. It makes a new actor, <em>The Echo of</em> that character: their token art tinted grey with no name, their size, speed and ability scores, and copies of their equipped weapons and their spells with every number halved (hit points, AC, attack bonuses, damage and healing, save DCs). The base Echo is left alone, so you can make another.",
            "Drag that actor onto the scene at the far door the party just came through. Its attacks and spells roll from its own sheet, already halved.",
            "No time for the macro? Use The Echo as it is (a 5th-level adventurer halved) and give its token the character's art.",
            "Roll initiative. The Echo acts immediately <em>after</em> the character it copies, every round.")
         + "<h3>Running it: it repeats their last turn</h3>" + ul(
            "<strong>Round 1.</strong> The Echo does nothing. It stands at the door in the pose the character is in, and moves when they move. Let the table look at it.",
            "<strong>Every round after.</strong> On its turn the Echo takes the copied character's previous turn again: it moves to the square the character started that turn in, and makes the same attacks, spells and actions at the same squares, with every number halved. It does not choose targets; it hits whatever is standing in those squares now: the character, an ally who moved in, or nothing.",
            "<strong>You only track one character.</strong> When the copied character finishes their turn, note what they did and which squares it touched. That is the Echo's next turn. A token marker or a quick drawing on each square helps.",
            "<strong>It copies everything.</strong> A heal heals whoever is in that square. A shove shoves. A Fireball comes back on the same point at half damage. If the character took the Dodge action, the Echo dodges. If they did nothing, it does nothing.",
            "<strong>It cannot be killed while the corridor loops.</strong> It never drops below 1 hit point. Damage still shows: let it crack and blur, but it stays standing.",
            "<strong>Doors don't help.</strong> If the party goes through the far door, the Echo steps out of the next far door at the start of the following round.")
         + "<h3>How it ends</h3>" + P(
            "Only when the loop breaks: the moment you fire Loop Break, the Echo stops where it stands and is not there a moment later. That is the point of the fight. The party cannot win it, so it pushes them to work out what the corridor wants. Watch for the copied player realising that every attack they make comes back at the party a round later. When they stop attacking, the Echo stops too, and the corridor goes very quiet: that is the best moment for the next clue on the ladder. And if the copied character is the one who leaves something behind, and spends their highest spell slot into the empty air, say, the Echo copies that too, into nothing, before it goes.")
         + aside("If the table is struggling", ul(
            "Half damage keeps it survivable, but if the party is in real trouble, have the Echo copy a turn the character spent healing or dodging.",
            "Point at the mirror: describe the Echo's swing as exactly the character's swing from a moment ago, same angle, same grunt. The player should feel it is theirs.",
            "Never let it drop a character to 0 more than once. It is pressure, not a killer.")), 2),
    ]))

    # ------------------------------------------------------------------ 05 ROOM 4
    entries.append(("05. Room 4: The Hoard", [
        ("The Reading Room", "<h1>Room 4: The Hoard</h1>" + box(
            "A dragon's hoard with no dragon. And the room is the upstairs reading room, fully arrived: pointed arches and dark timber ribs overhead, the stained-glass lantern in the ceiling, two tall stained-glass windows with dawn behind them, green wainscoting, armchairs. The hoard is the ring of armchairs round the low table, and on the table, where the coins should be, are dice — warm, as if they have just been rolled.")
         + P("The dark lord's tower, painted, hangs between the arches where a portrait would; it is the same size it has been from every window. At the far end, the inner glass-walled room with the double wooden doors: through the glass, bookshelves, and the Remnants, seated, waiting for the session to start.")
         + aside("Keyed areas", ul("<strong>D1. The glass doors.</strong> The party enters through them. They are the exit, later.",
                                   "<strong>D2. The armchairs.</strong> The hoard. Dice on the table, warm.",
                                   "<strong>D3. The portrait.</strong> The tower, between the arches.",
                                   "<strong>D4. The inner room.</strong> Bookshelves of half-page books. The Remnants, and one empty chair.",
                                   "<strong>D5. The windows.</strong> Dawn. The same dawn as Room 5."))),
        ("The Antagonist", "<h2>The Antagonist's Motive</h2>" + P(
            "The Remnants are here, the full first party, all but one: Rorvik's chair is empty. They have been waiting for the boss. They think the party <em>is</em> the boss, or the rescue, or the sequel — it changes mid-sentence. What they want is simple and sympathetic: for the session to not end. They were never given an ending; they are offering the party the same.")
         + "<h2>The Fight That Can't Be Won</h2>" + P(
            "Remnants have max HP and their Signature always works. Dropped to 0, a Remnant stands up at the start of its next turn in the same pose it fell in. Beating them rebuilds the room (the load-bearing boss, in reverse). Spell the stakes out at the top of round 3: the players should <em>understand</em> that winning is the loop.",
            f"<strong>Rorvik is late.</strong> {A('remnant-rorvik')} is not in the room when the fight begins. At the top of round 2 the inner room's double doors bang open and he strides in, longsword already out:")
         + box("'Sorry I'm late. What did I miss?'")
         + P("From that round on he acts first, every round, as if he had been there all along. (His player will know exactly why.)")
         + "<h2>How It Actually Ends</h2>" + P(
            "The glass double doors the party came in by (D1) now lead back the way they came — the first time in the adventure that's been true. Combat ends the moment a character walks through them without looking back. Remnants will not follow. They will call after the party by the players' real character names from Room 1, and then by the <em>first</em> characters' names, and then stop. The Room 4 Exit tile sends the party to Room 5."), 2),
    ]))

    # ------------------------------------------------------------------ 06 ROOM 5
    entries.append(("06. Room 5: The Back Room, Again", [
        ("Dawn", "<h1>Room 5: The Back Room, Again</h1>" + box(
            "The storeroom over the kitchen. Dawn light under the landing door, and through the small window — which is now, entirely, a stained-glass window — the colours of the reading room laid across the cots. The cots are made. The lantern is out. The stone in the corner has no hilt in it.")
         + P("This is the Room 1 scene with the fog <em>kept</em> and the same entry square: let Foundry tell them. The toothless key from Room 1 fits the door at the top of the stairs.",
             "<strong>The revelation.</strong> They never left. Say it plainly through the environment, not a monologue: provisions still on the shelf with the receipts the party paid for, the hooded stranger's voice rising from the common room below, ordinary morning noise, and under it, pages turning. Fire the GM <strong>Reveal</strong> tile now if you want the players to see the whole shape of it in the scene list.")),
        ("The Choice", "<h2>The Choice</h2>" + P(
            "Two doors, and each one is an answer. Nobody has to say the word <em>choice</em>: the room says it.")
         + ul("<strong>The landing door (A1): leave.</strong> The door at the top of the stairs is locked, and the toothless key from Room 1 turns in it. Beyond it, ordinary stairs, the right number of them, and the common room in the morning.",
              "<strong>The hayloft door (A3): stay.</strong> The second door, behind the shelves: the riddle door from the night. Through it, from the hayloft, the Remnants, laughing (SoundBard: <em>Remnants laughing, through the door</em>, or the Stingers playlist). It is the only time the riddle door does not ask its riddle. It says, quietly: <em>\u201cOh, it's you. Go on through. They kept your seats.\u201d</em>")
         + "<h3>Making it a real choice</h3>" + ul(
              "<strong>Each player chooses for their own character.</strong> Not a party vote. The party can split, and it is allowed to.",
              "<strong>Let each Remnant ask its own player.</strong> Through the loft door, one at a time, use their Room 4 lines (on their Person pages): Fred's \u201cSame time next week?\u201d, Strider's \u201cThe road can wait.\u201d Speak to the player, not the character.",
              "<strong>Put a real price on leaving.</strong> Read out the tally: every Misremembering change stays changed, every thing left behind in Room 3 stays left, and the Remnants will be gone. Leaving is the healthy choice, and it costs.",
              "<strong>Put a real gift in staying.</strong> Staying gives everything back: every changed detail is as it was, everything left behind in Room 3 is on the cot, the party is whole, and nobody ever has to say goodbye to anyone. Say so plainly. It is not a trick.",
              "<strong>Don't lean.</strong> No music cue, no meaningful look, no hint that one answer is right. Let the silence go on longer than is comfortable. The back room is warm; outside it is a cold morning and a long road.",
              "<strong>Make it physical.</strong> On three, each player puts a hand on the table (stay) or a die in the middle (leave). Or have each player move their token: to the landing door, or to the loft door.")
         + "<h3>If they leave</h3>" + box(
              "The key turns as if the lock had been waiting for it. The stairs down are wooden, and there are fourteen of them; you count. The common room smells of bread. Barnaby is behind the bar in his apron, wiping a mug that is already clean, and he looks up and says, \u201cThere they are. Bread's hot. Jug's by the door.\u201d",
              "In the corner booth, the stranger has his hood down. He is younger than you thought, and he is checking the straps on a pack. \u201cWagon's in the yard,\u201d he says. \u201cIf you're still coming.\u201d",
              "Outside, it is a cold, clear morning. The wagon smells of lamp oil and wet rope. The Kettle Pass road goes up into the hills exactly the way roads do, one bend at a time, and nobody has to count the bends.",
              "Somewhere behind you, an upstairs window catches the sun. Just glass. All four panes clear.")
         + P("Then the mechanics: each character who left keeps the changed details as they are now, gains a level, and gets one boon of your choice tied to what they left behind in Room 3 (a character who left a holy symbol finds their faith sits lighter and surer; one who spent a story finds people listen when they speak). The Remnants are gone. The toothless key is gone from every pocket.",
             "Any character who stayed is simply not at the bar in the morning. Barnaby sets out one fewer mug and does not say anything about it, and neither does anyone else.")
         + "<h3>If they stay</h3>" + box(
              "The hayloft is warm and full of lamplight, and there is a table up here that was never in any hayloft: a low table, and chairs round it, and the people you used to be already sitting down. Someone has rolled dice. They are still warm. There is a chair for each of you, and a character sheet on each chair, and the name at the top is the one you almost gave them.",
              "Nobody asks whether you are ready. Somebody says, \u201cRight. Where were we?\u201d, and nobody remembers, and it doesn't matter.")
         + P("The campaign ends here, and it is allowed to be a good ending. Every session is session one. Tell the players that in those words.")
         + "<h3>Then, The Last Word</h3>" + P(
              "When the last character has gone through a door, stop the scene's sound (Playlists sidebar: stop <em>Back Room: Ambience</em>) and start the track <em>The Last Word: Sad Strings</em> in the <em>Back Room: Music</em> playlist. Let it play for a few bars. Then put the dice down and read The Last Word.")
         + aside("The twist, for the GM only", P("The back room is still there, under every tavern the party ever starts in. Any future campaign at this table can open with the barkeep setting out a tray.")), 2),
        ("The Last Word", "<h2>The Last Word</h2>" + P("Whichever way the party chose, close the campaign out of character: put the dice down, look up from the screen, and say this to the players, not their characters. If the party stayed, it lands harder: the characters stay in the back room; the players go home.")
         + box("Over the years, this game has been our interstice: our liminal space. We pause our busy lives, the ones where we hurtle from one thing to the next, and make room around a table to weave stories about things that don't exist.",
               "After tonight it's back to the real world, and whatever the next destination is, good or bad.",
               "There have been times when being in the back room, playing this game, was better than real life. There have been times, I think, when all of us thought it might be better just to stay in that back room.",
               "But our time here is done now. Time to go back.")
         + P("Then stop. Don't recap, and don't explain the ending. Let the table sit with it, and let whoever wants to say their first character's name one last time say it."), 2),
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
              aside("The loft door is the riddle door", P("This place is entered from the hayloft above; the ladder down is the door into the stalls. The hayloft door — the one behind the shelves in Room 1 and the loft door in every copy — speaks, as the two guards of the old riddle, one who always tells the truth and one who always lies. There is only one door. It cannot get the riddle right, contradicts itself mid-riddle, apologises, starts again. It opens the moment anyone tells it which guard it is; either answer works; it is grateful. (It is on the way in, not in the room, so it is not a second wrongness.)"))
              + "<h3>The riddle door, in its own words</h3>" + P("Its voice comes from the wood, about head height: polite, earnest, and a little out of breath, like someone reading from a card they wrote years ago and can no longer read. Play it as two voices that keep collapsing into one.")
              + table(["When", "The door says"], [
                  ["Someone comes near", "\u201cHalt! Who goes\u2014 no. Sorry. Hello. You'll want to go through. Of course you will. There's a riddle. There is always a riddle.\u201d"],
                  ["Setting it up", "\u201cBefore you stand two doors. One leads onward, and one leads to certain\u2026 hm. Before you stands <em>a</em> door. One door. That's fine. That's fine. It still works.\u201d"],
                  ["The guards", "\u201cTwo guards watch the door. One always tells the truth. One always lies. I am\u2026 both of them. I am the guards. I'm the door <em>and</em> the guards. It's been a long night.\u201d"],
                  ["Trying again, in the truthful voice", "\u201cI always tell the truth.\u201d (Then, in the same voice, sadly:) \u201cThat was a lie.\u201d"],
                  ["Trying again, in the lying voice", "\u201cI always lie.\u201d (A pause.) \u201cWait. Then that\u2019s\u2026 no. Start again. Please let me start again.\u201d"],
                  ["The question it is meant to ask", "\u201cYou may ask me one question. Only one. Choose wis\u2014 oh, you could ask what the other guard would say. That\u2019s the clever one. That\u2019s the one everyone asks. I shouldn\u2019t have said that.\u201d"],
                  ["Asked what the other guard would say", "\u201cThe other guard would say\u2026 that I would say\u2026 that you should\u2026\u201d (A long silence.) \u201cI\u2019m so sorry. There isn\u2019t another guard. There\u2019s just me, and I don\u2019t remember which one I am.\u201d"],
                  ["Asked which door is safe", "\u201cThis one. It\u2019s the only one. Unless I\u2019m the liar. Am I the liar? Which one am I?\u201d"],
                  ["If they try to force it, pick it, or go round", "\u201cOh, please don\u2019t. It\u2019s not locked. It\u2019s just\u2026 I have to finish. I always have to finish.\u201d"],
                  ["Stuck: a hint, if the table needs one", "\u201cIf someone would just <em>tell</em> me which one I am\u2026 I\u2019d believe you. Either way. I\u2019d believe you.\u201d"],
                  ["Told it is the truthful guard", "\u201cThe truthful one. Yes. Yes, I think I was. Thank you. Thank you so much.\u201d (It opens.)"],
                  ["Told it is the lying guard", "\u201cThe liar. Oh. That\u2019s\u2026 actually that\u2019s a relief. At least I\u2019m <em>something</em>. Go on through.\u201d (It opens, and then, very quietly:) \u201cThat was the truth, by the way.\u201d"],
                  ["Told it is both, or neither", "\u201cBoth.\u201d (It thinks about it.) \u201cThat\u2019s the nicest thing anyone\u2019s said to me.\u201d (It opens.)"],
                  ["As they pass, every time after", "\u201cHalt! Who\u2014 oh, it\u2019s you. Go on. I remember you. I\u2019m the one who\u2026 I remember you.\u201d"],
              ])),
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
              [["3–4", "The fire crackles with the rhythm of someone's breathing."], ["5–6", "Figures dancing just outside the firelight who never look over."], ["7+", "A Remnant sitting at the fire with its hands out, warming nothing."]],
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
        place(8, "c8-cellar", "Cellar", "The Stickit Inn's cellar, cider barrels and all; the back room again.",
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
         + P("The monsters do not acknowledge the party. They keep fighting nobody, as they have since 1977. The thing in the room is busy; the party has to decide whether to interrupt it.",
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
            f"{A('remnant-fred')}, {A('remnant-thon')}, {A('remnant-rorvik')}, {A('remnant-morlock')}, {A('remnant-strider')} — this table's Remnants, the players' first characters.",
            f"{A('remnant-rogue')}, {A('remnant-barbarian')}, {A('remnant-wizard')} — the fallback Remnants, for an absent player or another table.",
            f"{A('echo')} — Room 3's blank-faced copy, built as a 5th-level character halved; swap in the mirrored character's own sheet if you have time, it plays as written if not.")
         + "<h2>Monsters</h2>" + ul(f"{A('dragon')}, {A('unicorn')}, {A('centaur')}, {A('troll')}, {A('roper')}, {A('owlbear')} — The Cover.")),
    ]))

    # ------------------------------------------------------------------ 10 HANDOUTS (split into one entry per page by build.py)
    entries.append(("10. Handouts", [
        ("Handout: The Job", "<h2>The Job</h2>" + P("<em>Wanted: four or five capable people to ride guard on a wagon of lamp oil from the Stickit Inn over the Kettle Pass to Thistlecross. Three days by the high road. Forty gold a head, twenty of it tonight, the rest from the chandler at Thistlecross on delivery. We leave at first light. Bring your own bedrolls; the wagon has room for packs. Ask for the one in the corner booth.</em>",
            "<em>The pass is quiet this time of year. The road is good. Nothing about this is a trick.</em>")),
        ("Handout: The Toothless Key", "<h2>The Toothless Key</h2>" + P("A long iron key, drawn from a stone in the corner of the storeroom. It has a bow, a shank, and no teeth at all. It opens nothing in the room you found it in.", "<em>Keep it.</em>")),
        ("Handout: The Kettle Pass", "<h2>The Kettle Pass</h2>" + P(
            "<em>What anyone in the valley could tell you, and what a traveller picks up over a mug at the Stickit Inn.</em>")
            + "<h3>The road</h3>" + ul(
                "The Kettle Pass is the only road over the hills between the valley and Thistlecross: three days by wagon, two on a good horse, one if you are a fool.",
                "It takes its name from the Kettle, a round, steep-sided basin near the top where the road runs along the rim. On cold mornings the basin fills with mist to the brim and steams like a pot on the hob.",
                "The road is old and well kept: stone-cobbled on the steep stretches, with mile-stones every mile and three way-shelters, a day apart, each with a roof, a fire-ring and a cord of wood that travellers are expected to replace.",
                "The Stickit Inn stands where the road leaves the valley floor. It is the last proper bed and hot meal before the pass, and the first after it. Nobody remembers it not being there.")
            + "<h3>The trade</h3>" + ul(
                "Thistlecross makes its living on wool, slate and lamp oil, and the oil goes over the pass in wagons all year. A chandler in Thistlecross, Old Wenna Marsh, buys every barrel the valley sends and pays on the nail.",
                "Wagons hire guards for the crossing as a matter of course. Usually the guards are bored. Being bored is the job.",
                "Stickit cider goes the other way: half the taverns in Thistlecross keep a barrel of it behind the bar and charge double.")
            + "<h3>The weather</h3>" + ul(
                "The pass is quiet in the late season, before the snow. After the first heavy snow it closes until spring, and nobody tries it.",
                "The mist in the Kettle can come up fast. The rule every carter learns from their mother: if you lose the road, stop, light a lamp, and wait. The road will be there when it clears. It always is.",
                "The wind across the top sounds like voices if you let it. Carters sing to drown it out, and every one of them has a song for it.")
            + "<h3>What people say</h3>" + ul(
                "There have been no bandits on the pass in living memory. There was a troll under the Kettle bridge once, in somebody's grandfather's day, and it was dealt with by four or five capable people nobody remembers the names of.",
                "Count the mile-stones as you pass them. Everybody does. Nobody can tell you why.",
                "The middle way-shelter has names carved into every beam, left by travellers over the years. It is lucky to add yours, and unlucky to look for your own.")),
        ("Handout: The X Map", "<h2>The X Map</h2>" + P("A map, drawn in a hand none of you recognise, of a place none of you have been. There is an X on it. The X marks the way out.", "<em>Do not look at the X for a moment. Now look again.</em>")),
    ]))

    return entries
