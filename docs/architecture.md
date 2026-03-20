# AlphaPatch Architecture

High-level flow:
1. GitHub Action triggers on issue events.
2. `bot/main.py` loads config and coordinates analysis.
3. Analysis produces a response and later patch/PR artifacts.
4. Results are posted back to GitHub.

Module boundaries:
- `bot/github/`: GitHub API access + models
- `bot/analysis/`: issue analysis + context selection
- `bot/patch/`: patch proposal + validation
- `bot/pr/`: PR drafting + comments
