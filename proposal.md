**Brendan Myers | Final Project Proposal | October 25, 2026**

# Predicting Weekly Fantasy Football Performance

## 1. Research question

How strongly are a wide receiver’s targets and PPR fantasy points each associated with his next-week PPR points during the 2024 NFL regular season, and how much do those associations differ? A target is a pass directed toward a receiver, and PPR scoring awards one point per reception. I will compare both measures using the same set of players and consecutive weeks.

This question matters to fantasy football managers deciding whom to start or pick up after a big game. A receiver can score a touchdown on very few opportunities, while another can receive many targets without producing a high score. Knowing which measure carries over better would help managers decide how much weight to give a recent performance. Fantasy writers could also use the results when explaining weekly recommendations.

I expect targets to have a stronger relationship with next-week scoring because they reflect a receiver’s involvement in the offense. I would be surprised if current-week fantasy points were clearly more strongly associated with next-week results, or if neither measure had much relationship with future scoring. Either outcome would answer the question; the project will not assume that targets are better.

## 2. Data sources and method

I will use the [nflverse 2024 weekly player statistics CSV](https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats_2024.csv) hosted on GitHub. The [player-statistics data dictionary](https://nflreadr.nflverse.com/articles/dictionary_player_stats.html) explains its fields. The exact download URL is included in the retrieval example below. This is a direct HTTP download of structured web data, followed by CSV parsing in Python; it does not require scraping dynamic pages or logging into a fantasy platform.

I will collect the file once and save a dated local copy. Filtering to position WR and season_type REG produces 2,132 player-week records across weeks 1–18. I will join each player’s week t record to week t+1 using player_id and week, with weeks 1–17 as predictors. Only pairs present in both consecutive weeks will be included. I will not treat a bye or missing record as zero points, and I will report the final number of matched pairs.

The analysis will compare two Pearson correlations: targets versus next-week fantasy_points_ppr, and current-week versus next-week fantasy_points_ppr. I will report both correlation coefficients and their difference (the targets correlation minus the points correlation). Two scatterplots with trend lines will show these relationships. I will also compare average next-week scores across target groups of 0–3, 4–7, and 8 or more, reporting each group’s size. These are descriptive associations, not proof that additional targets cause future points or a validated forecasting system.

Course methods: I will use [Chapter 5, “Web Architecture and Protocols”](https://github.com/cuinfoscience/Web-Data-Science-Book/blob/main/ch-05-protocols.qmd), for HTTP GET requests, custom headers, and checking response status codes. I will parse the downloaded CSV with pandas. [Chapter 2, “Ethics, Law, and Responsible Data Collection”](https://github.com/cuinfoscience/Web-Data-Science-Book/blob/main/ch-02-ethics.qmd), will guide robots.txt checks and request limits. [Chapter 15, “Research Design with Web Data”](https://github.com/cuinfoscience/Web-Data-Science-Book/blob/main/ch-15-research-design.qmd), will guide sampling, limitations, and a reproducible analysis.

## 3. Ethics and feasibility

The [nflverse-data license](https://github.com/nflverse/nflverse-data/blob/main/LICENSE.md) is Creative Commons Attribution 4.0. I will credit nflverse, link the license, and identify filtering and derived variables. I am relying on the dataset’s reuse license rather than assuming that educational use automatically qualifies as fair use. GitHub’s [Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) and [Acceptable Use Policies](https://docs.github.com/en/site-policy/acceptable-use-policies/github-acceptable-use-policies) also govern access. I will publish the analysis openly and avoid collecting GitHub user information.

I retrieved [GitHub’s robots.txt](https://github.com/robots.txt) and found no applicable rule blocking this release-asset URL. Robots rules are access guidance, not a substitute for the license or terms. I will download the provided file rather than crawl repository pages, identify requests with User-Agent BrendanMyers-ClassResearch/1.0, cache the response, and pause at least two seconds between any additional requests. If access is limited, I will honor Retry-After instructions and stop repeated retries.

The file includes professional athletes’ names, identifiers, and photo URLs. I will retain player IDs for matching, omit photos and photo URLs from my working table, and present aggregate results. Names are unnecessary for the statistical comparison. I will not collect fantasy managers’ accounts, league information, or other private details.

One record, retrieved: The following URL was actually requested during proposal preparation with the User-Agent above. The response was HTTP 200 OK. The CSV contained the Adam Thielen record below; this is a selected-field excerpt, not the entire HTTP response.

```text
GET https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats_2024.csv
User-Agent: BrendanMyers-ClassResearch/1.0

HTTP status: 200
player_id: 00-0030035      player_display_name: Adam Thielen
position: WR             recent_team: CAR
season: 2024             season_type: REG
week: 1                  opponent_team: NO
targets: 4               receptions: 3
receiving_yards: 49       receiving_tds: 0
fantasy_points_ppr: 7.9
```

The analysis fields will be player_id, position, season, season_type, week, targets, and fantasy_points_ppr. The player name and receiving statistics above help check that the sample was parsed correctly.

The biggest risk is interpreting missing weeks incorrectly: injuries, byes, or absent statistical records can remove players from the matched sample. Findings will therefore apply only to receivers observed in consecutive weeks. I will check duplicates and missing values before joining. If missing weeks prevent a reliable next-week comparison, my fallback is a smaller descriptive question: how average same-week PPR points differ among receivers with 0–3, 4–7, and 8 or more targets. This uses the already downloaded 2024 records without joining weeks. It answers a narrower question about current scoring rather than future performance, while keeping the project feasible without another source.
