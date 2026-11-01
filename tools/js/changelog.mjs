// CHANGELOG.md tooling (Keep a Changelog). Three commands:
//   node tools/js/changelog.mjs check            Warn when there are commits since the last tag but [Unreleased] is empty,
//                                                or when a bullet is wrapped onto a second line (BBMM can't render that).
//                                                Runs at the end of every `npm run build:packs`.
//   node tools/js/changelog.mjs ship <version>   Used by package.mjs at release time. Writes dist/CHANGELOG.md (the shipped
//                                                copy, without [Unreleased]) and dist/RELEASE_NOTES.md (this version's section,
//                                                used as the GitHub release body). If CHANGELOG.md has no section for the
//                                                version, [Unreleased] becomes it (dated today). Fails if there are no notes.
//   node tools/js/changelog.mjs release <version>  Local: turn [Unreleased] into [version] - today in CHANGELOG.md itself,
//                                                add a fresh [Unreleased], and update the compare links. Commit the result.
import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";
import { execSync } from "node:child_process";

const FILE = "CHANGELOG.md";
const REPO = "https://github.com/bularzik/the-back-room";
const today = () => new Date().toISOString().slice(0, 10);
const sh = cmd => { try { return execSync(cmd, { stdio: ["ignore", "pipe", "ignore"] }).toString().trim(); } catch { return ""; } };

// Split the file into: head (up to the first "## ["), sections [{title, version, body}], and link-reference lines.
function parse(text) {
  const lines = text.split("\n");
  const head = [], sections = [], links = [];
  let cur = null;
  for (const line of lines) {
    if (/^\[[^\]]+\]:\s/.test(line)) { links.push(line); continue; }
    const m = line.match(/^## \[([^\]]+)\](.*)$/);
    if (m) { cur = { title: line, version: m[1], body: [] }; sections.push(cur); continue; }
    (cur ? cur.body : head).push(line);
  }
  return { head, sections, links };
}
const trimBlank = arr => { const a = [...arr]; while (a.length && !a[0].trim()) a.shift(); while (a.length && !a.at(-1).trim()) a.pop(); return a; };
const hasContent = s => trimBlank(s.body).some(l => l.trim());
function render({ head, sections, links }) {
  const out = [...trimBlank(head), ""];
  for (const s of sections) out.push(s.title, ...(hasContent(s) ? ["", ...trimBlank(s.body)] : []), "");
  if (links.length) out.push(...links, "");
  return out.join("\n");
}
function compareLinks(sections) {
  const versions = sections.map(s => s.version).filter(v => v !== "Unreleased");
  const links = [`[Unreleased]: ${REPO}/compare/v${versions[0]}...HEAD`];
  versions.forEach((v, i) => links.push(versions[i + 1] ? `[${v}]: ${REPO}/compare/v${versions[i + 1]}...v${v}` : `[${v}]: ${REPO}/releases/tag/v${v}`));
  return links;
}
// Make sure there is a section for `version`, taking [Unreleased]'s notes if needed. Returns the section (or null).
function promote(doc, version) {
  let sec = doc.sections.find(s => s.version === version);
  const unrel = doc.sections.find(s => s.version === "Unreleased");
  if (!sec && unrel && hasContent(unrel)) {
    sec = { title: `## [${version}] - ${today()}`, version, body: unrel.body };
    unrel.body = [];
    doc.sections.splice(doc.sections.indexOf(unrel) + 1, 0, sec);
  }
  return sec && hasContent(sec) ? sec : null;
}

const [cmd, arg] = process.argv.slice(2);
if (!existsSync(FILE)) { console.error(`${FILE} is missing.`); process.exit(cmd === "check" ? 0 : 1); }
const doc = parse(readFileSync(FILE, "utf8"));

if (cmd === "check") {
  const tag = sh("git describe --tags --abbrev=0");
  const since = tag ? Number(sh(`git rev-list --count ${tag}..HEAD`) || 0) : 0;
  const unrel = doc.sections.find(s => s.version === "Unreleased");
  const tagVersion = tag.replace(/^v/, "");
  // After a release made straight from [Unreleased], the repo copy still holds those notes under [Unreleased]; date them,
  // or the next release would ship them again.
  if (tagVersion && unrel && hasContent(unrel) && !doc.sections.some(s => s.version === tagVersion))
    console.warn(`CHANGELOG: ${tag} was released but has no section here; its notes are probably still under [Unreleased]. Run \`npm run changelog:release -- ${tagVersion}\` and commit.`);
  if (!unrel) console.warn("CHANGELOG: there is no [Unreleased] section.");
  else if (since > 0 && !hasContent(unrel)) console.warn(`CHANGELOG: ${since} commit(s) since ${tag}, but [Unreleased] is empty. Add the user-facing changes to CHANGELOG.md.`);
  else console.log(`CHANGELOG: [Unreleased] ${hasContent(unrel) ? "has notes" : "is empty"}${tag ? ` (${since} commit(s) since ${tag})` : ""}.`);
  // BBMM renders one line at a time: a bullet continued on the next line becomes a stray paragraph.
  const wrapped = doc.sections.flatMap(s => s.body).filter(l => /^\s{2,}\S/.test(l) && !/^\s*[-*+]\s/.test(l));
  if (wrapped.length) console.warn(`CHANGELOG: ${wrapped.length} wrapped line(s); keep each bullet on one line so BBMM shows it properly. First: "${wrapped[0].trim().slice(0, 60)}"`);
} else if (cmd === "ship") {
  const version = (arg || "").replace(/^v/, "");
  const sec = promote(doc, version);
  if (!sec) { console.error(`CHANGELOG: no notes for ${version}: [Unreleased] is empty and there is no [${version}] section.`); process.exit(1); }
  // The shipped copy is what Big Bad Module Manager (BBMM) shows the GM on login: it reads CHANGELOG.md from the module's
  // root with a line-based Markdown renderer, so drop what it can't render (the blockquote note, link references).
  const shipped = { head: doc.head.filter(l => !l.startsWith(">")), sections: doc.sections.filter(s => s.version !== "Unreleased"), links: [] };
  mkdirSync("dist", { recursive: true });
  writeFileSync("dist/CHANGELOG.md", render(shipped));
  writeFileSync("dist/RELEASE_NOTES.md", trimBlank(sec.body).join("\n") + `\n\nFull changelog: ${REPO}/blob/v${version}/CHANGELOG.md\n`);
  console.log(`CHANGELOG: shipped notes for ${version}.`);
} else if (cmd === "release") {
  const version = (arg || "").replace(/^v/, "");
  if (!/^\d+\.\d+\.\d+$/.test(version)) { console.error("usage: changelog.mjs release <x.y.z>"); process.exit(1); }
  if (!promote(doc, version)) { console.error(`CHANGELOG: [Unreleased] is empty; nothing to release as ${version}.`); process.exit(1); }
  doc.links = compareLinks(doc.sections);
  writeFileSync(FILE, render(doc));
  console.log(`CHANGELOG: [Unreleased] is now [${version}] - ${today()}. Commit CHANGELOG.md, push, then create the v${version} release.`);
} else {
  console.error("usage: changelog.mjs check | ship <version> | release <version>"); process.exit(1);
}
