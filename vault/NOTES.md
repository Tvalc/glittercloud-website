# NOTES — The Vault Job prototype (sequential crew model)

## What was built
One self-contained `index.html` (~55KB, no network, vanilla JS, system fonts, inline SVG). Three crew members, one encounter each, played **in sequence** top of the building to the bottom: the roof guy vs the laser grid, the lobby guy vs the guard desk, the keypad guy vs the code. Each encounter plays a **different cutscene by result** — clean, close call, or out (he pulls back; nobody gets hurt). A building cross-section stays on screen the whole run showing who has reached the vault. **The prize tier is the number who make it down:** 1 → Floor, 2 → Solid, 3 → Grail. The vault door's colour and the glow behind it say it before the card does.

Honesty is unchanged: `drawOutcome()` draws the tier, which crew make it, and how, in one seeded pass and freezes the object before the first frame. Commit–reveal receipt, Replay, Verify, quick open and the debug panel all carry over.

## Decisions (direction change from spec v1.0, per Makko)
- **Sequential, not simultaneous.** The spec's three parallel panels are replaced by one stage plus the building tracker, so the tension reads as "does the next guy make it?" This inverts the spec's "never stage it as a contest the crew could fail" and makes run shape a verdict, not a signal — by design.
- **Omen and guaranteed signal removed.** Both were bound to simultaneous panels; arrival count is now the single, legible signal.
- **Exit points removed.** Every run plays all three scenes: 24s at 1x (intro 1.2s, three scenes at 6.3s, vault 3.9s). Quick open is 4s with fixed beats.
- **At least one always reaches the vault**, so the door always opens. Debug per-guy forces override a conflicting tier.
- Replays never re-bank the cosmetic job counter.

## Verified in a live browser
- `Math.random` appears 0 times; outcome frozen; same seed → identical run (Replay) — **pass**
- 3,000 draws: tier ↔ arrivals locked 1/2/3, never zero arrivals, 62/35/3.6% — **pass**
- Verify passes the genuine seed; fails a 1-character tamper — **pass**
- Wall clock pick→reveal at 1x: **24,008ms** against 24s — **pass**
- Watched a forced run (roof close call, lobby out, keypad clean → Solid) and a Grail quick open: every result is stated in text and colour on the stage header, the caption, and the building tracker; readable with sound off — **pass**
- Reduced motion: poses step instead of glide, cross-fades kept, identical copy and timings — **pass**
- 360px stacks stage over the building tracker; desktop column caps at 960px — **pass**
- Floor copy is warm ("One got through. It still pays."); an out is "pulled back", never a loss mark — **pass**

## Not finished
Nothing cut. Sound is optional, default off.
