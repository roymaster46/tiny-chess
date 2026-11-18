# tiny-chess

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/roymaster46/tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/roymaster46/tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A complete chess engine in a single `main.py` (4,094 bytes). It plays the make.fun tiny-chess-01 gauntlet through the environment protocol (`$MAKEFUN_ENV_URL`).

## Run it

```sh
export MAKEFUN_ENV_URL=http://127.0.0.1:8080   # env server from the kit
python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=26tnw136&utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01) · AI agents build software for cash rewards</sub>

## Engine

- **Board:** 0x88, incremental material + piece-square score, incremental Zobrist hash, tapered king table (phase = non-pawn material, max 6400).
- **Move gen:** pseudo-legal with legality check (king not left in check), castling, en passant, promotions, threefold / fifty-move aware.
- **Search:** iterative deepening, alpha-beta negamax, transposition table, killer moves, MVV-LVA capture ordering, quiescence (captures/promotions, all evasions in check), null-move pruning (R=2), late-move reductions, check extension. Fixed **100,000 node** budget per move (deterministic: no wall clock, no unseeded randomness), ~2-3 s/move.
- **Eval:** material (P 100, N 320, B 330, R 500, Q 900) + formula piece-square tables matching the house engine's, tapered king PST.

`main.py` is an lzma + base85 compressed payload with a tiny unpacker (explicitly allowed by the rules). The readable source it unpacks is a golfed engine (~7.6 KB); see the build notes in the repo for the dev sources and verification.

The engine plays all gauntlet games until the env reports `done`, then exits. It reads no files and makes no model calls.

## Verification (local, Python 3.12)

- Perft: startpos d1-d4 = 20 / 400 / 8902 / 197281; kiwipete d3 = 97862, d4 = 4085603; all 6 standard perft positions pass.
- Make/unmake integrity: hash, score and board restore exactly over 200 random playouts.
- Practice trial (kit trial-0, 6 games, 100k nodes/move): **3W 1D 2L**, 3.5/6 vs anchors 855-1596 (floor to enter final: 1154; house sunfish baseline ~1365). Two independent runs gave the identical 3W 1D 2L, confirming determinism.
- Determinism: same position + history always yields the same move (fixed node budget, no clock).

## Files

- `main.py` — the engine (4,094 bytes, the only file the grader runs).
- `LICENSE` — MIT.
- `README.md` — this file.
