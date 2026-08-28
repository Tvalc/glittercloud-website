# NOTES — vault-CHIBI (forked from vault-next, 2026-08-27)

**THIS IS THE ART FORK.** `vault-next/` is the approved-and-frozen version
(Makko: "fork this so we don't mess up this version we like"); everything
below the fork line is inherited history. This fork's direction: a
professionally-styled mobile game in chibi/anime style with Pokémon-LIKE
(original) monsters as the characters — no plain geometric figures.

## Fork session 1 — the chibi cast + mobile skin (2026-08-27)

- **The cast.** `figureMarkup` now renders three original chibi monsters
  (big heads, glossy double-highlight eyes, blush, chunky ink outlines,
  cel-shaded in flat SVG), drawn in the SAME local frame as the old
  figures so every movement keyframe, held pose, rescue and camera cue
  rides unchanged: SOLBY the sun-gecko (first chamber — amber, sun
  crest), PUDDLI the axolotl (flooded passage — aqua, pink gill-fronds),
  EMBIT the ember-fox (deep chamber — dusk purple, flame-tipped ears and
  tail). The door's arrival figures are mini chibi heads keyed by slot.
  Original creatures only — Pokémon-style, never Pokémon.
- **The skin.** Baloo 2 via Google Fonts; rounded 18px chunky-outline
  panels with pressed-button drop shadows; glossy pressable pick buttons;
  chunky comic bubbles; gradient haul meter (gold → green past the
  notch); gradient scene grounds (warm shaft / teal water / dusk +
  torch-glow radial). Legacy figure path kept as fallback.
- Verified: full grail run to receipt (endcard === seal 8.9×), Baloo
  loaded, 6 chibi figs live (3 rooms + 3 door heads), bubbles/labels in
  the new type, zero console errors. `vault-next/` untouched this
  session.

## Fork session 2 — character life + living backgrounds (2026-08-27)

Makko: "i need these fuckers animating and i need you to make the
backgrounds etc. match."

- **The life layer.** Every monster gets secondary animation riding INSIDE
  the engine's .fig transform (walks, held poses and rescues stack
  unchanged): idle bob with squash-and-stretch (`cb-bob`), tail wag,
  Puddli's gill fronds swaying offset left/right, Solby's crest sway,
  Embit's ear/tail flames flickering on alternating delays, and eye
  blinks every ~3.6s. **A lost or downed monster goes perfectly still**
  (animation-play-state paused — stillness stays the loss language); a
  through monster keeps its happy bob. All rigs off under reduced motion.
- **Living backgrounds, per biome**: sun chamber — swaying round-leaf
  plants with a flower + drifting sun motes in the shaft; flooded
  passage — pink coral clumps, a bobbing lilypad, bubbles rising off the
  sunken wheel on staggered delays; deep chamber — a glowing purple
  crystal cluster + floating embers in the torch light.
- Verified (DOM, pane hidden): all nine animation channels computed
  `running` (bob/wag/blink/sway/flick/rise/float/plant-sway) across 6
  figures, 3 bubbles, 6 motes, 4 plants; lost-state probe pauses body and
  tail and restores on clear; zero console errors.

## Fork session 3 — the deep pass (2026-08-27, after "that was really lazy")

- **Monsters at mobile-game size**: a `cb-scale` wrapper (×1.5 rooms, ×1.25
  door heads) between the engine's .fig transform and the cb-anim life
  layer — scale is an attribute because CSS animation owns the inner
  group's transform.
- **Acted faces**: every monster carries THREE complete stacked expressions
  and the panel's state picks one — determined (default), squeezed-happy
  arcs + open smile + big blush (.locked), worried small-pupil eyes +
  slanted brows + wavy mouth + an animated dripping sweat drop
  (.trouble/.downed/.lost; the drop freezes with the rest on a held
  monster).
- **Rooms rebuilt chunky**: real grounds (dark strip + bright top edge +
  buried stones) in all three biomes; stone-slab ledges; the sun-plate,
  sunken wheel and counterweight redrawn as gold/bronze machines with ink
  outlines and parchment hubs; an arched doorway in the sun chamber. All
  rigged classes (.dial/.wheel/.gate/.beam/.weight/.gap/.slab/.hands/
  .vdoor/.cage/slots) keep their names and geometry — the update()
  choreography is untouched.
- **The guardian door**: a full stone arch behind the dial with two sleepy
  glowing eyes carved above (decoration; outcome-blind), the dial ring and
  spokes in warm gold with a parchment hub, chunky outlined bolt housings,
  a proper ground line.
- Verified (DOM, pane hidden): face-switch probe — default shows
  determined; +trouble swaps to worried with `cb-sweatdrip` running;
  +locked swaps to happy; 6 scale wrappers; guardian arch present; run to
  receipt endcard === seal (7.3×); zero console errors. Visual sign-off
  pending the client's eyes (pane not compositing this session).

Known next steps for this fork: illustrated card faces for the items, pick
screen title treatment, walk-cycle legs, and (optionally) real raster
assets — CC0 sprite packs or client-supplied PNGs wire in via the same
figureMarkup seam.

---

# INHERITED — NOTES — vault-next (the stack reveal session, 2026-08-25)

Scope: exactly three features on top of the live vault build — (1) item-by-item
ascending reveal, (2) the tell + player-turned items, (3) the worst tier as an
acquisition — plus the debug forcing for them, built and verified FIRST.
`vault/` untouched. Art direction, skip logic, session pacing and the quick
open untouched per instructions.

## Build order actually followed

1. Copied `vault/index.html` → `vault-next/index.html` verbatim.
2. **Debug forcing first**: stack drawn at seal, `Force stack length` and
   `Glow slot` selects added to the debug panel, stack line added to the seal
   dump, stack stats added to Run-100. Verified each force in isolation
   (results below) **before any reveal code existed**.
3. Then the reveal: the stack phase, the tell, the getaway acquisition path,
   the collection.

## What was built

**The stack (drawn at seal).** `buildStack()` runs inside
`derivePresentation()` on the same seeded stream, after the frozen outcome.
Per run it draws: length (from `CONFIG.stackLenByTier`, PLACEHOLDER bands
getaway 2–3 · floor 3–4 · solid 4–5 · grail 5–6 · lockbox 6–8), the items
(values strictly ascending), the on-screen row order (seeded shuffle) and the
glow position. The LAST item is the run's drawn prize — the same `prizeRoll`
the reveal card shows, so the stack and the receipt can never disagree. The
SECOND-TO-LAST is the deliberate step up (the reverse-holo beat): drawn from
one tier-rung below the run's tier, clamped under the best. Fills come from
the rungs below the step, values clamped into strict ascent. Debug forces
(`stackLen`, `glowRow`) apply at draw time like every other force; glow slot
clamps to the stack length.

**The reveal.** The engine's beat timeline ends as before (door, haul); then
the stack phase presents the items face-down. Auto pacing: low items 400ms,
step-up 700ms, best 950ms; deal-in 70ms stagger. Player taps turn items in
any order (taps are input only — they never touch anything sealed); 3s of
idle starts the auto-turn, ascending with the glowing item last; a player tap
re-arms the 3s clock until the auto-turn has begun. Nothing ever stalls.

**The tell.** One card back per run carries the tier's §6 treatment (flat
slate / soft green / pulsing violet / blooming magenta / gold sheen). Every
back is otherwise byte-identical, so the tell is tier-only and identity stays
unknowable until the card is turned. The glowing card IS the run's best item;
its position in the row is sealed (and forceable).

**The ending.** The emblem + tier name now ignite AFTER the last item turns
(non-getaway), confirming the tell. The single counting number is deleted
from all sequenced runs (`igniteEnd` survives only on the untouched quick
path). Item values are engraved on the card faces — numbers as objects (§7).

**The acquisition (worst tier).** The vault opens on 100% of runs. Getaway:
the alarm trip and strobe stay (spec v2 §5.1 mechanics unchanged — the trip
explains the cut), but the ending is warm: the camera settles on the vault
panel, the door opens quietly in-panel (beat `open.g` replaces `shut`), no
takeover, no blackout, no emblem, no bloom, no tier name, no failure copy
(action line: "they took what they could on the way out."), no low sad tone
(small neutral note instead). Two-to-three ordinary items turn at a uniform
quick 400ms.

**The aftermath.** Every sequenced run ends with the cards flying to a
persistent COLLECTION counter in the header (plus a pick-screen line), ticking
up one per item. `localStorage` under `vj.collection.items`.

## Decisions recorded (per v2 §7.5, numbering continues vault/NOTES.md)

30. **The stack lives in `derivePresentation`, not `drawOutcome`.** It is
    presentation flavour of an already-frozen tier (like the prize roll it
    reuses), and it must share `prizeRoll` so the best item and the reveal
    card always match. Forces are plumbed into `derivePresentation(rng,
    outcome, forces)`; they apply at draw time exactly like tier/exit forces.
31. **`stackLenByTier` added to CONFIG as PLACEHOLDER** (client owns the
    numbers; nothing existing was retuned; same precedent as `prizeValues`).
32. **Visual-spec test 9 amended by direction.** The tell shows the tier's
    reserved colour from the moment the stack presents — that is the entire
    point of feature 2 — so test 9 now reads "no tier colour before the door
    opens." Tier colours appear at: the tell, the turned best face, the
    emblem, the endcard name, the pick/reveal labels. Cyan and amber
    discipline unchanged (grep-verified).
33. **Decision 6 (getaway keeps its shut door) is reversed by direction.**
    "No locked-out state anywhere in the build": the getaway door opens, and
    the pick screen's locked-out copy went with it (`HOW_COPY.getaway`, the
    howto-note, the mini-vault's SHUT label → two dim gems for the thin
    haul; `TIER_COPY.getaway` now says "vault floor"). The getaway mini-vault
    keeps its flat, glowless slate treatment per §6.
34. **The step-up beat exists on every stack, including length 2** (stack =
    step + best). On getaway the step is drawn from the getaway pool itself
    (no rung below) and the pacing flattens to the warm 400ms — the fake-out
    beat is a value shape, not a timing beat, on the floor tier.
35. **Quick open untouched, contradiction noted.** Quick still plays the old
    counting number and still calls `vault.shut()` on a getaway quick — that
    contradicts "no locked-out state anywhere" but the instructions freeze
    the quick open for a later session, and the do-not-touch list outranks
    (resolution order rule 2). Quick runs DO bank their sealed stack into the
    collection, as a single silent counter jump at the reveal, so the
    persistent total never depends on which track was watched.
36. **Replays never re-bank the collection** (same rule as the jobs counter);
    the fly animation still plays, the number does not move. A replay is
    otherwise identical including glow position and auto-turn order.
37. **Pick-to-reveal caps are measured to the stack presenting.** The stack
    phase is player-paced (like the receipt screen) and runs after the
    engine's timeline, so no beat budget changed and no cap is violated. The
    3s idle default adds ~3s before auto-turn on a hands-off run — accepted:
    the tap path is faster and the caps govern pick-to-reveal, not
    pick-to-receipt.
38. **Flying cards clip at the stage edge** (`#screen-run` is
    `overflow:hidden`): they visibly leave toward the header counter and the
    counter ticks as they go. Accepted over a portal layer — simpler build.
39. **No push this session.** `BoxedPrototypes/` is not a git repository and
    the site repo (`Tvalc/glittercloud-website`) is not present in this
    workspace, so there is nothing to rebase or push from here. When
    vault-next is copied into the site repo: `git fetch && git rebase
    origin/main` first, never force-push, and do not touch `/vault/`,
    `/vault-job/` or `/boxlings/`.
40. **Reduced motion**: the stack ships CSS variants (instant flip, fade-in
    deal, fade-out fly, static tells) mirroring the build's existing rules.
    All states and durations identical; not visually verified this session
    (see method note).

## Verification (recorded pass/fail, as instructed)

Method note: as in the previous session, the review environment could not
composite frames, so runs were driven through the engine's own `tick()` with
a synthetic clock and the DOM sampled directly. The stack phase was verified
two ways: (a) live wall-clock runs while the tab's timers were unthrottled —
real cadences measured — and (b) a virtual-time harness that patches
`setTimeout` and drains the stack's own timer queue deterministically. All
checks below ran against `http://localhost:8648/vault-next/index.html`.

- **Force each tier 20 times (100 runs, debug-panel path, instant speed):
  vault opens every time** — door transform shows the open slide/rotate on
  100/100 including all 20 getaways; all 100 reach the reveal; **stack length
  changes by tier** (observed getaway 2–3, floor 3–4, solid 4–5, grail 5–6,
  lockbox 6–8, matching the bands) — **pass**
- **Debug forcing in isolation** (before the reveal was built): each tier ×20
  → crew results and stack band always consistent, 0 faults; each stack
  length 2–8 forced → 10/10 exact; glow slots 1–6 forced on a fixed
  tier+length → tell lands on the forced slot, best item under it, row still
  a permutation; per-guy `rescued` force → `downedThenRecovered` with a
  recovered window on the forced guy, all three guys; glow slot 8 on a
  3-stack clamps to 3 — **pass**
- **One item glows before anything is turned; identity not knowable until
  turned**: `turnedAtShow = 0` on every observed run; all card backs
  byte-identical (glyph only), the tell class carries the tier alone
  (`tell-<tier>`); same seed replayed with glow forced to slot 1 vs slot 4 →
  identical sealed values and best item, only the glow position moves —
  **pass**
- **Any order + auto-turn**: live run — player turned the GLOWING card first,
  then another; after 3.0s idle the rest auto-turned ascending (14 → 15 →
  35), nothing stalled, reveal reached. Hands-off runs on all five tiers
  (virtual time): order strictly ascending with the glow last, cadence
  400ms lows / 700ms step / 950ms best (measured live: 421/719/967 at 1x),
  getaway uniform 400ms — **pass**
- **Replay-this-seed reproduces the run identically including which item
  glowed and the auto-turn order**: 5 random runs + replay → sealed dumps
  identical in every sealed field including the full stack line (values, row,
  glow slot, best item); the only diff is the beat-depth marker (original at
  `reduced` session-pacing depth, replay forced `full` — spec v2 §2.4, by
  design, same as the previous session's result). Auto-turn order is a pure
  function of the sealed ascending values. Collection never re-banks on
  replay — **pass**
- **Every run yields at least two items**: minimum stack length over 500
  unforced draws and all forced batteries = 2 — **pass**
- **Worst tier is an acquisition**: getaway live + virtual — no `takeover`
  class ever set, no `blackout`, emblem opacity stays 0, no tier name, tell
  present but flat slate, door opens (transform + 0.5 glow), items turn at
  400ms and fly to the collection (+2), reveal copy warm — **pass**
- **Emblem & name after the last turn (non-getaway)**: emblem opacity 0
  until the final turn, ignites ~500ms after it, endcard shows the tier name,
  `end-value` stays empty (counting number gone from sequenced runs) —
  **pass**
- **Collection**: header + pick-meta counters tick per card and persist
  across reloads (localStorage); quick open banks silently (+len, stack not
  shown); replays bank nothing — **pass**
- **Preserved list (§6.5)**: commit (64 hex) shown before pick; Verify PASS
  on the real seed and FAIL on a 1-char tamper; Replay identical (above);
  debug panel extended, nothing removed; building tracker untouched; 5
  How-it-pays cards render (getaway card updated per decision 33); demo tier
  selector ↔ debug force sync intact; Restart mid-run and mid-stack aborts
  cleanly; quick toggle works and quick plays its old untouched ending
  (SOLID + counting 140 observed); CONFIG weights byte-identical
  (`stackLenByTier` added as a new PLACEHOLDER only) — **pass**
- **Colour discipline (grep)**: `--rescue`/#25D0E0 only in rescue rules,
  `--nearmiss`/#FFB020 only in jolt/callout-near rules, both unchanged from
  the live build; `Math.random` only in comments — **pass**
- **Console**: zero errors across the full battery except the by-design beat
  budget overrun asserts on debug-FORCED short exits (grail/window forced
  short — the assert firing is the specified behaviour) — **pass**
- **Reduced motion**: CSS variants ship; **not visually verified** this
  session (no compositing) — recorded as such per decision 40.

## Known placeholders

`stackLenByTier` is new and PLACEHOLDER; the client owns it. Stack item
names/values reuse the existing PLACEHOLDER `prizePool`/`prizeValues` (no
invented prize names, per visual spec §9.5). Card art is placeholder SVG
(bundle / gem / case) — art direction is a later session.

---

# Session 2 — skip and session pacing (2026-08-25)

Scope: skip and session pacing, nothing else. No change to the seal, the
stack draw, the debug forces, the getaway staging or the quick open's own
presentation.

## What was built

**Skip, everywhere.** The engine timeline already had tap-to-boundary and
hold-to-3× (§2.4); those are unchanged. New: the reveal phase is now fully
skippable through stage taps (taps on the stage background — card taps are
turns, not skips, and stop propagation at the card):

- **While the stack is dealing in:** a tap lands the whole stack at once —
  the deal's beat boundary. Nothing turns.
- **After the deal:** the **first** stage tap turns the next item now (the
  next in the sealed ascending order — the same beat the auto-turn would
  play). The **second** stage tap jumps to the final state: everything
  turned, the emblem and tier name said (non-getaway), the collection banked
  and the total shown, straight to the receipt.
- **During the celebration or the fly:** one tap is enough — straight out.
- Nothing is ever unskippable: not the vault opening (engine boundary taps),
  not the final item, not the celebration, not the fly. `finishAll()` is
  idempotent on the emblem (`ctl.emblemDone`) and the bank (`ctl.banked`),
  so a skip can never double-ignite or double-count.

**Session pacing.** After the 5th open in a session the **4-second quick
path becomes the default**; the existing **Full show** toggle restores the
sequenced track. Both the opens count (`vj.session.opens`) and the toggle
(`vj.fullShow`) were already persisted in localStorage and stay so. The
decision is made in `startRun()` AFTER the seal and the stack are drawn, so
pacing is presentation depth only — it cannot touch the tier, the crew
results, the stack, which item glows, or the reveal order (verified: a
quick-shown original and its full replay carry byte-identical sealed stack
lines). **Replay-this-seed always plays the full sequenced track**, ignoring
both the session state and the quick toggle.

## Decisions recorded (numbering continues)

41. **Stage taps skip; card taps turn.** The cards are the designed
    interaction and already stop propagation, so the skip gesture is any tap
    on the stage around them. "Second tap during the reveal jumps to the
    final state" is implemented literally on stage taps (`ctl.skipTaps`);
    card taps never count toward it. A tap that lands the deal counts as the
    first stage tap.
42. **The reduced-depth trigger is superseded, the machinery kept.** Spec
    v2's §2.4 reduced-depth session pacing is replaced by the quick-default
    per this session's directive; the scheduler's depth parameter and
    `buildBeatList` trimming survive untouched (normally unreachable now)
    in case a future pacing tune wants the middle setting back.
43. **Replays now ignore the quick toggle too.** Previously a replay
    re-read the quick checkbox; spec v2 §2.4 says the replay always forces
    the full presentation track, and this session's directive repeats it —
    so `startRun(…, replay=true)` hard-forces the sequenced full track.
    This also makes the debug seed-Replay always show the full show.
44. **`VaultDebug.getEngine` added** (review tooling only, like the rest of
    `VaultDebug`) so a reviewer can assert that taps land exactly on beat
    boundaries.
45. **Quick runs remain presentation-untouched** (still the counting-number
    ending, per the standing do-not-touch); as the new session-pacing
    default they stay fully skippable (their beat boundaries are start and
    end, so one tap jumps to the reveal) and still bank their sealed stack
    silently.

## Session 2 verification (recorded pass/fail, as instructed)

Method note: same as session 1 — no compositing in the review environment,
so the engine was pumped through its own `tick()` with a synthetic clock and
the stack's timers were drained through a virtual-time `setTimeout` patch;
taps were dispatched as real `PointerEvent`s through the live handlers.

- **Open fifteen times in a row, never trapped waiting**: 15 consecutive
  opens driven by stage taps alone, zero waits — sequenced full runs
  completed in 8–15 taps each (one per beat boundary plus the reveal's two),
  quick runs in exactly 1 tap; all 15 reached the receipt, zero errors; the
  collection banked every open — **pass**
- **A tap works at every frame including mid-celebration**: on a full grail
  run, a tap was issued from an arbitrary mid-beat frame before every beat —
  14/14 taps strictly advanced the clock and landed exactly on a beat
  boundary (`engine.boundaries`), never mid-animation. In the reveal: a tap
  mid-deal landed the stack (nothing turned), the first post-deal tap turned
  exactly one item (the lowest — the next auto beat), a tap with all items
  turned but the receipt not yet shown (mid-celebration, emblem not yet lit)
  went straight to the receipt with the tier name shown and the collection
  banked exactly once, and a tap mid-fly (cards in flight) did the same with
  no double-bank; a tap mid-quick-run jumped to its reveal — **pass**
- **After five opens the quick path is default and the toggle restores
  full**: opens 1–5 played the sequenced track, opens 6+ sealed-dumped
  `(quick shown)`; checking Full show on open 8 restored the full sequenced
  track, unchecking on open 9 returned to quick; `vj.session.opens`
  persisted (read 16 after the battery) — **pass**
- **Replay after ten opens still plays the full track**: at 15+ session
  opens, a quick-shown original replayed with no quick marker and
  `beats (full)`, identical sealed stack line (values, row, glow slot),
  finished by taps, collection unchanged by the replay — **pass**
- **Console**: no new errors; only the by-design budget-overrun asserts on
  debug-forced short exits (same as session 1) — **pass**

---

# Session 3 — the temple re-theme (2026-08-25)

Scope: re-theme the fiction and visuals from bank heist to temple raid per
the temple re-theme spec, structure untouched. The structure spec
(`vaultroomdetails.md`) is authoritative and unchanged; no structural logic,
weight, draw, beat or duration was altered (verified by byte-diff, below).
`vault/` untouched.

## Decisions recorded (numbering continues)

46. **Spec file resolution.** The instruction named `vaultretheme.md`, which
    does not exist in the workspace; `VaultJobReferenceRetheme.md` is the
    only temple re-theme spec present and was used as such. The structure
    spec is `vaultroomdetails.md` as named.
47. **What "the two trackers" means in this build.** The live build predates
    the room-structure spec's literal staging (there are no six-beat 4s
    rooms in code; the engine's beat scheduler stages the same information
    differently). The DO-NOT-CHANGE list was therefore read against the
    build as it stands: the bolts (the arrivals payline) and the glyphs
    (the sealed numbers) are the two independent trackers. Nothing in
    `drawOutcome`, `derivePresentation`, `buildStack`, `buildBeatList`,
    CONFIG numerics, `STACK_T` or the caps was touched — the whole region
    from the rng through the scheduler is byte-identical with the previous
    build (verification 7).
48. **Internal ids frozen; display names only.** Tier ids
    (getaway/floor/solid/grail/lockbox), scene ids (roof/lobby/keypad),
    manifest slot keys and localStorage keys are structural and unchanged.
    Display names: RETREAT / THRESHOLD / CHAMBER / SANCTUM / RELIQUARY;
    chambers FIRST CHAMBER / FLOODED PASSAGE / DEEP CHAMBER. The receipt's
    published-odds line shows the display names and states the internal ids
    in the parenthetical.
49. **The journal is the number tracker, live.** It sits in the great-door
    scene (the vault panel), so it is in frame from the first second with
    three sketched empty outlines. `fillSlot()` became the 400ms charcoal
    rub and is idempotent per slot: the live rub fires inside `lockPanel`
    the moment a numbered member's panel resolves (both trackers write in
    the same synchronous call — bolt + glyph within the same half-second),
    and a rescued member's rub therefore lands LATE, after the save, which
    is the temple spec's late-tracker beat. The pre-existing end-beat
    fillSlot cues (locktry/lockfill/radio) still fire and re-state already
    rubbed slots as no-ops; shout-across (radio-out) glyphs land at the
    radio beat exactly as before. The same glyph marks the reliquary's
    inscription band. Numerals appear nowhere on stone or paper — ten
    hand-drawn glyph strokes (`GLYPH_PATHS`) are indexed by the sealed
    lockNumbers.
50. **The temple waking is meterless.** The alarm pip element and its whole
    state machine survive untouched (renderPips/burnPip/resetPips, the
    critical threshold, the zero-cut), but the meter is `display:none` and
    the stages render as stage atmosphere: 3 pips = settled; 2 = dust
    settles heavier (`.stir`, faint wash); 1 = STIRRING (the old redpulse,
    now a slow failing-light pulse); 0 = WAKING (the old strobe, now a
    guttering flash plus a frame tremble). `strobeStage()` is the waking
    tremor and still explains every cut.
51. **Held and visible, always.** The `.lost` filters were lightened
    (grayscale .85, brightness floor .34 at the deepest dim) so a trapped
    member's held pose stays legible for the rest of the run. The old lobby
    out-path walked the member off screen (arrested) — gone: every trap
    ends with the member IN FRAME (hanging from the ledge / at the bars
    waist-deep / bracing the ceiling), not hurt, not mocked. The window's
    held frame (scene p=0.58) now IS the stuck pose, which also makes the
    downed window read as held-and-waiting.
52. **Reliquary visible on every sequenced run.** One presentation cue was
    added (the only scheduling call added anywhere): getaway's `open.g`
    beat shows the reliquary through the opening door at 0.8 of the beat,
    matching the door beat's existing 0.8 showLockbox on other tiers. The
    QUICK path stays frozen per the standing do-not-touch: quick getaway
    still plays its old `shut()` (decision 35 stands), quick runs do not
    live-rub glyphs (their fills come at the quick path's existing cues),
    and the only quick-path change is the callout word THE VAULT → THE
    GREAT DOOR. Contradiction noted, unchanged in kind from decision 35.
53. **Colour discipline kept.** `--rescue` #25D0E0 and `--nearmiss` #FFB020
    are untouched and grep-clean (rescue rules only / jolt+near rules
    only). All torch ambers (#C98A3B, #E8A050, #C9B98E, #F2E2B8, #B9A87E)
    deliberately avoid #FFB020. `--laser` stays as the trap/danger red.
    Real gold (#F4C430) appears only on the lockbox tier treatments and on
    the reliquary's prize, which only exists on lockbox runs.
54. **Manifest hand-edited.** Handler lines rethemed as data in the inline
    manifest (same keys, same variant counts, same {tokens});
    `vault-next/` has no `tools/build-manifest.mjs`, so the generated-file
    header's "do not edit by hand" could not be honoured by regeneration.
    Quick-open gag art untouched (frozen path).
55. **Still not a git repository** — nothing to fetch, rebase or push from
    here (decision 39 stands, re-verified this session).
56. **prizePool PLACEHOLDER names rethemed to artefacts** (pottery, coins,
    carved figures, gold at the top only); `prizeValues` and every other
    CONFIG numeric byte-identical.
57. **Chamber scenes rebuilt, movement clocks kept.** All three scene
    builders were redrawn (daylight break + sun-plate / flooded passage +
    sunken wheel + portcullis / torch + bones + counterweight + descending
    ceiling), but the figure-movement keyframes and caption FRACTIONS are
    the heist scenes' own, so every actionline cue lands at the same
    millisecond as before. Continuous machinery per chamber: drifting dust,
    lapping reflections, torch flicker — all t-driven, all stop dead on the
    resolve, honouring visual spec §3.

## Session 3 verification (recorded pass/fail, as instructed)

Method note: same constraint as sessions 1–2 — the review environment could
not composite frames (browser pane not displayed; requestAnimationFrame
suspended), so runs were driven at instant speed through the live engine,
timed sequences were pumped through the engine's own cue/animator lists with
a manual clock, and the DOM/SVG was sampled directly. The visual halves of
checks 1 and 5 are therefore verified at the markup/signature level and
recorded as such. All checks ran against
`http://localhost:8648/vault-next/index.html`; zero console errors across
every battery below.

1. **The three chambers are distinguishable from a single frame** — at a
   paused frame every chamber carries a mutually exclusive signature set:
   first = daylight-shaft polygons + drifting dust motes + vines +
   sun-plate; flooded = water overlay + 3 rippling reflection paths +
   sunken wheel + portcullis; deep = darkening overlay + torch flame/glow +
   bones + counterweight. Light drains across them by construction (pale
   shaft → teal half-light → near-black + amber). DOM-verified on a live
   frame; not eyeballed (no compositing) — **pass (by DOM signature)**
2. **Every failure leaves a visible stuck member on screen until recovered
   or the run ends** — 133/133 'out' members across the 100-run battery
   (plus 13/13 on a lockbox-only battery): panel in `.lost` (visible
   filter), held-pose geometry present (gap+hands / gate seated at 0 /
   ceiling slab at brace height), figure opacity ≠ 0. The pumped rescue run
   showed the held member visibly downed with both trackers refusing to
   update until the save — **pass**
3. **The door opens on every run including one bolt; forced 20 times** —
   floor (one bolt) forced ×20: door transform open 20/20. Every other
   tier also ×20 (100 runs, 100 unique seeds): open 100/100 including all
   20 zero-bolt retreats — **pass**
4. **The reliquary is visible on every run and opens only on three
   glyphs** — visible 100/100 (every tier, retreat included); lid opened
   on exactly the 20 lockbox runs (8 of them shout-across) and 0 others.
   Glyph independence seen both ways: two bolts with 0–1 glyphs, and 1–2
   bolts with 3 glyphs (radio-out) — **pass**
5. **Mute and blur, watch ten runs, count bolts lit and glyphs written** —
   sound off throughout (default, never enabled); ten unforced runs: lit
   bolt rods and rubbed journal glyphs counted from the rendered marks
   matched the sealed results 10/10. The countable marks are shape+contrast
   (parchment rod slid 18px in a dark housing; dark charcoal stroke on
   aged paper), no text anywhere; blur itself not eyeballed (no
   compositing) — **pass (counts verified; blur by contrast analysis)**
6. **Replay-this-seed reproduces everything identically** — 5 random runs +
   replay: seal dumps byte-identical, journal glyph paths/slots identical,
   bolt states identical, collection never re-banked — **pass**
7. **No structural timing changed from the previous build; beat durations
   diffed** — byte-diff against the pre-session snapshot: the entire
   rng → drawOutcome → buildStack → derivePresentation → buildBeatList
   region is IDENTICAL; CONFIG differs only in prizePool display strings;
   STACK_T / caps / durations identical; of all 128 scheduling calls
   (cue/anim/add), 0 removed, 0 retimed, 1 added (decision 52's getaway
   showLockbox, presentation only). Identical seeds therefore produce
   identical beat lists and durations by construction — **pass**

Also re-verified this session: Verify PASS on the real seed and FAIL on a
1-char tamper; commit (64 hex) shown before pick; the rescue's strict
ordering (failure visible → trackers hold → save → bolt AND glyph land
together 600ms later, the 400ms rub playing late); grep discipline
(--rescue / --nearmiss / no Math.random outside comments).

---

# Session 4 — the text pacing build (2026-08-25)

Scope: a completely text-based playback of the same runs, for judging
pacing without visuals. New files only; `index.html` untouched.

- **`text.html`** — every line lands at the exact millisecond the real
  build fires its cue, prefixed with the engine timestamp. The scoreboard
  (bolts ▮▮▯ · journal glyphs · temple waking) is a sticky text status
  line; beat markers (id + duration, toggleable) print at every beat
  boundary; the receipt carries the full seal + beat table for pacing
  analysis, plus Verify / Replay-this-seed / Copy-transcript. The skip
  grammar is the graphical build's: tap (or Space) = next beat boundary,
  hold = 3×, and the cloth phase takes the same land / turn-next /
  finish-all stage taps with the same 3s idle and 400/700/950ms cadences.
- **`tools/build-text.py` + `tools/text-template.html`** — the text build
  is ASSEMBLED, not forked: CONFIG and the whole rng → drawOutcome →
  buildStack → derivePresentation → buildBeatList core are spliced
  VERBATIM out of `index.html` at build time (21,455 bytes), so the text
  build cannot drift structurally. Re-run the script after any
  `index.html` change.

58. **Same seed, same moments.** Caption fractions, the capAt clock
    shaping (softfail stalls, decider hold, window falter), handler-line
    selection (same `handler.<state>` seed hash) and all cue times are the
    graphical build's; the handler is audible here (quoted italics) since
    text is the whole medium. Counters are session-only (no localStorage)
    so pacing tests never pollute the real build's collection.
59. **Two silent-duplicate cues dropped in text only**: the graphical
    build fires `say('downed')` at both the trap moment and the window
    start, and puts the stakes in both the callout and the handler line —
    inaudible there, a stutter in text. The text build speaks each once.
    Quick getaway still shows its shut door (decision 35 mirrored).
60. **Word density control (client feedback: "too many words coming too
    fast").** Every printable line carries a level: 1 = skeleton (rooms,
    resolutions + trackers, traps, saves, waking, door, reliquary, tier),
    2 = texture (captions, counter dust, ledge arrivals), 3 = flavour
    (handler quotes, CLOSE/CLOSE CALL markers, hints, beat markers).
    The `words` select prints sparse=1 / standard=1–2 / full=everything;
    default is standard. Captions were also cut to ≈5 words each, tracker
    lines compressed to scoreboard form (`THROUGH · bolt 2/3 · glyph ◇
    1/3`), and the per-artefact repeats collapsed to one `× n` line. The
    cue TIMES never move — density only chooses which of them print, so
    pacing measurements stay valid at any setting.

Verification: zero console errors; each tier + quick to receipt 6/6;
replay transcript byte-identical (collection line excluded) with no
re-bank; Verify PASS on the real seed, FAIL on a tamper; pumped grail
rescue transcript shows the trap → trackers-hold → save → late bolt+glyph
write at the same timestamps as the graphical build's cues (same
scheduler, by construction).

---

# Session 5 — re-issued re-theme brief, re-verified (2026-08-26)

The temple re-theme brief was re-issued naming
`vault-job-temple-retheme.md` and `vault-job-room-structure.md`. Neither
filename exists in the workspace; the specs present are
`VaultJobReferenceRetheme.md` (titled "The Temple: Re-theme Spec", whose
own text cites vault-job-room-structure.md) and `vaultroomdetails.md`
(titled "The Vault Job: Room Structure Spec") — the same two documents
session 3 was built from (decision 46). The brief's content is unchanged,
so no new work was required; the build was re-verified instead.

61. **Re-verification, 2026-08-26.** No file in `vault-next/` changed
    since session 4 (timestamps + hash checks). Structural parity re-run
    against the pre-retheme snapshot: draw/scheduler region still
    byte-identical, CONFIG still differs only in prizePool naming.
    `text.html` confirmed in sync with its generator inputs (the on-disk
    size differs from the generator's reported length only by CRLF
    translation). Fresh runtime battery, 43 runs: door open 43/43
    (including 20 forced one-bolt floor runs — check 3 re-run in full),
    reliquary visible 43/43 and open only on the 8 lockbox runs, bolts
    and glyphs matched the seal 43/43, held-and-visible poses 63/63,
    replay seal-dump identical 3/3, zero console errors. All seven
    session-3 pass verdicts stand. Still not a git repository — nothing
    to fetch, rebase or push (decisions 39/55 stand).

62. **Frozen-preview fix (2026-08-26): the run clock no longer depends on
    requestAnimationFrame.** In the embedded Claude preview pane the page
    reports visibility 'hidden' even while displayed, rAF is starved to
    ~1Hz or suspended, and hidden-page setTimeout is throttled to ~1/s —
    so a run froze on its first frame and every click read as dead ("i
    can't click on anything"). Both builds now drive their tick from
    whichever fires first: rAF (foreground, unchanged behaviour) or a
    50ms WEB WORKER ping (workers escape the hidden-page timer clamp),
    with a plain setTimeout as tertiary fallback if Worker creation
    fails. The stack phase's timeouts ride the same worker clock
    (paneTimeout/paneClear). No timing changed — dt still comes from
    timestamps, the beat scheduler and the whole draw region remain
    byte-identical with the pre-retheme snapshot (re-diffed). Verified in
    the hidden pane: both builds at 0.99x wall clock end-to-end through
    the cloth phase (exact 3s idle + 400ms cadence) to the receipt;
    10/10 instant battery unchanged; zero console errors. Note: the pane
    caches aggressively — a stale document can keep running old script,
    so hard-reload (or cache-bust) after edits.

63. **The rescue line is deleted (Makko, 2026-08-26: "completely broken,
    impossible to understand, persists between sessions — get rid of
    it").** The §4 panel-to-panel cyan path (`#rescue-line`,
    `drawRescueLine`) is removed outright: the HTML node, both CSS rules,
    the function and its call in the rescue cue, and the beginRun reset
    line. Two faults motivated it beyond legibility: its hide was a raw
    900ms wall-clock `setTimeout` (predating the decision-62 worker
    clock), so a skip, restart or throttled pane could strand the line on
    screen across runs; and after the temple retheme the "radio call drawn
    as a physical connection" fiction no longer mapped to anything. The
    rescue remains fully staged and readable without it — helper flare →
    reignition → GOT HIM → cyan lock ring — and the action-line copy ("a
    rope drops through the broken light—") still names the save. Visual
    spec §4 step 3 is amended by this direction; §4's "after two runs a
    player knows cyan means a rescue" now rests on the ring, the flare and
    GOT HIM. Cyan stays reserved for the rescue (grep re-run: `--rescue`
    only in flare/ring/callout rules). Verified live on a forced-rescue
    full run: no `#rescue-line` node, no stray stage SVGs, flare fired,
    GOT HIM landed, exactly one cyan-ring panel, run completed to the
    stack, zero console errors.

64. **The reel stays visible — the vault panel wakes on first arrival
    (Makko, 2026-08-26: "it would stay active as soon as one of the little
    people got there; the continuous work on the vault is the
    hold/spinning analog").** Root cause of the complaint: decision 27's
    dial-is-the-reel spin was implemented and never stopped, but the §5
    camera system dimmed and blurred the vault panel like every other
    non-focused panel (brightness .55 + 2px blur; .25 + 4px on the
    decider), so the analog was running invisibly. No session ever
    exempted the vault — a real gap between the recorded decision and the
    render, not a lost mechanic. Fix: `arrive()` now adds an `awake` class
    to the vault panel on the FIRST arrival; from then on it never blurs
    or shrinks again — brightness .82 while a chamber holds focus, .6
    through the deep decider hold (so the dial dragging to a crawl reads
    as the slow-stop), full frame at the takeover as before. §5's "exactly
    one element at full brightness" still holds: the focused chamber stays
    the single brightest thing. Getaway runs (nobody arrives) keep the old
    dimming until the warm open, which matches the direction ("as soon as
    one of them got there"). Verified on a self-driven 2x grail run in the
    pane: awake vault at computed brightness(.82)/no blur after arrival,
    brightness(.6)/no blur with the dial still turning through the hold,
    one focused panel throughout, run completed to the stack. Method note:
    the decision-62 worker clock now drives ticks in the pane, so
    synthetic tick-pumping corrupts the run clock — verification must let
    the build play itself and sample the DOM.
65. **The one-scoreboard pass (Makko, 2026-08-26: "so much happening and
    none of it ties together… when I look at a slot machine I know what
    winning and losing is").** Root cause: five build sessions each added a
    justified signal system and nobody reconciled them — by this session
    the stage carried five partial scoreboards (bright panels, bolts,
    journal glyphs, waking atmosphere, dial speed) plus three narration
    layers, and no single fixed place answered "am I winning." The slot
    grammar's core rule — one scoreboard, one place, always — was never
    enforced. Surgery, approved explicitly after flagging that it deletes
    prior direction:
    - **The door is the only scoreboard.** Every success now answers there,
      identically: bolt draws back, the door panel takes a physical kick
      (`vaultkick`), and the member's share of the haul flies as a
      face-down mini-card from his chamber INTO a visible pile (`.pot`) at
      the foot of the door. A failure sends nothing — the chamber greys and
      the door does not move. Two shapes, every time.
    - **The run builds the very stack the reveal opens.** The pile's final
      size IS the sealed stack length, split across the members who reach
      the door (earlier arrivals in reveal order carry the remainder —
      pure arithmetic on sealed values, replay-identical). On a getaway the
      whole thin haul surfaces at the warm door-open. The reveal then deals
      its row OUT of the pile (cards expand from the pot's position; the
      pot fades as the row takes over) — one object from run to reveal.
      The pile restates information the locks already made public
      (arrivals, banked depth); tier colour still waits for the tell.
      Pile count is END STATE: instant speed and hard skips land the
      complete pot with no flight.
    - **The cross-section tracker is deleted** (buildBuilding / descend /
      markOut and the SVG): a second scoreboard restating the bolts.
      **§6.5's "building tracker" preserve item is overridden by this
      direction.** The run-body grid is now a clean 2×2.
    - **The journal is deleted** from the door scene: a third scoreboard.
      Recovered glyphs now land only on the reliquary's own inscription
      band, which is invisible until the door opens — mid-run progress
      reads on the bolts alone. Pick-screen and reveal copy reworded.
    - **All three word layers are deleted** — the stage callout, the
      per-room callouts and the action line (decisions 24/25 and the
      session-4 pacing work are superseded; flagged and approved). The JS
      sinks are stubs so cue timing and replay comparability are
      untouched; the DOM elements and CSS are gone. §7's zero-text budget
      is restored: the only stage text is the tier name and the item
      values at the end.
    - Ambient (dust, flicker, water, dial) keeps moving and keeps meaning
      nothing; the waking atmosphere and strobe stay (spec v2 §5.1
      mechanics, rare and loud).
    Verified live (self-driven runs in the pane) and instant: chamber→pile
    flights = banked items exactly (grail: 6/6, MutationObserver); pot
    final = stack length on every observed run; door kick on every lock;
    zero text nodes on the stage mid-run; building/callout/actionline
    absent from the DOM; getaway pot 3/3 at the warm open; 25/25 instant
    runs across all tiers reach the receipt; replay seal-dump identical;
    **mute-and-blur proxy, 10 unforced runs: locked chambers = arrivals,
    bolts = min(3, arrivals), pot = stack length on 10/10** — a squinting
    viewer can read who made it, how much was banked, and (from the tell)
    how big the ending is, from fixed positions; zero console errors.


66. **The frame-state pass (Makko, 2026-08-26: "I just can't read the
    tells… impossible to know if something good or bad is happening in
    each frame and how that ladders up to goal").** Root cause, same
    family as decisions 64/65: the camera's dim+blur flattened STATE — a
    locked chamber, a lost chamber and a merely-unfocused chamber all
    read as "dark blurry box" — and the danger beats were 80ms flashes
    (glitch/jolt) that cannot be caught, let alone read. Fixes, all
    honesty-audited (nothing leaks the sealed outcome; §5.2's
    both-paths rule holds):
    - **Resolved states are never blurred.** Locked: brightness .75
      dimmed / .55 deep, ring lit, no blur. Lost: grayscale(1),
      .5/.4/.3, no blur, crack line doubled in weight. At any frozen
      frame: lit ring = made it, dead grey = out, moving+blurred =
      undecided background, brightest = where the camera is. Brightness
      bands: focus 1.0 > door .82 > locked .75 > trouble .7 >
      working-dimmed .55 (the only blurred thing) > lost .4.
    - **TROUBLE is a held state, not a blink.** From the first stall, the
      close-call jolt, or a member going down, until the chamber
      resolves: the panel's travelling arc turns machinery-red at double
      speed and the glass takes a faint red wash. Honest by construction
      — stalls play identically on winning and losing paths, so trouble
      means "strained, still undecided", never the outcome. The 80ms
      glitch/jolt frames remain as punctuation inside it. setState clears
      it on every resolution.
    - **The stake on the scoreboard.** During the decider hold the NEXT
      empty bolt slot pulses white (`.bolt-frame.staked`) — the frame at
      stake is visible on the goal itself while the camera holds. Stake,
      never outcome: it pulses identically both ways, clears the moment
      the bolt draws or the hold ends. Amber/cyan reservations untouched
      (the pulse is neutral white; the trouble red is the existing
      machinery/laser red, already the stage's danger hue).
    - **Reveal tells rank by intensity first, hue second**: flat → faint
      (8px) → breathing (14px, slow pulse) → blazing (24px, fast pulse)
      → sheened (28px + sweep), so the ladder reads without knowing the
      five colours.
    Verified live (forced close + drawn softfail + out + decider on one
    seal, MutationObserver with synchronous computed-style reads):
    trouble held from stall to resolution with computed red arc stroke,
    zero trouble/stake residue after resolution; the staked frame was the
    CORRECT next slot (f2 with two banked); settled filters probe exactly
    as designed and contain no blur on locked/lost/trouble while
    working-dimmed keeps its blur; run completed; zero console errors.

67. **The multiplier and the paytable words (Makko, 2026-08-27).** Two
    additions by direction. (a) **The multiplier**: `CONFIG.stake` added
    (PLACEHOLDER, 100 — the cost of one open in prizeValues units); the
    whole haul's value (sum of the sealed stack) over the stake is now
    shown as "N×" — counting up on the endcard beside the tier name
    (getaway included: the number alone, still no emblem), landed
    instantly by the skip and instant paths, and repeated as the largest
    element on the reveal card ("N× the stake") on every run including
    quick. Pure arithmetic on sealed values — replay-identical; the seal
    dump now prints `total N (M× the stake)`. (b) **Words for the
    shapes**: a fixed LEGEND strip under the stage — paytable glass, six
    icon+word pairs (moving = still working · red = trouble · solid frame
    = through · grey + crack = held · each bolt = one through · the pile
    = your haul) — static, identical every run, never animating. This is
    deliberately a different animal from the narration layers deleted in
    decision 65: those changed with the action; this names the vocabulary
    once. Plus a fixed caption under the reveal cloth ("tap to turn, any
    order · the glow marks the prize tier — not which item") and each
    How-it-pays card now shows its tier's emblem silhouette in its colour
    beside its name, so the end-of-run shape is taught on the pick screen
    with a word attached. Verified: all five tiers at instant — endcard,
    reveal card and seal dump agree to the digit (observed 0.16× retreat
    → 30× reliquary); a live 2x run counts up to the same number the seal
    computed; legend renders 6 items, 5 card emblems, caption present;
    zero console errors.

Artefact names in `prizePool` remain PLACEHOLDER (client owns them). All
scene art is still hand-drawn placeholder SVG in the temple grammar — the
generated-asset pass is a later session. Reduced-motion variants ship for
every new animation (static dust, no gate judder, instant rub) but were not
visually verified (no compositing), same standing as decision 40.

---

# Session 6 — one currency (2026-08-27, "Session A" of the legibility top-3)

Scope: every rendered number speaks stake multiples; nothing else. Chosen by
a 14-persona panel review (catalog + 10 fixes, Borda count; S1 ranked 2nd,
implemented first as the prerequisite). Next up: S2 (win-meter with 1×
break-even notch + session net) and S6 (one grammar at two lengths).

68. **One currency: stake multiples everywhere.** Three units coexisted —
    the paytable priced tiers in "× the reliquary", the receipt/endcard paid
    in "× the stake", and the card faces showed raw prizeValues units.
    Changes, all display-layer:
    - **Card faces** (`.sval`) render `fmtMult(value / CONFIG.stake)`.
    - **The paytable bands are COMPUTED from CONFIG** (`tierPayBounds`):
      lo/hi total-haul bounds mirroring `buildStack`'s clamp shape (len
      band, best from prizeValues, step under the best, fills in strict
      descent), divided by the stake — so a client retune reprices the
      glass automatically and the paytable can never drift from the draw.
      "× the reliquary" copy deleted. Placeholder CONFIG yields a
      continuous ladder: 0.16–0.46× / 0.46–1.1× / 1.5–3× / 5.4–11× /
      22–41×.
    - **The quick path's counting number now counts in ×** (unit-only edit
      to the frozen path, flagged: the anim window and staging are
      untouched; it still counts the PRIZE item, not the haul — that
      quantity split is pre-existing and dies when S6 unifies the quick).
    - **text.html transcript speaks stakes** (`fmtStake` added to the
      template — index's fmtMult is outside the spliced core); seal dumps
      in both builds keep raw values + mult (debug truth).
69. **Verification (recorded).** Same hidden-pane method as decisions 62-66
    (self-driven runs, DOM sampled). Reconciliation: on a live lockbox run
    all 7 card faces === fmtMult(sealed value / stake) exactly
    (MutationObserver capture vs seal dump); endcard = reveal card = seal
    mult on all five tiers (getaway 0.2×, floor 0.67×, solid 2×, grail
    8.4×, lockbox 27×); every observed total inside its computed paytable
    band; quick run endcard counts in × (4.3× prize vs 7.1× haul receipt,
    see 68); sval max width 38px on 74px cards (no overflow); byte-diff vs
    pre-session snapshot: CONFIG identical, the entire engine region
    identical except the single quick-counter display line; text.html
    rebuilt (core 21,609 bytes spliced verbatim), transcript lines show ×
    with zero raw-unit leaks; zero console errors in both builds. Note for
    future sessions: editing `tools/text-template.html` makes the pane
    auto-load the raw template (core missing → `makeRng is not defined`) —
    that error is the template, not the build; verify against the served
    text.html.

---

# Session 7 — the win-meter and the session net (2026-08-27, "Session B")

Scope: S2 from the panel review — one persistent payline with a break-even
notch, plus the session net the panel demanded unprompted (6 of 14 seats).
Presentation only; the draw region is untouched (verified below).

70. **The win-meter fills at the reveal, not mid-run.** The brief's S2 said
    "filling as value banks during the run", but decision 65's standing rule
    is that mid-run chrome may only RESTATE public information — a live
    value total would leak the glyph-decided sanctum/reliquary distinction
    before the tell, which is exactly the honesty line this build defends.
    So the meter is a pure accumulator of TURNED sealed values: it sits at
    0× through the whole run (teaching the notch), pays as each item turns,
    and every skip path (`finishAll`, instant) lands it on the full sealed
    total idempotently. This is also literal slot grammar — the credit
    meter moves at pay time, not mid-spin. Specifics:
    - Fixed chrome between the stage and the legend (`#winmeter`), one
      place, always. Notch at the 1× position with the label "the stake ·
      1×"; running value in ×.
    - Scale: linear from 0 to the notch (40% of track), log to 50× beyond
      it — a retreat reads visibly short, a reliquary reads far past,
      neither pins.
    - Value-neutral colours: parchment fill in a dark housing; brighter
      past the notch (`past` class at ≥1×). No reserved hue touched
      (grep-safe: cyan/amber/laser/tier colours unchanged).
    - HIDDEN on quick runs (`meterReset(!!run.quick)` in beginRun, and
      `meterSet` guards on hidden) — the frozen quick track gets the meter
      when S6 unifies it.
    - Reduced motion: fill transition off.
71. **The session net: `vj.session.net`.** Header now leads with
    "SESSION +N×/−N×" (pick-meta shows it too); accumulates
    `runTotal − CONFIG.stake` once per non-replay run in `finishRun` —
    the single site both tracks pass through — stored in raw integer
    units (no float drift), displayed as a signed stake multiple
    (negative gets a dimmed `under` class, NOT red — red stays the
    danger hue). Replays never move it (same rule as the collection).
    Same persistence semantics as `vj.session.opens`.

## Session 7 verification (recorded pass/fail)

Same hidden-pane method (self-driven runs, MutationObserver + DOM reads).
- **The meter never moves before the reveal**: live 2x grail run — reset to
  0× at beginRun, stack mounted at t+12.1s, first meter write at t+14.2s
  (first turn), monotonic 0.1→0.25→0.45→2.3→7.5×, `past` flipping exactly
  at the 1× crossing, final === seal === endcard (7.5×) — **pass**
- **Skips land it full**: auto-fired stage-tap skip mid-reveal (some cards
  still face down) → receipt reached, meter 2.1× === seal === endcard;
  instant battery across getaway/solid/lockbox → meter === seal mult on
  all — **pass**
- **Session net arithmetic exact**: +6.5× after a 7.5× run; battery
  getaway 0.24× → −0.76, solid 1.8× → +0.8, lockbox 34× → +33 — header
  matched the sum to the display rounding at every step; negative shows
  "SESSION −0.55×" with `under` set — **pass**
- **Quick**: meter hidden and untouched (0× after), net still banks
  (−0.55 → −1.4 on a quick getaway) — **pass**
- **Replay**: net unchanged, meter plays identically to 0.45× — **pass**
- **Structural parity**: xmur3/mulberry32/makeRng/drawOutcome/buildStack/
  derivePresentation/buildBeatList and CONFIG byte-identical with the
  pre-session snapshot (the only near-region diff is the added `net:` key
  in the LS constant, outside the spliced core — text.html regenerated,
  core 21,609 bytes unchanged) — **pass**
- **Console**: zero errors across the full battery — **pass**

Note: `vj.session.net` was zeroed once during verification (to exercise the
negative display); the collection and descents counters were not touched.

---

# Session 8 — one show, two lengths (2026-08-27, "Session C")

Scope: S6 from the panel review, with the client's explicit call ("20s"):
the ~20-second standard show is the default, the long descent is opt-in, and
the quick open is unified into the same grammar. This session DELIBERATELY
changes two things five prior sessions froze — the quick path and the beat
durations — both by direction.

72. **Depth 'standard' — the 20-second show — is the scheduler tune
    decision 42 predicted.** Added inside `buildBeatList` (the first
    sanctioned change to the frozen core since the retheme): flavour beats
    (prio 3) halve, texture beats (prio 2) sit at their floors, the chamber
    act tightens (enc 3200→1800), the door tightens (door 2000→1500,
    open.g 1400→1100, radio 6500→4500, lockfill 1500→1000, signal
    1500→1000, reveal 1000→800). The decider hold is UNTOUCHED — the
    tension beat is the show. Cues land at the same fractions, so the
    staging compresses proportionally (decision 57's fraction rule is what
    makes this safe). Depth selection: standard by default; 'full' via the
    opt-in toggle (rebadged "Full descent") and ALWAYS on replays;
    'reduced' now unreachable, machinery kept. Measured: grail full-exit
    beats 16.7s (was 24.0s), hands-off pick-to-receipt 25.8s worst case
    (includes the 3s idle grace, celebration and fly — decision 37's
    player-paced tail), typical exits land near 20s, tap-through far
    shorter. Standard totals sit under the CONFIG.caps floors; the caps
    only enforce the ceiling, floors are informational — noted, client
    owns the caps.
73. **The session-2 auto-quick rule is superseded (flagged, per the panel's
    C14).** Quick is opt-in only — never a surprise swap at open 6. The
    default at every session depth is the standard show.
74. **The quick open is unfrozen and unified — one grammar, two tempos.**
    The 4-second §5.7 staging keeps its opening cadence (gag included — it
    is charm, not scoreboard), and from the door onward IS the same show:
    - the getaway quick door OPENS (warm in-panel open, thin haul surfaces
      into the pile) — decisions 35/52's noted contradiction is finally
      resolved; `door-shut-v0` now unreachable from any path;
    - pot flights play on quick (`flyToPot` guard removed) — the pile
      fills on every track;
    - the legacy counting-number ending is DELETED (`igniteEnd` and its
      prizeValue count removed — the last divergent ending);
    - every track ends in `beginStackPhase`: quick plays the same reveal
      at `STACK_QUICK_T` (idle 250 · turns 200 · best 420 · deal 40), the
      meter now shows on quick (session-7 hidden flag removed), and quick
      banks through the fly like every run (the silent `bankItems` counter
      jump in finishRun is gone — no double-bank, verified);
    - `durations.quick` 4000→3000 (the cue timeline ends just past the
      last reliquary beat at 2850; cues past `total` would never fire).
    Measured quick end-to-end: ~6.3s getaway with the full reveal (the
    legacy 4s had no reveal). If the client wants it tighter, the knobs
    are durations.quick and STACK_QUICK_T.
75. **The text build mirrors the pacing rules** (its own startRun/depth
    lines are template code, not spliced): standard default, full on
    replay/toggle, quick opt-in only. Its quick transcript still narrates
    the OLD quick staging (shut-door getaway per decision 59) — a known
    lag, next text session. Core re-spliced at 22,646 bytes (the standard
    branch is core, as intended).

## Session 8 verification (recorded pass/fail)

- **Standard depth live**: seal dump `beats (standard) total 16700ms` on a
  grail full exit; instant battery all five tiers at standard, endcard ===
  seal every run; zero overrun asserts — **pass**
- **Full descent toggle**: `beats (full) total 24000ms` with the toggle on;
  **replay with the toggle OFF still plays (full)** — **pass**
- **Unified quick, getaway**: door opens warm, pot 3/3 (= stack length),
  meter visible and ascending on quick (0 → 0.32×), collection banked
  exactly +3 once (2174→2177, no double-bank), endcard multiplier with NO
  tier name (getaway rule holds), receipt 6.3s — **pass**
- **Unified quick, lockbox**: bolts slam, reliquary opens, stack reveals,
  endcard RELIQUARY 34× === seal, 8.3s — **pass**
- **Structural parity**: drawOutcome / buildStack / derivePresentation
  byte-identical with the pre-session snapshot; buildBeatList changed by
  exactly the standard branch; CONFIG differs only in durations.quick —
  **pass**
- **Text build**: grail full run's engine timeline ends 17.7s (standard
  live in text) — **pass**
- **Console**: zero errors across every battery — **pass**

76. **The collapsed-meter fix (Makko, 2026-08-27: "it looks the same").**
    The session-7 win-meter shipped with only a `max-width`; the stage
    centres its children, so the block shrank to fit its absolutely
    positioned contents — zero width, invisible bar, labels overlapping in
    one smudge. Every session-7 check passed because the verification was
    DOM-level (values, classes, timing) in a non-compositing pane; the
    client's eye caught what the batteries could not. Fix: explicit
    `width: 520px; max-width: 92%`, labels moved to normal flex flow (only
    the stake caption stays absolute at the notch), track housing given a
    visible border. VISUALLY verified this time — the pane composites
    again: screenshots confirm the meter at 0× during the run, filling
    past the lit notch mid-reveal (2.1× frame captured), stake-priced card
    faces, the session net in the header, and a full-exit run reaching the
    receipt in ~20s hands-off. Method lesson recorded: any new fixed
    chrome must get a rendered-geometry assertion (offsetWidth > 0 at
    minimum), not just value checks.

---

# Session 9 — the awake door and the tension rim (2026-08-27, "Session D")

Scope: Makko's two asks after seeing the build render — "the 4th panel
actively working" and "the tells in the other panels clearer, build
anticipation." All presentation; the seal, draw and scheduler untouched.

77. **The door is awake from the first frame.** `awake` now lands at panel
    construction, not first arrival — extending decision 64 from "as soon
    as one of them got there" to ALWAYS, getaway runs included (the
    decision-64 note that getaways keep the old dimming is superseded).
    The dial's rest speed rises 14→20°/s and each driven bolt now adds
    12°/s (was 9), so the always-visible wheel reads as working from
    across the room and visibly gains energy with every success — the
    hold/spin analog Makko asked for, escalating honestly on public
    information (arrivals only).
78. **The tension rim — anticipation, honest by construction.** At a fixed
    0.55 of EVERY shown chamber's beat, win and loss alike, the panel
    takes a `tension` class: a neutral parchment rim builds over ~1.1s
    (border + glow) and the live arc quickens (0.9s→0.6s lap). It says
    only "this resolves next", never which way; the resolution snap
    clears it via setState. On the decider it holds into the door's
    slow-stop, handing anticipation to the existing staked-bolt pulse. No
    reserved hue touched (rim is parchment; trouble red, rescue cyan,
    near-miss amber, tier colours unchanged). One cue added per shown
    chamber (fixed fraction — replay-identical by construction).
79. **The states sharpened.** Trouble's red wash .10→.16 and its arc
    thickened (2→2.5); the locked ring gains a drop-shadow so "solid
    frame = through" reads at a squint; lost/held unchanged (already
    unmistakable grey).

Verification (visual, pane compositing): 1x and 0.5x runs screenshot-
confirmed — tension rim building on the focused chamber, lit ring +
glow on a resolved chamber, held-grey distinct, the door panel unblurred
with dial + drawn bolt readable mid-run from the first beats; no
tension/trouble residue at the receipt (class sweep clean); endcard ===
seal (2.2×); zero console errors.

---

# Session 10 — the room grammar (2026-08-27, "Session E")

Makko, after session 9: "it is still impossible to understand what is
happening in an individual room, what I'm supposed to look for to know if
the outcome is going to be good or bad (for the ROOM and the whole VAULT)
— just shapes moving on a screen." Diagnosis accepted: the rooms had no
visible GOAL, no calibrated progress, and no stated worth. Three devices,
all presentation, all riding sealed values:

80. **The room grammar.**
    (a) **The goal halo** — each chamber's mechanism (sun-plate / sunken
    wheel / counterweight) wears a pulsing parchment halo: THIS is what he
    is walking toward. Legend gains its seventh item ("the lit halo = his
    goal").
    (b) **The objective strip** — a fixed line at the top of every chamber
    panel: a mini bolt chip in the door's own bolt shape (the room is
    worth one bolt) plus a progress track driven by the SAME sealed scene
    clock that moves the figure (`setProgress` in the scene animator).
    Filling = working · red = trouble/downed · full parchment = made it
    (CSS-forced on .locked) · grey, stopped short = held. It restates the
    visible walk, never the outcome — on a loss the fill freezes exactly
    where the trap sprang.
    (c) **The bolt flight** — on a success the chip's rod flies from the
    room into the door's next bolt slot (420ms) and the bolt SEATS ON
    ARRIVAL (driveBolt/doorKick/fillSlot deferred into the flight's
    landing); the room's win visibly becomes the vault's win. Failures
    send nothing. End state never at risk: instant speed, reduced motion,
    or zero-geometry (hidden pane) seat the bolt immediately — the flight
    is decoration on top of the same call order. The rod in the room chip
    dims once flown ("it left for the door"); quick runs skip flights
    (their triple slam stands).
    Verified (DOM, pane hidden mid-session): 3 halos, 3 strips filling
    with the clock and freezing at ~0.99 on each resolution, rods dimmed
    on all locked panels, **3 bolt flights observed on a 3-arrival run**
    (MutationObserver), zero stray .flybolt nodes at the receipt, endcard
    === seal (8.1×), zero console errors. The 420ms bolt-seat deferral is
    the only timing change and only when a flight actually plays.

---

# Session 11 — the word and the countdown (2026-08-27, "Session F")

Makko, after session 10: "you can't tell what the characters are WORKING
on… let's use the word 'Working' with a timer bar counting down that
turns red if they fail and green if they succeed." Implemented literally.

81. **WORKING / THROUGH / HELD / TRAPPED, and the countdown.** The
    objective strip's track is now TIME REMAINING: full at the room's
    start, draining on the same sealed scene clock that moves the figure
    (1 − p), so it empties exactly at the resolution moment on BOTH paths
    — running out says "the moment is here", never which way it lands
    (stalls freeze it; the decider's drains into the door's hold). A bold
    label sits beside it: WORKING while live; on the snap it becomes
    THROUGH in green with the bar slammed full green, or HELD/TRAPPED in
    red with the bar slammed full red; a rescue reignition returns it to
    WORKING (`rework()`), then THROUGH on the save. Two standing rules
    overridden BY THIS DIRECTION and noted: (a) the §7/decision-65
    zero-text stage budget — the room labels are the words Makko asked
    for, using the receipt's own vocabulary; (b) a success GREEN now
    exists (`--ok` #46B36E), adjacent to t-floor's tell green #3FB56B —
    the tell ladder reads by intensity first (decision 66) so the
    collision is tolerable, but flagged for the art pass. Quick runs get
    the same words via the shared snap/fail calls.
    Verified: timeline sampling on a clean/out/clean run — WORKING
    counting 100→27→THROUGH·green / HELD·red full bar / WORKING
    100→87→62→THROUGH·green; computed colours confirmed; screenshot
    frame shows WORKING + draining bar on the focused room, THROUGH green
    on a resolved room, the halo'd mechanism, the awake door; zero
    console errors.

---

# Session 12 — the word bubbles (2026-08-27, "Session G")

Makko: "give the characters word bubbles to describe what's going on and
really make the tells explicit."

82. **The callout sinks speak again — as the characters.** Decision 65's
    stubs preserved every call site's cue timing for exactly this reversal:
    `pn.callout(word, kind)` now renders a speech bubble from the room's
    member, and the global `callout()` bubbles from the door (via a
    per-run `stageBubbleFn`). Lines are a fixed (role, word) map
    (`BUBBLE_LINES`) in character voice — goal statements ("the sun-plate
    — I can turn it."), trouble ("that almost caught me—"), traps staged
    as held-never-hurt ("the floor's gone — I'm hanging on!"), successes
    ("it's balanced — through!"), the door's own beats ("one lock to go—",
    "the great door — get it open!", "…it sleeps. we're clear."). One new
    cue per shown chamber (GOAL at b.at+250 — fixed, replay-identical);
    every other line rides a pre-existing cue. Bubble chrome: parchment
    glass, ink text, border tinted by kind — green good / red bad-alarm /
    amber near / cyan rescue — all inside those hues' original
    callout-rule reservations. Hide timers ride the worker clock
    (paneTimeout — the decision-63 stranded-chrome lesson). actionSay
    stays silent: the caption stream was the "too many words" complaint;
    the bubbles speak only at state beats (~8-11 lines per run).
    Verified live: bubble timeline on a rescue+close grail run reads
    GOAL → TRAPPED → GOT HIM → GOAL → CLOSE CALL → THROUGH → GOAL →
    ONE TO GO → THROUGH → THE GREAT DOOR → THE TEMPLE SLEEPS, each in
    its kind tint at its cue moment; screenshot shows the door speaking
    "one lock to go—" beside the WORKING countdown; zero console errors.

---

# Session 13 — the quiet frames (2026-08-27, "Session H")

Makko: "remove the shit circling and flashing around the frames, it's way
too much."

83. **All frame motion deleted.** The travelling arc's live lap (working,
    900ms), its red double-speed trouble variant, and session D's tension
    rim are GONE — the WORKING label, the draining timer and the bubbles
    carry the live state now, and nothing around a frame moves or pulses.
    What survives, all static: the solid parchment result ring on a made
    room ("solid frame = through"), the cyan rescue ring, the red glass
    wash for trouble, and the lost grey + crack. The tension class still
    lands (cue kept, renders nothing — decision-65 style) and the arc
    element remains as the result-ring holder. Legend item reworded:
    "the timer = still working" (was "moving = still working").
    Verified: computed animationName "none" on every arc across a live
    run; screenshot shows a trouble room as still red wash + bubble +
    timer, a through room as quiet ring + green bar; zero console errors.

---

# Session 14 — the timer goes (2026-08-27, "Session I")

Makko: "why does the working timer stop when he is working, our engineer
says he hates the timer, get rid of it."

84. **The countdown is deleted.** Root cause of the "stops while working"
    read: the bar rode the sealed scene clock, which freezes during the
    §8.5 machinery flat-spots (the honest both-paths stalls) — honest,
    but chrome that needs explaining loses. The track and fill are gone
    from markup and CSS; `setProgress` stays as a no-op sink (decision-65
    style) so the animator's call site keeps its shape. The objective
    strip is now the bolt chip + the word alone (WORKING / THROUGH in
    green / HELD-TRAPPED in red); the session-F word grammar, the
    bubbles, the goal halo and the bolt flight all stand. Legend's timer
    item removed. Verified: zero .otrack/.ofill nodes at runtime, strips
    render word-only, mid-run screenshot clean (the takeover frame with
    the door bubble), zero console errors.

85. **The legend is deleted (session J — Makko: "get rid of the legend at
    the bottom with the frame definitions that don't exist anymore").**
    Decision 67(b)'s paytable-glass strip is gone — markup and CSS — its
    definitions half described deleted chrome (the moving arc, the timer)
    and the rooms explain themselves now: the words on the strips, the
    bubbles, the halo, the bolt flight. The stage ends at the haul meter.
    The reveal-cloth caption and the How-it-pays cards are untouched.
    Verified: #legend absent at runtime, mid-run screenshot clean (HELD
    room speaking "I'm pinned here — go on!" with cracked grey state),
    zero console errors.
