# Memory: analyze-dsp-display

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-06-16: Live MCP has no domain breakdown; use transparencyScore and re-pull a CSV for the blocklist ([Account: IWFB])
The live [DSP Platform] MCP `rtb_get_metrics` has no domain/site breakdown (its types are line, campaign, creative, geo, device, exchange, deal, daily), so a domain blocklist cannot be built from the live API; re-pull a [DSP Platform] CSV (with Site Domain) to refresh it. Use `transparencyScore` as the inventory-quality proxy instead (e.g., ~19% on an open-exchange line means ~81% non-transparent app/email inventory). Per-line monthly metrics come from one type=line call with startDate/endDate filters, but a multi-line type=exchange call can time out so pull one line at a time, and compare CTR (rate) not raw clicks when a partial month is in the window.

### 2026-05-19: First [DSP Platform] run; sitelist-constrained vs creative-constrained ([Account: IWFB])
[DSP Platform] scaffolding was stood up from scratch (data/raw, outputs, the agent spec, the skill, and the naming-hook branch). Low-click line items were sitelist-constrained, not creative-constrained (Wine and Beer Segments ran on a shared 139-site list weighted toward Wine), so the fix is the sitelist, not the creative. A broad open-exchange line carried about $500 in zero-click, off-context domain spend including `*.overwolf.com` gaming-overlay subdomains and `mail.yahoo.com` (80K impressions, 0 clicks), so build a domain blocklist.

## Standing preferences (apply every run)

- **Schema is account-specific.** The agent's "Detected columns" block in the spec is populated per account on first run so it carries durable schema knowledge; sniff for a BOM and use `encoding='utf-8-sig'` if present.
- **Conversion columns are often absent.** Fall back to click-volume-weighted rollups and label them `(click-volume weighted; no conversion tracking)`.
- **DSP dimensions to expect:** line item, creative, exchange / inventory source, domain / app, audience segment, viewability, frequency, and video starts / completes.
- **CTV gets impressions with about zero clicks by design** (it is not click-driven), so do not flag CTV zero-click as a problem. A flat CPM is common on these buys.
