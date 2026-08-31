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

## Fork session 4 — the hard-iteration loop (2026-08-27, "iterate until pro")

Makko called out single-pass laziness; this session built a SELF-SERVE
screenshot loop and iterated against real frames:
- **The camera rig**: `?shot=1&tier=..&r1=..&t=8000` auto-starts a forced
  run and pumps the engine's own tick() to any millisecond (virtual-time
  budgets don't drive the worker/rAF clock), photographed via headless
  Chrome CLI (`--headless=new --screenshot`). Review tooling only.
- **Iteration 1 (shell + occlusion)**: framed game stage with vignette +
  faint stone-grid texture; HUD counters as pills; gold gradient title;
  trap occlusion fixed — foreground ground with a hole at the gap, so the
  trapped monster hangs IN the hole gripping the ledge instead of floating
  over a black box; the portcullis re-layered IN FRONT of the monster;
  crew-marker token retired (the monster is the presence; the rescue drain
  ring survives).
- **Iteration 2 (rooms + door, from screenshots)**: the sun chamber's
  floating pill-ledges became a broken CEILING — two heavy jagged stone
  masses with daylight pouring through the hole; deeper wall tone; light
  shaft brightened; fallen column simplified; doorway arch enlarged;
  sun-plate and sunken wheel scaled up ~1.2x with bigger halos; bolt
  housings railed into the guardian arch.
- Verified BY LOOKING: headless frames confirm the acted faces switching
  live (happy Solby at the door, worried faces under trouble), the held
  pose reading as hanging-in-the-hole, the rescue moment, and the full-
  frame door takeover with seated bolts and the cast's heads at the door.

## Fork session 5 — iterations 3-4 (2026-08-27, "you didn't iterate very hard")

- **Iteration 3 — the title screen**: gold THE TEMPLE logo (58px gradient) +
  spaced tagline + **the cast lineup** — Solby, Puddli and Embit standing
  under the logo, bobbing and blinking (figureMarkup reuse in a #cast svg).
  Locomotion lean added in placeFig (tips up to 7° into the direction of
  travel, decays upright on stop; scene-passed held rotations win).
  Keypad slot rack restyled to fitted purple-stone pockets; door
  mini-heads brightened one step.
- **Iteration 4 — the payoff**: per-tier prize ILLUSTRATIONS on the reveal
  card (painted potsherd / oil lamp with flame / carved idol / radiant
  sun-disc with a face / jeweled crown — PRIZE_ART map, tier-generic so
  the sealed name stays the draw), 62px gold-gradient multiplier, 19px
  tier label, a soft radial glow behind the reveal screen. Screenshot-
  verified: the reliquary receipt now reads as a jackpot.
- All rounds screenshot-critiqued through the headless camera rig; pushed
  live at glittercloud.solutions/vault-chibi (commits 23c21e3, 2e6fb75).

Known next steps for this fork: reveal card-back/face art, walk-cycle leg
articulation, celebration confetti scaled to multiplier, room-state
vignettes, and (optionally) raster assets via the figureMarkup seam.

## Fork session 6 — the raster cast (2026-08-28, OpenArt pass)

Makko approved the generated character sheets ("that guy is great"; bar:
"cohesive mobile game, NOT AI slop") and said "make me the mobile game."

- **Assets**: 12 PNGs under `assets/` — {solby,puddli,embit}-{idle,happy,
  worried,trap}, ~80-105KB each at 320px tall, cut from Kling 3 Omni
  sheets (~99 credits total). Slicing pipeline (scratchpad, python):
  near-white bg → alpha, projection grid split, largest-component keep
  (drops detached props/shadows), then targeted scrubs — SOLBY's ropes
  (narrow-row kill), PUDDLI's bar (low-chroma band kill keeping blue
  paws), EMBIT's ground shadows (brightness rule below the lowest bright
  row).
- **Wiring**: `RASTER` map + `rasterImgs()` build four stacked `<image>`
  elements per monster in the SAME local frame as the SVG bodies (feet ≈
  y 5, H=34, trap H=36, width from measured aspect), inside the untouched
  cb-scale/cb-anim wrappers — so the engine's walks, leans, held poses,
  camera cues, bob and the loss-stillness (paused cb-anim) all ride
  unchanged. CSS `.cb-img/.cbi-*` mirrors the acted-face rules with one
  upgrade: .downed/.lost show a dedicated TRAP pose (fists overhead /
  gripping / bracing) instead of standing-worried; .trouble keeps the
  worried pose. `USE_RASTER=true` flag; SVG bodies kept as fallback.
  Door mini-heads and all scene/mechanism SVG untouched.
- **Verified** (headless camera rig + live-tab DOM, pane not
  compositing): 12/12 assets 200, zero console errors; state probe
  default→n, trouble→w, locked→h, downed/lost→t, cb-bob running; frames
  confirm the cast lineup on the title, all three monsters in their
  chambers, the rescue moment (cyan ring + bubble beside PUDDLI's happy
  pose), the HELD room grey-and-still with SOLBY's fists-overhead pose in
  the gap hole, and the 33× reliquary receipt.
- NOT deployed — glittercloud push waits on Makko's in-game approval.
  Environment art (room plates, guardian door, card back, 5 prizes, logo
  ≈ 11 generations) not started: over the ~10 batch threshold, needs an
  explicit go.

## Fork session 7 — the environment pass + the charged tell (2026-08-28)

Makko: "make me the mobile game… it's not cohesive… the tells are still
happening so fast that you can't build any tension." Two workstreams:

- **Environment art** (11 Kling generations, ~99 credits): painted plates
  for all three chambers + the guardian door (`assets/room-*.jpg`,
  `door.jpg`, 1200x540 JPEG, cropped to the scenes' 400:180 frame — the
  flood plate cropped high so its painted waterline lands near y135 and
  the wader reads waist-deep, not drowned), a card back
  (`cardback.jpg`, byte-identical on every card; the tier tell stays
  border/glow tint only), five painted prize cutouts
  (`prize-*.png` → PRIZE_ART via `prizeImg()`, same 68x68 frame), and a
  guardian-medallion title emblem (`emblem.png`, `.temblem` above the
  h1). Scene builders now paint an `<image>` base (per-scene rounded
  clipPaths) and DELETE the hand-SVG scenery the plates carry (gradient
  backdrops, broken-ceiling masses + shaft polys + vines + plants,
  coral + lilypad, crystals + bones, the door's SVG arch + cb-guardian
  eyes). Every rigged element is untouched: machines, grounds +
  occluders, gap/slab/hands, gate, cage/slots/beam/weight, bolts, dial,
  torch + flame/tglow flicker, dust/motes/bubbles/ripples ride ON TOP of
  the paint.
- **The charged tell** (pacing): STACK_T low 400→600, step 700→1300,
  best 950→2200, deal 70→90; on the auto-turn the best card takes a
  `.charge` beat through its whole delay — scale strain + glow bloom
  (chargestrain/chargebloom), cleared on turn, reduced-motion off,
  quick/getaway exempt, player taps still flip instantly and all skip
  taps still work.
- **Verified** (headless rig + live pane): full-frame door takeover with
  the painted arch, all three painted chambers with monsters + machines
  live, title with medallion + gold logo + cast, painted prizes on
  SANCTUM 7.3× and RELIQUARY 33× receipts, computed card-back art
  (fixed a cascade collision: the chibi-skin .sback gradient at the
  bottom of the sheet was overriding the art — layered tint + url
  there), live charge probe measured 2284ms ≈ ST.best on the glowing
  card, zero console errors across all runs. Still NOT deployed.

## Fork session 8 — the slow show (2026-08-28, "no, it's WAY TOO FAST")

86. **Session C's 20-second tune is reversed by direction.** 'standard'
    now STRETCHES instead of compressing: enc 3200→4500, door 2000→3000,
    open.g 1600, reveal 1200; nothing halved, no texture floors. 'full'
    (opt-in + replays) gets its own branch: enc 5500, door 3500. Cues
    still land at beat fractions, so the choreography dilates honestly
    on both paths; the getaway keeps its warm brisk exit; quick
    untouched. `CONFIG.caps` ceilings raised (client direction — Makko
    IS the client here): short 14000 / medium 26000 / full 34000 /
    premium 38000, so the slow show never trims or overruns. STACK_T
    slowed again: low 900, step 2000, best 3200 (the charge beat covers
    the whole 3.2s), deal 110.
    Measured live, hands-off grail full-exit: stack at ~30.1s (was
    ~16.7s), charge 3151ms on the glowing card, endcard at ~43.4s, zero
    console errors, no overrun asserts. Tap-through unchanged — every
    boundary still skippable, so the impatient path stays fast.

## Fork session 9 — the room formula (2026-08-28, "I can't understand it")

Makko dictated the room grammar: enter → FIND the thing that decides the
puzzle (the tell) → work → solve/fail/whiff → SOMETIMES find a parchment
with one code digit → advance to the door. "The tension is 'does my
character get the thing' and 'does he find the secret code'."

87. **The find — the room tell.** Every shown room now stages a container
    (`findMarkup`, per-biome position on the walk path — the roof walk
    already pauses exactly at it) that shakes at 0.18 of the act and pops
    at 0.30: sun-key / pearl-crank / weight-stone. The item's condition
    foretells the SEALED result — fq-good bright + pulsing glow (clean),
    fq-worn dim + flicker (close), fq-bad cracked + grey (out/windowed).
    Honest exactly the way the reveal tell is: sealed information staged
    early BY DIRECTION, replay-identical, never a lie. Bubble lines per
    (role, FIND GOOD/WORN/BAD) in character voice.
88. **The parchment — the code piece.** Only glyph carriers
    (`hasNumber`: clean + downedThenRecovered) surface a parchment
    bearing their ACTUAL sealed glyph stroke (`GLYPH_PATHS[
    pres.lockNumbers[i]]`, drawn at scene build via a new `realResult`
    param — the staging still collapses rescued to the 'out' walk, but
    the parchment markup follows the uncollapsed truth). Clean rooms:
    surfaces at 0.72 of the act, floats away at the snap. Rescued: after
    the save lands (decision 49's late-glyph beat, now visible in-room).
    Decider: as the hold breaks, right before THROUGH. Radio-out glyphs
    stay a door event (unchanged). PARCHMENT bubble + glow; `.parch-out`
    float-away.
    Verified live (DOM probes, real-time runs): findspots ×3 every run,
    shake→open cadence on the sealed beat, fq classes match results
    (radio-out lockbox: clean room good + parchment, out rooms cracked;
    grail close room worn), parchment show/out on the clean room only,
    walk/lean/faces/machines untouched, zero console errors.

## Fork session 10 — the reach pass (2026-08-28, "go research gacha/slots/
pachinko — we're doing none of it")

Research (sources in session log): pachinko reach = escalating staging on
a visible waiting object + a learnable reliability ladder (white→green→
red→gold→rainbow); Genshin wish = one pre-reveal animation whose colour
IS the tell, revealed after a held beat; slots = the scatter tease +
last-reel slowdown + rising pitch — anticipation beats the reward.

89. **The find plays the reach.** Two-stage escalation: small shake at
    0.12 of the act, violent shake + a NEUTRAL parchment pre-glow
    blooming at 0.24 (nothing known yet — pure anticipation), reveal at
    0.36: the item POPS (scale 1.8 → settles 1.3) with a one-shot burst
    whose intensity is the ladder — radiant rays (clean) / pale (close)
    / dull + crack (out). Rising two-tone ticks during the shake and a
    graded reveal chord when sound is on. Intensity-first ladder keeps
    the §6 colour reservations clean.
90. **The parchment plays the scatter.** `parchMarkup` now renders in
    EVERY room: a parchment corner peeks from the mechanism at 0.5 and
    wiggles — the code question is asked every room. A true carrier
    unfurls it (burst + the sealed glyph large, pop-and-settle). A close
    room's corner SINKS back at 0.95 — the honest near-miss. A held
    room's corner freezes with the room (radio-out can still call that
    glyph across — visibly still down there). Rescued: unfurl after the
    save. Decider: unfurl at the hold break; a close decider sinks after
    the snap — the strongest reach lands on the biggest beat.
91. **The door blobs are the sprites now** ("why are the characters
    little blobs at the end") — the mini-head silhouettes at the door
    are replaced by the real happy-pose rasters at door scale (H=24,
    legacy silhouettes kept as the non-raster fallback).
92. **The colour choice is visible again** ("what does the player choice
    do? seems like nothing") — regression from the raster pass: crewHex
    used to tint the SVG bodies. Now the picked colour renders as a
    soft `crew-aura` ellipse under every monster (rooms ×1, door minis
    ×0.75). Cosmetic and honest as ever: the choice picks the descent
    you watch, never the prize. Title lineup (pre-choice) has none.
    Verified live: 6 auras + 3 door sprite images per run; event probe
    shows shake→shake2→open cadence (~540ms per stage), peek in all
    rooms, sink on close rooms and on a close decider after the hold,
    the full whiff arc (cracked item → trap → rescue → parchment) on a
    drawn rescue; door-takeover frame shows the three sprites at the
    arch; zero console errors.

## Fork session 11 — the hero camera (2026-08-28, the Cursor staging audit)

Makko brought a Cursor audit ("four equal postcards force every story to
postage scale"). Half its facts describe some other build (Veo clips /
green screen / cream page / "cue() is a no-op" — none of that is this
codebase), but the camera critique is correct and is this session.

93. **The hero camera.** `focusOn` now also sets `f0/f1/f2/fv` on
    #run-body: the focused panel takes the left ~70% of the stage
    (grid-template-areas, hero spans three rows), the other three become
    a right-rail of pips. The camera CUTS — no tween, a filmic cut per
    beat. Soft/establishing focus keeps the flat 2x2; the takeover
    still owns the endgame; ≤700px stays single-column; classes reset
    in beginRun. Pips: bubbles hidden, status strip scaled .8 — one
    word and the state colour; the hero carries the story (audit:
    "speech only on focus"). Monsters at hero scale are ~4x larger —
    faces read at arm's length.
94. **Contact: he TAKES the charm.** On every solve (room snap, decider
    snap, rescue lock) the found item darts toward the mechanism and is
    gone (`find-taken`, 500ms) — the charm is loot he uses, not UI. A
    held monster's cracked item stays by the box.
    Verified: hero frames (SOLBY walking the sun chamber at hero size;
    PUDDLI at the wheel with bark + EMBIT's pip flashing THROUGH;
    EMBIT worried at hero size with his crimson crew aura), camera
    probe f2→f0→fv+takeover across a live run, full radio-out lockbox
    run to the RELIQUARY endcard, zero console errors.
    NOT DONE from the audit (agreed backlog): grab-pose contact clips
    at the mechanisms (needs a generation round), full-bleed shell /
    thumb-zone HUD, hit-stop juice, portrait re-layout.

## Fork session 12 — two questions, every channel (2026-08-28, "me no
understand how to feel when shaking happen")

Makko couldn't read the find even watching repeatedly — the three-grade
ladder differed only by glow opacity, one channel, invisible at panel
scale. Also the two tensions had collapsed into one: clean ⇔ glyph, so
a bright item answered both questions at once.

95. **Two grades, not three, and the questions decouple.** The item now
    answers ONLY "does he get through": fq-good = clean OR close (room
    will be won), fq-bad = out/windowed (the trap is coming). The
    parchment is the genuinely separate second reveal: unfurl = clean
    (code piece), sink = close (through, but the code slipped away).
    Two hopes, two answers, in sequence, each its own beat.
96. **Every channel fires at once — the monster IS the tell.** On a
    good find: the item leaps up golden with the burst, FX.sparks on
    the panel, the room flashes bright (joyflash), and the monster
    JUMPS to his happy pose for ~0.14 of the act (.panel.findjoy pose
    override, specificity above the state rules). On a bad find: the
    item FALLS, breaks and lies on the floor (finddrop — motion is the
    channel: up = good, down = bad), the room dips dark (dreadflash),
    and the monster slumps to his worried pose (.finddread). Graded
    chords/thud when sound is on. FIND WORN retired from use.
    Verified: joy frame live (Embit mid-cheer at the opened box, room
    flashed); finddread probe shows the class landing with exactly one
    visible pose (w) mid-reaction; zero console errors.

## Fork session 13 — the wordless show + the parchment party
(2026-08-28, "WHY ALL THESE THINGS ON SCREEN WORDS AND SHIT?")

97. **The parchment celebrates like the find.** All three unfurl sites
    (room, rescue, decider) now fire the full channel set: findjoy jump
    to the happy pose, FX.sparks, room flash, chord — a code piece is a
    WIN and looks like one. (No conflict with .locked — both show the
    happy pose.)
98. **Meta chrome leaves the stage.** `showScreen` toggles
    body.in-run: SESSION/COLLECTION/DESCENTS pills and the sound
    toggle hide during a run and return with the lobby (RESTART
    stays). The win-meter drops its words — value "N×" + notch "1×"
    only. The reveal caption is now "tap to turn". Verified live:
    all four chrome nodes display:none mid-run, meter text "30×1×",
    three parchments unfurled on a lockbox run, zero console errors.

## Fork session 14 — the production pass (2026-08-28, "up to 10,000
credits, stop being cheap")

Twelve generations (~110 credits — quality was the constraint, not
spend): contact work poses, painted charms, shell art, UI props.

99. **Contact poses.** {solby,puddli,embit}-work.png — profile,
    hands-gripping poses (image2image on each anchor; PUDDLI needed a
    retake — first take stood upright with a prop). Wired as pose key
    'k' (H=31) with an `atwork` panel class cued over [0.52, 0.84] of
    solver rooms (not the decider — he stands off-mechanism through the
    hold). Cascade: atwork suppresses idle+worried, shows work; the
    reaction and resolved states outrank it; no overlap with finddread
    (bad rooms never get atwork).
100. **Painted charms.** charm-{sun,pearl,stone}.png replace the vector
    find items (sun-key kept its painted burst; stone retake killed a
    literal letter 'R' rune). H=15 in the find frame.
101. **The shell.** assets/backdrop.jpg — hand-painted dark brick wall
    behind everything (takes 1 and 2 hilariously produced a chibi HUMAN
    in a temple and photoreal Angkor faces; take 3 with 'flat cartoon
    brick pattern, no faces' landed). Gem pick buttons
    (gem-{crimson,azure,bone}.png) replace the flat colour chips.
    plaque.png wraps the endcard (plaquewrap, scale-pop on show).
    Hero-grid stretching fixed: align-items:start + pip scenes capped
    at 132px, so the hero panel hugs its content.
102. **Sound defaults ON** (stored OFF respected; AudioContext still
    gated on the first click). Session-F tones now play the find/
    parchment/charge grammar out of the box.
    Verified: work pose live in the hero frame (Embit braced at the
    rack beside his painted stone), brick shell + gems + medallion on
    the title, 6 work-pose images + 3 painted charms in DOM, SOUND ON,
    zero console errors. Still NOT deployed.

## Fork session 15 — THE GEM GAME (2026-08-28, Makko's "stupid simple"
formula: solve the room, win gems, match the door's element)

103. **The mechanic.** Every solver wins TWO elemental gems at the
    solve (ember/tide/bone/sun); they land with a pop in a six-socket
    rack on the door's right column (mirroring the bolts: left = who
    got through, right = what they carry). The door's element hides
    until the finale: on the full-frame takeover the recess CHARGES
    white, SNAPS to its colour with a stage kick, then every gem
    answers — misses die first, matches flare last, so hope survives
    to the final gem. Matches = the sealed tier EXACTLY (floor 1,
    solid 2, grail 3, lockbox ALL — radio-out included since its gems
    = 2×arrivals all matching; getaway one dead scrap): the lotto draw
    is pure presentation of the sealed outcome. `gemPlan(seed, o)`
    rides its own rng fork (seed+'♦gems') so the engine's seeded
    stream is untouched — replay-identical, honest.
104. **What retired.** The parchment/scatter system (markup, cues, all
    three unfurl sites) — the gem rack carries the second tension now.
    The glyph machinery (fillSlot, inscription band, radio staging)
    still runs underneath as deep-lore decoration; receipts, TIER_COPY,
    HOW_COPY and the howto-note all speak gems (rooms list their gem
    colours with ✦ on matches; radio-out reads "GEMS THROWN ACROSS").
    The reveal beat is 3600ms at both depths — the draw lives there.
    Elemental colours (D6455E/3E8FD0/EAE4D4/F2C14E) are a by-direction
    amendment to the §6 reservations — the gem game IS the new tier
    language on the door.
105. **Bug caught in staging:** windowed and decider rooms drop their
    gems in their OWN resolution blocks (after the save / after the
    hold) — the room-loop drop is guarded !windowed && !isDecider, or
    gems landed before the member had actually resolved.
    Art: gemel-{ember,tide,bone,sun}.png (the first "bone gem" take was
    a literal cartoon dog bone; retaken as a moon-white jewel).
    Verified live: drops 2→6 across a grail run, ignite at the reveal
    beat (#EAE4D4 that draw), flare order 0/1→0/3 then 1/3→3/3, endcard
    reached, receipt reads "Three gems burn — but not all of them" with
    per-room EMBER✦/SUN/BONE lines matching the seal, zero console
    errors. Quick runs skip the draw (their own path, unchanged).

## Fork session 16 — the AAA overhaul (2026-08-28, "spend at least 3,000
credits and completely overhaul every element")

Best-of-8 curation on every asset via a manifest pipeline (scratchpad
job.py: thumbnail contact sheets → pick → auto crop/cutout). ~112 images
this wave (~1,010 credits; ~1,368 total across the project).

106. **One painter's voice.** All four plates regenerated with the
    style key "THICK dark ink outlines / bold cartoon linework like a
    chibi monster-collecting game / NOT soft painterly realism" —
    room-sun (take 6/8), room-flood (5/8, crop-biased waterline),
    room-deep (1/8), door (6/8: the guardian's dark mouth-arch backs
    the dial). The soft-painterly v1 plates were the cohesion break;
    reject reel again included surprise monsters in two takes.
107. **Painted props replace the vector machines.** prop-sunplate
    (blushing sun face) rides INSIDE .dial so it rotates; prop-wheel
    inside .wheel (spins); prop-gate (bars-only take) inside .gate
    (drops); prop-scale behind invisible beam/weight sinks (settle()
    keeps working); prop-doordial inside .spokes (the reel-spin drives
    it; rim kept as an invisible sink for shut()). All rig names and
    choreography untouched.
108. **The two-frame walk cycle.** {char}-walk.png strides (best-of-6
    each, shadows scrubbed); pose key 'l'; placeFig toggles .moving on
    the fig from the lean magnitude; CSS steps() alternates idle/walk
    at 0.48s — a stride, not a glide. Any acted state outranks it;
    reduced-motion falls back to idle.
109. **Prizes v2 as one sheet** (5 items per take, take 4/6 sliced by
    column projection into prize-*.png, aspects re-measured), cardback
    v2 (Hearthstone-grade parchment+gold, take 1/8, byte-identical
    backs / tint-only tell unchanged), and the lobby key art
    (title-bg.jpg, take 6/8: the temple gate at sunrise) behind
    #screen-pick under a dark gradient.
    Verified: hero frames show the ink-lined flooded passage with the
    painted gate/wheel/crank and PUDDLI at hero scale, the sun chamber
    find beat, gems accumulating on the door rack, the painted dial
    spinning on the guardian door; lobby = key art + medallion + gems;
    zero console errors. NEXT SPEND (queued to honour the 3,000 floor):
    the video-animation wave — kling image2video clips from the sprite
    stills (~175 cr each, 9 clips ≈ 1,575) to frame-extract real idle/
    walk/celebrate loops.

## Fork session 17 — LEGENDS OF THE HIDDEN TEMPLE pivot (2026-08-28)

Makko: "make this legends of the hidden temple style, an autoplay
platformer through an obstacle course — much more legible."

110. **The dashboard is gone; the course is the stage.** The four scenes
    are no longer a 2x2 of boxes — they are ONE continuous temple
    cutaway laid left to right: three obstacle stations then the great
    door. `#run-body` is now the CAMERA (fixed viewport, overflow
    hidden); a new `.coursetrack` flex row (width 368%, each section
    flex 25% = 92% of the viewport) is the world. `focusOn()` no longer
    swaps grid areas — it PANS the track
    (`translateX(-idx * 92%)`, .85s cubic-bezier) and lights the
    matching lamp. Sections butt together with a carved pillar seam
    (`.panel + .panel::before`) so it reads as one place. A held runner
    stays visibly stuck at his station as the camera travels on — the
    Temple Guard beat, and it preserves HELD-and-visible for free.
111. **The temple map** (`.coursemap`): four lamps under the course on
    a carved ledge — past stations amber, current lamp lit and scaled,
    the door lamp square. Legends' map, and the run's progress bar.
112. **Takeover unchanged in spirit**: on the finale the vault panel is
    lifted OUT of the track (`body.appendChild`) so the door owns the
    viewport; the track fades.
    Engine, cues, scenes, sealed outcome, gem game: all untouched.
    Verified live: geometry probe rb 1106 / track 4048 / sections
    ~1100 / pan -184%; a live frame shows one wide station filling the
    stage (Solby at the sun-plate, next chamber as a sliver, lamps
    tracking). KNOWN OPEN: some states paint a narrow section in the
    scaled preview pane — sizing needs one more pass; portrait rules
    for the old grid were removed (the course is orientation-agnostic).

112b. **COURSE BUG FIXES (same session, after Makko: "half of the next
    one... still not a platformer").** Three real bugs, all found by
    DOM probe not by eye:
    (i) `translateX(-N%)` resolves against the TRACK's width (4x the
    viewport), so every pan threw the world ~4x too far and sections
    landed thousands of px off-frame. Camera is now PIXELS.
    (ii) `layoutCourse()` measured `body.clientWidth` before the stage
    had settled (1012 vs 1100), so sections were short and the next
    room bled in. Now re-measures on rAF + a ResizeObserver, and pins
    width/minWidth/maxWidth as well as flex.
    (iii) the legacy `.panel.focus { transform: scale(1.06) }` was
    still zooming the focused section, breaking the grid — killed
    inside .coursetrack (the camera does the framing now).
    Plus, for the platformer read: a real FOLLOW CAMERA (reads the
    active runner's `_cbx` each frame and centres him, smoothed 0.1,
    MONOTONIC so a course never backtracks), stations ahead of the
    camera hide their runner (`.notyet`), the establishing shot moved
    from the door to the temple MOUTH (a course runs left to right),
    and seams became carved threshold pillars instead of hard cuts,
    with passed chambers only receding to brightness .74 rather than
    blacking out.
    STILL OPEN: the three plates have different floor heights, so the
    ground line does not run continuously across a threshold — the
    biggest remaining break in the one-course illusion; fixing it
    means re-cropping the three room plates to a shared floor Y.

113. **Juice + portrait (same session, pre-pivot, still live):** hit /
    thud punches with a flash rip on every resolution, small stage
    shake on a gem match, hard shake on the door ignite; portrait
    media-query pass for phone.

114. **IP FILTER FINDING (important).** wan2-7 image2video REFUSED
    PUDDLI's walk clip: "IPInfringementSuspect — input data is
    suspected of being involved in IP infringement". Solby and Embit
    passed. The axolotl reads as Pokemon-adjacent to Alibaba's
    classifier. This is a publishing risk signal, not just a
    generation hiccup — flagged to Makko.
115. **Video->sprite pipeline WORKS.** wan2-7 image2video at 720p/2s is
    ~45 credits; ffmpeg 9 needs `-fps_mode passthrough` (not -vsync).
    Solby's 60-frame clip extracted 12 candidates: on-model, centred,
    white bg, real stride. Frames not yet keyed/wired.

## Fork session 18 — THE PARALLAX PLATFORMER (2026-08-28, PLATFORMER-BRIEF.md)

Makko's brief: rebuild the run as a parallax autoplay platformer — one
continuous world, a party you collect, a starter pick that means something,
and PUDDLI retired. Built code-first against placeholder art by direction
("code first, then art"), so the ~1,000-credit art wave lands on a proven rig.

116. **The seam was never in the rigs.** Every chamber already used the SAME
    `FLOOR = 150` inside its own authored 400x180 frame — the ground line
    broke only because each scene painted `assets/room-*.jpg` UNDER its own
    ground rects, and the three plates carry different painted ground
    heights. So the fix was not to re-crop the plates or re-author the
    rooms: the plates moved OUT of the play plane onto the parallax mid
    layer, and butting the untouched station rigs together gives one
    unbroken floor by construction. Every walk keyframe, mechanism,
    find-spot, held pose, gem drop and occluder rode across unchanged.
117. **The world is five layers on one camera.** `#run-body` is the
    viewport; `.world` holds far (0.20) / mid (0.50) / PLAY (1.00) /
    party (1.00) / fore (1.30), each translated by `-camX * factor` from a
    single camera position in world units. Biomes are one tiled strip per
    chamber per layer, cross-faded on camera progress — strip 0 is the
    opaque base and each later strip dissolves in over its own threshold,
    so the layers are always fully covered. The dissolve band is
    deliberately NARROW (`XF_AT 0.66`, `XF_W 0.30`): a wide fade
    double-exposes two chambers and reads as ghosting, badly so with the
    stand-in diorama plates, which are full-detail paintings. The fore
    layer is drawn, not painted — one repeating SVG tile of soft-gradient
    columns and hanging growth, so it is seamless at any level width.
    **Trap re-found:** an SVG background tile needs
    `preserveAspectRatio="none"` or it letterboxes inside its background
    box and its columns render as black slabs floating in mid-air.
118. **COURSE POSITION is not STATION INDEX — the brief's one real
    collision.** A platformer camera must be monotonic, but the sealed beat
    list stages encounters in the REVEAL order (`o.order`, decider last),
    which is not station order: the camera was starting mid-course and
    would have had to backtrack. The level is therefore LAID OUT in the
    sealed play order — course position p holds station `o.order[p]`.
    Three things fall out free: the expedition travels strictly left to
    right; the decider is always the last chamber before the great door,
    exactly where its hold wants to land; and off-screen-resolved stations
    sit at the front of the course, passed and reported early as the
    fiction already said. `focusOn` now speaks positions; `posOf[station]`
    is the inverse. Sealed data is read, never rewritten.
119. **The party line IS the scoreboard.** Joined members run as a trailing
    line behind the leader in their own world-coordinate layer inside the
    play plane (so a member can stand between two stations). `clean` /
    `close` -> JOIN at the solve; `out` -> LEFT BEHIND, the station figure
    simply stays where the existing held staging already put him;
    `downedThenRecovered` -> he starts at his own station and SPRINTS to
    the tail. The line integrates toward its target at 300 world-units/sec
    with a snap-on-large-gap, so a tap-skip or an instant finish never
    leaves it trailing. Verified: **party size == o.arrivals == bolts drawn
    on 45/45 tier x exit x starter combinations.**
120. **THE PICK IS NOW HONEST — it used to move the outcome.** The run seed
    was `serverSeed:pick:nonce`, so the choice was literally an input to
    `drawOutcome` — the exact opposite of what the pick screen promised.
    The seed is now `serverSeed:nonce`; the outcome depends on the seed
    alone, still committed to before the pick and still verified by the
    same `sha256(serverSeed) === commit` check. The pick rotates which
    CHAMBER opens the course (SOLBY -> sun/flood/deep, POTTS ->
    flood/deep/sun, EMBIT -> deep/sun/flood) and therefore which species
    stands at which station. **Proof: 60/60 seeds produce a byte-identical
    sealed dump under all three starters**, and the 100-draw tier
    distribution is identical because `drawOutcome` has no pick parameter
    to give it.
121. **The seal dump now draws its own boundary.** Everything above the
    `—— presentation (the pick) ——` marker is a pure function of the seed;
    below it is starter, course order, species-per-station and the variant
    slots. The variants line is the one thing that legitimately follows the
    pick — a staging variant belongs to its CHAMBER, not to a slot number,
    so rotating the chambers rotates which slots the run draws. Asserting
    against `run.sealedDump` rather than the whole textarea is what makes
    the honesty claim precise instead of approximately true.
122. **One place, one light.** The dashboard pointed the player with
    per-panel brightness (focus bright, the rest `brightness(.55) blur(2px)`).
    Across a continuous world that draws a hard brightness step AND a blur
    boundary straight through the middle of the art at every station edge.
    The camera stopped using it — framing does the pointing now. STATE
    filters stay, because a held chamber going grey is meaning, not camera.
    The decider hold's "near black around one point of light" became ONE
    `.holdveil` vignette over the whole world instead of a per-station
    filter that would cut the place in half. The full-panel result ring and
    crack overlay were authored for a small box and read as stray lines
    stretched across a station — dropped inside `.coursetrack`.
123. **Brace or leap (Task 3).** The missing platformer beat, cued off the
    sealed clock at 0.86 of the encounter: a runner who gets through
    gathers himself and JUMPS; one about to be caught sees it coming and
    braces. The decider gets his against the HOLD instead, since he stands
    off the mechanism through it — the biggest beat in the run, right
    before the door.
124. **PUDDLI -> POTTS.** The species key `tide` and every measured aspect
    ratio stay put; only the file stem moves, so the whole pose/state
    cascade rides across. `POTTS_ART = false` keeps PUDDLI's plates on
    screen as a stand-in; flipping it to `true` when the generated pose set
    lands IS the entire swap. Name chosen by Makko (the terracotta
    pagoda-pot shell).
125. **Bugs caught by probe, not by eye:** the door's arrival figures were
    keyed `mini0/mini1/mini2` — arrival index assumed to equal species,
    which goes wrong the instant the course can rotate (now `mini:<species>`
    read off the station's real occupant); and an EMPTY party at the door
    (the legitimate getaway case) built one phantom figure for a member who
    did not exist and crashed on `.species`, because `xs` fell back to
    `[200]` when `standing.length === 0`. Getaway staging otherwise needed
    nothing: it already pans to the door, so the camera arrives alone —
    Makko's chosen read.

### Session 18 verification (recorded pass/fail)
- Sealed dump identical across all three starters: **60/60 seeds**.
- Party size == arrivals == bolts: **45/45** (5 tiers x 3 exits x 3 starters).
- Course laid out in sealed play order, decider last: **30/30**.
- Picked starter's chamber opens the course: **30/30**.
- Replay -> identical seal: **12/12**.
- **90 unforced runs to completion: zero console errors.**
- Headless frames confirm: level start at the temple mouth, the walk with
  parallax depth, a left-behind member held at his gate as the camera moves
  on, a full party of three at the great door with 3 bolts and 6 gems, the
  reduced-motion variant, and portrait (document width == viewport, no
  horizontal overflow).
- Geometry probe: sections 1100x495 each, track 4400px, party plane
  4400x495 (1:1 with the play plane), layer widths 1760 / 2750 / 5390 =
  `viewW + factor * (levelW - viewW)` exactly.

### PRE-EXISTING DEFECT FOUND, NOT FIXED (out of scope)
A naturally-drawn `short` exit played at `full` depth overruns its band —
**27 of 800 schedules**, all `floor/short/full` and `solid/short/full`, e.g.
15900ms against `caps.short` 14000ms. This is a session-8 slow-show artifact
(`full` sets enc 5500 / door 3500 while the short cap stayed at 14000) and it
predates this session: `buildBeatList`, the depth branches and `CONFIG.caps`
were not touched here. It bites on REPLAYS and with the "Full descent"
toggle on. The overrunning beats are priority 0/1 and never trim, so the only
fixes are raising `caps.short` or lowering the `full` durations — both CONFIG
numerics, which the brief forbids changing. Flagged for Makko's call.

### NOT DONE — the art wave (approved as phase 2)
Tileable far/mid strips per biome (the stand-in mid layer is the old diorama
plates, which do not tile — the repeat seam is visible), a fore plate set,
and POTTS's six poses (idle / happy / worried / trap / work / walk).
~110-130 generations at best-of-8, ~1,000-1,300 credits. Not deployed.

## Fork session 19 — THE SEARCH BEAT + THE OPENART WAVE (2026-08-28)

Makko: the room formula is "enter → puzzle → solve → **and then, walking out,
he can stop and look around** → if he finds the thing, a super bonus with an
awesome animation." Plus: stop shipping hand-drawn frames and UI, make it in
OpenArt, and give the characters **real animations** when they solve and when
they find something. ~15,000 credits authorised.

126. **THE HIDDEN THING WAS ALREADY IN THE SEAL.** The search does not roll
    anything: whether he finds the relic shard is `hasNumber(result)` —
    `clean` and `downedThenRecovered` carry a code piece, and always have.
    The engine has been filling the door's inscription band off exactly this
    bit since the original build (it was `fillSlot`, called silently inside
    `lockPanel`); it was simply never staged anywhere the player could watch
    it happen. Moving that call to the moment he FINDS it changes nothing
    sealed and buys the whole beat:
      - all three shards recovered  <=> **lockbox**  -> the super bonus
      - three through, one shard missed <=> **grail** -> the real near miss
    A member who is caught never searches, because he never walks out.
127. **The search is a per-member state machine in the party line**, not a new
    beat — the beat list is untouched. On joining he goes
    `walkout -> search -> react -> catchup -> inline`: he walks past the
    mechanism to a spot near the threshold, STOPS and looks around (620ms,
    a slow sway), the room answers (760ms — shard or shrug), then he sprints
    to the party tail. `snap()` resolves every pending search at once, so a
    tap-skip or an instant finish can never leave the door's band short:
    the shard landing is END STATE, not decoration.
128. **THE SUPER BONUS FIRES OFF THE BAND, NOT THE SEARCH.** First wiring hung
    the trigger inside the search reveal, which silently missed the one tier
    that most deserves it: on a **radio-out lockbox** only one or two members
    reach in person, and the last shards are called across by the radio beat,
    so the band completed without any search ever firing. Caught by an
    assertion, not by eye (`seed12 fired=false band=3 tier=lockbox`). The
    trigger now lives in `fillSlot` itself via `setOnFull` — a full band is
    the lockbox by the seal, whichever way the shards arrived.
129. **Real drawn celebration cycles.** Each monster now has a five-frame
    jump-and-cheer strip — anticipation crouch, coil, launch, airborne peak
    with both arms up, settle — packed as one horizontal sprite strip and
    played with CSS `steps(5)`. **The frames share ONE baseline**: they are
    cut from a single generated row with a common vertical crop, never
    per-frame bbox trimming, so the jump arc lives in the ART rather than
    being faked by a transform. A species without a strip still gets the CSS
    squash-and-stretch leap, so the system is purely additive.
    Two wiring traps: the legacy `.leaping .cbi-h` rule re-showed the happy
    still ON TOP of the cycle (now scoped with `:not(:has(.cb-cheer))`), and
    the same species appears both at its station and in the party line, so
    the clipPath id needs a counter or two identical ids collide.
130. **THE PLATES LEFT THE PLAY PLANE FOR REAL.** Six purpose-authored
    parallax strips (far + mid per biome), each generated so the far-left and
    far-right edge are the same column — they genuinely tile under
    `repeat-x`. The stand-in diorama plates are gone. `PLX_HAVE` is the whole
    switch, so a missing strip still falls back rather than rendering empty.
131. **Painted floors.** The ground was a flat SVG rect per chamber, which
    read as a dead grey band the moment real painted parallax went in behind
    it. Each biome now has a hand-painted stone strip tiled through an SVG
    `<pattern>` at 120x30 user units, so the masonry keeps its natural size at
    any station width. The band is still y=FLOOR..FLOOR+30 everywhere, so the
    ground line is exactly as continuous as before — only the paint changed.
    The sun chamber's gap occluders take the same pattern, so the trap hole
    still reads as a hole.
132. **POTTS is real; PUDDLI is gone.** Full six-pose set generated
    (idle / happy / worried / trap / work / walk) plus his cheer cycle, and
    `POTTS_ART` flipped to true. The axolotl that tripped
    `IPInfringementSuspect` is off the board entirely.
    **Scale trap:** POTTS carries a tall pagoda shell, so normalising his
    TOTAL height to the cast's shrank the actual crab to about two-thirds the
    others. `RASTER.sc` is a per-species multiplier that sizes the BODIES to
    match; POTTS sits at 1.16.
133. **Curation stayed best-of-8 on every asset.** Contact sheets are built
    locally and read as ONE image per batch, which is what makes an eight-take
    curation affordable. Two takes were rejected for character drift on the
    cheer sheet — the sheet that "looked best" in isolation was a different
    animal from the established SOLBY, and only a side-by-side against
    `solby-happy.png` caught it.

### Session 19 verification (recorded pass/fail)
- Sealed dump identical across all three starters: **40/40 seeds**.
- Party size == arrivals == bolts: **45/45** forced (5 tiers x 3 exits x 3 starters).
- Shard band full <=> lockbox: **45/45** forced, **60/60** natural.
- Super bonus fires exactly with a full band: **45/45** forced, **60/60** natural.
- **Zero console errors** across all 105 runs (excluding the known pre-existing
  beat-budget overrun recorded in session 18, which is unchanged).
- Cheer cycle verified live by DOM probe (strip visible, pose stills hidden,
  `steps(5)`, `--cw` = strip width / 5) and by frozen-frame captures via a new
  `&cheer=N` review hook.

### Spend
~1,080 credits this wave (13 best-of-8 batches at 2k). Balance 22,398 -> 21,534.

### NOT DONE — still hand-drawn, next targets
The **UI and chrome** are still CSS/SVG: the stage bezel, HUD pills, the win
meter, the temple-map lamps, speech bubbles, the starter plaques. So are the
lockbox/reliquary case props at the finale, which now look unrefined against
the painted door (visible as flat dark rectangles in the takeover frame).
Also not done: a drawn SEARCH cycle (the look-around is currently a CSS sway)
and a drawn shard-found reaction distinct from the cheer.

## Fork session 20 — IT WASN'T A PLATFORMER (2026-08-28)

Makko: "how is it that you just rebuilt the same thing we already had instead
of building a platformer?" He was right, and one grep proved it.

134. **THE DIAGNOSIS: there were THREE runners, not one.** Every station owned
    its own `.fig.guy`, and each played a canned keyframe walk INSIDE ITS OWN
    400-unit box — all nine paths started at x=30 and ended near x=362 of
    their own frame:
        `placeFig(guy, kf(pose(p), [[0.08,30],[0.32,120],...,[0.84,362]]), FLOOR)`
    Sessions 18-19 gave that a scrolling camera, a continuous floor, real
    parallax and a party line that faked the continuity between boxes. None
    of it touched the runner layer. It was a **dolly track over three
    dioramas**, which is exactly what it looked like.
    The structural blocker: a station's SVG clips to its own box, so a figure
    living inside one physically CANNOT leave it. That is why the party line
    had to be bolted on as a separate layer in the first place — the fix was
    always to move the CAST out, not to add another layer beside it.
135. **One runner, one path, one level.** All nine per-station character paths
    are neutered by a single line — `const placeFig = () => {};` shadowing the
    global inside `buildScene` — which leaves every MECHANISM keyframe (dial,
    wheel, gate, cage, dust, ripples) completely intact while removing the
    character from the station entirely. The cast now lives in the level-wide
    play layer and the lead position comes off `RUN_PATH`: a single monotonic
    time->world-x curve built from the SEALED beat map, 16 units to 1368
    across the full 1600-unit level. Four anchors per shown station — enter,
    run up, cross, exit — and the DECIDER's crossing is anchored to the HOLD
    rather than his encounter beat, which puts the longest hold in the run on
    a runner frozen one stride short of the last obstacle before the door.
136. **THE HAZARDS ARM ON EVERY PATH.** The real tell that this was never a
    platformer: a chamber's hazard only ever moved on the FAILURE path. The
    floor gave way solely when the runner was doomed, so a clean run had
    literally nothing to get past. `armObstacle` now arms the hazard as he
    closes on it whatever the seal says — the slab tips and the hole opens,
    the portcullis drops to slide height, the ceiling comes down to duck
    height — and the sealed result only decides whether he clears it or it
    closes on him.
137. **The verbs.** Getting past costs a physical action, driven as a
    continuous animator across the crossing window rather than a pose swap:
    JUMP the hole (parabolic y, up to 34 units), SLIDE under the portcullis
    (rotated flat, stretched long), DUCK the descending ceiling (squashed
    wide). Each has its own silhouette and its own pose.
138. **A doomed runner is STOPPED BY the obstacle.** First wiring let the lead
    path carry him straight through the thing that was supposed to stop him —
    he ended up standing calmly past a portcullis that had just "caught" him.
    `blockAt()` pins his x a stride short of the hazard while the lead
    position keeps advancing, so the rest of the party visibly runs on
    without him. His verb also caps at 0.45: the action he was mid-way
    through never completes.
139. **Caught means caught AT the obstacle.** `losePanel` now calls
    `cast.caught()`, which puts him at that hazard's own caught position — in
    the hole gripping the ledge, behind the bars, braced under the ceiling —
    greys him, pauses his idle rig, and leaves him there for the rest of the
    run. The camera runs on past him, which is the correct read for a course
    you travel forward through: a held member ends up BEHIND you.

### Session 20 verification (recorded pass/fail)
- Sealed dump identical across all three starters: **40/40 seeds** (the runner
  rebuild is presentation only; nothing sealed moved).
- RUN_PATH strictly monotonic in both t and x, starting at the level mouth and
  ending at the door: **40/40 seeds**.
- Every runner ends where the seal says — `out` => held AT his obstacle,
  otherwise in the line — and party size == arrivals: **45/45** forced
  combinations (5 tiers x 3 exits x 3 starters), **zero** failures.
- **Zero console errors** across the battery.
- Runner position sampled against each obstacle's world x at its verb-window
  midpoint: exact match on both non-decider stations.

140. **Review tooling: `&seed=` pins the server seed.** Every capture before
    this was taken against a fresh random seed, so a timestamp read off one
    load landed on a different beat on the next — which is why several
    "wrong" frames were actually correct runs photographed at the wrong
    moment. Captures are reproducible now.

### STILL NOT DONE
The UI and chrome remain CSS/SVG (stage bezel, HUD pills, win meter, map
lamps, speech bubbles, starter plaques), as do the reliquary case props at the
finale. No drawn SEARCH cycle yet — the look-around is still a CSS sway. The
run is also still a fixed-speed traversal: he never actually accelerates,
stumbles, or recovers, so there is no *momentum* in the platforming yet.

---

## Fork session 21 — THE PLATFORMER REBUILD (2026-08-28, PLATFORMER-BRIEF +
## THE-TEMPLE-GDD)

Brief: kill the puzzle verb, build real platformer traversal, make the level
dense, and land an art wave. **Built in `vault-temple/`, not `vault-chibi/`** —
see decision 141.

141. **TWO SESSIONS WERE EDITING THE SAME FILE.** A peer Claude session was
    given this same kickoff prompt and was patching `vault-chibi/index.html`
    concurrently. It was caught by a whole-file diff showing `driveMachine`
    code this session did not write, and confirmed by cross-session message.
    The file on disk was BROKEN at that moment — the peer's `driveMachine`
    had landed with all four `armObstacle` call sites still live, and because
    the throw escapes the animator loop in `tick()` before `scheduleTick()`,
    **the engine died at 4617ms on every run**. Makko chose a fork; the peer
    then stood down and restored `vault-chibi/` to the pristine build
    (md5 `f72e001bc33e41cfa5ac97de66c010c4`). This fork started from a
    byte-identical copy of that same pristine build, so nothing of the peer's
    work is inherited and nothing of theirs was clobbered.

### Phase 1 — the puzzle verb is gone

142. **`atwork` is cut.** Two cues put the runner's hands on the mechanism for
    a third of every encounter (0.52 → 0.84 of the beat). That one cue is what
    turned this into a diorama with a walk cycle, and it is deleted along with
    its four CSS rules. The `-work.png` plates survive in `RASTER` — a
    hands-up gripping silhouette is a better BRACE than it ever was a work
    pose.
143. **The machine and the hazard are ONE quantity, on the sealed clock.**
    `armObstacle` is replaced by `machineDrive(svg, kind, strain, release, t)`
    plus the two end states `machineHeld` / `machineGone`. `strain` is how far
    the machine has slipped from holding, and it IS the hazard arming: the
    plate tipping is the floor opening, the wheel losing grip is the gate
    creeping to slide height, the counterweight riding up is the ceiling
    coming to duck height. There is no second system to keep in sync.
144. **The decoupling that mattered was in the CLOCK, not the code.** The
    machinery was already driven by `sceneClock[i](t)` and session 20 had
    already removed the character from the station, so the brief's expectation
    that decoupling would be "the real work of the phase" was not correct
    about this codebase. What WAS coupled was the arming WINDOW: 0.58 → 0.82
    of the beat, which is exactly when the runner closes on it, so the hazard
    was effectively armed by his approach. It now strains from 0.05 and is
    fully armed by 0.70 — the player watches the pit open while the runner is
    still most of a chamber away. The decider's machine strains from his own
    encounter beat right through the hold, which is the longest "about to
    know" in the run.
145. **A REAL BUG: the hazards did not arm on every path, contrary to decision
    136.** `machineDrive` is now the ONLY writer of hazard geometry. The scene
    `update()` functions were writing `.slab` / `.gap` / `.gate` / `.cage` as
    well, and because the master animator is registered AFTER the arming
    animator, `update()` won every frame. Consequences, both on the `close`
    path: the flooded passage pinned its portcullis fully UP (`gateY(...)` ran
    unconditionally every frame), so there was nothing to slide under and he
    played a slide under open air; and the sun chamber opened its pit
    UNDERNEATH an intact slab. One writer, no race.
146. **Every machine reaches an end state on every path.** An off-screen
    station resolves through `report()` without ever running an arming
    animator, so `lockPanel` / `losePanel` drive the machine to its end state
    themselves. A rescued member's machine ends `gone`, not `held` — the
    hazard DID take him and the save is him being pulled back out of it, not
    the machine relenting. Caught by assertion (8 mismatches), not by eye.
147. **The copy was the failure mode written as dialogue.** Every per-chamber
    bubble line had him operating the mechanism — "the sun-plate, I can turn
    it", "a pearl-crank, made for this wheel", "balance the counterweight",
    "the wheel turned, through!". All rewritten to a runner reading a hazard
    ahead of him. The status word `WORKING` → `RUNNING`.

### Phase 2 — traversal

148. **THE RUNNER DID NOT RUN.** The single biggest finding of the session and
    it is not in the Known-traps list. Traced live over a full `solid`/`full`
    run: `leadX` advanced 22 → 101 world units while the visible monster sat
    at `wait@134` the entire time. EVERY monster including the starter was
    parked at his own obstacle from frame one and only snapped onto the lead
    position at 0.62 of his encounter beat — and snapped BACKWARDS, 134 → ~106.
    For the first ~8 seconds of the level the lead position advanced with
    nobody rendered on it at all. Session 20 moved the cast into the play
    plane and gave it one continuous path; it never put anyone ON that path
    until the beat said so.
    Fixed three ways: the picked starter begins at the LEVEL MOUTH and owns
    the lead from frame one (GDD §7, "your starter is standing there, he
    starts running"); a chamber's own monster takes point BY POSITION, the
    moment the expedition physically reaches where he is waiting, so there is
    no jump-cut; and when nobody is on point the HEAD OF THE PARTY occupies
    the lead, so the level is never running itself with an empty space out
    front.
149. **THE MONSTER'S REACTION — THE GDD'S PRIMARY TELL CHANNEL — RENDERED ON
    NOTHING.** `findjoy`, `finddread`, `leaping` and `bracing` are applied to
    the station PANEL and styled `.panel.<state> .cb-img`, but the station
    figure was retired when the cast moved to the play plane; the sprite on
    screen is `.pm`, which had no rule for any of them. Proved by toggling
    each class and reading computed style on the visible sprite — identical
    output in all five cases (`pmi-n` 1, `pmi-h` 0, `pmi-w` 0, scale animation
    `none`). Decision 96 ("every channel fires at once — the monster IS the
    tell") and decision 123 ("the platformer's most legible moment") were both
    no-ops on screen. `cast.react()` now drives `pjoy` / `pdread` on the
    figure that actually renders, and the reaction plays OVER his stride.
150. **Real jump arcs.** The verb was one sine on y with a static CSS squash
    pinned per verb by `!important`, so every jump was the same shape from
    launch to landing — a pose swap with the body floating. It is now five
    beats driven per frame off one normalised `u`: anticipation crouch (0 →
    0.18), launch (→ 0.30), airborne on a real parabola (→ 0.62), landing
    impact squash (→ 0.80), recovery. The squash is written to the scale
    wrapper's inline transform; the old `!important` rules survive only as the
    reduced-motion fallback. A runner the seal says is caught still caps at
    u 0.45, so his action dies in the launch.
151. **The item container is a question block.** It was a chest on the floor at
    a fixed spot (120 / 140 / 215 in chamber units) that opened by itself
    while the runner was somewhere else, so the "contact" never happened. It
    is now a carved block hanging at head height, placed at HIS OWN x at the
    sealed reveal moment (read off `RUN_PATH`, so still a pure function of the
    seal), and it bonks upward off his head with a flash when he hits it.
152. **The secret spot is a hop, not a stop.** He used to plant his feet and
    sway for 620ms — the one rule this build is not allowed to break. He now
    takes a quick hop over the spot, still travelling, and the room answers at
    the top of it.
153. **The party line eases to its slot instead of snapping.** Snapping was
    invisible until the point man changed, at which point the whole file
    shifts one slot in a single frame — 21 such pops measured on a grail run.
    Also `blockAt` now stops a doomed runner just short of where the hazard
    will hold him, because `caught()` was teleporting him up to 51 world units
    FORWARD into the crusher.

### Phase 3 — level density

154. **The level is dense now.** `MINOR` is a per-biome prop vocabulary (sun:
    rubble / lintel / crack / loose stones / light shaft; flood: puddle /
    debris / lily pad / low arch / reeds; deep: bones / sagging slab / low
    arch / bats / vines), laid out by `minorLayout` from its OWN rng fork
    (`seed + '#minor' + kind + from`), exactly the way `gemPlan` does, so the
    engine's seeded stream is untouched and a replay lays out an identical
    level. None of them decides anything and none carries a tell — which is
    precisely why they can be this loud. Keep-out zones hold them off the
    hazard, the governing machine and the item block.
155. **Crossings are driven by the EXPEDITION, not the point man.** First
    wiring hung them on `pointSt`, which left every stretch between one
    chamber's monster falling in behind and the next taking over completely
    untouched — 5 of 10 props crossed on a grail run. Off `leadX` it is 8 of
    10, and the micro-verb (hop / duck / splash) lands on whichever figure is
    at the front. A real obstacle verb always outranks a micro-verb, so the
    two can never fight over the same body.
156. **The approach to the great door was 400 bare units** and now carries the
    last chamber's biome, because the temple does not change character between
    the final hazard and the door — it just gets grander.
157. **The pit was a flat black rectangle** with square corners, reading as a
    hole cut in a wall. Redrawn with broken masonry teeth on both lips, a
    shaft falling away into black and the two courses of stone the collapse
    exposed. It is Mario's first primitive and it has to read as depth from a
    moving camera.
158. **The brightness seam is gone.** Decision 122 established that the camera
    stops pointing with per-panel brightness across a continuous world, but
    `.coursetrack .panel { filter: brightness(.74) }` survived it and drew a
    hard vertical light break down the middle of the frame at every threshold
    — visible in every capture taken this session before the fix. State
    filters stay, because a held chamber going grey is meaning, not camera.

### Phase 4 — the art wave (PARTIAL — see NOT DONE)

159. **SOLBY TRIPS THE IP FILTER. This is the session's biggest open item.**
    `wan2-7` refused his run clip outright: `IPInfringementSuspect`. POTTS and
    EMBIT passed. Looking at the plate, the classifier is right and it is a
    real publishing risk, not a generation hiccup: an orange bipedal lizard
    with a cream belly and a FLAME ON ITS TAIL TIP is Charmander's silhouette
    and palette almost exactly. This is the same filter that retired PUDDLI in
    session 17, and this time it is the flagship character and the default
    starter.
    A redesign is generated and curated: SOLBY keeps the amber sun-gecko
    identity and his sunrise crest becomes the signature — a wide fan of flat
    golden spines radiating around the skull — and the tail flame is replaced
    by a flat carved GOLD SUN-DISC MEDALLION. No fire anywhere on the
    character. `assets/solby-v3-idle.png` and `assets/solby-v3-run.png`.
    **NOT WIRED**, deliberately: his other five plates are still the original
    design and mixing them would put two different characters on screen in the
    same run. Needs Makko's call before the rest of the pose set is generated.
160. **CURATION AGAINST THE CAST OVERTURNED THE PICK, exactly as decision 133
    warned.** In isolation the best SOLBY redesign was a beautifully drawn
    lizard on all fours. Side by side against POTTS and EMBIT it was plainly a
    different animal — realistic proportions against the cast's big-head
    chibi. The pick moved to the take with the right proportions and a weaker
    crest, and a second round upgraded the crest and the tail medallion on top
    of those proportions. The sheet that looks best alone is still, reliably,
    the wrong one.
161. **THE BRIEF'S ANIMATION PIPELINE IS THE WRONG ONE FOR THIS CAST, with
    receipts.** `wan2-7` image2video held the characters beautifully and
    produced NO LOCOMOTION — 12 clips across POTTS and EMBIT gave a gentle
    idle bob with a wildly animating tail flame and almost no leg travel. The
    contact sheet is unambiguous. It also billed at ~125 credits a clip, not
    the ~45 the brief assumed (`duration: 2` does not reduce the charge).
    The pipeline that actually shipped in session 19 was never video: decision
    129's cheer cycles came from a GENERATED ROW — one still image containing
    N deliberate keyframe poses — which is why `solby-cheer.png` is 1140x340
    and not a stack of 720p video frames. Cycles are generated as sprite-strip
    stills through `kling-3-omni` image2image at 2k (same 9 credits as 1k;
    resolution is free on this model), and the strip is sliced by column
    projection through ONE shared vertical window. Real keyframes beat
    interpolation here, and it is roughly a fifth of the price.
162. **The slicer is the asset.** `scratchpad/slice.py`: white-key → shadow
    kill → column-projection band find → ONE shared vertical crop for the
    whole row → largest-connected-component keep per frame. That last step is
    what finally removed the ground-shadow ellipses the models draw under
    every pose (the colour rule alone could not separate them from the cast's
    near-black ink), and it also takes the fragment of the neighbouring pose
    that a tight column split clips in at the edge. Best-of-8 earns its keep:
    only 4 of 8 EMBIT takes, 4 of 8 POTTS takes and 1 of 8 SOLBY takes split
    cleanly into six bands.
163. **Run cycles are drawn and wired for POTTS and EMBIT.** Six-pose strips
    played with CSS `steps(6)` through `RUNCYC` / `runMarkup`, mirroring the
    cheer-cycle machinery — same lesson, same shared baseline, so the body's
    rise and fall is in the art. A species without a strip keeps the old
    two-frame idle/walk toggle, so the rig never depends on the art existing.

### Session 21 verification (recorded pass/fail)

- Sealed dump identical across all three starters: **40/40 seeds**.
- 100-draw tier distribution identical across all three starters: **PASS**
  (getaway 22 / floor 46 / solid 26 / grail 5 / lockbox 1, all three).
- Replayed seed → identical seal dump: **12/12**.
- Party size == arrivals == bolts: **45/45** forced (5 tiers x 3 exits x 3
  starters).
- Every machine reaches the end state its station's sealed result requires
  (`out` or windowed → gone, otherwise held): **45/45**.
- **Zero real console errors across the 45-run battery** and across the
  reduced-motion, portrait and desktop runs. The only asserts seen are the
  known pre-existing beat-budget overruns (6 of 45), all on debug-FORCED short
  exits — counted separately by the harness so they can never mask a real
  error.
- THE ONE RULE, measured over full real-time runs on five tier/starter
  combinations (~1,700–2,000 sampled frames each): **empty-screen frames = 0**
  on all five, and **longest stretch with the front runner not advancing =
  0ms**. Before this session he sat still for the first ~8 seconds of every
  run.
- Density: median gap between minor-hazard clears **757–1392ms** across three
  tiers, against the brief's 1.5–3s target (the decider hold is excluded — the
  GDD's one allowed silence).
- Run cycle proven COMPOSITING, not merely present: `opacity 1`,
  `animation-name runplay`, `animation-timing-function steps(6)`, `--rw`
  32.59px, rendered 825x137 = 6 cells, and **still poses hidden underneath
  (stillsVisible 0)**.
- Rendered geometry on chrome (`offsetWidth > 0`): win meter 520, coursemap
  1100 with 4 lamps, bubble 83, run-body 1106x526. Portrait 390px: document
  width == viewport width, **no horizontal overflow**.
- Reduced motion: `runimg` animation-name resolves to `none`; zero errors.

### Credits

Spend this session: **2,373 credits** (21,534 → 19,161). Of that, ~1,500 went
on the twelve `wan2-7` clips that produced no usable locomotion — recorded
here as a real cost of finding decision 161 rather than written off. The rest
is 5 best-of-8 `kling-3-omni` batches.

### NOT DONE — and it is a lot

**The art wave is well short of the brief's 6,000-credit floor.** The honest
reason is throughput, not unwillingness: OpenArt allows roughly two concurrent
generations, and every asset is upload → generate → poll → download → slice →
curate against the cast → wire → re-verify. At best-of-8 that is one asset
family per several minutes of wall clock, and the ~70 batches the floor
implies did not fit in this session. What is missing:

- **SOLBY's full pose set on the v3 design** (idle / happy / worried / trap /
  walk / cheer, plus his door mini-head, title-lineup figure and starter
  plaque). Blocked on Makko approving the redesign — see decision 159. This is
  the top of the list; the game should not ship the current SOLBY.
- **SOLBY's run strip is generated and sliced but not wired**, for the same
  reason.
- **Jump / brace / duck / hop / land-recover strips for all three.** The verbs
  are all real animator-driven arcs now, but they still play on stills; the
  drawn frames would land straight into the same `RUNCYC`-style seam.
- **Minor hazard props are hand-drawn SVG**, not painted. They read at speed
  and they are biome-distinct, but they are the weakest art in the level.
- **The chrome is still CSS/SVG** — stage bezel, HUD pills, win meter, temple-
  map lamps, speech bubbles, starter plaques, and the lockbox/reliquary case
  props at the finale. Unchanged from session 20's list.
- **The hazards themselves** (portcullis, crusher slab) are still the old
  props; only the pit was redrawn, and that in SVG.
- No drawn SEARCH cycle. Still a CSS hop.

### PRE-EXISTING DEFECT, STILL NOT FIXED — NEEDS MAKKO'S CALL

The beat-budget overrun recorded in session 18 is unchanged and this session
found it is slightly broader than recorded: it bites at `standard` depth too
when the exit is `short`, not only at `full` (measured 6 of 45 forced
combinations, e.g. `floor/short` at 15700ms against `caps.short` 14000ms).
Both fixes are still CONFIG numerics — raise `caps.short` or lower the
encounter/door durations — which the brief forbids. Flagged, untouched.

### Deployment

NOT deployed. Built in `vault-temple/`; `vault-chibi/` is byte-identical to
the pristine pre-session build and `vault-next/` was never touched.

---

## Fork session 22 — IT STILL LOOKED LIKE A SLIDESHOW (2026-08-28)

Makko, on the session-21 captures: *"are you building a platformer like Mario
Brothers or something that looks like a shitty children's slide show?"* He was
right, and the reason I had missed it is recorded here because it is the more
useful half of the lesson.

164. **THE METRICS PASSED AND THE FRAME STILL FAILED.** Session 21 verified
    that the runner never stalls (0ms), that he jumps on a real arc, and that
    something is cleared every 757–1392ms. Every number was true. But they all
    measured EVENTS PER SECOND, and none of them measured whether the screen
    looks like a level. It did not: one monster on a flat strip in front of a
    painted wall. A verification suite that cannot fail the thing the client
    can see in one glance is not a verification suite, it is reassurance.
165. **THE ROOT CAUSE WAS ONE CONSTANT.** `PLAY_FLOOR = 150`, one value, for
    all 1600 world units. Mario 1-1 is VERTICAL before it is anything else —
    blocks at head height, stair-steps, platforms you land on top of and run
    along. With a single unbroken ground line, a character can have a perfect
    run cycle and a perfect jump arc and still read as a walk cycle over
    wallpaper, because his silhouette never moves against the background.
    Worse, session 18 had recorded that one shared floor height as a FEATURE
    (decision 116) because it made the station seams line up — the thing that
    made the geometry easy is the thing that made it flat.
166. **The ground is a terrain profile now.** `terrainFor` lays out raised
    stone masses per chamber from the run's own rng fork (replay-identical, the
    `gemPlan` precedent), and `groundYAt(x)` is the surface the cast's feet
    actually stand on. Heights are chosen against his own jump — nub 18, low
    14, step 22, ledge 30, stack 40, against a 38-unit obstacle jump — so
    nothing is ever placed higher than he can reach. `place()` takes a rise
    instantly (he is on top of it) and eases a fall (he rides down off the
    edge), which is the difference between landing on a ledge and teleporting
    onto one.
167. **THE FIRST TERRAIN PASS PRODUCED ZERO PLATFORMS** and I nearly shipped
    it, because the level looked exactly as flat as before and the code was
    "done". Two compounding mistakes: the pieces were 52–104 units wide with a
    12-unit clearance, and between the hazard, the governing machine and the
    item block there was not one gap in a 400-unit chamber wide enough to hold
    one. Then the loop, on a clash, jumped a full piece-width PAST the spot
    instead of sliding along it, so it threw away the gaps that did exist.
    Fixed by narrowing every piece, tightening clearances, retrying smaller
    kinds at the same spot, and advancing only to the end of the blocking zone.
    4 platforms → 10.
168. **Retry order is by HEIGHT, not width.** Ordering the retries widest-first
    made `low` (54 wide, 14 tall) win nearly every spot, so ten platforms went
    in and the ground still barely moved. A tall piece gets first refusal on
    every spot now; the silhouette is the whole point of having them.
169. **Figure and ground.** Painting a platform with the same floor pattern as
    the band behind it made it a cut-out rectangle of wallpaper. The mass is
    the same stone pushed darker so it separates, the top face is the brightest
    edge in the chamber (the line the eye reads as "stand here" from a moving
    camera), and it casts a shadow at its own foot so it sits ON the floor
    rather than in front of it.
170. **THINGS COME TOWARD HIM NOW.** Every object in the level was static
    scenery he travelled past — there was not one approaching object in 1600
    units. 1-1's pace does not come from the pipes, it comes from the Goombas
    walking AT you: a closing gap you did not choose. One mover per shown
    chamber (a stone rolling down the terrace, a log riding the flood the wrong
    way, a boulder in the deep), armed when the expedition gets within 250
    units and closing at a speed that makes them meet. Always cleared, no tell,
    decides nothing — pure pressure.
171. **The lintel was a slab hanging in mid-air.** It had no posts, so it read
    as a bug rather than as something to duck. It is a leaning doorway with its
    own uprights on the ground now. Also added FURNITURE_ZONE so terrain stops
    growing out of the chambers' exit arches and carved recesses.
172. **The density measure was re-cut honestly.** The old test counted only
    minor-prop crossings, which after the terrain pass undercounts the level
    badly — most of what he clears is now geometry. Measured across props,
    terrain climbs and movers together.

### Session 22 verification (recorded pass/fail)

- Sealed dump identical across all three starters: **40/40 seeds**.
- 100-draw tier distribution identical across all three starters: **PASS**
  (22 / 46 / 26 / 5 / 1, all three).
- Replayed seed → identical seal dump: **12/12**.
- Party size == arrivals == bolts: **45/45**; machine end-states **45/45**.
- **Zero real console errors** across the 45-run battery and the reduced-motion,
  portrait and desktop runs (the 6 known pre-existing budget-overrun asserts on
  debug-forced short exits are counted separately and are unchanged).
- THE ONE RULE, five tier/starter combinations at ~1,700–2,000 sampled frames
  each, re-run after every motion fix: **empty-screen frames 0**, **longest
  stretch with the front runner not advancing 0ms**, **backward steps 0**, and
  **worst backward step 0.0 units**. The only position snap left in the whole
  battery is the catch itself (1011 → 1062 with `phase: held`) — the hazard
  taking hold of him, which is meant to be a snap.
- Blank-sprite frames (no visible image on any live figure): **0** across four
  tier/starter runs.
- **Density, counting all three kinds of clear**: median gap **1493–1750ms**
  against the 1.5–3s target, mix **7 climbs / 3 movers / 3–4 props** per run —
  i.e. most of what he clears is geometry, which was the point.
- Movers: 3 built, **3/3 converged on the runner**, zero errors.
- Terrain: 7–10 platforms per level, tops spanning 110–136 against a floor of
  150, so the ground genuinely undulates.

174. **THREE MOTION BUGS, ALL FOUND BY ONE PROBE ASSERTION.** Adding
    "worst backward step in a single frame" to the traversal probe turned a
    number I had already written off (`backwards = 18-49`, assumed to be smooth
    easing) into three real defects, every one of them a visible pop:
    (i) `blockAt` pinned a doomed runner with `min(leadX, stopX)`, and because
    the stop point is a beat fraction while his x comes off RUN_PATH, on a fast
    run he was already past it — so the hazard SNAPPED HIM 46 UNITS BACKWARDS
    into itself. Clamped forward: the hazard stops him where he is.
    (ii) The walk-out to the secret spot targeted a fixed point 78 units past
    the obstacle, but by the time he joins, the lead has reached the chamber
    threshold — so he TURNED ROUND and walked back up to 112 units to search.
    The spot is `max(m.x + 24, ...)` now; he never doubles back for anything.
    (iii) The locomotion timestep was clamped at 250ms, so a single slow frame
    moved a member 85 world units in one step. Clamped to 64ms — a stutter now
    looks like a stutter instead of a teleport.
175. **AND ONE REGRESSION I CAUSED FIXING THEM.** The first "never reverse"
    rule let a member who was ahead of his slot dawdle forward at 16 units/sec
    while the lead ran on at ~45, so the party slid out of frame behind the
    camera — **404 frames with nobody on screen at all**, on a test that had
    read 0 an hour earlier. He keeps pace with the group instead (82% of the
    lead's own step) and lets the slot close on him. The lesson is the same one
    as decision 164: the assertion is only worth what it measures, and a fix
    that satisfies one assertion can break another that was already green.
176. **AND A FOURTH, WHICH ONLY THE INSTRUMENTED PROBE COULD HAVE NAMED.**
    After three fixes the worst backward step was still 46 units, twice a run.
    Recording WHICH figure and WHICH phase pair produced it gave the answer in
    one line: `{from: 611, to: 564.8, phA: "wait", phZ: "point"}`. The
    positional handover added this session was correct, but the old
    beat-fraction `takePoint` cue was left in as a fallback and fires at 0.62
    of the encounter — at which point the expedition can still be 46 units
    short of where the chamber's monster is standing, so taking point snapped
    him backwards into the party. `takePoint` now refuses until the party has
    actually reached him. A probe that reports a number tells you something is
    wrong; a probe that reports the state transition tells you what.
177. **AND A FIFTH, WHICH THE FIX FOR THE SECOND ONE CREATED.** Making the
    search spot `max(m.x + 26, ...)` per frame meant the target RECEDED exactly
    as fast as he closed on it, so he never arrived and simply kept walking —
    a party member measured at world x **5788 in a 1600-unit level**, still in
    phase `walkout`. The spot is now pinned ONCE, at the moment he joins. Three
    of the five motion bugs this session were introduced by the fix for the
    previous one, which is the honest shape of this kind of work and is why
    every fix got a re-measure rather than a look.
178. **A BLANK-SPRITE ASSERTION now guards the pose cascade.** The cast's
    poses are a stack of opacity rules with `!important` on both sides, and the
    run cycle added another layer of them (`:has(.cb-run)`). A state
    combination nobody wrote a rule for renders NOTHING while every value check
    passes — which is precisely how session 19 shipped an invisible win meter.
    The probe walks every live figure every frame and fails if no image inside
    it is both non-transparent and non-zero-width.

### THE FILMSTRIP PASS — what single frames were hiding

Makko, on the session-22 build: *"the animations are all fucked up, there's a
ton of overlapping UX, the characters overlap."* All three were true, and none
of them were visible in the way I had been looking.

180. **SINGLE STILLS AT MOMENTS I CHOSE IS NOT LOOKING AT THE GAME.** Every
    capture up to this point was one frame at a timestamp I picked, usually the
    beat I had just built. Overlap, clutter that accumulates, and anything that
    only appears between beats is invisible to that. Sampling a run at a fixed
    cadence and reading it as a strip surfaced six distinct defects in one
    image. The filmstrip is now the default way to review a change.
181. **THE PARTY LINE OVERLAPPED ITSELF, AND IT WAS ARITHMETIC.** A figure is
    `asp * H * scale` wide — about 0.81 * 34 * 1.5 = 41 world units — and
    PARTY_GAP was **27**. Consecutive members were always going to sit a third
    of a body inside each other. The cast is also 34% bigger now (FIG_BOOST):
    at 34 units against a 180-unit chamber the runner was a small thing in a
    large empty room, which is a large part of why the level read as scenery
    with a sprite on it. Gap is derived from the resulting body width, not
    guessed.
182. **AND MY FIRST MEASUREMENT OF IT WAS WRONG.** The overlap probe used
    client rects, and a run-strip `<image>` is SIX CELLS wide — so every pair
    came back "100% overlapping, 945px" whatever the truth was. Measured in
    world units instead. The real figure was 47 units — a whole body — between
    a `catchup` member and a `follow` member.
183. **THE FILE IS ORDERED BY POSITION, NOT BY JOIN ORDER.** That 47-unit
    overlap was structural: a member walks out and searches AHEAD of the party,
    so when he finishes he can be in front of the man holding the front slot —
    and with the never-reverse rule he then simply parks there, one body on top
    of another. Slots are assigned by who is actually furthest along, so the
    man in front IS the front of the line. 2,349 overlapping frames -> 495.
184. **THE LINE MAKES ROOM FOR THE MAN IT IS ABOUT TO REACH.** The last case:
    between chambers nobody is on point, so the party head rides at leadX — and
    the next chamber's monster is standing still at his own obstacle, so the
    moment the party arrives the two are in the same place. Reserving the front
    slot while he is still ahead drops it to **0 overlapping frames** on both
    test runs. A member who ends up ahead of his slot now eases off
    proportionally (28% of the lead's pace when badly ahead) instead of holding
    a flat 82%, which had left two bodies stacked for the best part of ten
    seconds.
185. **A MONSTER WAS STANDING INSIDE THE MACHINE.** POTTS waits a stride short
    of his hazard, which is local x 211 in the flooded passage — and the sunken
    wheel occupies 178–224. He stood in the middle of the mechanism with the
    wheel drawn across his body for most of the run. The waiting spot now moves
    in front of the machine when the natural one collides with it.
186. **THE VEILS WERE AUTHORED FOR A SMALL PANEL.** A station is the whole
    frame now, so the near-miss jolt flooded the entire screen with amber over
    warm art through `mix-blend-mode: screen` and came out as a **full-screen
    magenta wash** that read as a rendering fault. Inside the course they are a
    masked pulse from the edges. Decision 122 dropped the full-panel ring and
    crack for exactly this reason and simply missed the veils.
187. **THE PORTCULLIS HAD NOTHING TO COME OUT OF.** Its housing was 38 units
    wide against a 56-unit gate and the rails stopped short of the ceiling, so
    parked high all that showed was the spearheads on its bottom rail — a row
    of blue spikes floating in the passage. Full-width recess, rails the whole
    drop, and the gate CLIPPED to its slot so it is genuinely inside the wall
    until it descends. Fading it was the wrong fix and looked like a bug.
188. **SPENT ITEM BLOCKS LEAVE.** One hangs in every chamber and all three were
    still on screen at the end of the run, competing with the three things that
    decide it. Each fades once its own chamber resolves.
189. **THE GOAL HALOS ARE GONE.** A pale ring around each mechanism, from when
    the mechanism was a destination the runner had to reach. It has not been a
    goal since the puzzle verb was cut in Phase 1, and at station scale it
    rendered as a smudge across the art.

190. **THE PARALLAX STRIPS NEVER TILED.** Decision 130 recorded that the six
    far/mid strips were "generated so the far-left and far-right edge are the
    same column — they genuinely tile under repeat-x". That is not true of any
    of them. Measured: the difference between a strip's first and last column
    against the difference between two random interior columns — sun mid 10.5
    vs 19.4, flood mid 8.8 vs 22.1, deep mid 16.6 vs 16.4. A seamless tile
    would be near zero. They are MIRROR TILES now, `[image | flipped image]`,
    which joins exactly at its own centre and at the wrap by construction
    whatever the content is (wrap difference 0.00 on all six) and doubles the
    repeat period as a bonus. No regeneration needed.
191. **THE MOVING VERTICAL SEAM WAS THE FOREGROUND TILE, AND IT WAS MINE FROM
    SESSION 18.** The fore layer's SVG tile put a 34px dark pillar hard against
    x=0 with a gradient fading rightward to transparent — so every 760px the
    layer jumped from fully transparent straight to 78% black. One hard
    vertical edge, repeating the length of the level, sliding at 1.3x, which is
    exactly the "seam that moves" in the captures. The pillar sits in the
    middle of the tile now and fades out both sides, so both edges are
    transparent and it wraps by construction.
192. **A SEAM DETECTOR, calibrated against the art.** Score every column of the
    background band by its horizontal gradient and compare the sharpest against
    the frame's median. The calibration is the important half: the painted
    colonnade itself peaks at 9.8x, so a threshold below that would fail on
    correct frames forever. Worst edge went 16.4x -> 11.9x, and the two peaks
    that survived the first fix turned out to be the stage bezel, not the
    world — the scan insets past it now.
193. **AND TWO OF MY OWN FIXES WERE WORSE THAN THE BUG.** Giving the portcullis
    a housing to emerge from produced, first, a flat black rectangle floating
    in mid-air (the hardest edge anywhere in the frame) and then a stone block
    that filled with the FLOOR pattern — which is anchored at y=PLAY_FLOOR, so
    it sampled the mossy part and read as a fish tank hanging from the ceiling.
    The right answer was no housing at all: two rails and a clip, so the gate
    descends from above the play plane and the painted ceiling behind it is
    where it came from.

194. **THE RUNNER WAS INVISIBLE FOR THE WHOLE OF EVERY JUMP.** Makko:
    *"the animations don't flow from one to another."* He was being generous.
    Sampling a beat at ~7fps instead of every 1.3s showed the character simply
    GONE for ~400ms stretches — at the item block, through every climb, and
    through every jump. Cause: `.pm.onpoint:has(.cb-run) .pmi` is (0,4,0) and
    outranks `.pm.vair .pmi-h` at (0,3,0), so during a jump the run strip was
    hidden by the verb rule AND the pose meant to replace it was hidden by the
    strip rule. Nothing left to draw.
195. **AND THE VERIFICATION THAT WAS SUPPOSED TO CATCH IT WAS MEASURING THE
    WRONG THING.** The blank-sprite assertion from decision 177 read each
    `<image>`'s OWN computed opacity and never walked its ancestors — so a
    sprite inside a group at opacity 0 counted as visible and the check passed
    vacuously on every run while the runner was invisible on screen. This is
    the same class of mistake as the session-19 win meter, made again, by the
    probe written to prevent it. Effective visibility now multiplies opacity up
    the ancestor chain and honours display:none.
196. **AND IT FAILS BOTH WAYS NOW.** Once it could see properly it found the
    other half immediately: TWO poses drawn on one body — `solby3-happy` +
    `solby3-worried` under `pdread+vair`, `happy` + the cheer strip under
    `foundit`, the trap pose plus a verb pose under `held+vduck`. Hundreds of
    frames per run. That is the overlap that needs no instrumentation to see.
197. **ONE AUTHORITY FOR THE POSE.** The cause of all of it was a dozen
    independent CSS rules each forcing a sprite visible with !important, where
    any two state classes that happened to be on at once both won. `poseKey()`
    now decides in ONE place, in priority order — held > celebration > verb >
    reaction > run cycle > idle — and writes `data-pose`; the last block in the
    stylesheet shows exactly that sprite and hides everything else. No
    specificity war is possible because only one rule can win.
198. **MY OWN FIX WAS THE LAST THING IN THE WAY.** The `:not()` chain I wrote
    to break the first specificity war scored (0,15,0) with !important and then
    outranked the pose authority itself, blanking the runner in `follow` +
    `moving` — 28-90 frames a run. Deleted. Three separate attempts at this
    cascade each fixed one hole and opened another; the lesson is that the
    answer to a specificity fight is never a more specific selector.
    Result: **0 invisible frames and 0 double-drawn frames** across four
    tier/starter runs, where the same probe read 46-1571 before.

## THE CANVAS REBUILD (2026-08-29)

Makko showed a recording of `vault-chibi/beats.html` — a separate prototype in
this workspace, built on this session's art — and said: rebuild toward it, it
does not have to look the same, it has to be that quality.

199. **THE QUALITY GAP WAS ARCHITECTURAL.** beats.html is ONE `<canvas>` drawn
    in immediate mode. index.html was ~40 nested DOM/SVG layers whose
    appearance was decided by a CSS cascade. Every defect chased this session —
    two poses on one body, the runner invisible through every jump, tiles
    seaming, veils flooding the frame — is structurally impossible in immediate
    mode: draw order IS z order, pose is whichever image you drew this frame,
    and there is no inheritance to lose. The run stage is a canvas now.
    Phases 1-3 had already turned the level into DATA (run.terrain,
    run.minorAll, run.movers, machine strain, cast world positions), which is
    exactly what a renderer consumes, so the port was additive: the DOM world
    is still built and measured for layout, it just no longer paints.
    THE SEALED ENGINE IS UNTOUCHED — the renderer only reads.
200. **The layering recipe is lifted from beats.html**: far plate at 0.22x, a
    warm tint over it that unifies everything, the mid plate at 0.55x, one
    light shaft, a vignette, then a floor that is deliberately DARKENED so the
    brightest thing on screen is the cast and not the ground. Stride cell is
    tied to distance travelled (`x / 12 % cells`), not to a timer, so the run
    cycle can never slide against the movement.
201. **THE CAMERA IS DIRECTION, NOT TRANSPORT.** Makko: *"it's impossible to
    tell if I should be excited about anything."* Correct, and it was not a
    rendering fault — nothing in the show ESCALATED. One camera distance for
    the whole run, a clear and a catch landing with identical weight, and
    reactions that were single frames gone before you could read them. The
    camera pushes now: 1.00 running, 1.12 on approach, 1.24 on contact, 1.38
    on the decider hold — the tightest shot in the run on the beat that decides
    the tier — and the vignette closes down with it. He sits at ~38% of frame
    so there is always road ahead; a runner centred in frame reads as standing
    still.
202. **Impact.** A hit-stop freezes the PICTURE for 70ms on a clear and 120ms
    on a catch (the sealed clock keeps running underneath, so nothing about
    the schedule or the outcome moves), plus a weighted shake, dust off the
    landing, and a colour flash. A loss now lands heavier than a win instead
    of exactly the same.
203. **The old visibility probe is obsolete and now reports a false failure.**
    It walks the DOM party figures, and the DOM world is `visibility: hidden` —
    so every frame reads as "invisible". It is measuring a layer that no longer
    paints. The canvas needs no equivalent: exactly one `drawImage` runs per
    body per frame by construction of the draw loop.

204. **FEEDBACK ON ANOTHER BUILD, ABSTRACTED INTO PRINCIPLES.** Makko gave a
    punch list against `beats.html` and I made the mistake of patching that
    file instead of taking the lesson. The list is really seven rules, and this
    build broke most of them harder than the one he was looking at:
      - a moving thing needs a real CYCLE, not a transform (our movers were a
        spinning disc with one dot on it - nothing on the surface to track, so
        the rotation did not read as rotation);
      - sprite baselines must be FLUSH (our run strips carried 5-6% transparent
        rows under the feet, so the whole cast hovered - my own slicer computed
        the shared vertical window with the ground shadows still in it and then
        scrubbed the shadows, leaving the gap);
      - text must be MEASURED against its panel, never hard-sized (the win
        meter's value sat at the left of the bar and collided with the fill and
        the notch label the moment it reached two digits);
      - the payout must never OCCLUDE the payoff;
      - the win moment needs the cast REACTING;
      - no two pieces of furniture may share space, and it should be asserted;
      - a death is a readable SEQUENCE, not a state flip.
205. **THE PAYOUT WAS PARKED ON TOP OF THE PAYOFF.** `#stack` was
    `inset: 0; align-items: center` - dead centre over the great door, covering
    the guardian, the dial, the bolts and every character who reached it. Three
    placements were tried and the first two only moved the problem: at the
    bottom it covered the cast standing at the foot of the door and collided
    with the meter; on the left it covered the bolts. It lives BELOW the play
    frame now, where it cannot occlude anything, and the stage is entirely the
    payoff.
206. **AND THE CAST WAS DELETED EXACTLY WHEN IT SHOULD HAVE BEEN CELEBRATING.**
    Two separate causes, both invisible until the figures were probed: the door
    scene faded every arrival to `opacity: 0` at 0.88 of its beat, and the walk
    that gathers them at the door moved them 200 units in a 400-unit frame, so
    the far two of three ended up outside it. The payout was playing to an
    empty doorway. They hold at full opacity now, gather at 74 units, and play
    a drawn jump-and-settle in sequence down the line.

### Art (SOLBY v3 continues)

173. **Six acted poses in one sheet was too much to ask of one generation.** Of
    the six, only `idle` came back clean; `trapped` was just standing, `duck`
    read as falling, and `braced` came back with Chinese characters rendered
    across it. One pose per best-of-8 batch instead, which is both cleaner and
    the honest way to hold the 8-take curation bar. Happy and trapped landed
    8/8 and 8/8 on-model with no drift and no artefacts.

### Credits

Session 21 + 22 running total: **3,542 credits** (21,534 → 17,992). Still short
of the brief's 6,000 floor. The art wave was deliberately paused mid-session
until the level geometry read right — that was the correct order and it was not
the order the brief specified. What was spent went on the SOLBY redesign, which
was not optional, and on the three run cycles.

179. **SOLBY V3 IS LIVE.** Full pose set generated one-pose-per-best-of-8
    (idle / happy / worried / trapped / walk), cut through the same shared-
    baseline slicer, and wired behind `SOLBY_V3` — the identical one-flag swap
    POTTS used in decision 124, so the original plates stay on disk and the
    fallback costs nothing. His run strip goes live on the same flag, because
    the two must never be on screen in different generations of the design.
    The `work` plate points at `worried`: the pose is unreachable since the
    puzzle verb was cut, and the RASTER map has to stay complete.

### STILL NOT DONE

Jump / brace / duck strips for all three; painted minor props and
painted terrain blocks (both are hand-drawn SVG); the movers are simple drawn
shapes; the whole chrome list from session 20 is unchanged.

---

## Fork session 23 — THE PHYSICS CORE (2026-08-28, THE-TEMPLE-GDD v3 — "build
## a real Mario game, then have a robot play it")

Brief: the v3 kickoff VOIDS the instruction every previous attempt followed —
"animate motion keyed to the sealed timeline". Phase 0 is a standalone
platformer with placeholder boxes, gated on a human being able to play it on
the arrow keys. Phases 1-3 are NOT started; this session stops at that gate as
instructed.

Built in `vault-chibi/`, the fork carrying sessions 21+22 work (`terrainFor`,
`groundYAt`, `MOVER`, SOLBY v3) — confirmed by grep against the two sibling
forks, which are behind. `vault-next/` untouched. `index.html` untouched.

### 174. THE DIAGNOSIS: the spine was a TIME-DOMAIN CONTRACT.

Sessions 20, 21 and 22 each added a genuine platformer feature — one runner on
one path (135), real five-beat jump arcs (150), a terrain profile (166),
objects that close on him (170) — and each still photographed as a slideshow.
The reason is one line, and it is not in the Known-traps list:

    index.html:5666   const runX = (t) => { ... }        // keyframe lookup
    index.html:5640   const RUN_PATH = [[0, 16]];        // built from bMap

`buildBeatList` emits a schedule in MILLISECONDS (`enc.0 at 4200ms`, `hold`,
`door at 22000ms`) and roughly 300 cues hang off those stamps. A platformer is
a SPACE-DOMAIN simulation: WHEN the runner reaches obstacle 2 is an outcome of
physics, not a time that can be promised in advance. The two cannot both drive
the same body. Every session that kept the beat clock as the spine ended up
writing his position to make him arrive on schedule — a slideshow with extra
steps, no matter how good the individual features were.

**The resolution, and it needs no CONFIG change:** the sealed beat list stays
sealed and keeps supplying the run's CONTENT and its beat DURATIONS, but the
run's spine becomes the level's geometry. Beats fire on POSITION triggers, not
on wall-clock. `buildBeatList` is still called unmodified and still dumped as
sealed evidence; its `at` times simply stop being the traversal clock. That is
Phase 1's wiring and it is not written yet.

### Phase 0 — `vault-chibi/phase0.html` (standalone, no art, no sealed data)

175. **One rule, enforced structurally.** Nothing writes `runner.x`, `runner.y`
    or `runner.vx` except the integrator in `step()`. The driver's entire
    surface is `poll(simT, observedX) -> {left, right, jump}`. It holds no
    reference to the runner object, so it has nowhere to write even if it
    wanted to. The observed x is what a player reads off the screen.
176. **Fixed timestep, 1/120s.** Determinism lives here. Physics never sees a
    variable dt, so a replay of the same seed reproduces the run exactly. The
    renderer runs on its own clock; the simulation does not.
177. **Constants chosen against each other, not in isolation.** G_UP 1900,
    G_DOWN 2600 (lighter up, heavier down — he hangs at the top and lands with
    weight), JUMP 500, RUN_MAX 138. That yields apex 65.8, airtime 0.488s,
    horizontal reach 85.3 units. Every gap width and ledge height is then
    derived FROM those numbers rather than guessed, so a 48-unit gap is a
    comfortable hop and 66 is cleared by a hair — the GDD's staging, arrived at
    arithmetically.
178. **THE LEVEL IS A SURFACE PROFILE, and the driver's plan is DERIVED from
    it.** One table (`PROFILE`) generates both the collision solids and the
    driver's jump cues, so they can never disagree. The first version had
    hand-tuned launch x values and was wrong in a way worth recording: it
    jumped 23 units BEFORE the lip, wasted a third of the airtime over solid
    ground, clipped the far lip and slid down it. Hand-authored timings against
    a real simulation are a bug generator. `LIP_LEAD` and `riseLead(h)` compute
    launch points from the physics constants directly.
179. **LATE MEANS HE RAN OFF THE EDGE BEFORE THE BUTTON CAME — and that is the
    whole failure mechanism.** This is better than the brief hoped for. A late
    press does not "miss by a bit"; by the time it arrives he is past the lip
    and past coyote time (90ms, 12.4 units at run speed), so the impulse has no
    ground to act from and NO JUMP EVENT FIRES AT ALL. Measured at all three
    pits: `jumpsAtOrAfterTheLatePress: 0`. At PIT-A he is recorded falling in at
    t=8.425s and the press lands at t=8.460s — he was already in the hole when
    the button went down. Nothing is scripted; the button genuinely did nothing.
180. **Autonomous hazards take no runner term.** `driveHazards(H, simT)` is a
    pure function of the sim clock and each hazard's own seeded phase — there is
    literally no `runner` in scope inside it. Bats patrol, crushers cycle, slabs
    sag, stones roll. Seeded from the run seed, never from wall time, so a
    replayed seed reproduces the hazard clocks too.
181. **Crushers and sagging slabs are REAL SOLIDS in the one collision path.**
    The first pass had crushers shoving the runner's y directly, which fought
    the resolver and jittered him into the ground. They are moving solids now,
    and a rider standing on a moving solid is carried by its per-step delta —
    which is what makes the bridging slab (`slab0`, flush over gap-2) work: he
    runs onto it and rides it down as it sags. One collision path, no second
    system to keep in sync.
182. **A sagging slab sitting on the floor was an unjumpable wall.** The first
    slab placement sat at floor level with an 18-unit lip, and the plan
    derivation could not see it, so the runner ground against it at x=402 for
    the rest of the run — 5,976 wall-collision frames. Slabs are now either a
    flush bridge or a raised platform, and the plan derivation reads `SLABS`
    alongside `PROFILE`. A raised slab's cue is computed against its LOWEST
    position, so the jump clears it wherever in its cycle he happens to arrive:
    his clock and the slab's are independent and must stay that way.
183. **THE FRAME CAUGHT WHAT EVERY VALUE CHECK MISSED.** The first
    caught-in-a-pit capture passed every probe — `held: true`, `x: 1110.7`,
    `y: 188` — and the runner WAS NOT IN THE PICTURE. PIT_Y 214 put him at
    canvas y=370 on a 360px canvas: drawn off the bottom of the frame. The GDD
    is explicit ("still, never gone... no falling off-screen") and the brief is
    explicit that DOM probes are insufficient. PIT_Y is 178 now — head just
    under the lip, which is also the GDD's "hangs from the ledge by his
    fingers" — and `__probe.onScreen()` was added to assert it in PIXELS: it
    reads the canvas back and confirms the runner's colour is painted inside
    the frame.
184. **rAF STARVATION, again, in a new file.** `visibilityState` reports
    'hidden' in the embedded preview pane and rAF never fires, so the clock
    froze at t=0 on frame one. `index.html` already carries a web-worker clock
    for exactly this; phase0.html did not, and had to grow one. **This belongs
    in Known traps: any new page in this project needs the worker fallback from
    birth**, not after it is diagnosed a second time.
185. **Capture rigs, reusable for the rest of the project.** `tools/shot.py`
    drives headless Chrome over CDP: load, run setup JS, poll a predicate, run a
    hook, screenshot — from a real compositing browser, which is the whole
    point. `tools/playtest.py` is the acceptance gate: it turns the driver OFF
    and dispatches REAL key events via `Input.dispatchKeyEvent`, so the path
    under test is exactly a player's — key event -> keydown handler -> `keys[]`
    -> `humanInput()` -> `step()`.

### Session 23 verification (recorded pass/fail)

**THE PHASE 0 ACCEPTANCE GATE — a human plays the level: PASS.**
Driver OFF (asserted `driverOn === false` against the live world), 16 Space
presses dispatched as real key events -> 16 jumps -> 26 landings -> reached the
goal at x=2381.5 in 18.68 sim-seconds. Zero falls. **Zero console errors.**

- Clean scripted run: reaches the goal, 18.70s, 16 jumps, 25 landings, 0 falls.
- **Physics proof (a parabola, not an authored curve):** `d(vy)/dt` sampled
  across a jump reads 1902 / 1896 / 1902 / 1902 / 1896 / 1902 on the rise and
  flips to 2603 / 2603 / 2595 / 2603 on the fall — G_UP 1900 and G_DOWN 2600
  exactly, the few units of scatter being the finite-difference interval.
  Least-squares parabola fit to the rising half: implied gravity **1900**, **max
  residual 0.0159 units**. Averaged over all samples: rising **1900** against
  1900 declared, falling **2599** against 2600.
- **Autonomy proof:** crusher `crush2` at x=2214, sampled 251 times while the
  runner was **never closer than 606 units**; it completed **4 full cycles**
  through its whole 74-unit travel in that window. `driveHazards` takes no
  runner parameter, so this is structural rather than incidental.
- **Failure proof:** late by 260ms at each of the three real pits ->
  `jumpsAtOrAfterTheLatePress: 0` at **all three**, held in the pit at **all
  three**. At PIT-A the fall-in is timestamped 35ms BEFORE the press.
  (The first measurement of this reported 1 jump at PIT-C; that was a false
  positive of a +/-120-unit proximity window catching the previous cue's jump at
  x=1974.9. Recorded because it nearly went into these notes as a real
  asymmetry.)
- **Determinism:** same seed twice -> byte-identical position trace (374
  samples) AND byte-identical hazard-clock trace. A different seed changes the
  hazard clocks.
- **Pacing:** 46 interactions in 18.7s, mean gap **0.405s**, median 0.425s, max
  1.15s. Longest stretch with the runner not advancing: **0.30s**, riding the
  bridging slab down as it sags.
- **Animation states, all derived from physics, all visited:** run 151,
  jump-up 78, jump-down 80, land 61, idle 4 samples. Nothing assigns
  `runner.anim` anywhere except the derivation at the end of `step()`.
- **Frame truth:** `onScreen()` reports `inside: true, painted: true` at canvas
  (283, 283) for the caught pose, read back off the canvas pixels.
- Screenshots, headless Chrome: level start; runner mid-jump over PIT-A with
  the driver on; runner mid-jump over PIT-A with the **driver OFF, keyboard**;
  caught and held in PIT-A.

### Credits

**Zero.** No OpenArt calls this session — Phase 3 is the art wave and Phase 0
is explicitly "no art, placeholder boxes". Sessions 21+22 running total is
unchanged at ~2,700 (balance ~18,830).

### NOT DONE — deliberately, at the instructed gate

Phases 1, 2 and 3 are not started. The Phase 0 gate reads "show me a
keyboard-playable build and a screenshot of the runner mid-jump before going
further. Do not start Phase 1 until this passes." It passes; work stops here
for Makko's look. Still outstanding and unchanged from session 22: SOLBY v3's
remaining plates and their wiring, jump/brace/duck strips for all three,
painted minor props and terrain, and the whole chrome list from session 20.

### Session 23, second pass — Makko: "do you understand that this needs to
### feel like Mario Bros and it does not?"

He was right, and the more useful half of the lesson is WHY I missed it. The
first pass verified physics and called that done. Correct physics is not the
same thing as the right feel, and every number in the first verification was
true while the frame still failed — which is session 22's decision 164 all over
again, one pass later, in a new file.

186. **THE AIRSPACE WAS EMPTY AND THERE WERE ONLY TWO VERBS.** Looking at my
    own captures: the top 60% of the frame was empty black, there was not one
    object above the floor line in 2,400 units, and the entire interaction
    vocabulary was "jump a hole" and "jump onto a ledge". Session 22 diagnosed
    flatness and fixed the GROUND (decision 166, `terrainFor`); I reproduced
    the same failure one layer up by giving the ground a profile and leaving
    the air empty. The GDD's reference section says exactly what 1-1 is and I
    had not built it: *"a Goomba, a pipe, a gap, a block, a pipe, two
    Goombas."* Six things were missing, none of them art:
      - blocks at head height that BONK and pay out coins
      - walkers that come AT him and get STOMPED, with a bounce
      - coin arcs sitting ON the jump, so the coins read the line for you
      - pipes as silhouette punctuation
      - momentum: real acceleration, a skid, jump height tied to run speed
      - a camera with sky above it and the runner at 38%
187. **RUN_ACC 900 was a switch, not an accelerator** — full speed in 0.15s.
    430 takes 0.32s, so you can watch him lean into the stride. Added SKID
    (1500) for the reverse, which is the SMB turn; without it a platformer
    feels frictionless no matter how correct the gravity is.
188. **Jump height now rides on run speed** (JUMP_MIN 415 standing, JUMP_MAX
    520 at full tilt), as in SMB. It is the single biggest reason a Mario jump
    reads as earned rather than issued, and it costs four lines.
189. **The camera was vertically cramped and centred.** The runner was 1/6 of
    the frame height against Mario's 1/14, so there was no sky and nothing to
    anticipate with. The view is 527x231 world units now with the play plane
    low in frame, and he sits at 38% of the width so most of what you see is
    what is COMING.
190. **A greybox still needs a correct VALUE STRUCTURE.** The first pass was
    dark slate on dark slate on near-black and you genuinely could not read
    figure from ground. That is a Phase 0 failure, not an art problem — no
    amount of Phase 3 painting fixes a level you cannot parse. Sky light,
    ground mid, blocks bright, runner the highest-contrast thing on screen,
    parallax receding by VALUE and not merely by scroll rate.

### Five real bugs the rebuild surfaced, all of them systems colliding

191. **A walker at a pit lip throws the runner into the pit.** Stomping one
    BOUNCES him, so he is airborne when the pit's jump cue fires, coyote is
    zero, no jump happens and he drops in. Measured exactly: stomp at
    x=1133.7, PIT-A lip at 1156, fell in at 1165.9.
192. **A crusher hand-dropped over a slab crushes him against it.** crush1 sat
    at x=1420, directly over slab1 (1386-1456); standing on the slab puts his
    head at 96 and the crusher came down to 118. 63 collision frames, dead run.
193. **So placement is BY RULE now, for both.** `freeSpans()` returns clear
    stretches of flat ground with the elevated bits, the jump windows and the
    slabs subtracted; walkers and crushers are solved from it. The margins
    differ by severity, which is the point: a stomp-bounce into a pit is fatal
    so holes get the full 88-unit jump reach, while being bumped at a ledge is
    survivable so ledges get 26. Both bugs above are now unrepresentable
    rather than fixed.
194. **A sagging bridge trapped its own rider.** A flat slab sagging 17 units
    below the ground line puts the far lip above its rider's feet — a 1.2s
    stall at x=538, which breaks the GDD's one rule outright. The bridge
    hinges now: five panels sagging by sin(pi*u)^2, so the ends stay put and
    only the middle dips.
195. **STEP_UP, and it fixed a whole class at once.** A running man should
    step over a 2-unit lip, not stop dead against it. Without it every seam
    and every hinged panel was a wall — 244 frames of grinding.
196. **THE DRIVER NEEDED TO RETRY, AND THEN NEEDED TO STOP RETRYING.** Cues
    were one-shot: anything that disturbed a jump left him grinding at x=962
    for the remaining 62 seconds. Adding a retry fixed that and immediately
    caused a worse bug — retrying on PROXIMITY re-pressed 25ms after he had
    already landed on the pipe at 1780, and that unwanted second jump sailed
    him off the pipe straight into gap-4. The gate has to be the OBJECTIVE,
    not the neighbourhood: a hole is cleared by being past the lip, a rise by
    having your feet at or above the top. `cleared(cue, x, feetY)`.
197. **THE LEVEL HAS NO CRUSHERS AND THAT IS THE HONEST ANSWER.** The block
    rows cover nearly all the clear flat ground, so every legal crusher site
    was gone. Forcing one in meant deleting a brick row — the level bending to
    the hazard instead of the other way round — and 1-1 has no crushers
    anyway; it is a Phase 2 temple element ("the ceiling comes down"). The
    code path stays and is exercised by the sagging slabs, which are the same
    moving-solid machinery, and the autonomy proof runs on a bat instead.

198. **Two of my own MEASUREMENTS were wrong and nearly went in as results.**
    Gravity read 2538 against a declared 1900, and the crusher cycle count read
    zero. Neither was the physics. The 0.62s arc window can contain a SECOND
    launch (a retry, or a stomp bounce) and finite-differencing across that
    join is meaningless — the fix is to take the first CONTIGUOUS monotonic
    run. The cycle counter still used thresholds from a taller crusher, and
    then, once the subject became a bat, measured its 9-unit vertical bob
    instead of its 100-unit horizontal patrol. Recorded because a broken
    measurement that reports a number is more dangerous than one that crashes.

### Session 23 second-pass verification (recorded pass/fail)

**THE PHASE 0 ACCEPTANCE GATE — a human plays the level: PASS.**
Driver OFF (asserted against the live world), 16 Space presses dispatched as
real key events -> 16 jumps -> 28 landings -> goal at x=2562 in 23.72
sim-seconds. Zero falls. **Zero console errors.**

- Clean scripted run: goal reached, 23.68s, 22 jumps, 32 landings, **0 falls**,
  35 coins, 6 bonks, 3 stomps, 13 bumps.
- **Physics proof:** measured over the first contiguous monotonic run of a
  jump arc — rising **1900** against G_UP 1900 (31 samples), falling **2600**
  against G_DOWN 2600 (22 samples), launch vy -477.4, apex rise 58.0.
- **Autonomy proof:** bat3 completed **4 full 100-unit patrol sweeps** while
  the runner was **never closer than 362 units** (313 samples).
  `driveHazards(H, simT)` takes no runner parameter at all.
- **Failure proof:** late by 260ms at each of the three real pits ->
  `jumpsAtOrAfterTheLatePress: 0` at **all three**, held at all three. At
  PIT-A the fall-in is stamped t=10.100 and the press t=10.135 — he was in the
  hole 35ms before the button went down.
- **Determinism:** same seed twice -> byte-identical position trace (474
  samples) AND byte-identical hazard-clock trace. A different seed changes the
  hazard clocks.
- **Pacing: 48 beats in 23.7s, mean gap 0.486s, median 0.45s, MAX GAP 0.975s**
  — something happens at least once a second, everywhere in the level. (Beats
  collapse bursts inside 0.25s, so a row of coins counts once; 116 raw
  interactions.) Longest stretch not advancing: **0.40s**.
- **Animation states, all derived from physics:** run 194, jump-down 105,
  jump-up 97, land 67, skid 8, idle 3 samples.
- **Frame truth:** `onScreen()` reports `inside: true, painted: true` for the
  held pose, read back off the canvas pixels.

### Still not right, and worth saying

Stomps land only 3 times a run against 8 walkers — the reactive rule fires at
a 44-68 unit gap so contact happens on the way DOWN, but a hole cue outranks
it, and several walkers sit inside those suppressed zones. It reads as too few
enemy interactions for a 1-1 pastiche. Tuning that is a Phase 2 level-design
job, not an engine one.


### Session 23, third pass — Makko: "running into enemies doesn't do anything"
### and "there's no end, he just runs into a wall"

Two problems, and the honest answer is that ONE of them was covered by a later
phase and one was not — recorded that way because "a future phase will catch
it" is exactly the kind of claim that needs checking rather than asserting.

199. **THE ENDING WAS ALREADY COMING, THE ENEMY CONTACT WAS NOT.** The card
    reveal Makko describes already exists in `index.html` and Phase 2 arrives
    at it: `.scard` face-down cards on `assets/cardback.jpg`, dealt at the foot
    of the great door and turned one at a time, with the reliquary case opening
    at the top tier. So "a chest that opens and a card pack comes out" is the
    Great Door sequence, already built. What was missing was that PHASE 0 had
    no ending at all — a bare unjumpable wall — so there was nothing to play
    toward. Enemy contact, by contrast, was covered by nothing: the GDD says
    minor hazards never decide anything, so no phase was ever going to give
    them teeth. That one was a real gap.
200. **CONTACT COSTS TIME, NOT LIFE.** It used to be `r.vx = min(r.vx, -40)`,
    a nudge you cannot see. It cannot kill him — only the three real obstacles
    decide anything, and nobody in this temple gets hurt — so it takes the one
    thing a runner has. He trips, tumbles backward off his feet, rolls, gets
    up and keeps going: ~0.85s, entirely visible, decides nothing. Fall Guys'
    pratfall rather than Mario's death. Plus TRIP_GRACE (1.05s), the standard
    post-hit invulnerability, because without it he gets up into the same
    walker and trips again — measured six times in a row against walk5.
201. **THE LEVEL ENDS ON AN OBJECT.** A chest at x=2960: he runs up, pulls up
    in front of it (the driver simply stops holding right — still only an
    input decision), the lid swings open away from him, light spills out and
    a card pack rises. `reached-chest` -> `chest-open` -> `pack-out`, on the
    chest's own clock. Phase 2 replaces it with the Great Door and the real
    reveal; this exists so the level has an ending to play toward now.

### The enemy problem took five wrong fixes, and they are worth recording

202. **A GOOMBA IS THE SAME HEIGHT AS MARIO AND THAT IS NOT DECORATION.** At
    16 tall against a 26-tall runner the vertical overlap window is about
    0.02s — he sailed clean over their heads and only ever clipped one on the
    way down, shoulder-first, which read as a trip. 0 stomps, 10 trips. Now 22.
203. **Tuning the stomp as a precise ballistic solution failed twice.** Both
    attempts computed the exact gap at which a jump lands on the head, and
    both produced almost no stomps, because the window is hundredths of a
    second wide and missing it means meeting him at ground level. The
    reframing that fixed it: **the goal is not to maximise stomps, it is to
    never meet one with your feet down.** Jump early and you clear him
    cleanly, jump right and you land on him, and only running into him costs
    anything. So the band is generous (8-104 units) and re-arms on landing.
204. **THE BUTTON-HOLD DURATION IS PHYSICS, NOT COSMETICS.** The reactive
    press held for 0.26s. Apex is at JUMP_MAX/G_UP = 0.274s, so every reactive
    jump was released 14ms before the top, triggered the variable-height CUT,
    came out short, and dropped him right beside the walker. The driver was
    pressing jump four times per walker and still tripping. Held past apex
    (0.34s) it is a full jump.
205. **THEY WERE PING-PONGING, SO THEY CHASED HIM.** The walkers patrolled
    back and forth inside their span, which meant that after he cleared one it
    reversed and came back at him and caught him on landing. A Goomba walks
    one way and never turns around. Left-only at constant speed, wrapping at
    the span end: a stream of things walking AT him, each met exactly once.
206. **AND THE COLLISION TEST ITSELF WAS TOO STRICT.** Even airborne and
    descending, a stomp also required his feet within 15 units of the walker's
    head. Miss that and a correctly-timed jump still registered as a trip.
    The contract is simpler and it is Mario's: coming DOWN on one stomps it,
    going UP through one is a clean pass, and only feet-on-the-floor contact
    costs you. That makes "get off the ground" the whole skill. This single
    change moved it from 5 stomps / 12 trips to **8 stomps / 6 trips**.
207. **THE LEVEL WAS TOO DENSE TO HOLD ENEMIES AT ALL, and that was the root
    cause under all of the above.** Every flat run was 78-130 units with a
    jump at both ends, so there was nowhere a ground creature could stand
    where the runner was not already committed to something. **Mario 1-1 is
    not uniformly dense** — it has long plain stretches whose only event is a
    Goomba walking at you. The profile was rewritten with 230-360 unit flats
    between features (level 2760 -> 3140 units), which is 1.7-2.6s of running
    each, and the walker sites went from 0-2 viable to ten. The beat gap moved
    from a frantic 0.45s to 0.56s mean / 1.42s max, which is finally inside
    the GDD's "something every second or two" rather than under it.
208. **Trailing margins matter as much as leading ones.** walk4 sat 10 units
    past a ledge drop and walk5 right on the gap-4 landing, so he came down on
    top of them with no room to react. Keep-outs now extend 56 units past a
    hole and 46 past a ledge, plus SPAWN_CLEAR so nothing stands on his first
    150 units of run-up.
209. **`tools/jscheck.sh`, after a self-inflicted outage.** A patch script's
    end-marker `"const COIN_R"` is a PREFIX of `const COIN_ROWS`, so a cut
    stopped early and left a duplicate `const` declaration that took the whole
    page down. Every edit now runs `node --check` on the extracted inline
    script before anything else touches it.

### Session 23 third-pass verification (recorded pass/fail)

**KEYBOARD GATE: PASS.** Driver OFF, 9 Space presses as real key events -> 9
jumps -> 27 landings -> reached the chest at x=2935 in 32.69s. Zero falls.
**Zero console errors.**

- Clean scripted run: **30.11s**, 29 jumps, 37 landings, **0 falls**, 30 coins,
  13 bonks, **8 stomps, 6 trips**. Ending fires in order: `reached-chest@28.2`
  -> `chest-open@29.25` -> `pack-out@30.11`.
- **Physics:** rising **1900** vs G_UP 1900 (32 contiguous monotonic samples),
  falling **2601** vs G_DOWN 2600 (24 samples), launch vy -504.2, apex 64.8.
- **Autonomy:** bat4 completed **7 full 110-unit patrol sweeps** while the
  runner was never closer than 364 units (489 samples).
- **Failure:** late 260ms at all three pits -> `jumpsAtOrAfterTheLatePress: 0`
  at all three, held at all three; at PIT-A the fall-in is stamped 43ms BEFORE
  the press.
- **Determinism:** same seed twice -> byte-identical position trace (603
  samples) and byte-identical hazard clocks.
- **Pacing: 54 beats, mean 0.557s, median 0.492s, max 1.417s.** Longest
  stretch not advancing **0.80s** (measured only up to arrival - standing at
  the chest is the ending, not a stall, and the old metric counted it).
- **Animation states, all off physics:** run 189, jump-down 135, jump-up 127,
  land 56, trip 65, idle 31.

### Open

Six trips a run is still more than it should be for a 1-1 pastiche, and the
level has no crushers (decision 197). Both are level-design work for Phase 2
rather than engine work.


### Session 24 — THE THREE BEATS (2026-08-29, Makko's beat design)

Makko: *"we need distinct beats a viewer could get excited about... we want
FEWER, CLEARER challenges, rather than more."* Then the structure, in his
words: does the single runner get over the first enemy, or does it get him —
then two question boxes where a character is best, a power-up second, nothing
third and an enemy worst — then a trap where the question is how many of the
party you now have actually make it over.

This is a better design than what was built, and it inverts the thing I had
been optimising. Sessions 22 and 23 chased DENSITY, on the reading that a level
with three interactions is a slideshow. That was right about the failure and
wrong about the fix: what makes 1-1 exciting is not events per second, it is
that each event is a QUESTION WITH A COUNTABLE ANSWER. Built in `beats.html`;
`phase0-core.html` is a snapshot of the proven physics gate, untouched.

210. **THE SEQUENCING IS FREE, AND THAT IS THE WHOLE ARGUMENT FOR THE
    ARCHITECTURE.** Every party member is a full physics body running the SAME
    cue list, so they arrive at the trap staggered by their spacing and resolve
    ONE AT A TIME — first one clears, and only then do you find out about the
    second. Nothing about that is staged; it falls out of having real bodies.
    A timeline build would have had to author each ordering by hand, which is
    precisely the work that turned into a slideshow three times.
211. **The draw reaches the simulation through exactly one hole: `fumble`.**
    It is a set of cue ids a given body will get WRONG — the press comes 300ms
    late, or for the first enemy it never comes at all. Everything downstream
    is physics. `fumble` is the seam Phase 1 replaces with the real sealed
    region; nothing else has to change.
212. **The party line is the scoreboard, so held bodies must be COUNTABLE.**
    Two members falling in the same trap landed on the same spot and read as
    one. They now spread along the pit floor. Small, but the GDD's "the player
    reads the score by counting bodies" fails outright if they stack.
213. **The four box outcomes are different SHAPES, not different colours.** A
    character drops out and joins as a real body from the frame it exists; a
    power-up is a spinning star that grants a shield (eats one elimination); a
    dud is a puff; an enemy drops right on top of the party, close enough that
    nobody can set up a jump — which is what makes "worst" actually cost
    something rather than being a fourth flavour of nothing.
214. **AN ENEMY IS A ONE-WAY PLATFORM, and the test has to be SWEPT.** Landing
    on one was checked as an AABB overlap plus "feet within 15 units of its
    head". A full jump carries him 71 units up against a 22-tall enemy, so he
    is ABOVE it for all but the last 0.045s of the arc — the window was four
    hundredths of a second and he flew over, landed beside it and was caught on
    the ground. **Every one of 14 seeds died on the first enemy, including the
    ones the draw said should clear it.** Sweeping "were his feet above its
    head last step, and are they at or below it now?" makes landing on one as
    reliable as landing on a platform, which is what it is.
215. **The jump band has an upper bound for a reason.** During a 0.508s jump he
    covers 70 units while the enemy closes 17, so the gap shuts by ~87. Firing
    at ~87 lands him on its head; below ~77 carries him clean over; but firing
    at 104 lands him just SHORT — inside touching distance, on the ground,
    which is the one outcome to avoid. The band stops at 97 and he waits.
216. **He also needed telling to jump INTO the boxes.** Beat 2 never fired at
    first because the plan had no cue for it and he ran underneath them. His
    head rises the 36 units from 124 to the soffit at 88 in 0.0813s, covering
    11.2 units, so the press goes in 12 units before the box's near edge.
217. **Beats settle independently.** Beat 3 was gated on beat 2 having
    resolved, so a run that lost its only runner at beat 1 reported nothing for
    either. Each beat now settles on its own condition, and "never opened" is a
    legitimate verdict for boxes you did not live to reach.

### Session 24 verification (recorded pass/fail)

- **Beat 1 matches the draw on 14 of 14 seeds** — every `clear` clears, every
  `out` is caught. Before decision 214 it was 0 of 14.
- Beat 3 matches the per-member draw exactly: `clear/clear/out` with a party of
  2 gives "2 of 2"; `out/out/clear` with a party of 3 gives "1 of 3";
  `out/clear/out` with a party of 2 gives "1 of 2".
- Beat 2 produces all four outcomes across the battery, and the enemy outcome
  really does cost a member (seed beats-10: cleared the first enemy, box gave
  an enemy, ended 0 of 1).
- **Zero console errors** across the 14-seed battery.
- Replay: same seed reproduces the draw and the run.

### Open, and needing Makko

The odds are placeholders and they matter: 6 of 14 seeds currently end four
seconds in, on the first enemy. The GDD wants losing your starter early to be a
real beat, but 43% may be too often to sit through. In Phase 1 these stop being
free numbers — they come from the sealed tier weights, which are CONFIG and
off-limits — so the mapping from tier to beat outcomes is a decision to make
deliberately rather than tune by feel.


### Session 25 — EVERY RUN OPENS A CHEST (2026-08-29)

Makko: *"we need every run to end with opening a treasure chest because every
pull results in some sort of win — let's do that by having the character
picking up coins and those coins being spent dramatically on opening a chest
either at death or when they make it to the end, and multiple characters act as
coin multipliers."*

This closes a real hole. Before it, a wipe simply stopped: the party died and
the run was over, which is a dead end rather than a bad result. Now the run has
one ending and only its SIZE varies.

218. **The ending is a four-phase machine, and every path reaches it.**
    `gather` -> `spend` -> `lock` -> `open`. Arrived on foot, the survivors
    walk into a line at the chest. Wiped, nobody is walking and the camera
    travels on to the chest alone — which is exactly what the GDD already
    asks for ("if nobody reaches the door, the camera arrives alone and the
    door opens quietly"). 24 of 24 seeds reach `done`.
219. **`coins x survivors = the haul`, floor of x1.** The multiplier is the
    reason beat 3 now matters twice: it decides who is standing AND what the
    chest is worth. It is also STAGED rather than stated — the spend launches
    one coin stream per survivor, so three survivors visibly send three
    streams into the lock. You see the multiplier; you do not read it.
220. **THE COINS WERE ALL ABOVE HIS HEAD.** Four of twenty-four were being
    collected, and it took measuring the haul to notice. His box is y 124..150
    standing, so a coin centred at 112 spans 106..118 and sits entirely in the
    air over him — catchable only by accident, mid-jump. Running-height coins
    sit at 130 now; the ones meant to reward a jump stay high, ON the line of
    that jump. Collection went 4 -> 28 and the whole economy appeared.
221. **The lock charges as the haul goes in.** A thin run barely lights it; a
    fat one makes it the brightest thing on screen before the lid moves. That
    is the "dramatically" in the brief — the chest visibly fills up, and the
    counter over the stage runs with it.
222. **Bodies have to keep walking through the whole ending.** They were only
    being stepped during `gather`, so they froze mid-stride on top of the
    chest, which stacked both coin streams on one spot and hid one body behind
    the other. Caught in a frame, not in a probe.

### Session 25 verification (recorded pass/fail)

- **Every run opens a chest: 24 of 24 seeds reach `done`.**
- The economy has a real shape, and it is legible as "how far did you get, and
  how many came home":
  **4** died at the first enemy · **11** died at the boxes · **20** died at the
  trap · **28** one home · **56** two home · 84 all three.
- Tier spread over 24 seeds: CHAMBER 9, SANCTUM 7, RETREAT 7, THRESHOLD 1.
- Replay identical on a fixed seed (haul, tier and all three beat verdicts).
- **Zero console errors.**

### Open, and worth Makko's eye

- **Coins do no work as a variance source.** Collection is deterministic, so
  anybody who finishes collects all 28; the only thing that moves the payout is
  the multiplier. That makes six possible outcomes in total (4 / 11 / 20 / 28 /
  56 / 84). It reads fine, but "coins" currently means "how far you got"
  rather than "how you did". Optional high coins that only a well-timed jump
  reaches would give it a second axis — worth doing only if the sealed tier
  does not already supply the variance, which is the Phase 1 question.
- **RELIQUARY never came up in 24 seeds** (it needs all three home) and
  THRESHOLD came up once. The bands are placeholders; tuning them now is
  premature because Phase 1 replaces them with the sealed tier.
- **The honesty reconciliation is now the live design question.** If coins are
  physically collected and set the payout, the payout is no longer sealed. The
  fix is the discipline already used for `party size == arrivals == bolts`: the
  seal picks the tier, the tier decides how many coins are PLACED, the
  multiplier comes from arrivals, and what the viewer watches reconciles to a
  number committed before the first frame. Nothing in CONFIG was touched.


### Session 26 — THE TRACKER, STARS AS MULTIPLIERS, AND COINS WORTH JUMPING FOR
### (2026-08-29)

Makko: *"add a coin and multiplier tracker, assume stars are multipliers too,
the character should be able to jump and get coins, but shouldn't jump and get
them every time."*

223. **A STAR IS A MULTIPLIER, NOT A SHIELD — and that makes the box ranking
    explain itself.** A character gives you a body AND a multiplier; a star
    gives you just the multiplier. That is now visibly WHY one outranks the
    other, rather than a ranking you have to be told. `mult = max(1, survivors
    + stars)`, and the shield is gone entirely.
224. **The tracker shows what the multiplier is MADE OF.** Top-left of the
    stage: the coin count, then a coloured pip per party member (greyed when
    one is lost) and a star pip per star, then the ×N. Both cells pulse when
    they change. The haul is something you watch accumulate now instead of a
    number that appears at the end.
225. **HIGH COIN CLUSTERS HE DOES NOT ALWAYS TAKE.** Five clusters at head
    height plus a jump, kept clear of all three beats so going for coins never
    competes with a decision that matters. A seeded `reach` draw decides per
    cluster whether he goes for it; a cluster he skips he runs underneath. Cue
    lead is 38 units, because apex is 71 up and arrives 0.274s / 37.8 units
    after the press, which puts the top of the arc through the cluster.
    **Finisher coin counts went from a single value (28) to 23 / 26 / 29 / 32.**
    That was the gap flagged at the end of session 25: the haul had only one
    axis, and now it has two — how far you got, and how you did.

### Two pickups were unreachable, and both for the same reason

226. **THE STAR RESTED ABOVE HIS HEAD, exactly as the coins had.** Session 25
    fixed coins at y=130 and I placed the star's resting height at SOFFIT+6
    (y=94) without re-applying the lesson. His box is 124..150, so the pickup
    test `b.y < p.y + 8` could never pass: **zero stars collected in 24 seeds**,
    across 8 runs that actually opened a power-up box. Anything a running
    character is meant to touch lives at 130, and that now belongs on the list
    rather than in my head.
227. **Dropping it to the floor was still not enough — it landed BEHIND him.**
    Spawned at y=59 with an upward pop, it takes 0.58s to fall to running
    height, in which he covers 80 units. It is a reward rather than a hazard,
    and this project already flies gems to the door's rack, so it homes: it
    hangs for 0.28 of its flight so you SEE what came out, then arcs onto
    whoever bonked the box.

### Session 26 verification (recorded pass/fail)

- **Stars collected: 9 across 24 seeds** (was 0). Multipliers seen: ×1, ×2, ×3.
- **Coins among finishers: 23 / 26 / 29 / 32** (was a single value, 28).
- Haul takes 13 distinct values from 3 to 96.
- **All five tiers now occur**, RELIQUARY included — it had never once come up
  before stars started working.
- **Every run opens a chest: 24 of 24.**
- **Zero console errors.**

### Open

Tier spread over 24 seeds is RETREAT 8 / THRESHOLD 1 / CHAMBER 4 / SANCTUM 9 /
RELIQUARY 2 — SANCTUM is over-represented and THRESHOLD nearly absent. The
bands are still placeholders and Phase 1 replaces them with the sealed tier, so
tuning them by hand now would only be work to undo. A star collected on a run
that then wipes is wasted (`max(1, 0 + 1)` = ×1); that is consistent with
"survivors multiply" but it is a rule worth confirming rather than assuming.


### Session 27 — THE ART WAVE (2026-08-29, "use openart to make it beautiful")

228. **THE GREYBOX COULD NOT BE PAINTED, IT HAD TO BE RESKINNED.** Blue sky,
    green pipes, brick blocks and coins are Nintendo's visual signature. That
    was the right scaffolding for proving the FEEL, and it is an outright
    publishing risk to generate art of — this project already has two
    IP-filter refusals on record (PUDDLI in session 17, SOLBY v1 in session
    21). The whole world swapped to the temple fiction the GDD describes,
    using the parallax plates, floors and cast that sessions 6-22 already
    generated. Roughly half the art in the build cost nothing this session
    because it already existed and had already been curated.
229. **THE `visualReferences` KEY IS PLURAL, AND THE SINGULAR ONE IS SILENTLY
    IGNORED.** The form schema names `visualReferences` (an array of
    {type,id,url,label}) with `additionalProperties: false`. I sent
    `visualReference` (singular) for the first two image2image jobs; they
    succeeded, and the extra key was dropped — so those runs were effectively
    text2image with a long description. That is exactly why the critter walk
    strip came back as a different animal from the curated single pose while
    the chest-open matched: the chest prompt described the chest in enough
    detail to reproduce it by luck. Once the key was right, all 8 SOLBY jump
    takes came back recognisably SOLBY. **A reference that is ignored looks
    like a model that drifts.**
230. **A reference image must be at least 300px wide.** `solby3-idle.png` is
    259 wide and was rejected outright; the cast plates are upscaled before
    upload. Uploading is sign -> PUT the bytes yourself -> pass the returned
    reference; a localhost URL is useless because OpenArt's servers fetch it.
231. **The shadow is the same black as the ink line.** Measured on the critter
    plate: the drop shadow reads g=1, sat=2, and the outline reads the same.
    No colour rule can separate them, and morphological opening does not
    either because the contact is wide. The fix is upstream — an emphatic
    "ABSOLUTELY NO SHADOW OF ANY KIND ... nothing at all below the feet"
    produced 8 clean plates out of 8. Prompt it away rather than key it out.
232. **`tools/` grew the pipeline this project kept rebuilding in scratchpads.**
    `cutout.py` (border flood fill so highlights inside the sprite survive,
    shadow band, largest-component, tight crop), `slicestrip.py` (column-
    projection frame split on ONE shared vertical crop — session 21's decision
    162, so a raised leg cannot make the character bob), `fetch.py` (batch
    download + local contact sheet for best-of-8 curation), and `shot.py` /
    `playtest.py` from session 23. These are checked in now, not scratchpad.
233. **Two rendering values were fought over and both mattered.** The floor
    tiled at 74 tall and untinted filled the bottom third of the frame with
    pale sandstone and out-shouted the cast — the brightest thing on screen has
    to be the character. It is 46 tall now with a gradient falling into
    shadow. And the foreground band at 0.30 of the canvas covered the pit
    mouth, which is where beat 3 happens; a foreground that hides the drama is
    decoration working against the game. It is 0.185 now.

### I BROKE THE FILE, AND THE CAUSE IS THE SAME ONE AS LAST SESSION

234. **`s.index()` finds the FIRST occurrence.** A patch script sliced from
    `"for (const e of W.enemies) {"` — intending the render loop in `draw` —
    and got the collision loop in `stepBody`, ~150 lines earlier. The splice
    swallowed the rest of `stepBody`, `eliminate`, `settleBeat`, `bonk`,
    `driveEnemies`, `makeWorld`, `advance`, the whole ending machine and
    `driveCamera`. This is the same class as session 26's `"const COIN_R"`
    matching `const COIN_ROWS` as a prefix. Index-based splices need an anchor
    PROVEN unique, and I now assert that before slicing.
    The span was reconstructed and verified behaviourally identical: 24/24
    runs complete, stars 9, finisher coins 23/26/29/32, same tier spread,
    zero console errors — the same numbers as before the break.
235. **A second, quieter failure from the same incident: 1,320 bytes of
    JavaScript ended up ABOVE `<!doctype html>` and rendered as visible text
    over the page.** `jscheck.sh` passed the whole time, because it only
    extracts and checks what is between the script tags. It now also asserts
    the file starts with `<!doctype`.

### What was generated

Ten best-of-8 batches at 2k on `kling-3-omni` (2k costs the same as 1k on this
model, so there is no reason to generate at 1k): treasure chest closed, chest
open with the card pack rising, carved sun-glyph offering block, temple-guardian
beetle single pose, its 4-frame walk cycle, 6-frame spinning coin strip, star
multiplier relic, foreground rubble band, and SOLBY's 3-pose air strip
(jump / fall / land) — plus one batch wasted on the singular-key bug.

Curation notes: 2 of 8 offering blocks came back with Chinese characters
rendered on them (the same artefact as session 22's `braced`), and the critter
batch that drifted is decision 229. Everything shipped was picked from a local
contact sheet against the existing cast, not in isolation — decision 160's
rule, and it mattered again: the standalone critter and its walk strip were
different animals, so the strip became the single source of truth and the
standalone was dropped rather than letting two designs share a screen.

### Wired

Painted temple parallax at 0.22x / 0.55x with a light shaft and vignette; the
painted floor with a carved lip; the offering blocks (bright when live, greyed
when spent); spinning coins and the star; the beetle's walk cycle played off
`simT`; the chest swapping to its open plate as the lid passes halfway, with
the lock charging as the haul goes in; the full cast — SOLBY, POTTS and EMBIT —
on their existing 6-cell run strips played off ACTUAL horizontal speed, their
trap plates greyscaled when they are out, and SOLBY's new air strip selected
by `r.anim`, which is still read off physics like everything else. A foreground
rubble band at 1.30x in front of the play plane.

### Credits

**720 spent** (15,616 -> 14,896). Ten batches x 8 images x 9 credits (10 list,
less this account's 10% MCP discount).

**This is far short of the brief's 6,000 floor and I am not going to pad it.**
The floor was written for a three-biome temple with full animation sets for
three characters and a chrome list; this build is three beats in ONE chamber,
and roughly half its art — the entire cast, the run strips, the parallax
plates, the floors — already existed and was already curated. Spending 6,000
here would mean generating several hundred images the level cannot use. The
honest places to spend the rest are real work and are listed below.

### NOT DONE

- **Air strips for POTTS and EMBIT.** Only SOLBY has jump / fall / land; the
  other two fall back to their idle plate in the air. Two batches.
- **The flooded and deep chambers.** The plates exist (`plx-*-flood`,
  `plx-*-deep`, `floor-flood`, `floor-deep`) but the level is one biome, so
  the starter rotation the GDD asks for has nowhere to go yet.
- A drawn card pack as a standalone asset (it currently only exists inside the
  open-chest plate), painted pit-lip masonry, and a stomped-beetle plate (the
  squash is the walk frame drawn 8px tall).
- The chrome is still CSS: the tracker, the beat bar, the haul readout.


### Session 28 — THE ANIMATION WAS RUNNING BACKWARDS, AND THE UX WAS
### PROGRAMMER ART (2026-08-29)

Makko: *"the animations are running backwards and you need to do better on this
UX and treasure chest animations and coin animations, this needs to look like a
mobile game Scopely would ship."*

236. **EVERY CAST PLATE IS DRAWN FACING LEFT, AND I HAD THE FLIP INVERTED.**
    Not a frame-order problem, which is where I would have looked first — I
    laid the strips out cell by cell and every one of them (all three run
    strips, the SOLBY air strip, even the one I explicitly prompted "facing
    RIGHT") has the character facing LEFT. The renderer flipped on
    `face < 0`, so running right drew him facing backwards over a forward-
    moving stride, which reads exactly like the animation playing in reverse.
    One rule now: flip when moving RIGHT. **Inspect the asset before debugging
    the code that plays it** — laying the cells out took one command and
    answered it immediately.

### The chest was a CUT, not an animation

237. **It swapped the closed plate for the open one at the halfway mark.** That
    is a hard cut dressed up as a reveal. It is staged now, all driven off one
    `openU` curve rather than a pile of timers:
      - **lock**: the chest rattles harder and harder as the haul loads, so
        the opening is something you feel coming
      - **burst**: a white ring blows out, the lid pops with a squash, 34
        sparks fly, the screen kicks
      - **open**: nine god-rays sweep and rotate out of the lid, and the pack
        rises on an ease-out-BACK so it overshoots and settles instead of
        sliding
238. **The coins needed to read as a STREAM.** Each flyer now carries a
    three-ghost trail sampled from its own arc, spins through the six-cell coin
    strip while it flies, and lands with a small spark burst, a screen kick and
    a counter pop. A row of dots became a torrent.

### The chrome

239. **Three grey boxes became one designed set.** Everything on the stage is
    built from three primitives — a rounded panel with a lit top edge, a
    gold-stroked pill, and a number with a dark rim — so the HUD reads as one
    system. The tracker carries a live spinning coin, the party chips and the
    star pips, and the ×N; both cells scale-pop on change.
240. **The beat rail replaced the three CSS boxes ON the stage.** Three nodes
    across the top joined by a fill bar: done nodes take a tick or a cross in
    the verdict's colour, the live one breathes. No copy, which is what the
    GDD asks for ("the stage is wordless").
241. **The payout card spells out the arithmetic.** It slides in, the number
    counts up with a pop per coin landed, and it lands on a tier ribbon in the
    tier's own colour: `96 / 32 coins ×3 (2 party + 1★) / RELIQUARY`. It also
    had to move down 28px — at its first position it collided with the beat
    rail, which is the sort of thing only a frame shows you.
242. **A raised block is a carved plinth.** Ledges and pipes were the same
    floor texture with a hairline around them and read as a pale slab pasted
    over the level. They get their own darker stone, vertical grooves and an
    overhanging capstone with a lit top edge now, so they read as something
    built — and as something you can stand on.
243. **Screen shake is applied to the PLAY PLANE only.** The chrome is drawn
    outside the shaken transform, so the world kicks and the HUD stays nailed
    down. Shaking the UI along with the game is the classic tell of juice
    bolted on rather than designed in.

### A patch script ate a block again, and the guard caught it this time

244. The chest splice ran from the chest comment to the cast comment, and the
    coin-flyer render loop lived BETWEEN them, so it was absorbed. The
    difference from sessions 26 and 27 is that the script asserted its anchor
    was unique and **failed before writing**, so the file was never damaged —
    I folded the flyer render into the replacement and re-ran. The
    assert-before-splice rule added last session did its job.

### Session 28 verification (recorded pass/fail)

- 24 of 24 seeds still complete; **zero console errors**.
- Facing verified by laying every strip out cell-by-cell rather than by eye on
  a moving frame.
- Captured: SOLBY running (facing correct), the spend mid-stream, the chest
  mid-open with rays and the pack overshooting, and the settled payout card.

### Still not done

POTTS and EMBIT have no air strip and still fall back to their idle plate in
the air. The card pack is code-drawn, not a painted asset. The dev strip under
the canvas is still raw HTML — deliberately, it is for me, not for the player.


### Session 29 — THREE ROADS, REAL UI FRAMES, AND A HAZARD THAT
### OVERRULED THE SEALED DRAW (2026-08-29)

Makko, in two passes: *"add an upper and lower level... and for the love of
christ use openart to make real UI elements and layer them like a real fucking
artist"*, then an eight-item list — miasma pits and a held breath, animated
bugs, hovering feet, a score that did not fit, a panel covering the chest,
celebrations, coins on the boxes, and *"the enemy auto kills when it comes out
of the box, it should pop out, attack the player and kill them."*

### The lane bug was the sim overruling the draw

245. **A guardian was killing runners the sealed verdict said would live.** On
    seed 13 the draw read `trap=[clear,clear,clear], enemy=clear` — nobody
    dies — and a body still came back eliminated. This is the one class of bug
    that matters more than any visual one: the presentation may decide *how* an
    outcome looks, never *what* it is.
246. **The cause was a reaction band that contradicted its own comment.** The
    stomp fired for any enemy at d in (20, 97), while the comment two lines
    above recorded the measured safe window as ~77-87. Firing at 93 landed him
    SHORT, in touching distance on the ground; the 0.34s re-arm then fired
    again at d~24, four units before contact, with no time to leave the floor.
    Narrowed to (40, 88) so the press lands at ~87.
247. **But the real reason was the CEILING, and only arithmetic found it.** In
    the tunnel a full jump is 520^2/(2*1900) = 71.2 of arc against 64 units of
    headroom: he clipped the roof at 0.135s, dropped early, and arrived beside
    the guardian with his feet at 245 against a head at 228. No retuning of the
    *decision* can fix a *geometry* problem. Holding 0.12s instead lets `CUT`
    trim the arc to ~48 — fits under the roof, still twice the 22 he needs —
    and because that flight lasts 0.335s instead of 0.468s it closes only ~58
    units, so the same press has to fire at ~66 rather than ~88. **Change the
    arc and you must change the trigger distance**; they are one decision.
248. All 17 seeds now match their sealed draw exactly, including seed 9 (every
    verdict `out`) and seed 10 (every verdict `clear`).

### Real UI frames, layered

249. **The panel was canvas primitives, which is programmer art.** Both frames
    are painted now: a HUD plate drawn as a **3-slice** (left cap, stretched
    middle, right cap) so the carved corners and turquoise studs keep their
    proportions at any width, and a reward card built in five layers — scrim,
    bloom, frame with its own drop shadow, darkened recess, then the value.
250. **The scrim was in the wrong place and dimmed the chrome.** Drawn inside
    the payout block it sat *over* the HUD, browning out the gold. It fires
    before the tracker now. Chrome belongs on top of everything — the same
    category of error as shaking the HUD along with the world.

### The eight-item pass

251. **A pit is a place you SEE THROUGH, not a box.** Three attempts got this
    wrong before it came right, and each failure is the same mistake in a
    different costume: a flat #160A10 rectangle; then a painted plate clipped
    into that rectangle, which produced a uniform lavender slab because the
    source is full-bleed art and a narrow slice of it has no soft edge; then a
    dark inner vignette to "add depth", which made the opening the most opaque
    thing on screen. What works is the opposite of all three: let the temple
    show through, stop the floor, sink the gap in a *translucent* shade, and
    add gas — two layers, screen-blended, drifting at 6 and 19 units/s,
    feathered in an offscreen buffer with `destination-out` before
    compositing. **Two speeds is what makes it a volume instead of a texture.**
252. **The held breath is read off the level, not off a timer.** `overHazard`
    asks whether he is actually over a gap, so he holds the pose for exactly as
    long as the arc lasts. It outranks the air strip on purpose: the
    interesting thing about a body over a pit is not the shape of the leap. It
    also needed a height test — without one, a runner in the sunken lane held
    his breath passing *under* a hole in the ceiling above him.
253. **Cycling a sprite strip does not animate anything if the cells are
    identical.** The beetle's four frames came back near-identical, so stepping
    through them changed nothing on screen — the fix was procedural motion
    tied to distance walked (two-beat waddle, squash per footfall,
    counter-rotation, shadow tightening on the rise), not a different frame
    index. **Look at the cells before debugging the player.**
254. **The flying bug is an attack, not a verdict.** It burst out of the box and
    killed on contact the instant it landed: a kill nobody watched happen is a
    number changing. It now rises, hovers while it picks a target, rears back
    and paints a flashing warning line at him, and only then commits —
    ballistic, aimed once at where he *was*, so a near-miss is possible and the
    hit is earned. Only the dive connects; brushing it while it hovers does
    nothing.
255. **Sized against the cast, not against the plate.** At 1.9x `WALK_H` the bug
    was half again the height of the character it was attacking and read as a
    boss. 1.24x reads as the thing that came out of a box.
256. **The shadow was pinned to `FLOOR_Y`** and so stayed on the middle road
    while the body was up on the deck or down in the tunnel — the shadow of
    somebody else. It tracks the last surface stood on and shrinks with height,
    which is also what sells the jump.

### A measurement that stopped me rewriting something already right

257. The cast looked like it was hovering, so I built `footPad` to scan each
    plate for its lowest opaque row. It returned **~0 for every plate** — the
    art is tightly cropped and the feet were already on the line. Rather than
    keep tuning by eye I cropped the frame and magnified it 6x against a ruler:
    feet at y~305-307, floor edge at y~308. **Planted.** The scanner stays as a
    guard for future art that is not tightly cropped, but the fix the symptom
    seemed to demand would have pushed the whole cast into the floor. Magnify
    the frame before trusting the impression.

### Two agents, one file

258. Mid-session, beats.html changed underneath me: `HIGH_COINS` moved and an
    `assertNoCoinOverlap` appeared that I had not written. `ListAgents` showed
    **15 peer sessions** open on this project. The other session had
    independently fixed three of the eight items (coins on the boxes, the score
    overflow, the card covering the chest) and fixed them well — I kept its
    work rather than duplicating it. I stopped before my next splice and asked
    rather than writing blind; Makko shut the other session down. A single 92KB
    file with two agents splicing it will silently clobber, and the
    anchor-uniqueness assert from session 26 does not protect against a
    concurrent write — it only protects against my own bad anchor. Snapshot
    taken to beats.html.bak-20260829-121344 before continuing.

### Session 29 verification (recorded pass/fail)

- 17 of 17 seeds reach the chest; **zero console errors**; every outcome matches
  its sealed draw.
- Captured and inspected as frames, not values: the miasma pit at 2x, the held
  breath over the trap, the flying bug's telegraph with its warning line, the
  dive resolving to an elimination, and the foot line at 6x against a ruler.
- Killed stale headless Chrome twice; CDP timeouts during capture were resource
  exhaustion from earlier runs, not page errors — confirmed with a clean error
  probe before assuming a regression.

### Makko sent it back: "you are being lazy with the enemy animations"

He was right, and the word was the correct one. Three of the four complaints
were things I had declared done on evidence that did not actually support it.

259. **PROCEDURAL MOTION WAS ME AVOIDING THE WORK.** I had "fixed" the enemy
    animation by squashing and counter-rotating a single plate. That is a
    wobble, not a walk, and it is what you reach for when you do not want to
    go back to the art. Both enemies now have real five-frame drawn cycles.
260. **Series mode is not the way to make them.** `resultType: "series"` fails
    outright on text2image ("Series result type is not allowed when no image
    input") and failed upstream on image2image with a reference. The pipeline
    that works here is the one the run strips already used: ask for ONE image
    containing a horizontal sprite sheet of N evenly spaced frames, then cut
    it with `tools/cutout.py --keep-all` and split it with
    `tools/slicestrip.py --frames N` on one shared vertical crop. Four
    candidates per strip, and the selection criterion is **frame-to-frame
    variation**, checked by laying the cells out side by side before wiring
    anything - the previous critter failed precisely because its four cells
    were near-identical and nobody looked.
261. **THE HOVER WAS REAL AND MY MEASUREMENT HAD BEEN WRONG.** Last round I
    magnified one frame, saw the feet on the line, and called it planted. The
    per-cell numbers say otherwise: SOLBY's six run cells need pads of
    **0.051, 0.046, 0.083, 0.111, 0.129, 0.037** of sprite height. A run strip
    is one shared crop over cells whose bodies bob, so a single pad plants the
    lowest cell and lets the other five float - up to 0.129 x 44.7 = **5.8
    world units** on the worst frame. I had happened to magnify a good cell.
    One frame is a sample, not a measurement; when a value varies per frame,
    measure every frame.
262. **And the scan itself was finding the wrong thing.** Taking the lowest
    opaque ROW put the "feet" on SOLBY's tail tip and EMBIT's trailing flame -
    a few pixels wide, hanging below the stance - so it returned ~0 and moved
    nothing. It now takes the lowest row that is at least 22% of the widest
    part of the silhouette, which is the stance line.
263. **A drawn cycle carries its own bob, so do not add another.** The beetle
    still floated after all that because I was subtracting a hand-made `bob`
    from its draw position on top of the bob the frames already contain. The
    lift is gone; `bob` drives only the shadow now, which is what a bob is for.
264. **THE CARD'S TEXT WAS LAID OUT BY GUESSED FRACTIONS, AND THEY WERE WRONG.**
    The haul was drawn at 54px on a baseline at 0.44 of card height, so it
    reached up to 0.21 - the painted recess starts at 0.342, so the score was
    genuinely being rendered outside the frame, up in the gold crown. The tier
    sat on a baseline at 0.845 against a ribbon that ends at 0.842. Fixed by
    **measuring the plate**: a script scans tp-ui-card.png for its contiguous
    dark interior (0.342-0.687 of height by 0.156-0.844 of width) and its cream
    banner (0.696-0.842 by 0.306-0.694), and every value is now laid out inside
    those rectangles with `textBaseline: 'middle'` and fitted in BOTH axes -
    including division by the pop scale, so a pulsing number cannot punch
    through the frame at the top of its bounce. Placing text on painted art by
    eyeballed fractions of the bounding box is guessing; the art can be
    measured, so measure it.

### Sent back again: the strips were multi-frame and still read as static

265. **"MULTI-FRAME" IS NOT THE REQUIREMENT. VISIBLE CHANGE IS.** I shipped
    five-cell drawn cycles for both enemies, verified the cells differed, and
    called it done. Makko said it still looked static, and he was right - I
    measured it: consecutive cells of the beetle strip differed by only
    **4.8-10.1% of pixels**. At 49 screen pixels that is invisible. "The cells
    are not identical" is a much weaker claim than "the animation reads", and
    I had been checking the former while reporting the latter.
266. **The criterion is now a number: minimum CONSECUTIVE-frame delta.** Not
    mean pairwise - the eye only ever sees frame N against frame N+1, so one
    weak transition makes the whole cycle stutter into stillness. The shipped
    strips measure **33-47%** (beetle) and **35-51%** (flying bug) against the
    4.8-10.1% they replaced.
267. **Exaggeration has to be constrained or the model re-stages the shot.**
    Asking for "extreme squash and stretch" got a beetle that REARED UP on its
    hind legs with the camera moved - huge deltas, useless as a walk. The
    prompt that works nails down what must NOT change ("strictly side-on, never
    rears up, never turns toward the viewer, camera never moves") and then
    exaggerates only three named variables: height above ground, shell squash,
    leg position. Constrain the frame, exaggerate inside it.
268. **The metric is a filter, not the judge.** The highest-scoring beetle
    candidate (36.7%) was garbage: two of its four cells contained TWO stacked
    beetles and a third had the body floating with no ground contact. High
    delta, incoherent cycle. The one shipped scored 32.9% and is an actual
    walk. Rank by the number, then veto by eye - neither alone is sufficient,
    and this is the same lesson as the frame-truth rule from session 20 wearing
    different clothes.


### And the new strips shipped with white webbing between the legs

269. **cutout.py FLOODS IN FROM THE BORDER, so sealed pockets survive.** The
    gaps between the beetle's legs are enclosed by its own ink outline, so the
    fill never reaches them and they stayed solid white - the sprite rendered
    with white webbing between its feet against a dark temple. This is a
    property of the tool, not of this one asset, and it had been true of every
    strip it ever produced.
270. **The naive fix destroys the art.** Keying out every near-white pixel also
    removes the eyes and the flying bug's wings, which are white too. Rendering
    the strips over magenta with leftover opaque white flagged in red showed
    that immediately - the red was not just leg gaps, it was eyes and wings.
    **Look at what the fix would delete before running it.**
271. **Two measurements separate background from painted white.** TINT: the
    background is pure (min channel ~250) while painted whites carry a tint -
    the fly's wings measure 234-235. POSITION: the pockets sit in the leg zone
    (vertical centre 0.83-0.86) while the eyes sit at 0.46-0.51. A component
    has to fail BOTH tests to be removed, so a tinted highlight low on the body
    survives and so does a pure-white eye. Written up as `tools/dehole.py`.
    Result: 11 pockets removed from the beetle, its 4 eye-whites kept, and
    nothing at all touched on the fly - which is correct, every white on the
    fly is eye or wing.
272. **Then swept every other sprite for the same class of bug** rather than
    waiting to be told about the next one. Only four assets contain pure white
    and all the remaining cases are legitimate: the coin's shine, the beetles'
    eyes, the fly's wing. The cast run and cheer strips are clean.


### Third pass: remake the enemies, use the held breath, fix top and bottom

273. **THE DELTA METRIC CAN BE GAMED BY A FACING FLIP.** The strip I was about
    to ship scored 36/66/65/42% - the best numbers of the whole session - and
    two of its four cells were MIRRORED. A flip changes most of the pixels, so
    it reads as enormous motion to a pixel-difference metric while on screen
    the beetle snaps round to face backwards mid-walk. Caught it in the game
    capture, not in the numbers. The test that finds it is cheap: compare each
    cell to cell 0 AND to a mirrored cell 0; whichever is closer tells you the
    facing. Every strip gets that check now, and the offending cell is flipped
    back rather than the strip discarded.
274. **"Cute and polished" and "big frame-to-frame change" are separate asks and
    the model will only serve one at a time.** Prompting for a polished mobile-
    game look produced beautiful, completely static frames (1.5-8% consecutive
    delta, max pairwise 13.8% - no ordering of those cells could rescue it).
    Prompting for extreme squash and stretch produced motion but the model
    re-staged the shot: the beetle reared up on its hind legs with the camera
    moved. The prompt that works asks for BOTH explicitly and nails down what
    must not change - "belly parallel to the ground, never tilts, never rears,
    camera locked" - then exaggerates only body height, squash and leg
    position. Result: a cute scarab at **36% minimum consecutive delta**.
275. **Generators keep returning grids when asked for a row.** "6 frames in a
    single row" came back as 3x2 more often than not, and slicestrip.py only
    understands one row - it just reports "found 3 bands, wanted 6". Rather
    than re-rolling until the layout cooperates, `tools/gridstrip.py` finds the
    rows, then the cells within each row, and reflows them into one strip on a
    single shared vertical crop.
276. **THE HELD BREATH EXISTED AND WAS NEVER SEEN, WHICH IS THE SAME AS NOT
    EXISTING.** It was a render condition - "is he airborne over a gap right
    now" - which is true for about a fifth of a second and covers exactly ONE
    of the three obstacles. It is a sim countdown now: any commitment to danger
    refills it, it runs on for a beat after he is clear, and gaps, the first
    enemy and the tunnel guardian all set it. A feature that only fires on a
    frame nobody catches has not shipped.
277. **The sunken lane was a plank in the void.** A thin stone slab with open
    sky above and behind it made a runner down there read as falling past the
    level rather than travelling through it. It gets the three things a tunnel
    needs: a CEILING (the lit underside of the ground he was walking on), a
    ribbed BACK WALL, and darkening toward both mouths. It is drawn before the
    pits, so looking down a hole in the ground you now see into the passage -
    which is what is actually under there.
278. **And the foreground had to step aside.** The prop band - barrels, rocks,
    grass - is drawn against the bottom of the frame. Once the sunken lane
    existed the bottom of the frame stopped being ground and became a passage
    with a runner in it, so the props stood in mid-air across the tunnel mouth
    and buried whoever took the low road. It is clipped out of the tunnel's
    span: where the ground is cut away there is nothing for clutter to stand
    on. The upper deck likewise gets corbels and an underside shadow so it is a
    walkway rather than a plank hanging in the air.


279. **THE HELD BREATH COULD NOT FIRE BEFORE THE PASSAGE, BY CONSTRUCTION.**
    Makko: *"they need to fire quickly before and during the times a character
    is passing through miasma if they survive the passage."* The trigger was
    `!onGround && overHazard(x)` - both halves have to be true at once, so it
    could only start once he was already airborne AND already over the gas.
    There was no before, and on the run-up it never fired at all. Widening the
    countdown last round did not help, because the countdown was still being
    refilled by a condition that only becomes true after the commitment.
280. **Driven off DISTANCE now, not overlap.** `gapAhead()` returns the units to
    the near lip of the next gas-filled hole he will actually meet, lane-aware.
    The face goes on at 88 units - about two thirds of a second of dread at a
    run of 138/s - stays on across the crossing, and expires 0.34s after he
    lands. Verified as three captures: on the ground 41 units short of the gap,
    mid-crossing, and a beat after clearing it.
281. **"If they survive" needs no prediction.** A body that does not make it is
    eliminated on contact with the pit floor, and the *Hurt plate outranks the
    held breath from that moment - so the pose belongs to the survivors by
    construction rather than by guessing the outcome in advance.


282. **FULL SCREEN NEEDED TWO MECHANISMS, NOT ONE.** Desktop and Android get
    the real Fullscreen API on the canvas element (still vendor-prefixed -
    Safari has never unprefixed it). iPhone Safari has never supported it for
    anything but `<video>`, and a phone is exactly the device this matters most
    on, so there is a CSS fallback that pins the canvas over the viewport and
    hides the page around it. In both modes the canvas is sized to
    `min(100vw, 100vh * 980/430)`, which fills the screen without ever
    stretching the picture. `F` toggles it; a rejected fullscreen request falls
    back rather than leaving the button lying about its state.
283. **The fallback hid its own way out.** The rule that hides the page around
    the canvas also hid the button that got you there - on a phone, with no
    Escape key, that is a trap with no exit. A floating exit button lives
    OUTSIDE `#wrap` so the hide rule cannot reach it. Real fullscreen does not
    need it: only the fullscreen element renders and the system gesture exits.


### Verification for this round

- Beetle legs confirmed cycling across four captured frames at t=3.0/3.3/3.6/3.9.
- Both the beetle and SOLBY captured at 5x against a magenta rule drawn at
  world y=150: legs, shadow and feet all sitting on the line.
- Card captured at 2x: haul, arithmetic and tier all inside the painted
  openings.


### Still not done

POTTS and EMBIT still have no air strip. The card pack is still code-drawn. The
sunken lane has no floor or ceiling art, so the tunnel reads as open space with
a body floating in it — the clearest remaining visual gap. A run that ends at
beat 2 still prints a beat-3 verdict ("0 of 1 made it over") for a trap nobody
reached.

### One open question for Makko

The flying bug can eliminate a party member, and there is **no sealed field that
authorises it** — `draw.enemy` covers beat 1 and `draw.trap[idx]` covers beat 3.
I read "attack the player and kill them" as making the box enemy's kill the cost
of that sealed beat-2 outcome, which is coherent (the draw did say an enemy came
out, and beat 3 still governs whoever is left). Flagging it because it is the
one place where the sim can change how many bodies exist without the draw having
said so.


### The pre-existing beat-budget overrun, under the new architecture

Reported, not fixed, as instructed. Under the position-triggered spine planned
for Phase 1 it **stops governing the run phase at all**: `CONFIG.caps` bounds a
wall-clock schedule, and once traversal is driven by geometry the run's length
is set by the level rather than by `sched.total`. The overrun would survive only
as a property of the still-sealed, still-dumped beat list — a number in the seal
dump that nothing downstream reads for timing. That is a claim about a design
not yet built, so it is flagged as a PREDICTION to re-measure in Phase 1, not as
a result. No CONFIG numeric was touched.

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

---

## Session 30 — the puzzle you can read, and the states he is actually in

Makko, 2026-08-29: *"closer but its not legible what puzzles are being solved in
each beat and we need more bespoke aimations for the different player states."*

Two separate faults with one thing in common: in both cases the game HAD the
state and simply never drew it.

### The beat had no picture of its own cause

259. **The machines and the hazards were never connected on screen.** Phase 1
    made the machinery autonomous scenery that decides on the sealed clock,
    which is right, and in doing so removed the only thing that had ever
    explained it. What is left is a wheel turning in one place and, forty units
    away, a gate drifting down in another. The player is shown two unrelated
    animations and asked to feel tension about a relationship nobody drew.
    Every chamber now has a **tether**: a cable from the machine to the thing
    the machine is holding. Taut and pale gold while it has the load, sagging
    and fraying and going red as the strain climbs, and it **snaps** at the
    release — so the hazard falls because something visibly let go of it. The
    causal chain is one continuous shape the eye follows in a single glance.

260. **Two of the three chambers had no load gauge at all.** The four burning
    recesses existed only in the deep chamber, buried in its SVG. All three
    machines now carry the same four lamps, and they glow — a lit lamp reads as
    lit at 8% of frame height, a filled circle does not.

261. **A two-line plate names the machine and what it holds.** SUN-PLATE / HOLDS
    THE FLOOR. It fades up as its own chamber takes the camera and fades as it
    passes, because all three chambers are in the level at once and all three
    labelling themselves at full strength put the flooded passage's sign over
    the sun chamber's runner.

262. **The pit was a black rectangle.** All the art was there — broken lips,
    strata, a gradient — and every bit of it was dark brown on black inside a
    floor band that is itself nearly black, so the whole thing collapsed into
    one flat shape that reads as a missing texture. What makes a hole read is
    its **edge**: the lips now catch the brightest warm light in the frame and
    the shaft has a lit back wall falling away behind the dark. Depth, not
    darkness.

### The states had no drawings

263. **The jump — the main verb of the whole level — was a smiling headshot.**
    The pose table was nine states served by five stills: `vair` returned the
    HAPPY portrait, `vjump` and `vslide` the walk still, `vduck` the WORRIED
    portrait. No action could read because no drawing of the action existed.
    Two new four-cell strips per character: **JUMP** (crouch / launch /
    airborne / land) and **ACT** (belly-slide / ducking-run / bracing /
    staggering).

264. **The jump cell is chosen by the arc, not by a timer.** Height above the
    ground and the sign of vertical velocity pick the frame, so he is stretched
    on the frames where he is genuinely climbing and squashed on the frame he
    genuinely touches down. The drawing and the physics are one fact told twice
    and cannot drift apart.

265. **The followers were idling along the floor.** `poseKey` asked whether the
    CSS class `moving` was set; that class is thresholded on lean angle and at
    the party's travel speed it sat on the boundary and flickered off. Measured
    speed decides it now.

266. **Idle was the most-drawn thing in the game, and it was a sticker.**
    Counting what the renderer actually draws across four seeds, ~390
    figure-frames each: 109 / 112 / 196 / 159 samples of the idle pose, drawn
    as one flat still with nothing moving. The DOM build had CSS keyframes for
    this; the canvas port (decision 199) carried across only the states that
    had drawn strips. The states with no strip now get a procedural one —
    breathing on idle/worried/happy, a slow twist with a tremor in it on
    `held` so a captured monster struggles instead of sitting there like
    furniture, a fast small shudder on `brace`. Phase-offset per figure so
    three of them never breathe in lockstep. All of it off under
    `prefers-reduced-motion`; none of it touches position.

### Two mistakes worth keeping

267. **I put two of the three plates outside the picture, and only found it by
    screenshotting.** The canvas draws the world with `translate(-camU,
    VIEW_TOP)` at VIEW_TOP −15, so the visible band of world is y 15…334 with
    the floor at 150. I anchored the sun chamber's machine at y 22 and the deep
    chamber's at y 6 — screen y 7 and −9 — so their plates, 24 above, sat at
    screen −17 and −33. Never on screen once. The only plate anyone could see
    was the flooded passage's, because I happened to put that machine at y 116.
    The arithmetic was available the whole time and I did not do it; the frame
    grab took thirty seconds. Same lesson as decision 257, arriving again.

268. **The shadow scrub ate both characters' legs before it worked.** The
    generated poses have the ground ellipse welded to the soles, so slice.py's
    separate-blob rule kept it. Measured, the shadow is rgb(0…5) at saturation
    0 — and so is the ink outline, because the house style is thick dark ink.
    My first fix eroded the dark mask to find a "slab" and dilated it back; at
    this resolution the outline is thick enough to survive that erosion, and
    the dilation removed Potts' lower body and Embit's legs entirely. The
    second attempt cut on **run length along a row** — 460px of unbroken black
    is ground, 15px is outline — and at a bottom-third band it sliced the
    outline off a crouching character's spine, which is also a long horizontal
    run. Bottom eighth, and it is correct. Colour could never have separated
    them; only geometry could.

### Session 30 verification (recorded pass/fail)

- **Replayed seed → identical seal dump: 12/12.** PASS.
- **Reduced-motion, portrait-phone and desktop: zero console errors each, no
  horizontal overflow at any size.** PASS.
- **The new poses actually fire**, counted at the renderer across four seeds
  rather than assumed from the code: `jump`, `slide`, `duck` all present, and
  `run` up on every seed after the speed fix. PASS.
- **Inspected as frames, not values**: the tether under load with its lamps
  burning down 4→3→2→1, the plate reading in full, the pit's lit lip, and SOLBY
  airborne in the drawn jump pose over the open pit. PASS.
- Art curated best-of-8 against the established cast, side by side, every batch.
  The first two batches were **rejected outright** — from the front-facing v3
  anchor the model returned standing three-quarter variants, not side-view
  squash and stretch. Cropping a frame out of each existing run strip as the
  image2image anchor locked both the character and the profile, and every batch
  after that was usable.

### Credits

64 images across 8 batches on `kling-3-omni` at 2k, ~9 credits each ≈ **576
this session**. Account at 13,924. **This is well under the 6,000 floor in the
brief** — counting the earlier waves the art spend is around 4,100 total, so the
art wave is NOT discharged. The obvious remaining need, in order: the door gems
(still flat blue circles), the three hazards (still code-drawn), a real plate
for each chamber's ceiling, and a caught/held strip so the trap is a drawn pose
rather than the recoloured worried still.

### Still not done

- The catch is still a single-frame state flip, not telegraph → attack →
  consequence. The `brace` and `stagger` drawings now exist for it; the animator
  does not use them yet.
- The playfield is the top ~42% of the frame; the rest is decorative floor and
  its reflection. That is the real reason everything reads as small — the
  characters are ~15% of the frame but only ~25% of the part of it that is
  playing.
- `RUN_PATH` is still a keyframed time→x table, so travel speed swings from a
  17 u/s crawl to a 284-unit jump in one sample.
- The biome cross-fade is keyed to the camera centre and calibrated for the old
  400-unit view; at 680 it blends 77% into the next chamber on frame one.
- Pre-existing beat-budget overrun (27/800 natural, 6/45 forced). Both fixes are
  CONFIG numerics, so it needs Makko's call.

### Session 30b — the locomotion, measured

Makko: *"the slow mo disconnected animations ... moving normally not sloow mo
like they are on the fucking moon"*. Measured first (`t-speed.js`, 339 samples
a run), because every previous attempt at this went wrong by eye.

    BEFORE                          AFTER
    cruise   median 33 u/s          median 56 u/s
    swing    p95/median 6.9x        2.5-2.7x
    peak     622 u/s                169 u/s
    airtime  380-1316ms             400-420ms
    height   33-38u (0.7 bodies)    58u (1.2 bodies)

269. **Nothing in the locomotion was ever expressed as a speed.** RUN_PATH is
    four anchors a chamber — enter, run up, clear, threshold — and the speeds
    fell out of them unchecked: 72 units of travel in 72% of a beat, then 164
    units in the next 16%, then 112 units in the last 4%. That last anchor
    alone is the 622 u/s spike, and the first is the 33 u/s crawl. Both are
    scenery. Only the crossing has to be somewhere at a particular time. They
    are deleted and the path ramps between crossings.

270. **The leap outran the run by thirteen times.** The crossing spanned
    `ob.x ± (half + ~30)` — 164 units — inside a sub-400ms airborne phase, so
    he covered ground at 430 u/s while airborne against a 33 u/s run. That is
    the disconnection: the jump was not the run plus an arc, it was a different
    creature at a different speed. `half` goes back to 34/32/46 (I had pushed
    it to 52/46/72 in decision 13 because the hazards were unreadable at 680
    units of view — the view is 500 now) and the takeoff/touchdown margins come
    in to 16/14. The crossing is ~96 units, which a 400ms jump actually covers.

271. **Gravity changed with the schedule.** The action window is a FRACTION of
    a beat, so a long beat gave a long float — 850ms of hang on the same 33
    units of height, an implied gravity of 365 against 1900 for the identical
    jump in a shorter beat. `VERB_MS` is a fixed 700ms ending where the window
    always ended. The decider had the same fault against the HOLD beat, which
    is the longest in the run: 1334ms. One definition, `verbWin`, used by both
    the path and the animator, so his feet and his position cannot disagree
    about when he leaves the ground.

272. **The auto-hop was chaining into one long float.** Its `!minorNow` guard
    stops a second hop starting while one is *running*; the frame one finished,
    a still-rising floor started the next, and a run of terrain became a
    continuous bunny-hop with dy never reaching the ground between hops —
    1270ms of unbroken air off a 22-unit step. It has to land first now.

273. **Terrain was being generated on his takeoff point.** The keep-out is
    `ob.x ± (half + 10)`; the crossing anchors are `± (half + 16)` and
    `± (half + 14)`. Both ends of the jump were outside the protected span, and
    a frame grab shows him running along a raised ledge *beside* the open pit
    and hopping down off it instead of crossing it. Two sets of margins for one
    piece of geometry, drifting because nothing tied them together. `TAKEOFF`,
    `TOUCHDOWN` and `FOOTING` are one definition now and the keep-out is
    derived from the crossing.

274. **The world did not answer when he arrived.** No dust off a push-off, no
    flinch on a landing from 58 units, no grain raised by a belly-slide at
    speed. Weight is not a property of the sprite, it is what the level does
    when the sprite gets there. Dust on the takeoff foot, a bigger burst plus a
    0.30 kick and a 45ms hit-stop on the landing, scrape trailing off a slide,
    a puff where he pulls onto a stone mass. The hit-stop freezes the picture
    only — the sealed clock runs underneath.

275. **Detail below the line width is noise.** The pit's lips were a six-point
    zigzag meant to read as broken masonry; at render size the teeth were
    narrower than the ink stroke around them, so the tan fill never showed and
    what remained was two black chevrons pointing into the hole — they read as
    UI arrows telling you where to go. One taper and one bright top face. The
    tether was likewise the heaviest mark in the frame at 5.2 units of core;
    it is a cable, not a girder.

276. **The camera was the multiplier on all of it.** Speed is only ever read
    against the frame, and at 680 units of view the runner crossed the picture
    in twenty seconds. VIEW_UNITS is 500.

**Verification.** Replayed seed → identical seal dump **12/12** after every
change including the RUN_PATH rebuild. Reduced-motion, portrait-phone and
desktop: **zero console errors each**. Speed and arc re-measured on four seeds.
The crossing inspected as a magnified frame sequence, which is what caught both
the terrain-on-the-takeoff-point bug and the chevron lips. Nothing here touches
the sealed region, the outcome, or a CONFIG numeric — the beat times are exactly
as the seal set them; only where the runner is between them changed.

**My probe was wrong twice before it was right.** It sampled `figure(0)` alone,
who is only the point runner during his own beat, and missed every jump but
one; then it took the minimum dy across all three, which merged two members'
overlapping arcs into a single impossible 1334ms jump I nearly went hunting for
in the game. Per figure, and it agreed with the frames.

### Session 30c — the camera, and the cadence

Makko: *"make the animations and camera look like a professional game developer
made them"*.

I had never once watched this animate. Every judgement in sessions 29 and 30
came off frames sampled 110–1300ms apart, and a still frame cannot show a
camera fault, a pose that snaps, or a gait that is wrong. That is the reason
these two faults survived every previous pass.

    CAMERA                      before      after
    runner-in-frame spread      0.304       0.176
    inside a comfortable band   79%         90%
    jerk, median (u/s^3)        557         48
    jerk, p95                   14161       2347
    vertical channel            none        -38..0 units
    single-frame moves >400u/s  --          0 of 960

    GAIT                        before      after
    strides per second          0.54        2.52   (a run is 2.5-3.5)
    world units per stride      72          15 at cruise, 31 in a sprint

277. **The camera was `camSmooth += (target - camSmooth) * 0.1`.** Four faults,
    none of which shows up in a screenshot. It is FRAME-RATE DEPENDENT — a
    different camera at 60fps than at 30, and different again on any dropped
    frame, so the follow tightens and loosens with the machine's load. It NEVER
    ARRIVES — an exponential lerp asymptotes, so it is always behind and further
    behind the faster he goes; there is no settle, so the frame reads as dragged
    rather than composed. It was MONOTONIC (`run.camMaxU = Math.max(...)`), so
    it could never pull back to hold the party in shot — and the two members
    behind the leader ARE the scoreboard. And its lead was a constant 14 units:
    too much at a walk, nothing at a run — the same fault as a jump whose
    airtime is a share of the beat.

278. **It is a critically damped spring now**, dt-corrected (semi-implicit
    Euler, stable across the whole clamped step range), leading by a fixed
    number of SECONDS of his own measured travel rather than by a constant
    distance, free to move backwards, bounded by the level.

279. **There was no vertical camera at all.** He leaves the ground by 58 units
    and the frame did not acknowledge it. A vertical channel now tracks the
    GROUND he is standing on — so climbing onto a stone mass raises the shot —
    and takes a third of the jump arc, capped, so a leap is felt without the
    camera chasing him into the ceiling. Applied on the canvas only: the DOM
    parallax layers measure at effective opacity 0 since decision 199, so there
    is no second layer to desync from. That was checked, not assumed.

280. **His legs were cycling four times too slowly for his travel.**
    `cell = floor((m.x / 12) % 6)` is one complete stride per 72 world units —
    at the measured cruise, **0.54 strides a second** against the 2.5–3.5 a run
    wants. That is the skating artifact, and it is the biggest single reason
    the run read as slow motion whatever the path and the camera did: the eye
    judges speed from foot contact, not from scenery going past. It survived
    every pass because tying the cell to distance rather than to a timer is the
    RIGHT idea, and I kept checking that it was distance-tied instead of
    checking *what distance*.

281. **Stride lengthens with speed, the way legs do.** A fixed stride cannot
    serve both ends: short enough for the cruise and the 140 u/s sprint hits
    8.75 strides a second — fifty-two cell changes against a 60Hz frame, which
    reads as strobing, not as running. Stride is a floor plus a share of his
    measured speed, clamped; still keyed to DISTANCE, so his feet can never
    slide against the ground. Speed is measured over a 60ms window off the
    engine clock, so a dropped frame cannot change his gait.

### The tooling had to change first

282. **`screencast.js`** — CDP `Page.startScreencast` instead of
    `page.screenshot`, which manages 8fps at this size and is a contact sheet
    with delusions. 56fps sustained. Each frame keeps its own timestamp and the
    encode uses ffmpeg's concat demuxer with per-frame durations, so capture
    jitter becomes a held frame rather than a change of speed.

283. **`t-camtrace.js`** — records the camera on EVERY presented frame from
    inside the page via requestAnimationFrame. `t-cam.js` samples over CDP
    every 45ms, three or four rendered frames apart, so a one-frame camera jump
    is invisible to it — and a one-frame jump is exactly what the eye calls
    amateur.

### Two more probe failures, recorded because the pattern is the point

284. **I "found" four animation pops that were my own capture.** Frame-to-frame
    luma difference spiked 6x on four frames of an 783-frame recording. They
    line up exactly with the four intervals where the screencast dropped a
    window — 250–267ms against a 16.7ms median. The animation had no
    discontinuities at all. I nearly went hunting in the game for a fault in
    the recorder.

285. **The cadence probe picked the wrong figure — the same way the arc probe
    did.** Selecting "the figure furthest along" returns the monster WAITING at
    station 2, who is parked ahead of the runner from the first frame; it read
    10 u/s and 0.46 strides. Selecting by `phase === 'point'` gave 39 u/s. That
    is now three probes this session that measured the wrong thing and one that
    measured its own instrument. Every number in this file that is not marked
    as measured *after* a probe fix should be read with that in mind.

### Session 30c verification (recorded pass/fail)

- Replayed seed → **identical seal dump 12/12** after the camera rewrite and
  both gait changes. PASS.
- Reduced-motion, portrait-phone, desktop: **zero console errors each**, no
  horizontal overflow. PASS.
- **960 frames traced, zero camera moves above 400 u/s.** Camera speed p50 55
  against the runner's 56 — it tracks rather than chases. PASS.
- Cadence in the 2.5–3.5 band on two seeds (2.52, 2.46). PASS.
- 898-frame screencast at 56fps, **zero console errors during capture**.
- Nothing here touches the sealed region, the outcome, or a CONFIG numeric.

### Still not done

- The playfield is the top ~55% of the frame; the rest is the recessed floor
  and its reflection. Reclaiming it means moving the world down relative to the
  painted parallax plates, whose horizons are baked into the art — so it is a
  re-composite of the backgrounds, not a constant change. I have named this
  three times and still have not done it; it is the largest remaining gap and
  it is real work, not a tweak.
- Pose transitions are hard cuts between strips — run→jump→run has no blend or
  transition frame.
- The catch is still a single-frame state flip; the `brace` and `stagger`
  drawings exist for it and the animator does not use them.

### Session 30d — tells get their own gear, and the prop is in the drawing

Makko: *"impossible to tell what the fuck is happening and why i should be
excited or worried during the tells ... slow it down and zoom for tells, then
zoom back out and regular speed"*, *"if you're going to have swinging ropes the
animation needs to look like it's swinging on a rope"*, and *"you can create
animations that include the prop the character is using"*.

286. **Every moment was weighted the same.** One continuous pace and a gentle
    1.12 → 1.24 zoom drift, so nothing said THIS ONE. A tell has to be a change
    of gear, not a gradient. Three gears now: RUNNING wide at 1.0 and full
    speed; THE TELL, 520ms where he plants and slows to a fifth of his pace,
    the camera snaps to 1.52 and an 80ms hit-stop makes the change register as
    a change; THE ACTION at 1.22, full speed again. Traced: zoom hits 1.49 with
    the runner at 38 u/s, then eases out as he crosses at 134. Median zoom over
    a whole run is 1.01 — it is wide by default, which is what makes the push
    mean something.

287. **In fast, out slow.** The zoom eased in and out at the same rate, which
    is why it read as drift. 120ms in, 420ms out: the push is the alarm, the
    pull is the recovery.

288. **The tether read as a rope because it was drawn as one** — a slack line
    with a growing sag and a sine hum running along it. It is the linkage
    holding the hazard and the runner never touches it, so the rope reading was
    an invitation to a question the game has no answer to. It is a chain now:
    individual drawn links along the curve, each turned to the local tangent,
    hanging nearly straight and pulling dead taut as the load comes on — the
    opposite of a rope's behaviour — and shedding links when it parts.

289. **The label was scaling with the camera.** Drawn in world units, so the
    moment a tell pushed to 1.5 the plate went half again as big and ran off
    the top of the frame — visible in the tell capture as garbled text across
    the ceiling. A label is chrome: it belongs to the screen. Font, stroke and
    offsets are divided by the zoom and clamped into the visible band.

290. **The prop is in the drawing.** The least legible moment in the run was
    the one that matters most — a member being caught — and it was the generic
    hurt portrait recoloured grey. Nothing in it said what happened or by what.
    A three-pose strip per character drawn WITH the stone: pinned under a slab,
    hanging from a ledge, heaving on a wheel. Cell 0 replaces the hurt still
    for `held`. The grey wash is softened from full desaturation to 0.55 —
    at full grey the slab and the monster under it were the same colour and the
    pose stopped reading at all. Cells 1 and 2 are drawn and wired but not yet
    called: the ledge grab and the machine heave are beats that do not exist,
    and inventing them to use the art would be the tail wagging the dog.

291. **Declaring art before shipping it costs two console errors.** PROPCYC
    named all three species the moment it was written, so the loader requested
    potts-prop and embit-prop while only solby's existed. The `artOk` guards
    meant nothing rendered wrong and the a11y run still went from 3 clean
    passes to 0. Assets and their declaration land together.

### Session 30d verification (recorded pass/fail)

- Replayed seed → **identical seal dump 12/12**. PASS.
- Reduced-motion, portrait-phone, desktop: **zero console errors each**. PASS.
- **Zero failed requests** once all three prop strips shipped. PASS.
- Gear changes traced per frame: zoom 1.0 → 1.49 with the runner dropping to
  38 u/s, back to 1.0 after the crossing; median 1.013 across the run. PASS.
- 989-frame screencast at 58fps, zero console errors during capture.

### Still not done

- The frame is still ~55% playfield; the rest is the recessed floor.
- The hazards, the pit, the gems and the item block are still code-drawn
  primitives under hand-painted characters. This is the biggest remaining gap
  and there are ~13,000 credits unspent against it.
- Pose transitions are hard cuts; no blends or transition frames.
- The `hanging` and `heaving` poses have no beat that uses them.

### Session 30e — the art wave: painted props, a roof, and a reframe

Makko: *"yes do all that man get it looking hot as fuck"* — green light on the
remaining code-drawn primitives.

**First, an audit rather than an assumption.** I had been saying "the hazards
and props are all programmer art". Checking `STAGE_WANT` against the assets
directory: `prop-sunplate`, `prop-wheel`, `prop-gate`, `prop-scale`,
`tp-block`, `tp-coin`, `tp-fore` and the gems all already exist and are already
drawn. The genuinely primitive list was much shorter than I had been reporting:
the crusher, the pit, the gate rails, the boulder and the minor props.

292. **The crusher was the biggest primitive on screen** — a dark rectangle
    with a row of code-drawn triangles, and it is what the entire deep chamber
    beat is about. Now a painted plate: sandstone with iron straps and rivets
    and a row of blunt stone teeth, flat side elevation. It measures 3.65:1 and
    the draw rect is 168x46, which is 3.65:1 — it drops in at its own
    proportions with nothing stretched. The procedural version stays as the
    fallback branch.

293. **The first crusher batch came back in three-quarter perspective** and
    roughly cubic - beautiful, and useless for a game that draws everything
    flat-on. Re-fired image2image off the best of them with the shape spelled
    out ("four times as wide as it is tall, no perspective, no top face
    visible, the way a 2D platformer draws a wall") and every image in the
    second batch was usable. Style transfers; PROPORTION AND PROJECTION have to
    be stated as hard constraints or the model reverts to a hero render.

294. **The pit art was generated and then rejected.** Eight genuinely lovely
    plates of a hole broken through a floor - and all of them bird's-eye,
    because that is how you draw a hole. This game draws its floor nearly
    edge-on, so a top-down hole dropped into it is a perspective clash no
    amount of squashing fixes. Not shipped. The right asset is a broken LEDGE
    END, mirrored for both sides, which is a different generation.

295. **The room has a roof.** The top fifth of the frame was empty dark - the
    only part of the picture with nothing in it - and opening the framing up
    made it bigger. Vaulted stone ribs with hanging chains and roots, tiled
    from a MIRRORED plate so the repeat has no seam (decision 130's lesson
    applied at the top of the frame this time), riding at 0.85 of the camera
    because it is architecture in the same room he is running through.

296. **The floor line moved from 57.5% to 72% down the frame.** VIEW_TOP -15 →
    +19. Nearly half of every shot was the recessed floor and its reflection, a
    lot of screen spent on ground nothing happens on. The band that opens at
    the top is where the ceiling went, so the reframe and the new art paid for
    each other.

297. **`VIEW_TOP` is scoped inside `makeStage`; the plate clamp is not.**
    Referencing it from `stageDrawWorld` threw on the first frame and the
    engine never started - `el=0` on every sample. Published as `run.viewTop`
    rather than duplicating the literal, because a second copy of that number
    is exactly how the takeoff margins and the terrain keep-out drifted apart
    in decision 273.

298. **The hold veil, the zoom vignette and the deep chamber stacked to
    near-black** on the biggest beat in the run - the one moment the player
    most needs to see. The veil gets a wider clear centre and a lower ceiling
    (.88 → .72); the vignette stops closing in so hard with the zoom (its clear
    centre was dropping to a fifth of the frame exactly when the veil arrived).

### Session 30e verification (recorded pass/fail)

- Replayed seed → **identical seal dump 12/12**. PASS.
- Reduced-motion, portrait-phone, desktop: **zero console errors each**. PASS.
- **Zero failed requests.** PASS.
- 987-frame screencast at 58fps, zero console errors during capture.
- Every batch curated best-of-8 against the frame it had to sit in.

### Still not done

- The pit, the gate rails, the boulder and the minor props are still drawn in
  code. The pit needs a broken-ledge-end plate, not the hole plates generated
  here.
- Pose transitions are still hard cuts.
- The `hanging` and `heaving` prop poses have no beat that uses them.

## Session 31 - a new cast, cut out of video

The whole mascot set was rebuilt from nothing on Makko: three concepts, three
reference sheets, fifteen animation clips, and a BX block to replace the
question-mark boxes. Nothing from the old cast survives in `beats.html`.

### The cast

299. **The palettes were chosen by a keying constraint, not by taste.** Makko's
    reference-sheet mode puts the subject on a chroma field and ignores any
    instruction about the background - four separate attempts to ask for a
    neutral grey came back green. So the cast was recoloured to sit as far from
    a key colour as the wheel allows, and to carry NO white, cream or beige
    anywhere: a cream belly is a hole in the sprite. TIBBO burnt orange, MOSKA
    indigo violet, CORLI coral magenta. The payoff was better than expected -
    Makko picks the key per subject, and it handed the orange character a BLUE
    screen and the indigo one a GREEN one, which is only safe because the
    palettes had already been pulled apart.
300. **Three hues nobody confuses at thirty pixels, and three silhouettes.**
    Enormous ears, a slab shell, a long scaled tail. The colour work was forced
    by the keying, but legibility at size is the reason to keep it.

### Shooting animation instead of drawing it

301. **A locked camera changes what the cutter is allowed to do.** The old
    plates were separate drawings, each framed on its own, so `footPad` had to
    measure every cell and shove each one down until its feet met the floor.
    These strips are frames of one continuous take through ONE crop rectangle
    at fixed pixel coordinates, so the cells are already in true vertical
    register - the gap between the lowest cell and the highest IS the bob of
    the run and the arc of the jump. Measuring them one at a time would read
    that motion as framing error and flatten it: the feet would weld to the
    ground and the jump would stop leaving it. Hence `stancePad`, which takes
    ONE pad per strip, from its lowest cell. Same measurement, opposite
    conclusion, because the art is made differently now.
302. **Normalise scale per character or he shrinks when he jumps.** Every clip
    is cropped to its own subject, and a jump needs a tall crop for the arc.
    Scale each strip to the cell height independently and the character is
    visibly smaller in the air than on the ground. `vidstrip.py --scaleref`
    fixes how many SOURCE pixels map to one cell height across all of a
    character's strips, and bottom-aligns them so the feet line up too.
303. **Mirror the art, do not teach the renderer a second facing rule.** The
    clips were generated facing right; every existing plate faces left and the
    renderer flips when the body moves right. Two facing conventions inside one
    draw call is precisely the bug that reads as the animation playing
    backwards, so the flip happens once, at cut time.
304. **Despill before keying.** The green field lights the subject, so the ink
    outline picks up a fringe that survives a plain "is this pixel green" test
    and shows as a lime halo over dark temple stone. Pulling any pixel whose
    green exceeds the mean of its own red and blue back down to that mean
    removes it - and is only safe because the cast, by construction, has no
    green on it. Measured after: **max green-excess among opaque pixels = 7,
    and zero pixels above 25.**

### What the measurement caught

305. **The frame picker was locking onto the wrong cycle.** Autocorrelation
    finds the SHORTEST repeat. For a held breath that is the fast little tremor
    sitting on top of the slow action, so six cells sampled ten frames of
    nothing while a large swell underneath went missing - the clips scored
    5-13% between neighbours and looked static. The motion was there the whole
    time: max pairwise across the same clip was **62%**. `--minperiod` sets a
    floor on the cycle length, and TIBBO's hold went 13.6% -> 24.3% on the same
    footage. A bad number can be a bad measurement rather than bad art, and the
    way to tell is to measure something else.
306. **Fewer cells is a fix, not a compromise.** MOSKA and CORLI genuinely had
    less motion in their hold clips. Cut to six cells they measured 5.4% and
    6.4%; cut to three, 15.0% and 19.8% - and TIBBO's went to 40%. A cell that
    cannot be told from the one beside it is not animation, it is file size.
    All three holds ship at three cells: in, strain, out.
307. **Five jump cells, not six.** The strips were shot with an anticipation
    crouch at the front and the sim has no anticipation - a jump here begins
    the instant it is decided. That cell could never have been selected, so it
    was cut off the asset rather than left in as a frame nothing can reach.
308. **The mirror test does not transfer from run cycles to one-shots.** It
    flags a cell as flipped when a mirrored cell 0 is the closer match, which
    works when every pose is broadly similar. In a jump or a grab the pose
    changes wholesale, so it fired on clips that were perfectly fine. Its
    verdict on one-shots is now a prompt to look, not a result.
309. **"Jump" makes a four-legged animal leap.** CORLI reverted to all fours in
    three separate attempts, including one that said "never on all fours" five
    different ways. What fixed it was noticing her CHEER was already bipedal
    and reusing its language - "one big excited hop, like a happy character
    hopping for joy" - rather than arguing with the word jump. Borrow the
    framing from the shot that already worked.
310. **The one-shots re-staged themselves until the camera was nailed down.**
    First attempts zoomed in, turned the character to face the viewer, changed
    his body shape, and in MOSKA's case grew a hanging rope loop. Naming what
    must NOT change - "never changes distance, EXACTLY the same size in every
    frame, no ropes or dangling objects, keeps the same body shape" - fixed all
    four at once. Decision 274's lesson, applied to staging rather than to
    exaggeration.
311. **The BX block finally reads.** The key art drew B and X as two loose
    letters that would not survive being shrunk to thirty pixels. Generated as
    its own prop - thick gold on a dark inset panel, chunky stone frame, few
    shapes, high contrast - it does.

### Verification for this round

- All 35 art plates load. **Zero missing, zero console errors.**
- Every cell of every strip is reachable in play, checked by replaying whole
  runs and recording which cell the renderer would select:
  **run 8/8, cheer 8/8, jump 5/5, caught 6/6, hold 3/3.**
- Feet: the lowest run cell lands at y=149.3 against a floor at y=150.
- Facing: mirrored art plus the existing flip draws him facing his travel.
- Minimum consecutive-cell delta, the metric this project has used since the
  beetle: run **60.5 / 26.9 / 33.7%**, cheer **26.1 / 31.9 / 37.3%**, jump
  **92.7 / 53.3 / 66.2%**, caught **22.6 / 22.8 / 37.7%** (TIBBO/MOSKA/CORLI).
- Camera lock measured as subject pixel-count spread across each clip; every
  shipped strip is inside 20% except the jumps, where the spread is the body
  stretching and tucking rather than the camera moving.

### Still not done

- **MOSKA and CORLI's held breath measure 15% and 20%** against 40% for
  TIBBO's. They read as a tense near-still pose rather than a full breath
  cycle, which is defensible for a plate that shows for a third of a second,
  but it is the weakest art in the set and three attempts did not lift it.
- The enemies (`tp-critter-walk`, `tp-fbug-fly`) are still the previous
  generation's art and were not part of this remake.
- The old `solby*` / `potts*` / `embit*` plates are still sitting in `assets/`
  unreferenced.
- Nothing has been deployed.
