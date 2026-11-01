// The Back Room: make the Echo of a character (Room 3).
// Makes a new actor, "The Echo of <name>", from the base Echo: the character's art (tinted grey, no name on the token),
// their speed, size and ability scores, and copies of their weapons and spells with the numbers halved:
// HP, AC, attack bonuses, damage and healing, save DCs. The base Echo is left as it is, so you can run this again.
const base = game.actors.getName("The Echo");
if (!base) return ui.notifications.error("The Echo actor isn't in this world. Import the adventure first.");
const chars = game.actors.filter(a => a.type === "character").sort((a, b) => (b.hasPlayerOwner - a.hasPlayerOwner) || a.name.localeCompare(b.name));
if (!chars.length) return ui.notifications.warn("There are no player characters in this world.");
const id = await foundry.applications.api.DialogV2.prompt({
  window: { title: "Make the Echo" },
  content: `<p>Which character does the Echo copy? (The one with the fewest Misremembering changes.)</p>
    <select name="pc" style="width:100%">${chars.map(c => `<option value="${c.id}">${foundry.utils.escapeHTML(c.name)}</option>`).join("")}</select>`,
  ok: { label: "Make the Echo", callback: (ev, button) => button.form.elements.pc.value },
  rejectClose: false
});
if (!id) return;
const pc = game.actors.get(id);
const half = n => Math.floor((Number(n) || 0) / 2);
const halfFormula = f => `floor((${f}) / 2)`;

// Weapons the character has equipped, and their spells: copies with every number halved.
const items = [];
for (const item of pc.items) {
  if (!(item.type === "spell" || (item.type === "weapon" && item.system.equipped))) continue;
  const data = item.toObject(); delete data._id;
  for (const act of item.system.activities ?? []) {
    const a = data.system.activities?.[act.id]; if (!a) continue;
    if (act.type === "attack" && act.labels?.toHit) a.attack = { ...a.attack, flat: true, bonus: String(half(parseInt(act.labels.toHit))) };
    if (act.save?.dc?.value) a.save = { ...a.save, dc: { calculation: "", formula: String(half(act.save.dc.value)) } };
    const dmg = act.labels?.damage ?? [];
    if (a.damage && dmg.length) {
      a.damage.includeBase = false;
      a.damage.parts = dmg.map(d => ({ custom: { enabled: true, formula: halfFormula(d.formula) }, types: d.damageType ? [d.damageType] : [] }));
    }
    if (act.type === "heal" && a.healing && dmg[0]) a.healing = { ...a.healing, custom: { enabled: true, formula: halfFormula(dmg[0].formula) } };
  }
  items.push(data);
}

const data = base.toObject(); delete data._id;
const tok = pc.prototypeToken;
foundry.utils.mergeObject(data, {
  name: `The Echo of ${pc.name}`,
  img: pc.img,
  "system.abilities": Object.fromEntries(Object.entries(pc.system.abilities).map(([k, v]) => [k, { value: v.value }])),
  "system.attributes.hp": { value: Math.max(1, half(pc.system.attributes.hp.max)), max: Math.max(1, half(pc.system.attributes.hp.max)), formula: "" },
  "system.attributes.ac": { calc: "flat", flat: half(pc.system.attributes.ac.value) },
  "system.attributes.movement": foundry.utils.deepClone(pc.system._source.attributes.movement),
  "system.traits.size": pc.system.traits.size,
  "system.spells": Object.fromEntries(Object.entries(pc.system.spells ?? {}).filter(([, v]) => v?.max).map(([k, v]) => [k, { value: v.max, override: v.max }])),
  "prototypeToken.name": "—",
  "prototypeToken.texture.src": tok.texture.src,
  "prototypeToken.texture.tint": "#9a9a9a",
  "prototypeToken.width": tok.width, "prototypeToken.height": tok.height,
  "prototypeToken.actorLink": false,
  "prototypeToken.disposition": CONST.TOKEN_DISPOSITIONS.HOSTILE
}, { performDeletions: true });
data.items = data.items.filter(i => i.type === "feat").concat(items);  // keep the Echo's rules, drop its stand-in weapon
const echo = await Actor.create(data);
echo.sheet.render(true);
ui.notifications.info(`${echo.name}: HP ${echo.system.attributes.hp.max}, AC ${echo.system.attributes.ac.value}, ${items.length} halved weapons and spells. Drag it onto the far door when it steps out.`);
