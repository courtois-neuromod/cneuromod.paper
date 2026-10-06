// MyST plugin: `{all-references}` cites every reference used in paper/*.md, so the page holding it
// gets a single, complete reference list (per-page lists are hidden by site.css).
import fs from 'node:fs';
import path from 'node:path';

const ROLE = /\{cite(?::[a-z]+)?\}`([^`]+)`/g;
const BRACKET = /\[([^\]]*@[^\]]*)\]/g;

function citedKeys(dir) {
  const keys = new Set();
  for (const file of fs.readdirSync(dir).filter((f) => f.endsWith('.md'))) {
    const text = fs.readFileSync(path.join(dir, file), 'utf8');
    for (const m of text.matchAll(ROLE)) {
      m[1].split(/[,;]/).forEach((k) => k.trim() && keys.add(k.trim()));
    }
    for (const m of text.matchAll(BRACKET)) {
      for (const k of m[1].matchAll(/@([\w:.\-]+)/g)) keys.add(k[1]);
    }
  }
  return [...keys].sort((a, b) => a.localeCompare(b, 'en', { sensitivity: 'base' }));
}

const allReferences = {
  name: 'all-references',
  doc: 'Cite every reference used across paper/*.md (hidden), so this page lists them all.',
  run() {
    const keys = citedKeys(path.resolve('paper'));
    const cites = keys.map((k) => ({
      type: 'cite',
      kind: 'parenthetical',
      label: k,
      identifier: k.toLowerCase(),
    }));
    return [
      {
        type: 'div',
        class: 'all-references',
        children: [
          { type: 'paragraph', children: [{ type: 'citeGroup', kind: 'parenthetical', children: cites }] },
        ],
      },
    ];
  },
};

export default { name: 'All references', directives: [allReferences] };
