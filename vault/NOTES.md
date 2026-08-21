# NOTES — The Vault Job prototype (simultaneous crew · five-rung ladder)

## What was built
One self-contained `index.html` (~74KB, no network, vanilla JS, system fonts, inline SVG). Three crew members, three encounters, **all on screen at once** with the vault and a building tracker. Each crew member waits in position until his go-signal; the go **order is drawn per run**, so scenes resolve at different moments in a different sequence every time. Each result is clean / close call / out. **Out has a consequence on screen**: the roof turret drops the roof guy, the lobby guard cuffs and walks the lobby guy out, the keypad alarm strobes and a cage drops. **A clean solve also finds one number for the lockbox.**

**The ladder is a pure function of the three results:**
- 0 reach the vault → **Getaway** — the door never moves; they grab what they can on the way out (worst prize).
- 1 → **Floor** · 2 → **Solid** · 3 → **Grail** — the door opens and there is a lockbox inside with a three-number lock.
- 3 reach it **and all three were clean** → **Lockbox** — three numbers, the lockbox opens, the top prize.

The vault stays neutral grey until the finale, then takes the tier colour (getaway stays shut and dim). Crew who make it descend the tracker and appear at the door. **The open vault shows loot around the lockbox — gems, bars, coin stacks — scaled by headcount** (3 pieces for one, 6 for two, 11 for three), and the crew gather it and walk out with it. **The lockbox is only tried when all three are at the door**: found numbers fill its slots, three opens it, two leaves it shut and they take the rest. With one or two at the door it is simply not attempted.

Honesty is unchanged: `drawOutcome()` draws the guiding tier, who makes it, how, and the go order in one seeded pass; the tier is then derived from the results so forced and drawn runs are always internally consistent; the object is frozen before the first frame. Commit–reveal receipt, Replay, Verify, quick open and the debug panel carry over.

## Pick-screen additions
- **How it pays**: five cards built from `CONFIG` — mini vault in tier colour, three figures (solid = made it), how you win it, value band, two example prizes. Tier odds are deliberately not on the cards.
- **Show me a…**: Random / Getaway / Floor / Solid / Grail / Lockbox. A labelled demo control, same setting as the debug panel's Force tier, applied at draw time. Remove or hide before anything player-facing — the spec forbids a player choosing the outcome.
- **Restart** (header, during a run): abandons the run, nothing revealed, next pick uses a fresh nonce.

## Decisions (direction from Makko, replacing spec v1.0 sections 3–4)
- Simultaneous scenes with drawn sequencing; 20s at 1x (intro 1.2s, go-signals 2.8s apart, 5.5s action, 0.8s descent, vault from 13.8s, lockbox verdict at 18.5s). Quick open 4s, fixed beats.
- Consequences replace "never a contest the crew could fail." No blood, no mockery: stunned, arrested, caged, flat copy.
- Omen, guaranteed signal and exit points removed.
- Replays never re-bank the cosmetic job counter.

## Verified in a live browser
- `Math.random` appears 0 times; outcome frozen; same seed → identical run — **pass**
- 5,000 draws: tier ↔ results consistent on every draw (≈21 / 44 / 29 / 6 / 1%); forced all-out → Getaway, forced all-clean → Lockbox, forced Grail always keeps a close call — **pass**
- Verify passes the genuine seed; fails a 1-character tamper — **pass**
- Watched: Getaway (door never moves), Lockbox (three numbers fill, lid opens, prismatic glow), Floor/Solid/Grail with the lockbox staying shut — all readable with sound off — **pass**
- Wall clock pick→reveal at 1x: 20,050ms against 20s — **pass**
- Reduced motion: poses step instead of glide, cross-fades kept, identical copy and timings — **pass**
- 360px stacks panels, tracker and cards — **pass**

## Not finished
Nothing cut. Sound is optional, default off.
