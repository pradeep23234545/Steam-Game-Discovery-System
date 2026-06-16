# Workspace

## Overview

pnpm workspace monorepo using TypeScript. Each package manages its own dependencies.
Also includes a Python Streamlit application: **Steam Game Discovery Dashboard**.

## Stack

- **Monorepo tool**: pnpm workspaces
- **Node.js version**: 24
- **Package manager**: pnpm
- **TypeScript version**: 5.9
- **API framework**: Express 5
- **Database**: PostgreSQL + Drizzle ORM
- **Validation**: Zod (`zod/v4`), `drizzle-zod`
- **API codegen**: Orval (from OpenAPI spec)
- **Build**: esbuild (CJS bundle)

## Steam Game Discovery Dashboard (Python/Streamlit)

A full-featured Steam analytics and recommendation platform.

### Files
- `app.py` — Main Streamlit application
- `steam.csv` — Game dataset (~90 games)
- `.streamlit/config.toml` — Streamlit server config (port 8000)

### Features
- Dark glassmorphism UI with gradient background
- Sidebar filters (genre, player style, price, ratings, free-to-play, sort)
- Game tabs: Popular, Trending, Hidden Gems
- AI-style game descriptions (generated from attributes)
- Game DNA radar chart (Plotly)
- Game similarity map (PCA scatter)
- Recommendation engine (genre overlap + rating + price)
- Side-by-side game comparison with DNA charts
- Analytics dashboard (price histogram, ratings histogram, scatter, genre bar, box plot)
- Raw data explorer with CSV download

### Dependencies (Python)
- streamlit, pandas, numpy, plotly, scikit-learn, requests

### Workflow
- Name: `Steam Dashboard`
- Command: `streamlit run app.py --server.port 8000`
- Port: 8000

## Key Commands (TypeScript)

- `pnpm run typecheck` — full typecheck across all packages
- `pnpm run build` — typecheck + build all packages
- `pnpm --filter @workspace/api-spec run codegen` — regenerate API hooks and Zod schemas from OpenAPI spec
- `pnpm --filter @workspace/db run push` — push DB schema changes (dev only)
- `pnpm --filter @workspace/api-server run dev` — run API server locally

See the `pnpm-workspace` skill for workspace structure, TypeScript setup, and package details.
