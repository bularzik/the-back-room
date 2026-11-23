"""Keep every arrival spot at least CLEAR squares away from every door tile on its map.

Monk's Active Tile Triggers drops the first arriving token on the arrival tile and spreads the rest of the party
over the squares around it, without looking at walls. If one of those squares is a door tile, that character is
teleported straight on (seen at the table in 2.6.1: five characters bouncing between the Cellar and the Stable).
A clearance of 2 squares keeps a party of up to 8 on safe ground.

Moves arrive*/landing/mouth/stairs rects in tools/maps.json to the nearest spot that is clear of every door-type
rect, crosses no wall, stays in the same room as before (the move itself crosses no wall), and doesn't touch the
map's top or left edge (MATT ignores a token stopping at x or y = 0). Prints what it moved; --check only reports.
"""
import json, sys, os
CLEAR = 2            # squares between an arrival rect and any door rect
DOORS = ("door1", "door2", "door3", "doors", "xdoor", "stairwell", "loft", "exit", "seg1", "seg2", "seg3", "seg4", "seg5", "seg6")
ARRIVALS = ("arrive", "arrive1", "arrive2", "arrive3", "landing", "mouth", "stairs")
SKIP = {"corridor-between"}   # its arrivals are same-scene markers (no token is created there)

def gap(a, b):
    ax0, ay0, ax1, ay1 = a[0], a[1], a[0] + a[2], a[1] + a[3]
    bx0, by0, bx1, by1 = b[0], b[1], b[0] + b[2], b[1] + b[3]
    return max(bx0 - ax1, ax0 - bx1, by0 - ay1, ay0 - by1, 0) / 100
def seg_x(p1, p2, p3, p4):
    o = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2, d3, d4 = o(p3, p4, p1), o(p3, p4, p2), o(p1, p2, p3), o(p1, p2, p4)
    return d1 * d2 < 0 and d3 * d4 < 0
def rect_hits_wall(r, walls):
    x, y, w, h = r[0] + 3, r[1] + 3, r[2] - 6, r[3] - 6
    edges = [((x, y), (x + w, y)), ((x + w, y), (x + w, y + h)), ((x + w, y + h), (x, y + h)), ((x, y + h), (x, y))]
    for wl in walls:
        c = wl["c"]; p, q = (c[0], c[1]), (c[2], c[3])
        if any(seg_x(a, b, p, q) for a, b in edges): return True
        if x < c[0] < x + w and y < c[1] < y + h: return True
    return False
def path_hits_wall(a, b, walls):
    pa = (a[0] + a[2] / 2, a[1] + a[3] / 2); pb = (b[0] + b[2] / 2, b[1] + b[3] / 2)
    return any(seg_x(pa, pb, (w["c"][0], w["c"][1]), (w["c"][2], w["c"][3])) for w in walls if not w.get("door"))
def ok(r, doors, walls, W, H, orig):
    if r[0] < 100 or r[1] < 100 or r[0] + r[2] > W - 0 or r[1] + r[3] > H - 0: return False
    if any(gap(r, d) < CLEAR for d in doors): return False
    return not rect_hits_wall(r, walls) and not path_hits_wall(orig, r, walls)

def fix(maps, check=False):
    moved, stuck = [], []
    for key, e in maps.items():
        if key in SKIP: continue
        R = e.get("rects", {}); walls = e.get("walls", [])
        doors = [R[n] for n in DOORS if isinstance(R.get(n), list)]
        for n in ARRIVALS:
            if n not in R: continue
            r = R[n]
            if ok(r, doors, walls, e["w"], e["h"], r): continue
            if check: stuck.append((key, n, r)); continue
            best = None
            for rad in range(1, 9):
                for dx in range(-rad, rad + 1):
                    for dy in range(-rad, rad + 1):
                        if max(abs(dx), abs(dy)) != rad: continue
                        c = [r[0] + dx * 100, r[1] + dy * 100, r[2], r[3]]
                        if ok(c, doors, walls, e["w"], e["h"], r):
                            d = dx * dx + dy * dy
                            if best is None or d < best[0]: best = (d, c)
                if best: break
            if best: moved.append((key, n, list(r), best[1])); R[n] = best[1]
            else: stuck.append((key, n, r))
    return moved, stuck

if __name__ == "__main__":
    p = os.path.join(os.path.dirname(__file__), "maps.json")
    maps = json.load(open(p)); check = "--check" in sys.argv
    moved, stuck = fix(maps, check)
    for k, n, a, b in moved: print(f"moved {k}.{n}: {a[:2]} -> {b[:2]}")
    for k, n, r in stuck: print(f"{'TOO CLOSE' if check else 'NO SPOT'} {k}.{n} {r}")
    if moved and not check: open(p, "w").write(json.dumps(maps, indent=1) + "\n")
    sys.exit(1 if stuck else 0)
