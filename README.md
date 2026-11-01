# Targets or fantasy points? Predicting next-week scoring for NFL wide receivers

**Brendan Myers**

When a receiver scores a touchdown on two targets and another draws eight targets without scoring, which performance tells a fantasy manager more about next week? Using the 2024 NFL regular season, I will compare how strongly a receiver’s targets and his PPR (points per reception) fantasy score each correlate with his PPR score the following week. Both comparisons will use the same receivers observed in consecutive weeks.

## Data

[Weekly player statistics from nflverse](https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats_2024.csv). Source and collection notes belong in [data/](data/README.md).

## Methods

I will match receivers by player ID and consecutive week, then compare the two Pearson correlations. The [proposal](proposal.md) describes the sample, target groups, and missing-week rules.

## Findings

Pending analysis. The [report](report.md) will give the matched sample size, both correlations, their difference, and the target-group averages.

## How to reproduce

The [Python notebook](analysis.ipynb) outlines the planned workflow. Setup instructions and the order for running the analysis will be added when the code is available.
