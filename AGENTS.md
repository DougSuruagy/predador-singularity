# PREDATOR SYSTEM - AGENTS.MD

## 🧠 Project Context
**Name:** PREDATOR SINGULARITY (v21.4 APEX SCALPER)
**Goal:** Creating an autonomous, self-evolving HFT system for Crypto Futures.
**Core Philosophy:** "Flat Position Protocol" (Zero Overnight), 3-Strikes Limit, Genetic Evolution.

## 🛠 Tech Stack & Conventions
- **Backend:** Python 3.10+ (FastAPI) running on **Render**.
  - Entry point: `cloud_api.py`
  - Zero local dependencies (Cloud-native).
  - Uses `ccxt.async_support` for Binance Futures.
- **Frontend/Supervisor:** Node.js (Vercel Serverless).
  - Entry point: `/api/supervisor.js`
  - Frontend: Vanilla JS key files `main.js`, `index.html`.
- **Database:** Supabase (PostgreSQL).
  - **RLS Enabled**: Strict policies. `auth.role()` calls are wrapped in subqueries/initplans for performance.
  - Tables: `trades`, `daily_stats`, `system_logs`, `genetics`.
  - Indexes: BRIN for logs, B-Tree for trades.

## ⚠️ Critical Patterns & Gotchas
1.  **Environment Variables:**
    - Render needs `BINANCE_API_KEY`, `BINANCE_API_SECRET`, `SUPABASE_URL`, `SUPABASE_KEY`.
    - Vercel needs `RENDER_API_URL` to bridge the frontend.
2.  **Trade execution:**
    - ALWAYS check `state.is_locked` before execution.
    - ALWAYS use `execute_binance_order` with `use_compounding=True` for sovereign scaling.
    - NEVER hold positions past 17:30 BRT (Flat Position Protocol).
3.  **Supabase & Performance:**
    - Use `(SELECT auth.role())` in RLS policies to avoid `auth_rls_initplan` warnings.
    - Scalper Loop runs every 3s; avoid heavy SQL queries inside the main loop. Use `evolution_watcher_loop` for slow tasks.

## 🧬 Evolution Logic
- **Junior (Vercel):** Analyzes `trades` table. If Win Rate > 60%, generates new `genetics` row.
- **Senior (Render):** Watches `genetics` table. If new generation > current generation, hot-swaps active DNA.
