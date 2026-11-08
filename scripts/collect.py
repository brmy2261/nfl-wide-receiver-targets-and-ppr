"""Download and cache the unmodified nflverse 2024 player-statistics CSV."""
from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import io
import json
import time
from urllib.parse import urljoin
import requests

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats_2024.csv'
ROBOTS = 'https://github.com/robots.txt'
USER_AGENT = 'BrendanMyers-ClassResearch/1.0 (+https://github.com/brmy2261/nfl-wide-receiver-targets-and-ppr)'
METADATA = ROOT / 'data/collection_metadata.json'


def collect():
    # Reuse the exact cached bytes on subsequent runs instead of downloading again.
    if METADATA.exists():
        metadata = json.loads(METADATA.read_text())
        raw_path = ROOT / metadata['raw_path']
        if raw_path.exists():
            if hashlib.sha256(raw_path.read_bytes()).hexdigest() != metadata['sha256']:
                raise ValueError('Cached raw file differs from its checksum; inspect it before continuing.')
            print(f"Using cached raw file: {metadata['raw_path']}")
            return metadata
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    last_request = None

    def get(url):
        nonlocal last_request
        # Apply the pause to redirects too. No automatic retries on rate limits.
        for _ in range(6):
            if last_request is not None:
                time.sleep(max(0, 2.0 - (time.monotonic() - last_request)))
            response = session.get(url, timeout=(15, 120), allow_redirects=False)
            last_request = time.monotonic()
            if response.status_code in (301, 302, 303, 307, 308):
                url = urljoin(url, response.headers['Location'])
                continue
            if response.status_code in (403, 429):
                raise RuntimeError(f'Access limited ({response.status_code}). Stop; Retry-After: '
                                   f'{response.headers.get("Retry-After", "not supplied")}. Do not retry early.')
            response.raise_for_status()
            return response
        raise RuntimeError('Too many redirects')

    robots = get(ROBOTS)
    response = get(SOURCE)
    payload = response.content
    reader = csv.DictReader(io.StringIO(payload.decode('utf-8-sig')))
    required = {'player_id', 'season', 'season_type', 'week', 'position', 'targets', 'fantasy_points_ppr'}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError('Downloaded file does not have the expected CSV fields')
    raw_records = sum(1 for _ in reader)
    if not raw_records:
        raise ValueError('Downloaded CSV is empty')
    collected = datetime.now(timezone.utc)
    relative = f'data/raw/player_stats_2024_{collected:%Y-%m-%d}.csv'
    raw_path = ROOT / relative
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path.write_bytes(payload)
    (raw_path.parent / 'github_robots.txt').write_text(robots.text)
    metadata = {
        'source_url': SOURCE, 'collected_at_utc': collected.isoformat(),
        'http_status': response.status_code, 'user_agent': USER_AGENT,
        'pause_seconds': 2, 'raw_path': relative, 'raw_records': raw_records,
        'raw_bytes': len(payload), 'raw_columns': len(reader.fieldnames),
        'sha256': hashlib.sha256(payload).hexdigest(),
        'robots_url': ROBOTS, 'robots_http_status': robots.status_code,
        'license_url': 'https://github.com/nflverse/nflverse-data/blob/main/LICENSE.md'
    }
    METADATA.write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, indent=2))
    return metadata


if __name__ == '__main__':
    collect()
