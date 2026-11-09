// The Back Room: runtime helpers. Kept tiny on purpose; everything else in the module is data.
//
// Patrol (optional module, theripper93): the barmaid in the Common Room walks her circle.
// The adventure ships a plain Region flagged {"the-back-room": {patrol: "<token or actor name>"}} and a token flagged
// {patrol: {enablePatrol: true}}. A Region behaviour of Patrol's type can't ship in the scene itself: when Patrol is
// not installed, Foundry rejects the unknown behaviour type and the scene fails to import. So, on the GM's client,
// when Patrol is active: add Patrol's "edge" behaviour to each flagged Region that lacks it, and start Patrol's
// stepping whenever a scene with such a Region is viewed.
const MOD = "the-back-room";
const PATROL = "patrol";
const BEHAVIOR = "patrol.patrolArea";

async function ensurePatrolBehaviors(scene) {
  const regions = scene?.regions?.filter(r => r.getFlag(MOD, "patrol")) ?? [];
  for (const region of regions) {
    if (region.behaviors.some(b => b.type === BEHAVIOR)) continue;
    await region.createEmbeddedDocuments("RegionBehavior", [{
      name: "Walks the circuit (Patrol)", type: BEHAVIOR,
      system: { type: "edge", backAndForth: false, whitelist: [region.getFlag(MOD, "patrol")], weight: 100 }
    }]);
  }
  return regions.length > 0;
}

Hooks.on("canvasReady", async canvas => {
  try {
    if (!game.user.isGM || !game.modules.get(PATROL)?.active) return;
    const hasPatrol = await ensurePatrolBehaviors(canvas.scene);
    const api = game.modules.get(PATROL)?.API?.patrol;
    if (hasPatrol && api && !api.stepping) api.toggleStepping(true);
  } catch (err) {
    console.warn(`${MOD} | Patrol setup skipped:`, err);
  }
});

// Arrivals stay apart. Monk's Active Tile Triggers moves the whole party through a door in one go, and its own
// "avoid tokens" check can't see the tokens it is creating in the same batch, so two can land on one square. After a
// teleport (MATT marks the token flags.monks-active-tiles.teleporting), the GM's client nudges any token that overlaps
// another, or that MATT dropped onto a door tile, to the nearest free square that isn't through a wall or on a door tile.
const _queue = [];
let _running = false;
function overlaps(a, b, size) {
  return a.x < b.x + b.width * size && b.x < a.x + a.width * size && a.y < b.y + b.height * size && b.y < a.y + a.height * size;
}
function crossesWall(scene, A, B) {
  for (const w of scene.walls) {
    if (w.move === CONST.WALL_MOVEMENT_TYPES.NONE) continue;
    if (w.door && w.ds === CONST.WALL_DOOR_STATES.OPEN) continue;
    if (foundry.utils.lineSegmentIntersects(A, B, { x: w.c[0], y: w.c[1] }, { x: w.c[2], y: w.c[3] })) return true;
  }
  return false;
}
// Never nudge an arrival onto a door: a tile that teleports (one step later the party would be gone again).
function onDoorTile(scene, cand, size) {
  return scene.tiles.some(t => {
    const f = t.flags?.["monks-active-tiles"];
    if (!f?.active || !f.actions?.some(a => a.action === "teleport")) return false;
    return cand.x < t.x + t.width && t.x < cand.x + cand.width * size && cand.y < t.y + t.height && t.y < cand.y + cand.height * size;
  });
}
async function spreadOut(doc) {
  const scene = doc.parent; if (!scene || !scene.tokens.has(doc.id)) return;
  const size = scene.dimensions.size;
  const others = () => scene.tokens.filter(t => t.id !== doc.id);
  if (!others().some(t => overlaps(doc, t, size)) && !onDoorTile(scene, doc, size)) return;
  const half = size * doc.width / 2, origin = { x: doc.x + half, y: doc.y + half };
  for (let r = 1; r <= 4; r++) {
    for (let dx = -r; dx <= r; dx++) for (let dy = -r; dy <= r; dy++) {
      if (Math.max(Math.abs(dx), Math.abs(dy)) !== r) continue;
      const cand = { x: doc.x + dx * size, y: doc.y + dy * size, width: doc.width, height: doc.height };
      if (cand.x < 0 || cand.y < 0 || cand.x + doc.width * size > scene.dimensions.sceneWidth + scene.dimensions.sceneX * 2
          || cand.y + doc.height * size > scene.dimensions.sceneHeight + scene.dimensions.sceneY * 2) continue;
      if (others().some(t => overlaps(cand, t, size))) continue;
      if (onDoorTile(scene, cand, size)) continue;
      if (crossesWall(scene, origin, { x: cand.x + half, y: cand.y + half })) continue;
      await doc.update({ x: cand.x, y: cand.y }, { animate: false });
      return;
    }
  }
}
Hooks.on("createToken", (doc, options, userId) => {
  if (game.users.activeGM?.id !== game.user.id) return;            // one client does it
  if (!doc.getFlag("monks-active-tiles", "teleporting")) return;   // only arrivals by tile teleport
  _queue.push(doc);
  if (_running) return;
  _running = true;
  setTimeout(async () => {                                          // let the whole batch arrive first
    try { while (_queue.length) await spreadOut(_queue.shift()); }
    catch (err) { console.warn(`${MOD} | spreading arrivals failed:`, err); }
    finally { _running = false; }
  }, 400);
});
