# The Back Room

A Backrooms-inspired liminal-horror adventure for **D&D 5e (2024 rules)**, 4–5 characters of levels 5–8, 2–3 sessions.
For **Foundry VTT v14** with **dnd5e 5.x+**.

The party meets in a tavern, played completely straight. They take the hook, buy provisions, and bed down in the storeroom over the kitchen before the dawn road. They never leave that room. Stairwells, stables, corridors and campsites — all the back room, misremembered — and in there with them, their own first characters, who want the game to go on forever.

**Two adventures in one module.** *The Back Room* is the original: random Corridor doors, Misremembering, the Echo. ***The Back Room: The Unfinished Fight*** is a second adventure built from the same maps, people and art, for five 7th-level characters over three sessions. It's a fixed road instead of a maze: the Common Room, a crossroads, a cellar and a stable, each with a puzzle and one of the players' first-ever characters in it. At the end of the road the first party asks for help to finish the fight on the cover of the 1977 Monster Manual, fought in three back-to-back waves with the first party at the players' side. Import one adventure or the other into a world, not both.

**Requires** (Foundry offers to install them):
- [Monk's Enhanced Journal](https://github.com/ironmonk108/monks-enhanced-journal) 14.01+ — every journal entry is a Place, Person, Encounter, Organization or Quest
- [Campaign Companion](https://github.com/bularzik/mej-campaign-companion) 0.26+ — the adventure's journal folder is a campaign with three prepared Sessions, a portal and a timeline
- [Monk's Active Tile Triggers](https://github.com/ironmonk108/monks-active-tiles) 14.01+ — the random Corridor doors, the X door, the Corridor Between loop and the GM controls

## Install

In Foundry's Setup screen: **Add-on Modules → Install Module**, paste this into **Manifest URL**, and click **Install**:

```
https://github.com/bularzik/the-back-room/releases/latest/download/module.json
```

Then, in your dnd5e world:
1. **Game Settings → Manage Modules**: enable *The Back Room* and its three dependencies.
2. **Compendium sidebar → The Back Room** folder: open **The Back Room (Adventure)** or **The Back Room: The Unfinished Fight (Adventure)** and click **Import Adventure**.
3. For The Back Room, read the journal **00. The Back Room: Adventure Overview**, then **02. Automation**. For The Unfinished Fight, read **00. The Unfinished Fight: Overview**, then **How to Run It: Step by Step**. Each adventure's campaign portal entry opens its Campaign Hub and three Sessions.

## Contents

### The Unfinished Fight

- 15 scenes: the route (Room 1, the Common Room, the Crossroads, the Cellar, the Stable, the Hoard, the Cover), a welcome scene and seven vistas
- 37 Monk's Active Tile Triggers tiles: every door goes to one place and back, the whole party moves together and the new scene becomes active, loop roads at the Crossroads and Stable, and GM controls for Night falls, Rorvik and the Cover's waves 2 and 3
- 25 actors: the Cover's monsters rebuilt as three waves (troll, roper and piercers; centaur captain, unicorn and outriders; owlbear, cubs and a red dragon), four provisions chests for the Cellar, and the people, with the five Remnants as allies
- 33 journals: an overview, a step-by-step GM guide, every scene, the people with their lines, sessions 1–3, four handouts, and The Last Word (a new closing and the original)

### The Back Room

- 29 scenes from 13 Dungeondraft maps: the five fixed rooms, The Cover's cavern, and eight Corridor places as three hidden scene copies each
- 360 Monk's Active Tile Triggers tiles: pool doors that never lead back, fog resets, the X door (one hidden twin per destination room), the Corridor Between's identical segments and Loop Break, the Hoard's way back, the Cover's six waking gaps, and GM control buttons
- 12 actors: the six monsters of The Cover, the Echo, three fallback Remnants, the Barkeep, the Hooded Stranger (as NPCs, never monsters)
- 35 journal entries as Enhanced Journal types: 13 Places, 6 Persons linked to their actors, 1 Encounter, 1 Organization, 1 Quest, guides, rules, Cast, 3 handouts (the job notice, the Toothless Key, the X Map), 3 Campaign Companion Sessions, the campaign portal and timeline
- 2 roll tables (the Corridor pool, generic cues) and 2 playlists (3 ambient loops, 3 stingers)

Maps are built in Dungeondraft; audio is synthesised; token portraits are painted with Stable Diffusion and masked by `tools/make_tokens.py`.

## Development

```
npm install
python3 tools/build.py   # tools/maps.json + journal.py + actors.py + matt.py → src/packs/the-back-room + module.json
python3 tools/build_unfinished.py   # *_unfinished.py → src/packs/the-back-room-unfinished (npm run build:packs runs both)
npm run build:packs      # compile src/packs/*.json into LevelDB packs/
npm run validate         # check every link, tile reference and asset path
npm run package          # build + validate + dist/module.zip
```

`CLAUDE.md` is the project brief and the record of what has been learned (Dungeondraft map workflow, the MATT and Enhanced Journal data shapes, how to deploy to a test world). `docs/the-back-room.md` is the design, `docs/corridor-pool.md` the Corridor spec. Maps are made in Dungeondraft through the Dungeondraft MCP bridge, exported as `.dd2vtt`, and imported with `tools/import_dd2vtt.py`.

## Releasing

Every push to `main` runs **Validate**. Record each user-facing change under `[Unreleased]` in `CHANGELOG.md` as you make it (Added / Changed / Fixed / Removed); every `npm run build:packs` warns if there are commits since the last tag and `[Unreleased]` is empty. To publish a new version, either create a GitHub release with a tag like `v2.1.0`, or run `npm run changelog:release -- 2.1.0`, commit and push to `main`: when a push changes `CHANGELOG.md` and its newest dated version has no tag yet, the **Release Module** workflow creates the tag and the release itself. Otherwise, create a GitHub release with a tag like `v2.1.0` (optionally run `npm run changelog:release -- 2.1.0` first and commit, to date the section in the repo too). The **Release Module** workflow compiles the packs, validates them, stamps `module.json` with the version and URLs, turns `[Unreleased]` into the release's section (it fails if there are no notes), sets the GitHub release notes from it, and attaches `module.json`, `module.zip` and `CHANGELOG.md` to the release. `module.json`'s `changelog` points at the latest release's `CHANGELOG.md`. Foundry picks up the update through the manifest URL above.
