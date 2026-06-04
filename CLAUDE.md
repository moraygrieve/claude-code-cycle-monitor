# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

`claude-code-cycle-monitor` downloads the latest Santander Cycles (London) data from
the citybik.es API and visualises docking-station distribution and live availability in
a small Flask web UI.

## Commands

Setup (Python 3.13):

```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```

- Fetch a fresh data snapshot: `python -m cycle_monitor.fetch`
- Run the web UI: `python -m cycle_monitor.app` (serves http://127.0.0.1:5000)

There is no test suite or linter configured yet.

## Architecture

- `cycle_monitor/fetch.py` — fetches `https://api.citybik.es/v2/networks/santander-cycles`,
  writes a timestamped snapshot to `data/` and overwrites `data/latest.json`. This is the
  single source of downloaded data; the web layer never calls the API directly.
- `cycle_monitor/app.py` — Flask app. `build_summary()` normalises the raw citybik.es
  payload into a compact station shape; `load_latest()` reads `data/latest.json` (calling
  `fetch_latest()` if it is missing). Routes: `/` (UI), `/api/stations` (GET, current
  data), `/api/refresh` (POST, fetch then return).
- `cycle_monitor/templates/index.html` — self-contained front end (Leaflet map + Chart.js
  via CDN). Calls `/api/stations` on load and `/api/refresh` on the refresh button.

Data flow: `fetch.py` → `data/latest.json` → `app.build_summary` → `/api/*` JSON →
`index.html`. Snapshots under `data/` are gitignored.
