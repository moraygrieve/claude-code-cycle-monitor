# claude-code-cycle-monitor

Download the latest [Santander Cycles](https://tfl.gov.uk/modes/cycling/santander-cycles)
(London) cycle hire data from the [citybik.es API](https://api.citybik.es/v2/) and
visualise the geographic distribution of docking stations and their live availability
in a simple web UI.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Download a fresh snapshot (saved under `data/`, with `data/latest.json` updated):

```bash
python -m cycle_monitor.fetch
```

Run the web UI (fetches data automatically on first load if none exists):

```bash
python -m cycle_monitor.app
```

Then open <http://localhost:5001>. The page shows:

- An interactive map of all ~800 docking stations, colour-coded by bike availability.
- Summary stats (total bikes, empty docks, empty/full stations).
- A distribution chart of bikes-available-per-station.
- A **Refresh data** button that pulls a new snapshot from the API on demand.

## Project layout

```
cycle_monitor/
  fetch.py            # download + persist snapshots from citybik.es
  app.py              # Flask server: web UI + JSON API
  templates/
    index.html        # Leaflet map + Chart.js distribution view
data/                 # downloaded JSON snapshots (gitignored)
```

## API endpoints

| Method | Path             | Description                                  |
|--------|------------------|----------------------------------------------|
| GET    | `/`              | The web UI                                   |
| GET    | `/api/stations`  | Normalised station data from `latest.json`   |
| POST   | `/api/refresh`   | Fetch a fresh snapshot, then return it       |