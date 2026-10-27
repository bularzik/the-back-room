#!/usr/bin/env python3
"""Turn a Dungeondraft Universal VTT export (.dd2vtt) into a scene entry for tools/maps.json.

    python3 tools/import_dd2vtt.py <key> <file.dd2vtt> [--darkness 0.5] [--name "Scene Name"]

Writes maps/<key>.webp and maps/thumb-<key>.webp, then adds or updates `key` in
tools/maps.json with the walls, doors and lights from the export, converted to
Foundry pixel coordinates (100 px per grid square). Fields the export does not
carry (notes, rects, start, darkness) are kept from any existing entry, so
re-importing a revised map does not lose the keyed notes.

Walls use the same shape build.py already consumes:
    {"c": [x0, y0, x1, y1], "move": 20, "sight": 20, "light": 20, "sound": 20, "door": 0|1, "ds": 0|1}
Lights:
    {"x", "y", "dim", "bright", "color", "alpha", "anim"}   (dim/bright in feet, 5 ft per square)

Requires Pillow. Run from the repo root.
"""
import argparse, base64, io, json, os, sys

try:
    from PIL import Image
except ImportError:
    sys.exit("pip install pillow")

PPI = 100          # Foundry px per square, matching build.py's grid size
FT_PER_SQUARE = 5
MAPS_JSON = "tools/maps.json"
OUT_DIR = "maps"
THUMB_W = 300


def px(v):
    return int(round(v * PPI))


def color_hex(c):
    """dd2vtt colours are 'rrggbb' or 'aarrggbb'; Foundry wants '#rrggbb'."""
    c = (c or "ffffff").lstrip("#")
    if len(c) == 8:
        c = c[2:]
    return "#" + c.lower()


def convert(dd, key):
    ppg = dd["resolution"]["pixels_per_grid"]
    size = dd["resolution"]["map_size"]
    origin = dd["resolution"].get("map_origin", {"x": 0, "y": 0})
    ox, oy = origin["x"], origin["y"]

    def P(pt):
        return px(pt["x"] - ox), px(pt["y"] - oy)

    walls = []
    for line in dd.get("line_of_sight", []) + dd.get("objects_line_of_sight", []):
        pts = [P(p) for p in line]
        for a, b in zip(pts, pts[1:]):
            if a == b:
                continue
            walls.append({"c": [*a, *b], "move": 20, "sight": 20, "light": 20, "sound": 20, "door": 0, "ds": 0})

    for portal in dd.get("portals", []):
        b = portal.get("bounds") or []
        if len(b) < 2:
            continue
        a, c = P(b[0]), P(b[-1])
        walls.append({"c": [*a, *c], "move": 20, "sight": 20, "light": 20, "sound": 20,
                      "door": 1, "ds": 0 if portal.get("closed", True) else 1})

    lights = []
    for l in dd.get("lights", []):
        x, y = P(l["position"])
        rng = float(l.get("range", 2)) * FT_PER_SQUARE
        lights.append({"x": x, "y": y, "dim": round(rng, 1), "bright": round(rng / 2, 1),
                       "color": color_hex(l.get("color")), "alpha": round(min(1.0, float(l.get("intensity", 1)) * 0.35), 2),
                       "anim": "torch"})

    w, h = px(size["x"]), px(size["y"])
    return {"w": w, "h": h, "walls": walls, "lights": lights}


def write_images(dd, key):
    raw = base64.b64decode(dd["image"])
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    os.makedirs(OUT_DIR, exist_ok=True)
    fname = f"{key}.webp"
    im.save(os.path.join(OUT_DIR, fname), "WEBP", quality=85)
    th = im.copy()
    th.thumbnail((THUMB_W, THUMB_W * im.height // im.width))
    th.save(os.path.join(OUT_DIR, f"thumb-{fname}"), "WEBP", quality=70)
    return fname, im.size


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("key", help="scene key in maps.json, e.g. backroom, corridor-stairwell")
    ap.add_argument("dd2vtt")
    ap.add_argument("--darkness", type=float, default=None, help="scene darkness 0-1 (kept from maps.json if omitted)")
    ap.add_argument("--name", default=None, help="display name, stored as `name` for build.py")
    args = ap.parse_args()

    with open(args.dd2vtt, "rb") as f:
        dd = json.load(f)

    maps = json.load(open(MAPS_JSON)) if os.path.exists(MAPS_JSON) else {}
    prev = maps.get(args.key, {})

    data = convert(dd, args.key)
    fname, (iw, ih) = write_images(dd, args.key)
    if (iw, ih) != (data["w"], data["h"]):
        print(f"note: image is {iw}x{ih} but grid says {data['w']}x{data['h']}; using the image size", file=sys.stderr)
        data["w"], data["h"] = iw, ih

    entry = {
        "file": fname,
        **data,
        "notes": prev.get("notes", {}),
        "rects": prev.get("rects", {}),
        "start": prev.get("start", [data["w"] // 2, data["h"] // 2]),
        "darkness": args.darkness if args.darkness is not None else prev.get("darkness", 0.5),
        "source": os.path.basename(args.dd2vtt),
    }
    if args.name or prev.get("name"):
        entry["name"] = args.name or prev["name"]

    maps[args.key] = entry
    json.dump(maps, open(MAPS_JSON, "w"), indent=1)
    doors = sum(1 for w in entry["walls"] if w["door"])
    print(f"{args.key}: {entry['w']}x{entry['h']} px, {len(entry['walls'])} walls ({doors} doors), "
          f"{len(entry['lights'])} lights -> maps/{fname}, maps/thumb-{fname}, {MAPS_JSON}")


if __name__ == "__main__":
    main()
