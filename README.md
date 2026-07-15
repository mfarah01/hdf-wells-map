# HDF Wells Map — static site

Public map of Human Development Fund water wells, built from partner field reports.
Deployed as a Render **Static Site**. Intended to be linked from (or iframed into) hdfund.org.

## Files

| File | What | Changes? |
|---|---|---|
| `index.html` | The map page (Mapbox GL) | Rarely — only for design changes |
| `wells.json` | Well data: stats + pins + country aggregates. **Donor names, dedications, costs, and partner names are stripped** — locations, types, and statuses only. | Every data update |
| `token.js` | Mapbox public (`pk.`) token | Only if the token rotates |

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

- The Mapbox token is public-type and visible by design. It should carry
  **URL restrictions** (this site's domain + hdfund.org) on account.mapbox.com.
- Never commit donor names, dedications, costs, or partner names here. If re-exporting
  from the exporter, re-strip those fields before pushing.
