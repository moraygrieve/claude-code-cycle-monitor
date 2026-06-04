"""Download the latest Santander Cycles (London) data from the citybik.es API.

Run directly to fetch a fresh snapshot:

    python -m cycle_monitor.fetch
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import requests

API_URL = "https://api.citybik.es/v2/networks/santander-cycles"
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LATEST_PATH = DATA_DIR / "latest.json"


def fetch_network(url: str = API_URL, timeout: int = 30) -> dict:
    """Fetch the raw network payload from citybik.es."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def save_snapshot(payload: dict, data_dir: Path = DATA_DIR) -> Path:
    """Persist a timestamped snapshot and update latest.json. Returns the snapshot path."""
    data_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    snapshot_path = data_dir / f"santander-cycles_{timestamp}.json"

    snapshot_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    LATEST_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return snapshot_path


def fetch_latest() -> Path:
    """Fetch and store the latest snapshot, returning its path."""
    payload = fetch_network()
    snapshot_path = save_snapshot(payload)

    stations = payload.get("network", {}).get("stations", [])
    free_bikes = sum((s.get("free_bikes") or 0) for s in stations)
    empty_slots = sum((s.get("empty_slots") or 0) for s in stations)
    print(f"Saved {snapshot_path.name}")
    print(f"  Stations:    {len(stations)}")
    print(f"  Free bikes:  {free_bikes}")
    print(f"  Empty slots: {empty_slots}")
    return snapshot_path


if __name__ == "__main__":
    fetch_latest()