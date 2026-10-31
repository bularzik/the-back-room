# Brief: re-dress Back Room maps in Forgotten Adventures

You are re-dressing Dungeondraft maps for "The Back Room", a liminal-horror D&D adventure for Foundry VTT.
The user chose: **Forgotten Adventures art, full re-dress, brighter than a night scene**. The pilot map
`backroom-fa` is finished and approved in direction; match its quality and conventions.

## Before you start
1. Load these skills with the Skill tool and follow them: `battlemap-interiors` (or `battlemap-environments`
   for outdoor/cave maps), `battlemap-lighting-hierarchy`, `battlemap-material-language`,
   `battlemap-composition-audit`, `battlemap-visual-review`. The shared build loop is at
   `~/.claude/skills/_shared/build-loop.md` (read phases 3, 7, 8, 9).
2. Read each map's purpose in the design docs on the Mac (device_bash, repo at
   `$HOME/mnt/Claude/Projects/the-interstice`): `docs/the-back-room.md` (Rooms 1–5, The Cover) and
   `docs/corridor-pool.md` (the eight Corridor places, plus "Rules that apply to every place" and "The library steps").
   Never copy anything from `docs/reference/` into a map.
3. Read the map's entry in `tools/maps.json` (w, h in Foundry px at 100 px/tile; `rects`, `notes`, `start`).

## Hard constraints (the Foundry automation depends on them)
- Coordinates: Dungeondraft woxels = Foundry px × 2.56 (256 woxels per tile, 100 px per tile).
- Every `rects` entry is a Monk's Active Tile trigger. Keep each rect walkable and unobstructed; a door the
  rect belongs to must sit on/adjacent to it. If an existing door does not line up with its rect, MOVE THE
  DOOR to the rect (as the pilot did), never the rect.
- Keep the map size, the wall outline and door/window positions (except such alignment fixes). Same number
  of doors. `notes` and `start` must stay on open floor.
- Do not change the original maps. Work on a copy: `add_packs_to_map(campaign="BackRoom", map="<key>",
  new_map="<key>-fa", packs=["FA30DDXY"])` (it opens the copy).

## Art direction (set by the pilot)
- One art family: FA_Starter_Pack_v3.0 (pack id `FA30DDXY`), 323 objects. List them with
  `list_assets(pack="FA30DDXY", search="Asset Testing/", limit=500)`. Walls:
  `Wall_PlasterWood_Light_A1` (tavern/inn), `Wall_Stone_Slate_C` (stone), `Wall_Wood_Light_A` (stable/sheds),
  `Wall_StoneWood_Slate_Light_A`. Doors `portals/Door_Wood_Light_L_1x1.webp` (radius 128), windows
  `portals/Window_Frame_Wood_Light_A_1x1.webp`. Floors (Patterns): `Wooden_Flooring_C_Light`,
  `Large_Flagstone_A_02`, `Cobblestone_A_Dirt1`, `Cave_Floor_A`, `Dirt_A_01`. Terrain: Grass_A_03/09, Dirt_A/B,
  Rocky_Dirt, Large_Flagstone, Stone_Tiles, Water_Still_A_01, Cave_Floor_A. Wall shadow:
  `paths/ShadowPath_Half_B_40%.png` drawn along the wall loop at width 0.5.
- Ambient light **#a4a6b0** for interiors (approved "brighter" level). Outdoors at dusk/night choose a cool
  ambient that still reads at table zoom; daylight places use near-white. Every light has a visible emitter
  placed with it (`place_object(..., light={...})`). Light by role; leave quiet areas dimmer.
- Remove ALL old objects/lights (core assets, and any sci-fi pack pieces) — nothing from other packs remains.
- Furnish in clusters from an anchor; four dressing layers in hero/supporting rooms; fixtures square to
  walls, everything else jittered (scale 0.85–1.15, a few degrees). Use `arrange_objects` for along_wall /
  around / on_surface.

## Bridge quirks learned on the pilot
- `place_pattern` rotation is in RADIANS (1.5708 = quarter turn). Pattern/floor shapes cannot be deleted;
  place a new pattern over an old one at z -100 (later shapes draw on top). Fill the outside margin with
  `fill_terrain` so no core terrain shows.
- To restyle walls: delete the wall and its portals, `draw_wall(points, loop=True, asset=...)` on the same
  points, then `add_portal` each door/window again (doors radius 128). Run `validate_floorplan` (must be ok).
- `validate_placements` often flags against-wall pieces by canvas bounds; judge, nudge 10–20 woxels if real.
- `validate_scene` reports window/portal lights as "unexplained" (it matches object names only); acceptable
  when the emitter is a window or portal — say so.
- If screenshots come back blank white, stop and report: Dungeondraft needs a restart by the user.

## Lessons from batch A (verified in Dungeondraft)
- FA wall sconce (`Sconce_Orange_A_Lit_1x1`) has its wall bracket on the RIGHT at rotation 0: 270 on a north
  wall, 90 on a south wall (check east/west once).
- FA armchair faces UP at rotation 0 (opposite of the usual convention). Look at every FA family's facing once.
- FA fireplace base reads right at rotation 90 on a north wall; its chimney piece works as an exterior stack
  outside the wall at layer 700.
- FA has stairs only as Paths: `Stairs_Wood_Light_A_Path` + `Stairs_Railing_Wood_Light_A_Path`.
- `Large_Flagstone_A_02` pattern is greyscale: pass a colour or it comes out brown.
- Text labels read as big GM labels on the floor: don't add map text.
- **Library steps are content, not decoration.** `docs/corridor-pool.md` ("The library steps") and the
  Corridor places' text specify a library detail per scene copy (copy A/B/C differ by one step) and other
  per-place details. Repetition of base dressing is fine, but every detail the docs or journal text promise
  (keyed areas, clues, library steps, named props) must be on the map. Read `tools/journal.py` for the place's
  keyed areas before dressing. Where the three scene copies share one map, put copy A's library step on the
  map (that is what the original maps did) and say which step you placed.

## Lessons from batch B
- A coloured `place_pattern` at z -100 is safe (used for wainscoting). A thin pattern strip at z 700 preceded
  a Dungeondraft crash: don't place patterns above z 0.
- A window light placed just OUTSIDE the window throws an inward shaft. Keep its energy modest (≤0.6) or the
  shaft reads as a stage spotlight.
- FA couch faces up at rotation 0 (like the armchair); the fancy chair faces down. FA paper assets are tiny
  (scale >1 to read at token zoom).
- Save after the shell and after each dressed room, confirming each save.
- This table's Remnants (people the party meets; see tools/actors.py): Fred the Fighter (a fighter who may only
  have been a summer-camp comic strip; winged helmet), Thon (half-elf wizard with a Rod of Lordly Might),
  Rorvik (half-elven magic-user/thief, longsword, hothead), T. Morlock (halfling thief-acrobat; silver dagger,
  tightrope), Strider (ranger out of a beloved novel). Props that nod to "the first party" should nod to these.

## Corridor places: three copy variants (c1–c8 only)
Each Corridor place has three Foundry scene copies (a, b, c). Copy A = the place's base library step (see
its entry in docs/corridor-pool.md, usually 0); copy B = base + 1; copy C = base + 2 (the step table is in
"The library steps"). `build.py` uses a copy's own maps.json entry when it exists (`c1-stairwell-b`), else the
place's. So, after `<key>-fa` (copy A) is finished, saved and imported:
1. `add_packs_to_map(campaign="BackRoom", map="<key>-fa", new_map="<key>-b-fa", packs=["FA30DDXY"])` (a copy),
   add exactly ONE library step's details (keep everything else identical), validate, save.
2. Same again from `<key>-b-fa` to `<key>-c-fa` with the next step.
3. BEFORE importing a variant, create its maps.json entry by copying the place's rects, notes, start and
   darkness (otherwise the import has no trigger rects):
   `python3 -c "import json;p='tools/maps.json';m=json.load(open(p));b=m['<key>'];m.setdefault('<key>-b',{});[m['<key>-b'].__setitem__(f,b[f]) for f in ('notes','rects','start','darkness') if f in b];json.dump(m,open(p,'w'),indent=1)"`
   (check the file's existing indent first and match it), then
   `python3 tools/import_dd2vtt.py <key>-b dd2vtt/<key>-b-fa.dd2vtt`. The variant must keep the same walls,
   doors and rects; library steps are dressing (a door that becomes a glass double door is drawn over the
   existing portal, not a new portal).
4. Review jpgs for b and c too.

## Per map, in order
1. `add_packs_to_map` → `<key>-fa`. `checkpoint`. List portals/walls/objects/lights.
2. Plan in a few lines (purpose, hero/supporting/quiet zones, route between doors and trigger rects, focal light).
3. Shell: terrain, floor pattern, walls/portals restyled, `validate_floorplan` ok.
4. Dress cluster by cluster; light; `validate_placements` and `validate_scene`; fix findings.
5. Composition audit + visual review at whole-map and token zoom; at most three repairs.
6. `save_map` and confirm (`is_backup` false, `map_file` set).
7. `export_dd2vtt()` → `dd-transfer__dd_download(url, filename, sha256, dest_dir="~/Claude/Projects/the-interstice/dd2vtt", overwrite=true)`
   → on the Mac: `cd $HOME/mnt/Claude/Projects/the-interstice && python3 tools/import_dd2vtt.py <key> dd2vtt/<key>-fa.dd2vtt`.
   Then check the rects/notes/start are unchanged in tools/maps.json, and that wall count and door count match the dd2vtt.
8. Also `export_map(ppi=100, format="jpg", grid=False)` and `dd_download` it into `~/Claude/Projects/map-review/`.

## Report back
Per map: what the room is now (2–3 lines), door alignment changes (if any, with the rect name), validator
results quoted (`ok` values and anything you judged acceptable and why), path of the review jpg, and any
problem you could not fix. Do not commit to git, do not rebuild packs, do not touch Foundry.
