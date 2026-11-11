# What 4.0 took and what came back: the method

The launch post gives estimates, because time and spend were not tracked as the work happened. This file says how each figure was reached, so anyone can check it or redo it.

## Time: about 600 hours (400 to 800)

- **What git shows.** Grouping every commit on every branch into sessions (a gap over 45 minutes starts a new one, and each session gets 20 minutes added for the work before its first commit) gives 39 sessions and about 77 hours, on 24 days between 3 June and 2 November 2026. That is a floor, not the total:
  - the history before 3 June was squashed, so the May work is missing from it;
  - long sessions run for hours between commits.
- **What the release log shows.** CHANGELOG.md has 44 version entries from 1.0.0 on 22 May to 4.0.0 on 1 November; the alpha entries cover about a hundred builds in the last week of May.
- **The estimate:**
  - The May sprint, ten days of daily releases at roughly ten hours a day, is about 100 hours.
  - June to November, about 22 weeks at 20 to 25 hours a week of paired work, is about 450 to 550 hours.
  - Together that is about 600 hours. The range of 400 to 800 says how unsure this is.

## Money: about $1,400 over six months

The six months are May to October 2026, plus the start of November. The costs are the ones the author named; the amounts are list prices or estimates where no list price applies:

| Item | Monthly | Six months |
|---|---|---|
| AI coding subscription, top tier | about $200 | about $1,200 |
| Second AI coding subscription | $20 | $120 |
| Model router (open source, self-hosted) | $0 | $0 |
| Small server | about $5 to $20 | about $30 to $120 |
| Domain | about $1 | about $12 for the year |
| Site hosting, package registries, CI | $0 | $0 |
| **Total** | | **about $1,360 to $1,450** |

## What came back

- **Installs, measured on 2 November 2026:**
  - npm reports 537 downloads of `uxskill` between 27 May and 29 October (api.npmjs.org, downloads/range).
  - PyPI reports 230 downloads in the last month (pypistats.org). It shows no all-time total.
- **The product:** 17 tagged releases (v1.0.0 to v4.0.0), 13,101 passing tests, 171 lint rules, 25 MCP tools and 160 brand specs, MIT licensed. Every count is one the code gives today.
- **Not counted:** stars, client work and anything that cannot be measured from the repository or a public registry.
