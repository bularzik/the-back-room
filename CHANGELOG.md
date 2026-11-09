# Changelog

All notable changes to The Back Room are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Git tags (`v*`) are the source of truth for released versions — the committed `module.json` `version` intentionally lags and is patched at release time by the CI workflow, which also turns `[Unreleased]` into the release's section.

## [Unreleased]

## [2.5.5] - 2026-11-09

### Fixed
- **Handout pictures show.** The pictures for The Job, The Toothless Key and The X Map never loaded: the path to each image was written wrong. Each picture now sits at the top of its handout, above the text, and in the handout's Picture tab.

## [2.5.4] - 2026-11-09

### Fixed
- **Doors on the top edge of a map now work.** The Campfire Clearing's north path and the Crossroads' north road (in every copy, including the slot where the X door appears at the Crossroads) never fired, because Monk's Active Tile Triggers ignores a token that stops on the map's very edge. Both now sit one square in from the edge, and the arrival spot below each moved down to make room.
- **Arriving characters no longer land on a way out.** When the party came through a door, a character could be dropped onto another door's tile and leave again on their next step. Arrivals are now moved off any door tile.

## [2.5.3] - 2026-11-02

### Changed
- **Going through a door activates the new scene.** When the party moves to another scene through a Corridor door (or Room 1's night doors, Room 2's door, Room 3's exit, The Cover's door and exit, an X door or the Cellar control), that scene becomes the active scene: its ambience starts and everyone's view follows. The Hoard's exit is left to you, since characters walk out one at a time.

## [2.5.2] - 2026-11-02

### Fixed
- **Outdoor exits are visible.** The ways out of the Campfire Clearing, the Crossroads and the path into the Ferry Crossing had nothing on the map to mark them. Each now shows a free-standing open door frame with light spilling through it: the Corridors' doors, even outdoors.

## [2.5.1] - 2026-11-02

### Fixed
- **The party stays together in the Corridors.** Each character going through a Corridor door used to land somewhere different. Now the first one through a door takes the whole party, every player character on the scene, to one place. The same goes for Room 1's night doors, Room 2's door, Room 3's exit, The Cover's exit, the X doors and the Cellar control.
- Characters arriving through a door no longer land on the same square.

## [2.5.0] - 2026-11-01

### Added
- **Actors for the Common Room's roles:** the Barmaid, two Inn Guards, the Drunk, the Merchant and the Old Man, each with a portrait token, their one line, and a note that they never break role. They are placed in the Common Room.
- **The barmaid walks her circle.** With the optional Patrol module installed, she walks round the Common Room's middle table on her own whenever the GM is viewing the scene (Patrol's walking-figure button stops and starts her). Without Patrol she stands still and nothing else changes.
- **NPCs and monsters are placed on the maps.** Fred and three hooded strangers in the Common Room; the five Remnants round the inner room's table in the Hoard; the six monsters frozen in The Cover's tableau. People who arrive mid-scene are hidden tokens to reveal: Bartleby on the night stairs, the Echo in the Corridor Between, Rorvik in the Hoard, Strider beside the X door in every C copy of the Corridors.

## [2.4.2] - 2026-11-01

### Changed
- The barkeep is now **Bartleby Stickit**, Bart to his friends (was Barnaby). His Person page has a new link, so re-import the adventure.

### Added
- Bartleby used to be a scrivener. He isn't any more. He would prefer not to say why.

## [2.4.1] - 2026-11-01

### Added
- **Release notes.** This changelog ships in the module folder, so Big Bad Module Manager (BBMM) shows it to the GM on login after an update. It is also linked from Foundry's update check and becomes each GitHub release's notes.

## [2.4.0] - 2026-11-01

### Added
- **Macro: make the Echo of a character.** Pick a player character and it makes "The Echo of" them: their token art tinted grey with no name, their size, speed and ability scores, and copies of their equipped weapons and spells with hit points, AC, attack bonuses, damage, healing and save DCs halved. The base Echo is left alone.
- **Things They Say** on every Person page: lines for Barnaby, Kael, the five Remnants, the fallbacks and the Echo, each labelled with when to use it.
- **The riddle door's lines** (Corridor: Stable), from "Halt! Who goes— no. Sorry." to what it says when told which guard it is.
- **Handout: The Kettle Pass** — what the party already knows about the road, the trade, the weather and what people say.
- **Why they're here** (Room 1): four reasons the party is at the Stickit Inn.
- **Room 5: the choice as two doors.** The landing door leaves, the hayloft door stays; how to make it a real choice; read-aloud text for leaving and for staying; when to start *The Last Word: Sad Strings*.
- **Room 2:** every role's one line, the way out, and what happens if the party leaves without the map. **The X Map in play:** what the players see when they look at it, and revealing the X door only when nobody is looking.
- **Room 4:** how the fight starts ("Everybody roll initiative"), what each Remnant does on its turn, the round-3 stakes, and "Do you look back?"
- **Visit 7+:** Strider's encounter (he offers to lead; the X appears on his door) and what the other Remnants do in the Corridors.
- **Indoors to outdoors:** how to narrate crossing between Corridor places.
- The Cover: what happens afterwards.

### Changed
- **The library climbs.** The Corridor copy the party is in now follows the stage of the adventure: Room 1 leads to A copies (visits 1–2), Room 2 and The Cover to B copies (visits 3–6), Room 3 to C copies (visit 7+), and every Corridor door stays in its copy. Nothing to count or switch.
- **The Echo rewritten** to be runnable: it copies the character with the fewest Misremembering changes, acts right after them, and repeats their last turn with every number halved. It cannot be killed while the corridor loops.

### Fixed
- A Corridor door could lead to another copy of the place just left. It now never does.
- In Room 5 the stairwell and hayloft doors still led into the Corridors. They turn off when the party arrives from the Hoard.

## [2.3.0] - 2026-11-01

### Added
- **How to Run It: Step by Step** — a GM journal that walks the whole adventure in order, with the scenes, journals, tables, handouts, macros and GM controls each step uses.
- **Handout pictures** for The Job, The Toothless Key and The X Map.
- **Twelve half-page books**, each a short handout, and a d12 **Half-page Books** table.
- **Misremembering** table (d20 backstory details that change).
- **The Drunk's Joke** table (d12), for the drunk by the hearth in Room 2.
- **Room 3: Leaving Something Behind** — what counts, what doesn't, and the clue ladder that teaches it.
- Macro: **remove the adventure from this world**.

### Changed
- Room 3's exit now leads back into the Corridors (visit 7+, then the X door to Room 4), as the design intends, instead of straight to the Hoard.

### Fixed
- Journal headings, tables and links are readable in Monk's Enhanced Journal under Foundry's dark theme.

## [2.2.1] - 2026-11-01

### Fixed
- Foundry now offers to install all five recommended sound modules (each has an install link).

## [2.2.0] - 2026-11-01

### Added
- **Landing scene** ("Welcome: The Stickit Inn") for before the game starts.
- **Sound:** ambience for every scene and vista, a Back Room: Music playlist, and a macro that fills SoundBard with the adventure's cues.
- CC0 sounds made for the adventure: the ferry bell, pages turning, dice, cider poured, and the Remnants laughing through a door.
- Recommended modules: Ivan Duch's Music Packs, Michael Ghelfi, SoundFx Library, Adventure Music and SoundBard.

## [2.1.1] - 2026-10-31

### Removed
- The separate Bestiary compendium: the adventure's actors import with it.

## [2.1.0] - 2026-10-31

### Added
- This table's five Remnants: Fred the Fighter, Thon, Rorvik, T. Morlock and Strider.
- The latecomer (Room 1), Rorvik arriving late to the Hoard, and The Last Word.
- Vista scenes for the five rooms and the eight Corridor places.

### Changed
- NPCs have names; the inn is the Stickit Inn, famous for its cider.
- Person pages link their actors, and text links go to the Person pages.
- Every map re-dressed in Forgotten Adventures, with Corridor copy variants.
- Foundry darkness halved on every scene.

### Fixed
- Prepared-adventure and spoiler fixes from playtest feedback.

## [2.0.0] - 2026-10-27

### Added
- **The Back Room**: a new adventure, new maps and a new build pipeline.
- Journals as Monk's Enhanced Journal entries in a Campaign Companion campaign.

### Changed
- Monk's Active Tile Triggers automation verified in Foundry.

## [1.1.1] - 2026-10-03

### Fixed
- Packs are regenerated from the build script before compiling.

## [1.1.0] - 2026-10-03

### Added
- First release: Foundry module with Monk's Active Tile Triggers automation, CI validation and a release workflow.

[Unreleased]: https://github.com/bularzik/the-back-room/compare/v2.5.5...HEAD
[2.5.5]: https://github.com/bularzik/the-back-room/compare/v2.5.4...v2.5.5
[2.5.4]: https://github.com/bularzik/the-back-room/compare/v2.5.3...v2.5.4
[2.5.3]: https://github.com/bularzik/the-back-room/compare/v2.5.2...v2.5.3
[2.5.2]: https://github.com/bularzik/the-back-room/compare/v2.5.1...v2.5.2
[2.5.1]: https://github.com/bularzik/the-back-room/compare/v2.5.0...v2.5.1
[2.5.0]: https://github.com/bularzik/the-back-room/compare/v2.4.2...v2.5.0
[2.4.2]: https://github.com/bularzik/the-back-room/compare/v2.4.1...v2.4.2
[2.4.1]: https://github.com/bularzik/the-back-room/compare/v2.4.0...v2.4.1
[2.4.0]: https://github.com/bularzik/the-back-room/compare/v2.3.0...v2.4.0
[2.3.0]: https://github.com/bularzik/the-back-room/compare/v2.2.1...v2.3.0
[2.2.1]: https://github.com/bularzik/the-back-room/compare/v2.2.0...v2.2.1
[2.2.0]: https://github.com/bularzik/the-back-room/compare/v2.1.1...v2.2.0
[2.1.1]: https://github.com/bularzik/the-back-room/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/bularzik/the-back-room/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/bularzik/the-back-room/compare/v1.1.1...v2.0.0
[1.1.1]: https://github.com/bularzik/the-back-room/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/bularzik/the-back-room/releases/tag/v1.1.0
