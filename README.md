# HDF Wells Map — static site

Public map of Human Development Fund water wells, built from partner field reports.
Deployed as a Render **Static Site**. 

## Files

| File | What | Changes? |
|---|---|---|
| `index.html` | The map page (Mapbox GL) | Rarely — only for design changes |
| `wells.json` | Well data: stats + pins + country aggregates. **Donor names, dedications, costs, and partner names are stripped** — locations, types, and statuses only. | Every data update |
| `token.js` | Mapbox public (`pk.`) token | Only if the token rotates |
| `photos/` | Optional well photos, named `<well id>.jpg` (e.g. `RPT-001.jpg`). If present, shown inside the map popup. | When new photos arrive |

## Updating the data

From the WaterwellPreprod repo (`water-tracker/`):

```bash
# 1. Drop new partner report CSVs into data/partner-reports/
# 2. Rebuild the dataset
node scripts/build-wells-map-data.js
# 3. Export the static bundle into this repo
node scripts/export-static-map.js c:/Users/musta/hdf-wells-map
# 4. Push — Render redeploys automatically
cd c:/Users/musta/hdf-wells-map
git add -A && git commit -m "Data update" && git push
```

## Notes

- The public map shows **completed wells only**. A fresh export includes in-progress and
  planned wells (and donor fields) — re-filter to completed and re-strip donor names,
  dedications, costs, and partner names before pushing.

