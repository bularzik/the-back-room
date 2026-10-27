# The Back Room

A Backrooms-inspired liminal-horror adventure for **D&D 5e (2024 rules)**, 4–5 characters of levels 5–8, 2–3 sessions.
For **Foundry VTT v14** with **dnd5e 5.x+**.

The party meets in a tavern, played completely straight. They take the hook, buy provisions, and bed down in the storeroom over the kitchen before the dawn road. They never leave that room. Stairwells, stables, corridors and campsites — all the back room, misremembered — and in there with them, their own first characters, who want the game to go on forever.

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
2. **Compendium sidebar → The Back Room (Adventure)**: open it and click **Import Adventure**.
3. Read the journal **00. The Back Room: Adventure Overview**, then **02. Automation**. Open the campaign's portal entry (*The Back Room*) to reach the Campaign Hub and the three Sessions.

## Contents

- 29 scenes from 13 Dungeondraft maps: the five fixed rooms, The Cover's cavern, and eight Corridor places as three hidden scene copies each
- 360 Monk's Active Tile Triggers tiles: pool doors that never lead back, fog resets, the X door (one hidden twin per destination room), the Corridor Between's identical segments and Loop Break, the Hoard's way back, the Cover's six waking gaps, and GM control buttons
- 12 actors: the six monsters of The Cover, the Echo, three fallback Remnants, the Barkeep, the Hooded Stranger (as NPCs, never monsters)
- 36 journal entries as Enhanced Journal types: 13 Places, 6 Persons linked to their actors, 1 Encounter, 1 Organization, 1 Quest, guides, rules, Cast, 4 handouts, 3 Campaign Companion Sessions, the campaign portal and timeline
- 2 roll tables (the Corridor pool, generic cues) and 2 playlists (3 ambient loops, 3 stingers)

Maps are built in Dungeondraft; audio is synthesised; actor tokens use Foundry's core icons for now.

## Development

```
npm install
python3 tools/build.py   # tools/maps.json + journal.py + actors.py + matt.py → src/packs/*.json + module.json
npm run build:packs      # compile src/packs/*.json into LevelDB packs/
npm run validate         # check every link, tile reference and asset path
npm run package          # build + validate + dist/module.zip
```

`CLAUDE.md` is the project brief and the record of what has been learned (Dungeondraft map workflow, the MATT and Enhanced Journal data shapes, how to deploy to a test world). `docs/the-back-room.md` is the design, `docs/corridor-pool.md` the Corridor spec. Maps are made in Dungeondraft through the Dungeondraft MCP bridge, exported as `.dd2vtt`, and imported with `tools/import_dd2vtt.py`.

## Releasing

Every push to `main` runs **Validate**. To publish a new version, create a GitHub release with a tag like `v2.1.0`. The **Release Module** workflow compiles the packs, validates them, stamps `module.json` with the version and URLs, and attaches `module.json` and `module.zip` to the release. Foundry picks up the update through the manifest URL above.
