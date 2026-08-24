# NOTES — The Vault Job prototype (spec v2: tension, variety, all stages)

## What was built (v2, supersedes the v1 notes below)

Design_V7.md ("Build Spec v2") implemented in full, stages 1–4, on top of the live
build. Still one self-contained `index.html`, vanilla JS, no build step, works from
`file://` (the manifest is inlined, never fetched).

**The inversion (§0).** `drawOutcome()` now draws the tier FIRST from
`CONFIG.tierWeights`, then draws crew results, the exit, presentation paths and
holds consistent with it. Crew results are `clean · close · out ·
downedThenRecovered` (recovered counts as reaching the vault and contributes his
number and gem exactly as a clean solve, per 12c). Lockbox is a sealed tier in its
own right with a drawn mode: `inPerson` (3 in, all numbered) or `radioOut` (1–2
reach; the missing numbers come over comms), split by `CONFIG.lockboxRadioOutRate`.

**Stage 1 — backbone.**
- Reveal order via `pickRevealOrder()` (spec §4.1 verbatim, seeded Fisher–Yates):
  the tier-deciding encounter always resolves last among the shown encounters.
- The decider hold: 0.4s (no swing — dead branch under the arrivals ladder, kept
  defensively) / 2.4s / 3.4s (grail & lockbox), drawn at seal. The decider's
  attempt stretches across its encounter beat, freezes, and resolves across the
  hold. The only hold > 1.2s in any run.
- The alarm counter: 3 pips top-right from t≈2.0. Out burns a pip, clean resets
  to 3 with a snap, close/recovered leave it. It reaches 0 only on an
  out-out-out seal (getaway), where the trip cuts the run to the reveal and the
  door never moves. Pure presentation; it decides nothing.
- The beat scheduler (§2.2): every beat is `{id, dur, minDur, priority}`;
  priorities 0/1 never trim; the scheduler trims p3 (to zero) then p2 (to
  minDur) until the run fits its ceiling, and console-errors the beat list on
  overrun. Bands enforced: short 6.5–9.0s, medium 13–17s, full 19–24s, radio-out
  lockbox premium whitelisted to 26.5s, quick fixed 4.0s.
- Exits drawn at seal from `CONFIG.exitWeights`. Off-screen encounters are
  resolved and reported (panel status, reveal card "Not shown: …", and a new
  receipt `Exit` row) — the tier is a property of the seal, never of how many
  encounters were watched.
- Player controls (§2.4): tap advances to the next beat boundary, hold
  fast-forwards 3×, session pacing after the 5th open (`vj.session.opens`)
  drops p3 beats and trims p2 to minDur; the "Full show" toggle restores;
  **Replay always forces the full track** so replays are comparable.

**Stage 2 — second chances.**
- Soft-fail-then-assist (§5.2): flagged at seal on at most two shown,
  non-decider, non-window encounters; two near-miss flashes at +0.9/+1.8s on
  BOTH the win path (assist at +2.45s) and the loss path (the consequence just
  lands). Verified both paths occur (~44% win / 56% loss of flags in 2000 draws).
- The downed window (§5.3): sealed staging, bleedout bar, save moment drawn at
  seal between 1.5–2.7s; `CONFIG.recoveryRate` 0.33 ships as specced (measured
  0.33 over 5000 draws). Loss path completes the consequence when the bar runs
  out. Both outcomes staged.
- The handler (§5.5): 12 states, lines in the manifest as data with `{token}`
  substitution, selected deterministically by seed+slot hash. The decider-hold
  line names the stakes from the banked results ("two in. one to go. if he
  makes it, it's grail."). Never solicits input.

**Stage 3 — crescendo.**
- Five-level heat ladder (§5.4), final level drawn at seal from the tier's
  allowed set (`CONFIG.heatByTier`), foreshadowed faintly at the cold open,
  climbs monotonically at the heat beat. Never exceeds the sealed tier's set.
- Radio-out for the numbers (§5.6): premium 6.5s beat after the door — empty
  slots, each downed crew member reads his number through static, the case
  opens, one man carries it out. Whitelisted to 26.5s; only on a sealed
  radio-out lockbox.
- The guaranteed signal: grail/lockbox only, at `CONFIG.signalRate`; the alarm
  powers down without sounding before the door.
- Tier-scaled door (carried over): the `rich` curve keys flourish to arrivals.

**Stage 4 — the variety engine (§3).**
- `assets/manifest.json` schema inlined into index.html between
  `MANIFEST:BEGIN/END` markers as `<script type="application/json" id="manifest">`;
  the page reads the inline copy only, so `file://` works.
- `tools/build-manifest.mjs` (plain Node, no deps): walks `vault/assets/<slotId>/`
  folders, reads durations (sidecar JSON or `_1800ms` filename suffix), merges the
  builtin placeholder table, inlines the JSON. Dropping files + re-running is the
  whole pipeline; the engine hardcodes no counts.
- Selection: `variantIndex = xmur3(seed + ':' + slotId)() % len`. No session
  state, no no-repeat tracking; the quick-open gag pool (which WAS session
  state in v1) was replaced with this — a v1 determinism bug fixed.
- Placeholder library: one builtin CSS/SVG stand-in per visual slot (§3.5); the
  handler ships 4 lines per state and gag.quick ships 4, since those are data.
  Missing slots log once and fall back; loading can never stall a beat.

## Decisions recorded (per §7.5)

1. **Exit constraints by tier/window.** Priority-0/1 beats alone exceed the short
   ceiling for grail (3.4s hold + 1.5s signal) and for any downed-window run, and
   exceed the medium ceiling for grail+window. So: lockbox seals always draw the
   full exit; grail never draws short; a window run never draws short; grail with
   a window is always full (§7.5 rule 3 — stay inside the band). Debug can still
   force any combination; the overrun assert fires as designed.
2. **Off-screen reports on short exits are zero-cost events** during the
   blueprint (the 9.0s ceiling has no room for report beats); medium exits give
   them a 0.5s p2 beat.
3. **At most one downed window per run** (budget: each window costs up to 3.0s).
   Not drawn on radio-out lockbox seals (the radio beat already features the
   downed crew, and premium + window cannot fit 26.5s).
4. **Soft-fails never flag the decider** — its tension belongs to the hold — nor
   the window member.
5. **On a grail seal the window recovery never flips the last non-numbered
   member** (a recovered member carries his number, which would make all three
   numbered and contradict "the lockbox stays shut"). Caught by the 5000-draw
   consistency battery, fixed at the draw.
6. **Getaway keeps its shut door.** Spec test 16 ("door opens on 100% of runs
   including every one-haul run") is read as "every run with at least one at the
   door" — the preserved How-it-pays cards and getaway fiction say the door
   never moves, and §6.5 preservation outranks (rule 2). The point of the test —
   no anticlimax skip on a one-haul floor run — holds: the door opens fully for
   1, 2 and 3 arrivals.
7. **The alarm trip only fires at 0 pips** (i.e. on getaway seals, any exit —
   off-screen outs burn pips too, so a short getaway trips after its one shown
   encounter). Non-getaway short/medium runs end by cutting to the approach; the
   early exit is explained by the off-screen reporting, not by a fake trip.
8. **Grail may now be all-out of… nothing changed:** grail still always keeps at
   least one non-numbered member (close call), preserving "clean solves find
   numbers, three numbers open the box" and the lockbox cards. In-person lockbox
   reachers are drawn clean (numbers carried in); radio-out reachers likewise.
9. **Session pacing counts opens in `localStorage` under `vj.session.opens`**
   (spec-literal), so it persists across page loads; "Full show" is persisted
   too. Client can decide later if "session" should reset.
10. **stakesLine clamps the upside to grail on non-lockbox seals** — lockbox is
    sealed, not a sum, so the handler must not promise the box when flipping the
    decider would merely make all three numbered.
11. **Asset durations** come from a sidecar `<file>.json` (`{"dur":1800}`) or a
    `_1800ms` filename suffix; WebM parsing without deps was not worth it for a
    placeholder pipeline. A 0-duration entry never extends a beat.

## Verified in a live browser (this build)

- **Determinism:** same seed drawn twice → identical frozen Outcome (300 seeds);
  Replay reproduces the identical seal dump — tier, results, order, hold, heat,
  beat list, variant indices (15 runs); `Math.random` appears only in comments;
  runtime instrumentation counted 0 calls across 10 full runs — **pass**
- **Inversion (12a):** 5,000 draws + each tier forced 20× via the debug panel: crew
  results always consistent with the sealed tier (lockbox: in-person = 3 in all
  numbered; radio-out = 1–2 in) — **pass**
- **Pacing:** 5,000 scheduled runs: short 9000ms, medium 16600–17000ms, full
  20100–24000ms, premium 26500ms; zero ceiling overruns at full AND reduced
  depth; only the decider hold exceeds 1.2s — **pass**
- **Reveal order (7):** decider resolves last among shown in 5,000/5,000 draws
  with a swing — **pass**
- **Soft-fails (8):** flags land on winning and losing encounters (468/600 in
  2,000 draws), max two per run — **pass**
- **Downed window (9):** recovered 32–33% of windows over 5,000 draws — **pass**
- **Honesty (13/14):** signal fired 0 times below grail in 5,000 draws; heat
  level never outside the sealed tier's allowed set — **pass**
- **Radio-out (12b):** premium plays the empty-slot / read-back / case-open
  sequence at 26.5s and only on radio-out seals; in-person lockbox fills three
  carried numbers, no radio beat; quick-open lockbox shows the same sealed tier
  at 4.05s — **pass**
- **Reporting (12d):** short solid run reveal card: "Not shown: the lobby guy got
  through; the keypad guy got through — resolved off screen"; receipt Exit row
  matches — **pass**
- **12c:** a rescued member banks his number and gem (floor run off a single
  `downedThenRecovered`) — **pass**
- **Controls:** tap mid-cold-open jumped exactly to the blueprint boundary; hold
  = 3×; session pacing kicked in on the 6th open (beat list header shows
  `reduced`) and Replay forced `full` — **pass**
- **Preserved list (§6.5):** commit shown before pick, Verify PASS on the real
  seed and FAIL on a 1-char tamper, Replay, debug panel (extended, nothing
  removed), building tracker descents, 5 How-it-pays cards, demo tier selector,
  Restart mid-run, quick-open toggle, CONFIG weights byte-identical — **pass**
- **Variety (11):** N=1 placeholder library → recorded as **"N/A, placeholder
  library"** per spec. Handler (4/state) and gags (4) already vary by seed.
  (12) `node tools/build-manifest.mjs` regenerates and re-inlines the manifest;
  file drops appear with no code change — **pass**

## Known placeholder values (client owns; all marked PLACEHOLDER in CONFIG)

`exitWeights`, `signalRate`, `softFailChance`, `downedWindowChance` are new and
shipped as placeholders. `recoveryRate` (0.33) and `lockboxRadioOutRate` (0.5)
ship at the spec's stated values. `tierWeights`, `arrivalsByTier`,
`closeCallRate` are untouched from v1.

---

# v1 notes (historical — superseded above)

## What was built
One self-contained `index.html` (~74KB, no network, vanilla JS, system fonts, inline SVG). Three crew members, three encounters, **all on screen at once** with the vault and a building tracker. Each crew member waits in position until his go-signal; the go **order is drawn per run**, so scenes resolve at different moments in a different sequence every time. Each result is clean / close call / out. **Out has a consequence on screen**: the roof turret drops the roof guy, the lobby guard cuffs and walks the lobby guy out, the keypad alarm strobes and a cage drops. **A clean solve also finds one number for the lockbox.**

**The ladder was a pure function of the three results** (inverted in v2 — see above).

Honesty is unchanged: the outcome is drawn in one seeded pass and frozen before the first frame. Commit–reveal receipt, Replay, Verify, quick open and the debug panel carry over.

## Pick-screen additions
- **How it pays**: five cards built from `CONFIG` — mini vault in tier colour, three figures (solid = made it), how you win it, value band, two example prizes. Tier odds are deliberately not on the cards.
- **Show me a…**: Random / Getaway / Floor / Solid / Grail / Lockbox. A labelled demo control, same setting as the debug panel's Force tier, applied at draw time. Remove or hide before anything player-facing — the spec forbids a player choosing the outcome.
- **Restart** (header, during a run): abandons the run, nothing revealed, next pick uses a fresh nonce.

## Decisions (direction from Makko, replacing spec v1.0 sections 3–4)
- Consequences replace "never a contest the crew could fail." No blood, no mockery: stunned, arrested, caged, flat copy.
- Replays never re-bank the cosmetic job counter.
