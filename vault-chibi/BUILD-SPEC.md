# THE TEMPLE — build spec

A spec for rebuilding this game's art and presentation layer from scratch using
**Makko Art Studio** for assets and **Makko Code Studio** (or any canvas
renderer) for the game.

**Assumes you have:** Makko access, Python (Pillow, numpy) and ffmpeg, and a
sealed economy supplied by the client conforming to §0.1. Everything else —
the four cutting tools, the prompts, the constants and how to derive them — is
described here well enough to write from scratch.

Everything below was measured on a working build, not designed on paper. Where
a number looks arbitrary it is usually the result of something going wrong
first; those cases are called out, because they are the parts most likely to be
"simplified" back into bugs. Roughly half the numbers are measurements of
*specific art* — §4.2 says which, and how to rederive them.

---

## 0. The one architectural fact that governs everything

**The outcome is drawn and sealed before the first frame.** A seeded RNG
produces the run's result — which characters survive, which beats they clear,
how many coins, the multiplier, the final total — and *every* visual beat
downstream is a presentation of that already-decided number.

Consequences that constrain the whole build:

- **Nothing in the presentation may roll anything.** Not the coin scatter, not
  the rarity, not the bonus room. If it looks random it must be a hash of an
  index, so the same seed replays identically.
- **A "bonus round" is a delivery channel, not a second draw.** The vault
  chamber in §5 pays nothing. It shows the same total in a bigger space, the
  way a slot's free-spins round shows you a win it already decided.
- **Derived labels are fine; derived *values* are not.** The rarity ladder (§6)
  reads off the sealed total using the tier table's existing thresholds. It
  renames a result. It never changes one.

If you break this, everything still *looks* fine and the build becomes a liar.

### 0.1 The interface the sealed region must expose

The economy itself is supplied by the client. The presentation layer only needs
it to hand over a settled result and never change it again. Build against this
contract and the two halves stay independent:

| Field | Type | Meaning |
|---|---|---|
| `seed` | string | The whole run is a pure function of this |
| `party[]` | body[] | 1–3 characters; each has `id`, and an `out` flag once caught |
| `coinsGot` | int | Raw coins collected before any multiplier |
| `mult` | int | The multiplier the run earned |
| `total` | int | Final payout. **`coinsGot × mult`, and the only number that matters** |
| `tier` | `{name, hex}` | Band on `total` — thresholds shared with the rarity ladder (§6.1) |
| `beats[]` | verdict[] | Per-beat outcome, drives the run's staging |

Guarantees the presentation relies on:

1. **Same seed → same everything.** Replay-identical, including which body dies
   where. If the presentation adds any randomness of its own this breaks.
2. **`total` is final before the first frame is drawn.** Nothing after the seal
   may alter it.
3. **`tier` is a band on `total` and nothing else.** In particular it is *not* a
   headcount — see §5.1 for why that distinction matters.

Everything in §5 and §6 is a way of *showing* those fields. None of it writes to
them.

---

## 1. Makko Art Studio — how the tool actually behaves

### 1.1 Generation kinds

| Kind | Returns | Use for |
|---|---|---|
| **Concept Art** | Illustration, often in a scene | Character design exploration |
| **Reference Sheet** | Front / Side / Rear on a **chroma field** | The input to every animation |
| **Game Animation** (Veo 3.1) | 4s 24fps 1080p mp4 on a chroma field | All character/enemy motion |
| **Prop Sprite** | Still subject on a **chroma field** | Doors, pots, coins, parallax layers |
| **Panoramic Background** | Opaque full-bleed plate | Only genuinely opaque layers |
| **Side-View Tile** | Tileable terrain | Tilesets |

### 1.2 Three behaviours that will cost you hours if you don't know them

**Prop Sprite does NOT return an alpha PNG.** It returns the subject on a flat
chroma field, and **Makko picks the key colour per subject** — a sandstone door
came back on green, the same door open came back on blue. You must key it
yourself. Auto-detect the key from the border rather than assuming.

**Parallax layers must be generated as Prop Sprite, never Background.** A
Background is an opaque full-bleed plate, useless for a mid layer that has to
show the far layer through the gaps between columns. Only the furthest,
genuinely opaque layer is a Background.

**Reference Sheet ignores background instructions entirely.** Four separate
attempts to ask for neutral grey came back on chroma anyway. Do not fight it —
design the palette around it (§2.1).

### 1.3 Settings that persist and settings that reset

Model, quality, aspect and view persist across collections. **Choosing a kind
resets the aspect** — always set aspect *after* kind, or you will silently get
1:1 when you asked for 21:9.

### 1.4 Prompt rules that work

- **Name what must NOT change, then exaggerate one named thing.** "Camera never
  moves, never zooms, never changes distance, EXACTLY the same size in frame,
  same body shape, no ropes or dangling objects" — then "EXAGGERATE: the legs."
  Without the lock list, one-shots re-stage themselves: zooms, turns to camera,
  body-shape drift, invented props.
- **"Jump" makes a four-legged animal leap.** A quadruped-shaped character will
  drop to all fours no matter how many times you write "never on all fours".
  Borrow the framing from a shot that already worked — for the pangolin, the
  *cheer* prompt's "one big excited hop, like a happy character hopping for joy"
  produced a clean biped jump when five explicit prohibitions had failed.
- **State the negative space for cut-outs.** "The gaps between the columns and
  the whole area above the arches must be COMPLETELY EMPTY — no sky, no wall,
  no ground, no background fill of any kind."
- **Ask for one row, expect a grid.** "8 frames in a single row" often returns
  3×2. Have a reflow tool ready.

### 1.5 Fetching results without clicking

Generated videos live at a public URL. To enumerate them, read the Supabase
token from the page and list the bucket:

```js
const tok = JSON.parse(localStorage['sb-api-auth-token']).access_token;
await fetch('https://api.makko.ai/storage/v1/object/list/animation-frames', {
  method: 'POST',
  headers: { 'content-type': 'application/json', authorization: 'Bearer ' + tok },
  body: JSON.stringify({ prefix: '<collectionId>/videos', limit: 100,
                         sortBy: { column: 'created_at', order: 'asc' } })
});
```

Public URL pattern:
`.../object/public/animation-frames/<collectionId>/videos/<name>.mp4`

Still images appear in the DOM as `/generated/` URLs once lazy-loaded.

---

## 2. The cast

### 2.1 Palette design is a *keying* constraint, not a taste decision

Because every plate is cut from footage shot against a chroma field, each
character must sit as far from a key colour as the wheel allows and carry **no
white, cream or beige anywhere** — a cream belly keys out as a hole in the
sprite.

Makko chooses the key per subject, and it chooses well *if you give it room*:
the orange character got a **blue** screen, the indigo one got **green**. That
only works because the palettes were pulled apart first.

| | Design | Palette | Forbidden |
|---|---|---|---|
| **TIBBO** | Burnt-orange desert jerboa, enormous round ears, long tufted tail, crimson neckerchief | burnt orange, apricot, rust, crimson | green, olive, white, cream, yellow |
| **MOSKA** | Deep indigo-violet temple toad, lavender-blue belly, terracotta carved stone slab on his back with gold glyphs | indigo, violet, lavender-blue, terracotta, gold | green, moss, olive, white, cream |
| **CORLI** | Deep coral-magenta pangolin, warm rose belly, bronze scale-plates down back and curled tail, tufted ear plumes | coral, magenta, rose, bronze | green, olive, white, cream |

Three hues nobody confuses at 30px, which is the other job.

### 2.2 Enemies read by VALUE, not hue

The cast already owns three saturated hues and the temple is warm sandstone. So
enemies are **near-black obsidian with molten amber-gold glowing out of the
cracks in the shell**. A dark shape on pale stone reads instantly without
competing for a hue — and near-black on green is the easiest keying case there
is.

| | Design |
|---|---|
| **SKARN** | Chunky armoured temple scarab. Low, wide, heavy. Six short sturdy legs. Broad domed shell that looks like something you could jump on. Glowing amber eyes, small blunt mandibles. |
| **VYRE** | Temple guardian wasp-moth. Compact tapered body, short blunt amber stinger, two pairs of broad angular wings with glowing amber veins held wide and clearly separated from the body so the wing shape reads on its own. |

### 2.3 Pipeline per character

```
Concept (GPT Image 2, Chibi, Concept Art, 1:1, 4 images)   88 cr
   └─ save one as Concept image
Reference Sheet (from that concept, 1 subject only)         66 cr
   └─ save, named
Animation ×N (Veo 3.1, Game Animation, Side, Full, 4s)      90 cr each
```

Reference-sheet prompt template:

> `<NAME>` the `<one-line design>`. Keep the palette exactly as shown —
> `<allowed colours>` only, absolutely no `<forbidden list>` anywhere. Thick
> bold black ink outline, flat cel shading, full body, standing upright on two
> legs, both feet flat on the ground, arms visible and clear of the body,
> consistent proportions across every view.

**Jobs queue** — fire all of a character's animations back to back rather than
waiting.

---

## 3. Video → sprite strip

### 3.1 Four tools to write (Python + Pillow + numpy + ffmpeg)

None of these exist off the shelf. Each is 80–200 lines. Algorithms below are
complete enough to implement from.

---

#### `pickframes.py` — choose which frames become cells

`in:` mp4, cell count, loop flag, key colour · `out:` a frame list + a report

1. `ffmpeg -i clip.mp4 %03d.png`, then per frame build a boolean **subject
   mask** at low res (240×135 is plenty): `mask = NOT key`, where green key is
   `g>120 AND g-r>60 AND g-b>60`.
2. Difference between two frames — symmetric difference, normalised so it does
   not depend on subject size:
   ```
   delta(A,B) = popcount(A XOR B) / (popcount(A) + popcount(B)) * 2
   ```
3. **Cycle length**, for looping actions: the lag in `5..min(40, N-4)` with the
   lowest mean `delta(frame[i], frame[i+lag])`. Walk it up in whole multiples
   until it is at least `max(cells, minperiod)`.
4. **Search.** For a loop: sweep candidate periods around the detected one and
   every start offset; lay `cells` frames evenly across one period. For a
   one-shot: spread evenly across the clip, then hill-climb each cell ±3 frames.
5. **Score = the MINIMUM delta between consecutive cells**, with the wrap
   (last→first) counted for loops. Maximise it. Reject a candidate set outright
   if its *maximum* exceeds the ceiling, or if any frame falls outside the size
   band.
6. **Report** camera lock (spread of subject pixel-count across the clip),
   facing (§3.3), every consecutive delta, and the min/max.

Options that each exist because of a specific failure: `--maxdelta`,
`--sizeband`, `--minperiod` — see §3.2 and §3.3.

---

#### `vidstrip.py` — cut chosen frames into a strip with alpha

`in:` mp4, frame list, key, cell height, scaleref, mirror flag · `out:` PNG strip

1. **Despill, then key** — in that order, per frame:
   ```
   dist  = key_channel - max(other two)
   spill = max(key_channel - mean(other two), 0)
   key_channel -= spill                      # neutralise the fringe
   alpha = clamp((HI - dist) / (HI - LO), 0, 1) * 255      # LO=18, HI=70
   ```
   The ramp matters — a hard threshold stair-steps every curve.
2. **One crop rectangle for the whole strip, in BOTH axes**, at fixed absolute
   pixel coordinates: the union bounding box (alpha>40) across all chosen
   frames, plus a small pad.
3. `scale = cellHeight / (scaleref or cropHeight)`; cell width =
   `cropWidth × scale`.
4. Resize each crop by that scale and **bottom-align** it in a `cellHeight`-tall
   cell. Bail loudly if a scaled crop is taller than the cell.
5. Optionally mirror each cell horizontally.
6. Paste left to right into one image.

---

#### `keyprop.py` — key a single still

Same despill+ramp as above, but **auto-detect the key**: sample the image border
(where the field always is) and pick green vs blue by which channel mean is
higher. Then crop to content and optionally scale to a target height. Makko
picks the key per subject, so hardcoding it will silently destroy half your
props.

Verify: max key-channel excess among opaque pixels should be ≤ ~7.

---

#### `gridstrip.py` — reflow a grid sheet into one row

Generators return 3×2 when asked for 6-in-a-row. Find rows by horizontal
projection of the alpha, then cells within each row by vertical projection, then
write them out left-to-right onto **one shared vertical crop** so relative
height survives.

> **Do not use this when items differ hugely in width.** It centres every cell
> on one window sized for the widest item. Four gold piles running 117px to
> 347px came out with neighbours bleeding into the small cells. For that case,
> crop each item to *its own* bounding box and centre + bottom-align it in a
> uniform cell at one shared scale.

### 3.2 The metric: minimum consecutive-cell delta

Not the mean. The mean happily hides one repeated pair among seven good ones,
and that one pair is the visible hitch. For a looping action the wrap from last
cell back to first counts as a consecutive pair like any other.

**Floor: >20%.** Below that it is a slideshow.

**Ceiling: <~50%.** Added after shipping a cheer that closed on a **95% jump**
from last cell to first — a hard cut, once per cycle, forever. A floor alone
will select for that.

**Neither catches a pose *reset*.** A clip that celebrates and then winds down
to a stand can have perfectly even deltas all the way round and still snap when
looped, because the fault is in the *content*, not the pixel difference. Look at
a contact sheet of the source before trusting the numbers.

### 3.3 Guards

- **Facing.** Compare each cell to cell 0 *and* to a mirrored cell 0. A mirrored
  cell changes most pixels, so it scores as enormous motion while on screen the
  character snaps round to face backwards. **Only valid for cycles** — in a jump
  or a grab the pose changes wholesale and this fires on clips that are fine.
- **Camera lock.** Subject pixel-count spread across the clip. Under 20% is
  fine. Higher is expected for jumps (body stretches and tucks) and is a prompt
  to look, not a failure.
- **Size band** (`--sizeband`). For an action containing a jump, the character
  genuinely changes size between crouch and full stretch; cells picked from both
  ends read as the body growing and shrinking.
- **Period floor** (`--minperiod`). Autocorrelation finds the *shortest* repeat.
  For a held pose that is the fast tremor sitting on top of the slow action —
  lock onto it and you sample ten frames of nothing while missing a large swell
  underneath. One clip scored 13.6% at the detected period and **62% max
  pairwise** across the same footage.

### 3.4 Cutting rules

**`--scaleref` — one scale per character.** Every clip is cropped to its own
subject, and a jump needs a taller crop for the arc. Scale each strip to the
cell height independently and the character visibly *shrinks* in the air. Fix
the number of SOURCE pixels that map to one cell height across all of a
character's strips, and bottom-align them so the feet line up. Used: **980** for
all three heroes, **760** SKARN, **1060** VYRE.

**`--mirror` — one facing convention.** Decide which way art faces and enforce
it at cut time. Two facing conventions inside one draw call is the bug that
reads as the animation playing backwards.

> Do not *assume* which way the art faces — **measure it**. The enemies shipped
> walking backwards because the art faced right, the bodies travelled left, and
> the convention was assumed rather than checked.

**One shared crop rectangle, in BOTH axes, at fixed absolute pixel
coordinates.** The camera is locked, so the body does not translate; every
wobble in a frame's own bounding box is the legs reaching or the body bobbing —
which is the motion you are trying to keep. Re-centring each cell on its own
centroid cancels the bob and drags the body sideways chasing the trailing leg.

**Despill before keying.** The chroma field lights the subject, so the ink
outline picks up a fringe that survives a plain "is this pixel green" test and
shows as a coloured halo over dark scenery. Pull any pixel whose key channel
exceeds the mean of the other two back down to that mean. Safe *only* because
the cast, by construction, contains none of the key colour. Verify: max
key-channel excess among opaque pixels should be ≤ ~7.

**Soft alpha ramp, not a threshold.** Ramp alpha across a band of chroma
distance (e.g. 18→70) or every curve stair-steps.

### 3.5 Match cell count to the motion that is actually there

Fewer cells is a **fix**, not a compromise. A cell that cannot be told from the
one beside it is not animation, it is file size.

| Action | 6 cells | 3–4 cells |
|---|---|---|
| Held breath ×3 | 5.4% / 6.4% / 13.6% | **15% / 20% / 40%** |
| Catch ×3 | 15.5% / 30% / 19% | **63% / 30% / 29%** |

Different characters legitimately support different counts — one toad had no
clean 8-cell cheer loop and a good 5-cell one.

### 3.6 A strip carries an implied tempo

A strip cut from N frames of 24fps footage wants to be played back over exactly
`N/24` seconds. One global rate for three characters was **1.9× too fast** for
one of them (read as "super spazzy") and roughly half speed for the other two.

Store cells *and* rate per strip:

```js
const CHEER = {
  tibbo: { cells: 8, fps: 10.7 },   // cut from 18 source frames
  moska: { cells: 5, fps: 8.6  },   // 14
  corli: { cells: 6, fps: 6.9  },   // 21
};
```

---

## 4. Asset manifest

Cast strips: cell height **550**, `--mirror`, green key.
Enemy strips: cell height **340**, `--mirror`, green key.

Widths below are **what this build's art came out as**, not targets — they fall
out of each clip's crop. Cell *counts* are the meaningful column, and even those
are per-clip judgements (§3.5). Scalerefs measured here: 980 heroes, 760 SKARN,
1060 VYRE — rederive for new art (§4.2).

| Asset | Size | Cells | Notes |
|---|---|---|---|
| `tp-{name}-run.png` | ~4200×550 | 8 | full two-step cycle; find the period by autocorrelation, it is ~19 frames not ~10 |
| `tp-{name}-cheer.png` | varies | 8/5/6 | per-character count and tempo |
| `tp-{name}-jump.png` | ~2800×550 | 5 | anticipation crouch **cut off** — the sim has no anticipation, so that cell is unreachable |
| `tp-{name}-caught.png` | ~2800×550 | 6 | startle → hands up → struggle → slump → sulk |
| `tp-{name}-catch.png` | ~1800×550 | 4 | arms up scooping, loops |
| `tp-{name}-idle.png` | ~410×550 | 1 | frame 1 of the caught clip (a clean stand) |
| `tp-skarn-walk.png` | 3024×340 | 6 | six-leg scuttle |
| `tp-skarn-squash.png` | 3176×340 | 4 | stand → splat wide → settle → amber fades |
| `tp-vyre-fly.png` | 1280×340 | 4 | wingbeat |
| `tp-vyre-dive.png` | 1532×340 | 4 | 0,1 flare wind-up · 2 streamlined dive · 3 nose-down landed |
| `tp-coin-spin.png` | 528×72 | 8 | one full rotation, face → edge → face |
| `tp-gold-pile.png` | 1004×240 | 4 | scatter → mound → heap → crowned hoard |
| `tp-pot.png` | 484×420 | 1 | open-mouthed urn, empty |
| `tp-door-shut.png` | 401×420 | 1 | sealed, no gap between leaves |
| `tp-door-open.png` | 477×420 | 1 | leaves apart, **opening completely empty** |
| `tp-vault.jpg` | 1536×1024 | — | opaque room; floor edge measured at 0.84 of height |

### 4.1 Prop prompts that produced usable art

**Vault chamber** (Panoramic Background, 21:9):
> A wide panoramic BACKGROUND for the treasure vault of a chibi temple game —
> the reward room, seen straight on like a stage set for a 2D side-scrolling
> platformer. A vast carved sandstone chamber whose walls are lined with gold:
> rows of treasure alcoves packed with gold bars, jewelled cups, crowns and coin
> hoards, and two colossal guardian statues flanking the room. High above, the
> ceiling opens into a bright circular shaft with warm golden light pouring
> down — leave the upper middle open and bright and uncluttered. The lower third
> is a clean flat stone floor running the full width, unobstructed and clear.
> Much warmer, richer and BRIGHTER than the dusty outer temple. Chibi
> mobile-game look, thick bold black ink outline, flat cel shading. Absolutely
> NO characters, NO creatures, NO falling coins in the air, NO text.

**Growing pile** (Prop Sprite) — ask for **four separate piles in one horizontal
row, evenly spaced with clear empty gaps, all resting on the same invisible
ground line, drawn from the same straight-on side view**, increasing in size.

> **Slicing gotcha:** a shared-window slicer centres every cell on one window
> sized for the widest item. These piles run 117px to 347px, so the small ones
> came out with their neighbours bleeding into frame. Crop each item to **its
> own** bounding box, then centre and bottom-align it in a uniform cell at one
> shared scale.

**Spinning coin** (Prop Sprite) — eight frames in one row: face-on with a carved
glyph → narrowing → thin edge sliver showing the milled rim → widening → face-on
from the back.

**Parallax mid layer** (Prop Sprite, 21:9) — a row of columns and arches with
**wide open gaps of empty transparent space between them**, nothing behind or
above the arches, left and right edges matching so it tiles.

---

### 4.2 Constants — derive these, do not copy them

Roughly half the numbers in this build are **measurements of specific art**. Copy
them onto different assets and they are wrong in ways that look like bugs. Each
one below says what it means and how to get it.

| Constant | What it is | How to derive it |
|---|---|---|
| `--scaleref` | Source pixels that map to one cell height, per character | For each of that character's clips, compute the union crop of its chosen frames. Take the **tallest** and add ~2%. Use that one number for all their strips. |
| cell height | Output resolution per cell | Free choice. Pick so the largest crop scales *down*, never up. 550 for heroes, 340 for enemies here. |
| `RUN_STEP` | World distance advanced per run cell | `groundDistancePerCycle / cells`. Measure the cycle from the footage: at 24fps, `strideFrames / 24 × runSpeed`. Keep the *cycle distance* fixed if you change cell count, or the feet skate. |
| `CHEER[id].fps` | Playback rate of a strip | `cells ÷ (sourceFrameSpan ÷ 24)`. Per strip. See §3.6. |
| `VAULT_FLOOR_U` | Where the floor sits in the room plate, 0–1 | Measure it: strongest horizontal edge in the lower half of the image (largest smoothed row-to-row luminance delta). Do not eyeball it. |
| `VAULT_FLOOR_Y` | Where that floor lands on screen, 0–1 | Composition choice. ~0.80 leaves room for figures without crowding the ceiling. |
| `clearTo` | Half-width of the band the pot needs | `potHalfWidth + figureHalfWidth + smallMargin`, computed from the loaded art so it survives an art swap. |
| figure half-width | For overlap tests | The **drawn** width, `figHeight × cellAspect ÷ 2` — not the collision box. Bodies 45 units wide at 27 apart overlap by 40%. |
| rarity thresholds | Band edges | **Take them from the client's tier table.** Do not invent a parallel ladder. |
| `ART_V` | Cache-buster | Any string. Bump by hand whenever a plate changes on disk. |

Two that are genuinely arbitrary and safe to copy: the alpha ramp band
(`LO=18, HI=70`) and the delta floor/ceiling (`>20%`, `<~50%`).

---

## 5. Game architecture

### 5.1 Phase machine

```
run → gather → spend → lock → open → [vault] → tally → done
```

- **vault** fires only when the whole crew gets out: `party.length === 3 &&
  alive === 3`.
  > **Do not gate this on the payout tier.** The tier is a band on the *total*,
  > and a lone survivor riding a multiplier reaches the top band on his own — an
  > observed run paid 75 with one body home. Gate on the headcount.
- Once a run enters the vault it **stays there** through `tally` and `done`.
  Cutting back to the chest for the last few seconds throws away the best shot
  in the game and restarts the cheer loop.

### 5.2 Two pad functions, and when each is correct

```js
footPad(im, cell, cells)   // per-cell  — hand-framed drawings
stancePad(im, cells)       // per-strip — footage on a locked camera
```

`footPad` measures every cell separately and shoves each down until its feet
meet the floor. Correct for separate drawings, each framed on its own.

`stancePad` takes **one** pad from the strip's lowest cell. Correct for footage,
because the cells are already in true vertical register — the gap between the
lowest cell and the highest **is** the bob of the run and the arc of the jump.
Measuring them one at a time reads that motion as framing error and irons it
flat: the feet weld to the ground and the jump stops leaving it.

Find the stance line as the lowest row that is ≥22% of the widest silhouette
row — the lowest *opaque* row finds a tail tip or a trailing flame and reports
"planted" on a build that visibly is not.

### 5.3 Drive animation off physics, not off timers

- Run cell: `floor(x / RUN_STEP) % RUNCELLS`, distance-driven so feet do not
  skate. `RUN_STEP = 78 / RUNCELLS` — keep ground-distance-per-cycle constant if
  the cell count changes.
- Jump cell: read off vertical speed —
  `vy < -260 → launch · coasting → apex · vy > 200 → reach · sinceLand < 0.06 →
  squash · else → recover`. A timer drifts out of step the moment a jump is cut
  short.
- Enemy dive: use the **streamlined** cell, not the nose-down one — the renderer
  already rotates the sprite to aim it along travel, and nose-down art turns it
  twice.
- **Every cell must be reachable.** Sweep seeds and record which cell the
  renderer would select. A cell nothing can select should have been cut.

### 5.4 The ending is presentation, not gameplay

Do **not** hit marks by feeding synthetic left/right into the run's physics. It
fails quietly — bodies crawled at 3.6 units/sec against a run speed of 138 and
stopped short, two of them one unit apart. Flat ground, no obstacles, a mark per
body: place them directly and keep gravity from `stepBody`.

Space marks by the **drawn** width, not the collision box. Bodies drawn ~45
units wide at 27 units apart overlap by 40%.

---

## 6. The close

Runs on every run, vault or not. `TALLY_S = 5.6s`.

| t | beat |
|---|---|
| 0 → 1.7 | haul arcs up off the floor into the pot; counter climbs `coins ×mult` |
| 1.7 → 2.5 | pot shudders and glows as the multiplier lands |
| 2.5 → 3.9 | coins burst back out and fill a card silhouette from the bottom |
| 3.9 → 5.6 | card locks, glows in its rarity colour, name stamped on its face |

### 6.1 The rarity ladder — WoW colours

WoW rather than Pokémon because the ladder *is* WoW's: common, uncommon, rare,
epic, legendary are its exact words in its exact order, and those colours are
the most widely recognised quality scale in games.

| Rarity | Hex | Glow | Threshold |
|---|---|---|---|
| Common | `#B8B8B8` | `#EDEDED` | total < 10 |
| Uncommon | `#1EFF00` | `#B4FFA0` | 10–19 |
| Rare | `#0070DD` | `#7FC4FF` | 20–39 |
| Epic | `#A335EE` | `#D9A6FF` | 40–69 |
| Legendary | `#FF8000` | `#FFC46B` | 70+ |
| **Grail** | `#E6CC80` | `#FFF3C8` | vault opened |

The thresholds are the **existing tier bands**, reused. Grail is not a band — it
is whether the vault opened, i.e. whether all three got out.

> Known weakness: legendary orange sits close to a burnt-orange character and to
> the temple's gold. It reads because the card is on its own dark stage, but it
> is the thinnest separation on the ladder.

### 6.2 Layout collisions to design out

- The pot lands where the middle of a three-body line-up stands. **Re-lay the
  whole line either side of the pot** — moving only the middle one puts it on
  top of a neighbour, because three figures at ~148px plus a 148px pot do not
  fit at even spacing. Preserve order so nobody crosses.
- Move them **on screen**, animated — they are visible the whole time, and a
  body that changes place between two frames reads as a glitch. The catch cycle
  plus a hop arc, facing the direction of travel, is a jig.
- Size the card off the **gap above the pot**, not off canvas width, so the two
  can never collide however the pot is scaled. Put the rarity name on the card's
  face, not under it.

### 6.3 Determinism

Every coin is a pure function of its index and `phaseT`. No stored state,
nothing random. Spread comes from a hash of the index — `((i * 73) % 101) / 100`
— which looks scattered and replays identically. Fall on `u²`, not linearly; a
constant-speed coin reads as a sprite being moved rather than a thing with
weight.

---

## 7. Presentation traps

**A full-screen wash is a filter, and it reads as one.** A 58% black scrim
existed to sink a busy level behind the payout card, and it fired on every phase
except the run — including the bonus room, which came out grey and flat. Scope
scrims to the thing that needs them.

Its replacement — a "local" pool of shade behind each body — was **also** wrong:
at 46% over a radius of two-thirds of a figure's height, three of them cover
most of the frame. The cast has a thick ink outline and three unique hues; that
is what makes it read. Keep the contact shadow, drop everything else.

**Do not trust the Fullscreen API.** In an embedded view the method exists,
reports itself supported, returns without throwing, and silently does nothing —
the promise never resolves *and* never rejects. Fire the request, then check
`document.fullscreenElement` ~220ms later and fall back to a CSS blow-up if it
is empty. That one path covers silent no-op, async rejection, sync throw, and
browsers with no API.

**Set `touch-action: manipulation` on the canvas.** Without it a double-tap is a
browser zoom gesture, and players tap at exciting moments. Prefer
`manipulation` over `none` or `user-scalable=no` — it kills double-tap zoom
while leaving pinch-zoom for anyone who needs it.

**Version-stamp asset URLs.** Re-cutting a sprite does not change its filename,
so browsers keep serving the old one — including on the phone you are testing
on. `const ART_V = '?v=42'` appended to every asset URL, bumped by hand. A
timestamp would re-download every plate on every load.

---

## 8. Verification standard

> DOM probes are necessary and insufficient. **Look at frames.**

- **Exercise the real renderer.** A probe that re-implements the selection logic
  will report "all cells reachable" while the actual draw path throws every
  frame. That happened.
- **Cache-bust every verification.** Stale builds produce error line numbers
  that do not match the source — that mismatch is the tell.
- **Console history accumulates across navigations.** Verify in a fresh tab or
  you will chase errors you already fixed.
- Sweep 40–300 seeds and assert invariants, not vibes: every run reaches `done`;
  every cell of every strip is reachable; no body off its mark; no two bodies
  within a body-width; no GRAIL without a vault and no vault without a GRAIL;
  all assets loaded; zero console output.

### 8.1 A dev tool that does not lie

To test outcomes, **search for a seed** that produces one — run seeds headlessly
through the same code the live game uses and stop at the first match. Do not
override the sealed result: everything downstream would then be describing
something that was never drawn. Print the found seed so runs are reproducible.

Measured frequencies (400 runs): party of 1 → 67%, party of 2 → 28%, party of 3
→ 5.5%. All three home → **1.8%**. The binding constraint on the bonus room is
party size, not survival.

---

## 9. Cost

| Item | Credits |
|---|---|
| Concept (4 images) | 88 |
| Reference sheet | 66 |
| Animation (Veo 3.1, Full, 4s) | 90 |
| Prop / background still (4 images) | 88 |

A full cast of three with five animations each, two enemies, and the prop set
came to roughly **4,500 credits** including re-rolls — and re-rolls are the
norm: one jump took four attempts.
