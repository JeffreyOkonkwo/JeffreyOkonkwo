# Delivery Health Report: Power BI guide

Author: Jeffrey Okonkwo

## How to open it

1. Install Power BI Desktop (Windows, a recent release with PBIP support).
2. Open `project/DeliveryHealth.pbip`. The report, the semantic model, the theme and the page backgrounds load together.
3. If Power BI asks about the data source, choose Anonymous access for `raw.githubusercontent.com`.

## How to refresh it

Select Home, then Refresh. Every table loads its CSV straight from GitHub through the `DataRoot` parameter:
`https://raw.githubusercontent.com/JeffreyOkonkwo/JeffreyOkonkwo/main/delivery-health-report/powerbi/`.
To work from a local copy instead, change `DataRoot` (Transform data, then Edit parameters) to that folder's path,
and change `Web.Contents` to `File.Contents` in each query.

A manual build kit sits beside the project: `measures.dax` holds every measure and `power_query.m` holds every query.
`DeliveryHealth.theme.json` is the report theme.

## What each page answers

| Page | Question it answers |
| --- | --- |
| Overview | How predictable are the three teams overall? Say-do ratio, scope added mid-sprint, carry-over, cycle time, code review share and items stuck across sprints, with say-do by sprint against an 80% goal. Use the Team slicer to focus on one team. |
| Predictability | Did each sprint deliver what it committed to? A scorecard of every sprint, scope added per sprint, and the carry-over trend. Use the Period slicer to compare April to December 2025 with January to October 2026. |
| Flow | How long does finished work take, and where does the time go? Cycle time per item against the 85th percentile, the share of time spent in progress, in code review, blocked or waiting, weekly throughput and cumulative flow. |
| Backlog health | Which work keeps rolling forward, and how much added work is unplanned? Items that sat in three or more sprints, and items added mid-sprint by type, with bugs and build failures counted as unplanned. |

## Program totals (all teams, full period)

| Measure | Value |
| --- | --- |
| Say-do ratio | 45.3% (Foundations 56.6%, Persistence 34.4%, Transactions 42.9%) |
| Scope added mid-sprint | 67.4% of committed items |
| Carried over | 442 items |
| Sprints | 95 (84 with a commitment, 16 of them at 80% say-do or better) |
| Cycle time | 4.1 days at the median, 18.2 days at the 85th percentile |
| Code review share of cycle time | 23.2% |
| Flow efficiency | 32.7% |
| Items in three or more sprints | 105 |
| Unplanned share of added items | 41.3% (215 of 520) |

Source: MongoDB public Jira, project WT (WiredTiger).
