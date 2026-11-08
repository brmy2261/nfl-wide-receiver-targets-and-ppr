# Targets or fantasy points? Predicting next-week scoring for NFL wide receivers

**Brendan Myers**

When a receiver scores a touchdown on two targets and another draws eight targets without scoring, which performance tells a fantasy manager more about next week? Using the 2024 NFL regular season, I will compare how strongly a receiver’s targets and his PPR (points per reception) fantasy score each correlate with his PPR score the following week. Both comparisons will use the same receivers observed in consecutive weeks.

## Data

Source: [nflverse's 2024 weekly player statistics CSV](https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats_2024.csv), collected **November 8, 2026 at 23:01:52 UTC (4:01:52 p.m. MST)** with HTTP 200. The raw file contains **5,597 records and 53 fields**. Filtering and validation produced **2,132 regular-season wide-receiver player-weeks (227 receivers)** and **1,560 consecutive-week pairs**. No selected rows were missing required values or duplicated.

The repository includes a [50-row cleaned weekly sample](data/wr_weekly_sample.csv), a [50-row matched-pair sample](data/wr_pairs_sample.csv), a [data dictionary and cleaning notes](data/README.md), [collection metadata](data/collection_metadata.json), and [cleaning output](data/cleaning_summary.json). The [executed notebook](analysis.ipynb) shows the code calls and output.

Full raw data are saved locally but excluded from Git because they include unnecessary athlete names, photo URLs, and unrelated fields. Full cleaned tables are also excluded to keep the repository focused on small examples; the scripts regenerate them. Public athlete IDs remain in the sample for matching and are linkable, not anonymous. These omissions are a data-minimization and repository-size choice, not a claim that the license forbids redistribution. Data credit: nflverse contributors, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); the samples have been filtered and transformed as documented in the dictionary.

## Methods

I will match receivers by player ID and consecutive week, then compare the two Pearson correlations. The [proposal](proposal.md) describes the sample, target groups, and missing-week rules.

## Findings

Pending analysis. The [report](report.md) will give the matched sample size, both correlations, their difference, and the target-group averages.

## How to reproduce

Use Python 3.10 or newer. From the repository root, run:

```bash
python -m pip install -r requirements.txt
python scripts/collect.py
python scripts/clean.py
```

The collector identifies this project in its User-Agent, pauses at least two seconds between requests (including redirects), checks HTTP responses, saves the raw bytes under `data/raw/`, and records their SHA-256 checksum. It reuses an existing verified download. On a fresh clone, it downloads the source and updates the metadata; upstream revisions may change the checksum or counts from the recorded run.

Cleaning creates `data/processed/wr_weekly_2024.csv` and `data/processed/wr_consecutive_weeks_2024.csv`, plus the two committed samples and a JSON summary. Use the full generated paired table for the eventual analysis, not the 50-row samples. No API key is required. Git ignores both full-data folders.

For the interactive version, install JupyterLab (`python -m pip install jupyterlab`), open [analysis.ipynb](analysis.ipynb) from this folder, and run all cells. The saved notebook already contains the Week 12 collection and cleaning outputs. Statistical findings and the final report remain for a later project stage.
