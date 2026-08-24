#!/usr/bin/env node
/* build-manifest.mjs — the asset pipeline for The Vault Job (spec v2 §3.3).
   Plain Node, no npm dependencies, run by hand:

       node tools/build-manifest.mjs

   It walks vault/assets/<slotId>/ folders (folder name = slot id, e.g.
   assets/encounter.roof.clean/), reads each file's duration, merges the result
   with the builtin placeholder library, and inlines the JSON into index.html
   between the MANIFEST:BEGIN / MANIFEST:END markers. The page reads the inline
   copy and never fetches it, so file:// keeps working.

   Adding 40 new handler lines or 12 new encounter variants is a data drop:
   put the files in the right folder and re-run this script. No code change.
   The engine reads whatever counts are present and never hardcodes a count.

   Durations: the scheduler budgets from the manifest without loading assets,
   so every file entry carries a duration in ms. It is read, in order of
   preference, from:
     1. a sidecar JSON file  (clip.webm.json  containing  {"dur": 1800})
     2. a filename suffix    (clip_1800ms.webm)
     3. otherwise 0, with a warning — a 0-duration entry is treated by the
        engine as "fits any beat" and will never extend one.

   Builtin placeholder entries (and handler text lines) live in this script's
   BUILTINS table below — the single source of truth. Regenerating always
   re-emits them, then appends any real files found on disk. */

import { readdirSync, readFileSync, writeFileSync, statSync, existsSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const INDEX = join(ROOT, 'index.html');
const ASSETS = join(ROOT, 'assets');
const BEGIN = '<!-- MANIFEST:BEGIN';
const END = '<!-- MANIFEST:END -->';
const ASSET_EXT = /\.(webm|webp|svg|png|mp3|ogg|txt)$/i;

/* ---- the builtin placeholder library: one CSS/SVG stand-in per visual slot
   (spec §3.5), plus the handler's text lines and the quick-open gags. */
const BUILTINS = {
  'encounter.roof.clean':   [{ builtin: 'roof-clean-v0', dur: 0 }],
  'encounter.roof.close':   [{ builtin: 'roof-close-v0', dur: 0 }],
  'encounter.roof.out':     [{ builtin: 'roof-out-v0', dur: 0 }],
  'encounter.lobby.clean':  [{ builtin: 'lobby-clean-v0', dur: 0 }],
  'encounter.lobby.close':  [{ builtin: 'lobby-close-v0', dur: 0 }],
  'encounter.lobby.out':    [{ builtin: 'lobby-out-v0', dur: 0 }],
  'encounter.keypad.clean': [{ builtin: 'keypad-clean-v0', dur: 0 }],
  'encounter.keypad.close': [{ builtin: 'keypad-close-v0', dur: 0 }],
  'encounter.keypad.out':   [{ builtin: 'keypad-out-v0', dur: 0 }],
  'softfail.roof':   [{ builtin: 'softfail-v0', dur: 0 }],
  'softfail.lobby':  [{ builtin: 'softfail-v0', dur: 0 }],
  'softfail.keypad': [{ builtin: 'softfail-v0', dur: 0 }],
  'assist.roof':   [{ builtin: 'assist-v0', dur: 0 }],
  'assist.lobby':  [{ builtin: 'assist-v0', dur: 0 }],
  'assist.keypad': [{ builtin: 'assist-v0', dur: 0 }],
  'rescue.roof.recovered':   [{ builtin: 'rescue-v0', dur: 0 }],
  'rescue.roof.lost':        [{ builtin: 'lost-v0', dur: 0 }],
  'rescue.lobby.recovered':  [{ builtin: 'rescue-v0', dur: 0 }],
  'rescue.lobby.lost':       [{ builtin: 'lost-v0', dur: 0 }],
  'rescue.keypad.recovered': [{ builtin: 'rescue-v0', dur: 0 }],
  'rescue.keypad.lost':      [{ builtin: 'lost-v0', dur: 0 }],
  'heat.1': [{ builtin: 'heat-cold-blue', dur: 0 }],
  'heat.2': [{ builtin: 'heat-warm-amber', dur: 0 }],
  'heat.3': [{ builtin: 'heat-gold', dur: 0 }],
  'heat.4': [{ builtin: 'heat-white-gold', dur: 0 }],
  'heat.5': [{ builtin: 'heat-prismatic', dur: 0 }],
  'vaultopen.getaway': [{ builtin: 'door-shut-v0', dur: 0 }],
  'vaultopen.floor':   [{ builtin: 'door-v0', dur: 0 }],
  'vaultopen.solid':   [{ builtin: 'door-v0', dur: 0 }],
  'vaultopen.grail':   [{ builtin: 'door-v0', dur: 0 }],
  'vaultopen.lockbox': [{ builtin: 'door-prismatic-v0', dur: 0 }],
  'ambient':   [{ builtin: 'ambient-v0', dur: 0 }],
  'crew.skin': [{ builtin: 'skin-v0', dur: 0 }],
  'gag.quick': [{ gag: 'trip' }, { gag: 'cat' }, { gag: 'walkie' }, { gag: 'car' }],
  'handler.cold_open': [
    { text: 'overwatch on. cameras are mine for six minutes. let’s go to work.' },
    { text: 'three ways in, one box. quiet feet.' },
    { text: 'i’ve got eyes on all three. make me look good.' },
    { text: 'comms check. good. it’s a nice night to get rich.' },
  ],
  'handler.encounter_start': [
    { text: 'go. {where}.' },
    { text: '{where}. you’re up. clean and quiet.' },
    { text: '{where}. your window’s open. move.' },
    { text: '{where}. breathe. go.' },
  ],
  'handler.softfail_1': [
    { text: 'easy — hold. hold…' },
    { text: 'that was close. nobody breathe.' },
    { text: 'careful. careful.' },
    { text: 'i saw that. so did my heart.' },
  ],
  'handler.softfail_2': [
    { text: 'again?! okay. okay. you’re still alive.' },
    { text: 'twice. nobody’s that unlucky. reset.' },
    { text: 'i can’t watch. i’m watching.' },
    { text: 'second stumble. steady. steady…' },
  ],
  'handler.assist': [
    { text: 'got you — the loop’s frozen. go.' },
    { text: 'hatch on your left. that one’s mine. go.' },
    { text: 'and that is why you bring a crew.' },
    { text: 'handled. don’t ask how. move.' },
  ],
  'handler.downed': [
    { text: 'man down. talk to me. TALK to me.' },
    { text: 'he’s down. i still have a pulse on comms. hold on—' },
    { text: 'down. the clock is running.' },
    { text: 'no no no. he’s down.' },
  ],
  'handler.rescued': [
    { text: 'got him. GOT him. moving.' },
    { text: 'he’s up. limping, but up.' },
    { text: 'pulled him out. never do that again.' },
    { text: 'breathing. walking. good enough.' },
  ],
  'handler.lost': [
    { text: 'he’s gone. leave it. i said leave it.' },
    { text: 'no response. we’re minus one.' },
    { text: 'that’s it. he’s out of it. keep moving.' },
    { text: '…nothing. finish the job for him.' },
  ],
  'handler.counter_reset': [
    { text: 'clean. the board resets. breathe.' },
    { text: 'counter’s back to three. we’re whole.' },
    { text: 'reset. that buys the night back.' },
    { text: 'green across the board again.' },
  ],
  'handler.counter_critical': [
    { text: 'one pip left. nothing fancy from here.' },
    { text: 'we’re one alarm from done. walk, don’t run.' },
    { text: 'red board. the next mistake ends it.' },
    { text: 'one left. i don’t like this either.' },
  ],
  'handler.decider_hold': [
    { text: '{stakes} hold.' },
    { text: '{stakes} nobody breathe.' },
    { text: '{stakes} i’ll be watching through my fingers.' },
    { text: '{stakes} steady…' },
  ],
  'handler.tier_reveal': [
    { text: 'door’s yours. take it home.' },
    { text: 'open it up. we’re done here.' },
    { text: 'that’s the job. bag it and walk.' },
    { text: 'there it is. load up.' },
  ],
};

function durationOf(dir, file) {
  const sidecar = join(dir, file + '.json');
  if (existsSync(sidecar)) {
    try {
      const d = JSON.parse(readFileSync(sidecar, 'utf8')).dur;
      if (Number.isFinite(d)) return Math.round(d);
    } catch (e) { /* fall through */ }
  }
  const m = file.match(/_(\d+)ms\.[^.]+$/);
  if (m) return parseInt(m[1], 10);
  console.warn('  ! no duration for ' + file + ' (add a "' + file + '.json" sidecar or a _1800ms suffix); using 0');
  return 0;
}

const manifest = {};
for (const [slot, entries] of Object.entries(BUILTINS)) manifest[slot] = entries.slice();

let fileCount = 0;
if (existsSync(ASSETS)) {
  for (const slot of readdirSync(ASSETS).sort()) {
    const dir = join(ASSETS, slot);
    if (!statSync(dir).isDirectory()) continue;
    const files = readdirSync(dir).filter(f => ASSET_EXT.test(f)).sort();
    if (!files.length) continue;
    if (!manifest[slot]) manifest[slot] = [];
    for (const f of files) {
      manifest[slot].push({ src: 'assets/' + slot + '/' + f, dur: durationOf(dir, f) });
      fileCount++;
    }
  }
} else {
  console.log('no assets/ folder yet — emitting the builtin placeholder library only.');
}

const json = JSON.stringify(manifest, null, 2);
const block = BEGIN + ' — generated by tools/build-manifest.mjs; do not edit by hand.\n'
  + '     The engine reads this inline copy and never fetches it, so file:// works.\n'
  + '     "builtin" entries are the placeholder library (one CSS/SVG stand-in per\n'
  + '     visual slot); real assets are added by dropping files into vault/assets/\n'
  + '     and re-running the script. Handler lines are data entries here. -->\n'
  + '<script type="application/json" id="manifest">\n' + json + '\n</script>\n'
  + END;

const html = readFileSync(INDEX, 'utf8');
const a = html.indexOf(BEGIN), b = html.indexOf(END);
if (a < 0 || b < 0) { console.error('MANIFEST markers not found in index.html; aborting.'); process.exit(1); }
writeFileSync(INDEX, html.slice(0, a) + block + html.slice(b + END.length), 'utf8');

const slots = Object.keys(manifest).length;
const total = Object.values(manifest).reduce((s, v) => s + v.length, 0);
console.log('manifest inlined: ' + slots + ' slots, ' + total + ' entries (' + fileCount + ' from assets/).');
