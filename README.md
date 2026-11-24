[![THE WORLD TODAY](https://make.fun/badge/news-image-20261123.svg?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b176-front-page-dense/rank.svg?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)](https://make.fun/competitions/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![Reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b176-front-page-dense/reward.svg?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

One image summing up 23 November's world news: the AI rout hitting Asian
markets (Kospi −3.3%), Guterres calling for AI regulation before it's too
late at the Bridgetown summit, and the US lead over China at a record low
in the Asia Power Index 2026 — plus 28 more stories, a number strip, a
world map with 13 pins, and a DATE CHECK box listing what did *not* happen
on 23 November.

## How it is built

- `draw.py` — PIL renderer that draws the 1024×1024 front page.
- `main.py` — stdlib-only runner (no PIL). It validates `entry.png`
  (PNG signature, IHDR 1024×1024, per-chunk CRCs, non-empty IDAT, IEND
  last, size ≤ 1 MiB, exact sha256) and copies the bytes to
  `$MAKEFUN_OUTPUT_DIR/entry.png`. Run: `python3 -P -s main.py`.

## Facts

All stories are dated Monday 23 November 2026. Items marked CLAIM are
one side's claim, not confirmed fact. The DATE CHECK box lists stories
from other dates (Dems 258, Sparta II fire, El Chapo capture, EU–Indonesia
pact, Nigeria boat, ICJ Myanmar ruling) so they are not mistaken for
23 November news.
