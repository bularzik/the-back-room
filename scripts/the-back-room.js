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
