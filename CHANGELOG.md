# Changelog

All notable changes to The Back Room are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> Git tags (`v*`) are the source of truth for released versions — the committed `module.json` `version` intentionally lags and is patched at release time by the CI workflow, which also turns `[Unreleased]` into the release's section.

## [Unreleased]

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

[Unreleased]: https://github.com/bularzik/the-back-room/compare/v2.4.1...HEAD
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
