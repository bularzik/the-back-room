"""Build check: no tile that a party arrives on (a cross-scene teleport destination, or a same-scene loop landing) may
sit within 2 squares of a door tile (any tile that teleports) on the same scene. MATT spreads an arriving party over the
neighbouring squares, ignoring walls; a door tile there sends them straight on. Exits 1 on any violation."""
import json, sys, re
def tiles_by_uuid(adv):
    T = {}
    for s in adv['scenes']:
        for t in s['tiles']:
            T[f"Scene.{s['_id']}.Tile.{t['_id']}"] = (s, t)
    return T
def gap(a, b):  # squares of clearance between two rects (0 = touching/overlapping)
    ax0, ay0, ax1, ay1 = a['x'], a['y'], a['x']+a['width'], a['y']+a['height']
    bx0, by0, bx1, by1 = b['x'], b['y'], b['x']+b['width'], b['y']+b['height']
    dx = max(bx0-ax1, ax0-bx1, 0); dy = max(by0-ay1, ay0-by1, 0)
    return max(dx, dy)/100
total = 0
for pack in sys.argv[1:]:
    adv = json.load(open(f'src/packs/{pack}/{pack}.json')); T = tiles_by_uuid(adv)
    dests = set()
    for s in adv['scenes']:
        for t in s['tiles']:
            for a in t['flags']['monks-active-tiles']['actions']:
                if a['action'] == 'teleport' and (a['data'].get('deletesource') or a['data'].get('entity', {}).get('id') == 'players'):   # party arrivals; per-token steps along one scene (the Corridor Between) don't spread
                    locs = a['data']['location']; locs = locs if isinstance(locs, list) else [locs]
                    for l in locs: dests.add(l['id'])
    bad = 0
    for u in sorted(dests):
        if u not in T: print('MISSING', u); continue
        s, d = T[u]
        for t in s['tiles']:
            f = t['flags']['monks-active-tiles']
            if t['_id'] == d['_id'] or not any(a['action'] == 'teleport' for a in f['actions']): continue
            if f.get('trigger') == 'dblclick': continue
            g = gap(d, t)
            if g < 2:
                bad += 1; print(f"{pack} | {s['name']} | arrival '{d['flags']['monks-active-tiles']['name'][:40]}' {d['x']},{d['y']} -> {g:.1f} sq from '{f['name'][:45]}' {t['x']},{t['y']} active={f['active']}")
    print(f'{pack}: {len(dests)} arrival spots, {bad} too close to a door tile')
    total += bad
sys.exit(1 if total else 0)
