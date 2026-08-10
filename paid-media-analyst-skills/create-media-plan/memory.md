# Memory: create-media-plan

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-06-22: Maximize Clicks plans flex on daily budget only, never bids (user correction)
When a campaign runs Maximize Clicks, the only lever the client adjusts to deploy plan headroom or change pacing is the DAILY BUDGET; there is no manual bid up/down and the optional Max-CPC bid limit is not a lever to propose. Frame any "deploy the remaining budget" or pacing action as "increase the daily budget," never as a bid move or bid-limit change. Client quote: "we can only update daily budgets for pacing."

### 2026-06-22: Blank plan delivered/pacing columns mean compute actuals from exports ([Product Line A] EMEA)
When the plan's delivered and pacing columns are blank, compute actuals from the platform exports and footnote that they are computed. Reconcile each platform actual against its own plan line, not a blended total. Flight extensions mean a mid-flight platform sitting at about 50% can still be on-track, so check the schedule before calling it behind.

### 2026-05-24: Ground pacing in quarterly budgets and the run-rate plan ([Account: MOEM])
[Account: MOEM] runs quarterly budgets (Industrial $11,000 per quarter, Medical $9,000 per quarter across geos), so reconcile spend to the client pacing tool before projecting. Frame pacing against the run-rate plan to-date, not a single-month cap, and pair the variance with a forward action. Do not propose branded-campaign builds for [Account: MOEM] (the [Acquiring Co] transition is pending).

## Standing preferences (apply every run)

- **Two modes:** historical (ground projections in existing reports or raw CSVs) and net-new (B2B industry benchmarks). Saying "no historical data" or "new account" forces net-new, which needs no file upload.
- **Never blend CAD and USD** in projections; label currency. Honor an explicit user override with a per-table footnote.
- **Do not name "DataForSEO"** if search-volume demand feeds the plan; frame it as "our keyword research."
