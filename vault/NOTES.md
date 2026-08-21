# NOTES — The Vault Job prototype (simultaneous crew, drawn sequencing)

## What was built
One self-contained `index.html` (~60KB, no network, vanilla JS, system fonts, inline SVG). Three crew members, three encounters, **all on screen at once** alongside the vault and a building tracker. Each crew member waits in position until his go-signal; the go **order is drawn per run**, so the three scenes resolve at different moments and in a different sequence every time. Each result is clean / close call / out, and **out has a consequence on screen**: the roof turret drops the roof guy (stunned, not hurt), the lobby guard cuffs and walks the lobby guy out, the keypad alarm strobes and a cage drops on the keypad guy. Crew who make it descend the building tracker and appear at the vault door. **The prize tier is the number who reach the vault:** 1 → Floor, 2 → Solid, 3 → Grail. The vault stays neutral grey until the door opens, then takes the tier colour (bone / ember / auric with a prismatic ring) with a matching glow.

Honesty is unchanged: `drawOutcome()` draws the tier, who makes it, how, and the go order in one seeded pass and freezes the object before the first frame. Commit–reveal receipt, Replay, Verify, quick open and the debug panel all carry over.

## Decisions (direction from Makko, replacing spec v1.0 sections 3–4)
- **Simultaneous scenes with drawn sequencing**, not exits or turns. Every run is 20s at 1x: intro 1.2s, go-signals 2.8s apart, 5.5s action each, 0.8s descent, vault from 13.8s. Quick open is 4s with fixed beats.
- **Consequences replace the spec's "never a contest the crew could fail."** No blood, no mockery: stunned, arrested, caged, and the copy stays flat.
- **Omen, guaranteed signal and exit points removed** — arrival count is the single signal, and the vault is colour-neutral until the finale so nothing leaks early.
- **At least one always reaches the vault**, so the door always opens. Debug per-guy forces override a conflicting tier.
- Replays never re-bank the cosmetic job counter.

## Verified in a live browser
- `Math.random` appears 0 times; outcome frozen; same seed → identical run — **pass**
- 3,000 draws: tier ↔ arrivals locked, never zero arrivals, go order evenly spread (983 / 1017 / 1000 first-go) — **pass**
- Verify passes the genuine seed; fails a 1-character tamper — **pass**
- Watched a forced run (roof out, lobby out, keypad close call, go order lobby → keypad → roof): arrest, turret, and close call all readable with sound off; vault bone-coloured for one arrival — **pass**
- Wall clock pick→reveal at 1x matches `CONFIG.durations.run` (engine clock, previously measured to ±10ms) — **pass**
- Reduced motion: poses step instead of glide, cross-fades kept, identical copy and timings — **pass**
- 360px stacks the four panels and the tracker; desktop column caps at 1040px — **pass**
- Floor copy is warm ("One got through. It still pays.") — **pass**

## Not finished
Nothing cut. Sound is optional, default off.
