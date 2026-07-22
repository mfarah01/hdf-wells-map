# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **single-page static site** that renders the Human Development Fund water-wells map (Mapbox GL JS). No build system, no package manager, no tests — just three files served as-is by Render's Static Site hosting. Pushing to `main` triggers a Render redeploy.

- `index.html` — the whole app (styles, markup, and the Mapbox script inline)
- `wells.json` — the data payload fetched at runtime
- `token.js` — sets `window.MAPBOX_TOKEN` (public `pk.` token, safe to commit)
- `photos/<well-id>.jpg` — optional; popups reference `photos/<id>.jpg` and the `<img>` self-removes on 404, so missing photos are fine

## Local preview

Serve the directory over HTTP (opening `index.html` via `file://` breaks the `fetch('./wells.json')` call):

```bash
python3 -m http.server 8000    # then open http://localhost:8000
```

## Data pipeline — the data is generated elsewhere

`wells.json` is **not hand-edited here**. It is produced in the sibling repo `WaterwellPreprod` (`water-tracker/`) and exported into this repo. From that repo:

```bash
node scripts/build-wells-map-data.js
node scripts/export-static-map.js <path-to-this-repo>
```

Then `git add -A && git commit && git push` from this repo.

**Critical filter step before pushing:** a fresh export includes in-progress and planned wells and donor-identifying fields. The public map must show **completed wells only**, with donor names, dedications, costs, and partner names stripped. Re-filter and re-strip before committing.

## `wells.json` shape (what `index.html` consumes)

- `stats.total`, `stats.completed`, `stats.countries` — header counters
- `pinned[]` — wells with real coordinates; rendered as clustered points (`wells` source, layers `clusters`, `cluster-count`, `well-pins`). Fields used by the popup: `id`, `country`, `location`, `type`, `depth`, `system`, `status`, `startDate`, `endDate`, `beneficiaries`, `photoLink`, `lat`, `lng`.
- `aggregates[]` — country-level bubbles for wells without precise coordinates; rendered as a second source (`aggs`, layers `agg-bubbles`, `agg-count`). Each carries `country`, `count`, `completed`, and `wells[]` (list surfaced in the popup).

Two independent Mapbox sources — pinned wells cluster; aggregate bubbles never do. Bounds are auto-fit from both.

## Editing conventions

- Popup HTML is built by string concatenation and passed through the `esc()` helper — keep every dynamic value wrapped in `esc(...)` to preserve XSS safety.
- Status values `completed` / `in_progress` / `planned` are hardcoded in CSS (`.wm-pop-badge.*`) and in the pin opacity rule (`well-pins` layer). Adding a new status means updating both.
- Design tokens live in the `:root` CSS variables at the top of `index.html` (`--hdf-primary`, `--hdf-gold`, etc.).
- Map style is `mapbox://styles/mapbox/outdoors-v12`. If you switch it, verify pin/cluster contrast against the new basemap.
