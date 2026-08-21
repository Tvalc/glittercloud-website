# NOTES — The Vault Job prototype

## What was built
One self-contained `index.html` (~52KB, no network, vanilla JS, system fonts, inline SVG). The outcome is drawn once in `drawOutcome()` and frozen before the first frame; presentation flavour (staggers, keypad digits, gag roll, prize pick) is drawn from the same seeded stream *after* the freeze and cannot touch the outcome. Commit–reveal via SHA-256 (`crypto.subtle` with a sync fallback), mulberry32 PRNG seeded from `serverSeed:pick:nonce`. The vault door is on screen from the first frame — dormant, waiting — so every run ends where it was always pointed. Debug panel on `D`.

## Ambiguities, resolved in favour of section 2
- **Quick open vs exits.** Quick open always shows 3 panels on fixed beats (split 600ms, sync 1500ms, resolve 1950ms, door 2400–3400ms, reveal 4000ms) for every tier; only outcome data (grade colours, case count) differs. Unused panels "stand down" neutrally. Omen stagger and the guaranteed signal do not play in quick open — both correlate with tier and would break identity. Door spectacle is fixed, tier-blind.
- **Forced signal on a non-grail tier stays false** — the signal is licensed to grail only, so forced runs stay internally consistent.
- **Replays never re-bank cases**, so the cosmetic counter can't be farmed.
- **Gag no-repeat** is session state, so a replayed seed can show a different gag (outcome-irrelevant by design).

## Acceptance tests — all verified in a live browser
1. `Math.random` appears 0 times in the source (grepped) — **pass**
2. Replay reproduced a byte-identical run (tier, prize, grades) via the Replay button — **pass**
3. Verify passed the genuine seed; failed after a 1-character tamper — **pass**
4. Signal never fired across 20× forced floor + 20× solid (even forced on); fires on grail — **pass**
5. Door opened on every watched run including one-case runs (single unconditional animator) — **pass**
6. Run 100 opens: every exit reachable from every tier; 3000-draw check showed 17 grail shorts — **pass**
7. Watched a short run land GRAIL ("Founders Vault Card", one BONE chip) — resolves warmly, feels fine — **pass**
8. Wall-clock, pick to reveal, 1x: full **26,006ms**, medium **16,001ms** (engine clock, same for short/quick) — **pass**
9. Quick open beats are fixed constants, structurally identical across tiers — **pass**
10. Sound off at 1x: each panel's secure moment states its grade in colour and text; best panel callable at a glance — **pass**
11. Reduced motion: transforms dropped, cross-fades kept, identical durations and information — **pass**
12. Watched at 360px (panels stack) and desktop (column caps at 960px, identical at 1440px) — **pass**
13. Floor reveal: warm copy, no losing marks or sounds — **pass**
14. All four gags watched; none lands at the player's expense on any tier — **pass**

## Not finished
Nothing cut. Sound (optional) is two tones, default off.
