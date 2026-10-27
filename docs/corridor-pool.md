# The Corridor pool — scene spec

This is the specification the eight Corridor maps are built from. Where it disagrees
with the pool list in `the-back-room.md`, this file wins. Raw trope material is in
`tropes.md`; the rules the Corridors run on (no door leads back, the visit counter,
rest costs memory, the X door) are in the design doc and are not repeated here.

## Rules that apply to every place

- **One trope, one wrongness.** Each place is one in-between place from the trope
  lists with exactly one thing wrong. Never two — one is uncanny, two is a joke.
- **Three copies.** Each place is imported as three Foundry scenes (A, B, C), same map,
  hidden from the navigation bar, all named with the place's bland name. Copy B is one
  step more library than A, copy C one more than B. The library steps are the only
  difference between copies; the wrongness is in all three.
- **Every book is a half-page book.** Wherever the library layer puts a book or a
  shelf, every volume is one half-page long. This is a global rule of the library
  layer, not a place's trope.
- **Entry doors.** Each map has two or three doors. The random-door tile uses all of
  them as exits; arrivals are placed inside whichever door the GM's tile chose, so a
  revisit can start from a different door. One door per scene is the **X door** slot:
  it is a plain pool door until the progression condition is met, then the X appears
  on it (a tile swaps the door texture) and it leads to the next fixed room.
- **Cue overlays by visit band** (from the design doc): 1–2 nothing; 3–4 sound; 5–6
  glimpse; 7+ a Remnant in the room. Place-specific versions are listed below; the
  generic ones (footsteps a half-beat late; a figure at the end of the corridor) apply
  anywhere.
- **Darkness** 0.6–0.8 on every Corridor scene; one or two light sources at most.
  Small vision is part of the concealment.
- **Size.** Small: 12×10 to 16×14 squares. These are places to pass through, not explore.

## The library steps

Step 0 is the place as it is. Each copy adds one step; Room 3's segments and the
visit-band cue table use the same ladder.

| Step | Detail |
| --- | --- |
| 1 | A strip of green-painted wainscoting on one wall, chair-rail height. |
| 2 | A door (or the door) is now a double wooden door with glass panels; through the glass, a bookshelf. |
| 3 | A pointed arch where a square frame was; a small stained-glass lantern-window high in a wall; carpet over stone or dirt. |
| 4 | Dark timber ribs overhead, meeting in a point. The room is half library now. |

Copy A = the place's base step (0 for most; see each entry). Copy B = base + 1.
Copy C = base + 2.

## The eight places

### 1. Stairwell — `c1-stairwell`

- **Trope.** The dungeon stair; the inn's back stairs.
- **Wrongness.** The steps go *down* and arrive one floor *up*. Three flights, two
  landings; the party descends and comes out above where they started, every time.
- **Map.** A stone stairwell in section-as-plan: three flights around a square well,
  two landings. Entry doors: bottom (arrival), top (arrival), one landing door.
  14×10.
- **Library base step.** 0. (Its copies: B = wainscoting on the landing walls;
  C = the landing door becomes the glass double door, bookshelf behind it.)
- **Cues.** 3–4: a footstep on the flight above, matching the last step someone took.
  5–6: a figure on the landing above, gone when the party arrives there. 7+: a
  Remnant sitting on a step, delighted.
- **Dressing line.** One half-page book on each landing, face down, as if someone
  stepped out for a moment.

### 2. Stable — `c2-stable`

- **Trope.** The party's mounts; the stable behind the inn.
- **Wrongness.** The horses face the wall. They are the party's own mounts, saddled —
  the ones they never bought.
- **The loft door (its one extra: the riddle door).** This place is entered from the
  hayloft above; the ladder down is the door into the stalls. The hayloft door — the one
  behind the shelves in Room 1 and the loft door in every copy — is the **riddle door**:
  it speaks, as the two guards of the old riddle, one who always tells the truth and one
  who always lies. There is only one door. It cannot get the riddle right, contradicts
  itself mid-riddle, apologises, starts again. It opens the moment anyone tells it which
  guard it is; either answer works; it is grateful. (The riddle door is the Stable's
  trope-dressing and not a second wrongness: it is on the way in, not in the room.)
- **Map.** Hayloft platform along one side (arrival from the loft door), ladder down,
  four stalls, a yard door, a tack-room door. Entry doors: loft door, yard door, tack
  door. 16×12.
- **Library base step.** 0.
- **Cues.** 3–4: a horse shifts its weight; none of them has moved. 5–6: a saddle on the
  rail that fits a character who has never ridden. 7+: a Remnant brushing a horse that
  is facing the wall.
- **Dressing line.** The mounts' names are on the stall doors, in the players' own
  handwriting.

### 3. Hallway of inn doors — `c3-inn-hallway`

- **Trope.** The inn's upstairs corridor of guest rooms.
- **Wrongness.** Identical doors, every one numbered with the same number. One is ajar:
  inside, a made cot with someone's pack on it. The inn has beds and nobody has ever
  slept in one — nobody here eats, sleeps, or was ever a child.
- **Map.** A straight corridor, six doors a side, a window at one end, a stair-head at
  the other. Entry doors: the stair-head, the far-end door, the ajar room (it has a
  second door). 16×8.
- **Library base step.** 1 (it already has the wainscoting: inn corridors do). So
  B = glass double doors, C = pointed arches over them.
- **Cues.** 3–4: a door closes somewhere behind the party; all the doors are as they
  were. 5–6: through the ajar door, the pack on the cot is one of theirs. 7+: a Remnant
  in the ajar room, sitting on the cot, asking if this is their room.
- **Dressing line.** The number on every door is the number of the room the players
  played in upstairs at the library, if they remember it; otherwise 2.

### 4. Campfire clearing — `c4-campfire`

- **Trope.** The campsite; the one place every TTRPG assumes is safe.
- **Wrongness.** The fire gives no heat. A bedroll is already slept in, still warm.
  Anyone who rests here wakes at full hit points, every wound healed overnight — and
  the misremembering rule (Mechanic 1) takes its due.
- **Map.** A clearing ringed by trees, fire at the centre, three bedrolls, a log, a
  stream edge. "Doors" are gaps in the trees: three paths out. 14×14.
- **Library base step.** 0. (B: the log is a bench with green wainscoting behind it,
  against a tree; C: a glass double door standing free between two trunks, a shelf
  behind it.)
- **Cues.** 3–4: the fire crackles with the rhythm of someone's breathing. 5–6: figures
  dancing just outside the firelight who never look over (the dryads this table
  remembers). 7+: a Remnant sitting at the fire with its hands out, warming nothing.
- **Dressing line.** The bedroll that is already slept in has a character's initials
  worked into the lining.

### 5. Market row at closing — `c5-market`

- **Trope.** The shopping trip; the potion seller.
- **Wrongness.** The stalls are being shuttered by nobody. The potion stall's labels
  are every one almost a word (HEALNG, MANNA, CURE LIHGT); the potions are all red.
- **Map.** A short street of six stalls, awnings half down, a well, an arch at each end.
  Entry doors: the two arches and the back of one stall. 16×10.
- **Library base step.** 0.
- **Cues.** 3–4: a shutter comes down on an empty stall as the party passes it. 5–6: the
  stallholder's chair is warm. 7+: a Remnant behind the potion stall, open for business,
  no idea what anything costs.
- **Dressing line.** The potions work. Nobody can read which one they drank.

### 6. Ferry crossing — `c6-ferry`

- **Trope.** The boatman; the river that must be crossed.
- **Wrongness.** A jetty, a lantern, no water and no ferry. The sound of a waterfall,
  close, with no waterfall. A bell on a post: ring it and it is answered from behind the
  party.
- **Map.** A jetty running out over a dry riverbed, a boathouse, a path in through trees.
  Entry doors: the path, the boathouse door, the far end of the jetty (a door standing
  on the last plank). 16×12.
- **Library base step.** 0.
- **Cues.** 3–4: the waterfall sound stops when someone speaks, resumes when they stop.
  5–6: a lantern on the far bank that was not lit. 7+: a Remnant on the jetty with a
  pole, waiting for the water.
- **Dressing line.** Under the jetty, where the water should be, a treasure chest. It
  has not been opened because nobody could get to it. It is right there.

### 7. Crossroads at dusk — `c7-crossroads`

- **Trope.** The signpost; the road the party sets out on.
- **Wrongness.** Every arm of the signpost points the same way, to a town with the
  party's home town's name spelled almost right. The light never finishes going.
- **Map.** Four roads meeting, a signpost, a milestone, a shrine, a verge with a
  stopped cart. "Doors": the four roads. 16×16.
- **Library base step.** 0.
- **Cues.** 1–2 onward: the roads are busy — every traveller is an adventuring party,
  not one farmer or merchant among them, all heading the way the arms point, and every
  party has its one member in the genre's impractical armour, whatever their race or
  number of legs. None of them stop. 3–4: a party passes whose rear guard has a character's
  walk. 5–6: a party passes going the other way; nobody looks. 7+: a Remnant leaning on
  the signpost, waiting for its party, which is any party.
- **Dressing line.** The milestone gives the distance to the town as a number that
  changes each time it is read, and is never smaller.

### 8. Cellar — `c8-cellar`

- **Trope.** The tavern cellar; the back room again.
- **Wrongness.** It is the back room — Room 1's storeroom — seen from the wrong angle:
  below it, the same shelves from underneath, the same cots' outlines in the boards
  overhead. The provisions chest is breathing.
- **Appears from visit 5 only.** Never in the pool before then.
- **Map.** A cellar the exact footprint of Room 1, casks, the chest, a trap in the
  ceiling (the storeroom floor), a coal chute, a stair. Entry doors: the stair, the
  chute, the ceiling trap (arrival only). 12×10.
- **Library base step.** 2 (the cellar's shelving is already library shelving, every
  book a half page). B = step 3, C = step 4: by copy C the cellar's ribs meet in a point.
- **Cues.** 5–6: footsteps overhead, in the storeroom, in the party's own rhythm. 7+: a
  Remnant asleep on the chest, which is breathing in time with it.
- **Dressing line.** The receipts for the party's provisions are nailed to a cask.

## Not placed

- *The wise old wizard mid-sentence forever* — a person, not furniture, and every place
  already has its one trope. Keep for Room 2's roles if a slot opens.
- Everything else left in `tropes.md` stays there (see the design-doc review of Oct 26).

## Build notes

- Eight Dungeondraft maps in campaign `BackRoom`, named `c1-stairwell` … `c8-cellar`.
- Export each once; `tools/import_dd2vtt.py` imports it under `c1-stairwell-a/-b/-c`
  (copies share the image; only the `name`, `darkness` and the copy's library-step
  dressing differ, and dressing is a tile overlay or a note, not a separate image).
- The X door is the same door in every copy of a place.
