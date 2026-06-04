"""Flask web UI for the Santander Cycles monitor.

    python -m cycle_monitor.app

Then open http://127.0.0.1:5000
"""

from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, jsonify, render_template

from .fetch import LATEST_PATH, fetch_latest

app = Flask(__name__)


def load_latest() -> dict:
    """Return the latest snapshot, fetching one if none exists yet."""
    if not LATEST_PATH.exists():
        fetch_latest()
    return json.loads(Path(LATEST_PATH).read_text(encoding="utf-8"))


def build_summary(payload: dict) -> dict:
    """Normalise the citybik.es payload into a compact, UI-friendly shape."""
    network = payload.get("network", {})
    raw_stations = network.get("stations", [])

    stations = []
    for s in raw_stations:
        free = s.get("free_bikes") or 0
        empty = s.get("empty_slots") or 0
        extra = s.get("extra", {}) or {}
        stations.append(
            {
                "id": s.get("id"),
                "name": s.get("name"),
                "lat": s.get("latitude"),
                "lon": s.get("longitude"),
                "free_bikes": free,
                "empty_slots": empty,
                "capacity": free + empty,
                "ebikes": extra.get("ebikes"),
                "timestamp": s.get("timestamp"),
            }
        )

    total_free = sum(s["free_bikes"] for s in stations)
    total_empty = sum(s["empty_slots"] for s in stations)
    empty_stations = sum(1 for s in stations if s["free_bikes"] == 0)
    full_stations = sum(1 for s in stations if s["empty_slots"] == 0)

    return {
        "name": network.get("name"),
        "city": network.get("location", {}).get("city"),
        "station_count": len(stations),
        "total_free_bikes": total_free,
        "total_empty_slots": total_empty,
        "empty_stations": empty_stations,
        "full_stations": full_stations,
        "stations": stations,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/stations")
def api_stations():
    return jsonify(build_summary(load_latest()))


@app.route("/api/refresh", methods=["POST"])
def api_refresh():
    fetch_latest()
    return jsonify(build_summary(load_latest()))


if __name__ == "__main__":
    app.run(debug=True, port=5000)