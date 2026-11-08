"""Create tidy WR player-week and consecutive-week tables from cached raw CSV."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['player_id', 'season', 'season_type', 'week', 'position', 'targets', 'fantasy_points_ppr']
KEY = ['player_id', 'season', 'season_type', 'week']


def clean():
    metadata = json.loads((ROOT / 'data/collection_metadata.json').read_text())
    raw_path = ROOT / metadata['raw_path']
    if hashlib.sha256(raw_path.read_bytes()).hexdigest() != metadata['sha256']:
        raise ValueError('Raw checksum mismatch; do not silently analyze changed data')
    raw = pd.read_csv(raw_path, dtype={'player_id': 'string'})
    missing = set(FIELDS) - set(raw.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    for field in ['player_id', 'position', 'season_type']:
        raw[field] = raw[field].astype('string').str.strip()
    selected = raw.loc[(raw['position'] == 'WR') & (raw['season_type'] == 'REG') &
                       (pd.to_numeric(raw['season'], errors='coerce') == 2024), FIELDS].copy()
    selected_count = len(selected)
    for field in ['season', 'week', 'targets', 'fantasy_points_ppr']:
        selected[field] = pd.to_numeric(selected[field], errors='coerce')
    numeric = ['season', 'week', 'targets', 'fantasy_points_ppr']
    valid = (selected['player_id'].notna() & selected['player_id'].ne('') &
             np.isfinite(selected[numeric]).all(axis=1) &
             selected['week'].between(1, 18) & selected['week'].mod(1).eq(0) &
             selected['targets'].ge(0) & selected['targets'].mod(1).eq(0))
    invalid_count = int((~valid).sum())
    weekly = selected.loc[valid].copy()
    exact_duplicates = int(weekly.duplicated().sum())
    weekly = weekly.drop_duplicates()
    if weekly.duplicated(KEY).any():
        raise ValueError('Conflicting player-week duplicates require manual review')
    for field in ['season', 'week', 'targets']:
        weekly[field] = weekly[field].astype('int64')
    weekly = weekly.sort_values(KEY).reset_index(drop=True)
    # Join by NFL week number, not by next available appearance: no bridging byes.
    following = weekly[KEY + ['fantasy_points_ppr']].copy()
    following['next_week'] = following['week']
    following['week'] -= 1
    following = following.rename(columns={'fantasy_points_ppr': 'next_week_ppr'})
    eligible = weekly.loc[weekly['week'] < 18].copy()
    pairs = eligible.merge(following, on=KEY, how='inner', validate='one_to_one')
    pairs = pairs.sort_values(KEY).reset_index(drop=True)
    pairs['target_group'] = pd.cut(pairs['targets'], [-1, 3, 7, float('inf')],
                                   labels=['0-3', '4-7', '8+']).astype('string')
    assert pairs['next_week'].eq(pairs['week'] + 1).all()
    assert not weekly.isna().any().any() and not pairs.isna().any().any()
    if weekly.empty or pairs.empty:
        raise ValueError('No eligible records; inspect collection before publishing')
    processed = ROOT / 'data/processed'
    processed.mkdir(parents=True, exist_ok=True)
    weekly.to_csv(processed / 'wr_weekly_2024.csv', index=False)
    pairs.to_csv(processed / 'wr_consecutive_weeks_2024.csv', index=False)
    for table, name in [(weekly, 'wr_weekly_sample.csv'), (pairs, 'wr_pairs_sample.csv')]:
        table.sample(n=min(50, len(table)), random_state=42).sort_values(KEY).to_csv(
            ROOT / 'data' / name, index=False)
    summary = {
        'source_collected_at_utc': metadata['collected_at_utc'],
        'source_sha256': metadata['sha256'],
        'raw_records': len(raw), 'raw_columns': len(raw.columns),
        'wr_regular_season_records_before_cleaning': selected_count,
        'excluded_other_positions_or_seasons': len(raw) - selected_count,
        'invalid_or_missing_rows_removed': invalid_count,
        'exact_duplicate_rows_removed': exact_duplicates,
        'conflicting_player_week_duplicates': 0,
        'clean_weekly_records': len(weekly), 'unique_receivers': weekly['player_id'].nunique(),
        'week_min': int(weekly['week'].min()), 'week_max': int(weekly['week'].max()),
        'predictor_rows_weeks_1_to_17': len(eligible),
        'consecutive_week_pairs': len(pairs),
        'eligible_rows_without_following_week': len(eligible) - len(pairs),
        'weekly_sample_records': min(50, len(weekly)), 'pairs_sample_records': min(50, len(pairs)),
        'retained_fields': FIELDS, 'sample_random_seed': 42
    }
    (ROOT / 'data/cleaning_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    print('\nClean weekly data preview:\n' + weekly.head().to_string(index=False))
    print('\nConsecutive-week preview:\n' + pairs.head().to_string(index=False))
    return weekly, pairs, summary


if __name__ == '__main__':
    clean()
