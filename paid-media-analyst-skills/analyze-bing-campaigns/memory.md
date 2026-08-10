# Memory: analyze-bing-campaigns

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-08-05: Build a full-flight cumulative + MoM table across every period analyzed, and let a repeat finding's trend direction set its tone ([Account: Water])
When the client sends a new period's data for an account already reported on, recombine it with the prior period(s) into a cumulative total plus a month-over-month table (by program, if the account splits that way), recomputing the prior period from its original raw export rather than trusting the old report's prose. When a prior recommendation reappears (e.g. an "industrial" negative recommended in May, still not applied in the June-July pull), check the actual trend before framing it — [Account: Water]'s leakage share had improved from 60%/65% to 52.7%/45.0% on its own, so the finding stayed HIGH priority but shifted from "unresolved failure" to "trending better, this captures the remaining upside." A brand-new ad group's first leakage signal (3 weeks of data) should be logged as MONITOR/LOW, not an active recommendation, until there's a second period to confirm the pattern.

### 2026-08-05: Verify a "position"-style column's exact header text hasn't changed between two export pulls before trending it ([Account: Water])
Two Bing exports for the same account and report type can differ in which columns are present even when the numbers look plausible to compare — [Account: Water]'s June-July Bing files dropped the `Ad distribution` (Search vs Audience Network) split that the April-May files had, so a blended "Search" total from one period can't be assumed directly comparable to a period that includes Audience spend without checking. Note a missing column as a data gap in that pull, not evidence the metric stopped applying. (See the equivalent Google-side entry in `analyze-search-campaigns/memory.md` for a sharper case where the SAME nominal column name meant two different metrics across pulls.)

### 2026-07-08: A client-confirmed "just added" keyword may not yet be in the export's active-keyword set
If a keyword was added very recently or after the export cutoff, its absence from the current period's performance export is not proof it is still a gap. Cross-check against the client's own confirmation or the team's recent recommendation history before re-flagging it as net-new. ([Account: MedTech] Q2, Google-side finding — applies equally to Bing dedup checks.)

### 2026-07-08: Tally the embedded keyword count across ALL matching change-history rows, not just recognizable examples ([Account: MedTech] Q2, qa-reviewer catch)
When summarizing a "N keywords paused/added" change-history event, sum the keyword-count number in each matching row's change block across every row for that date/event. Pattern-matching to a handful of familiar-looking example keywords understated a bulk cleanup 10x (6 cited examples vs. the true 62 keywords across 23 ad-group actions in 9 campaigns) — caught by qa-reviewer before commit.

### 2026-07-08: Despace CJK keywords before dedup checks, not just lowercase ([Account: MedTech] Q2)
A keyword-performance export's `Search keyword` column and the Search Query Report can tokenize CJK terms differently (inter-word spaces in one, none in the other), so a lowercase-only net-new check can falsely flag an already-active CJK keyword as a new candidate. Strip all whitespace, in addition to lowercasing, from both the active-keyword set and candidate search terms before comparing. Discovered on the Google side ([Account: MedTech] Q2); applies to Bing's Search Query Report dedup the same way.

### 2026-06-22: Maximize Clicks = daily-budget-only pacing; never recommend bid moves (user correction)
When a Search campaign runs Maximize Clicks, the ONLY pacing lever the client can adjust is the DAILY BUDGET; there is no manual bid up/down and the optional Max-CPC bid limit is NOT a lever to recommend either. Never write "raise the bid limit / ease daily caps," "bid up/down," or "lift Max CPC"; frame all headroom/pacing deployment as "increase the daily budget" and set the action-CSV recommendation type to `INCREASE_DAILY_BUDGET` (never `ADJUST_BID_UP` / `RAISE_BIDS_FOR_RANK`). Client quote: "we can only update daily budgets for pacing."

### 2026-05-07: The Bing "Total" footer row doubles click and impression aggregates
Microsoft Ads CSV exports (campaign performance and Search Term Report) append a `Month = "Total"` row whose Clicks and Impressions equal the sum of the monthly rows, so summing naively yields exactly double the real values (Spend is safe, it is "-" in that row). Always filter to rows where `Month` matches a date (for example starts with `2026-`) before summing. This was caught when a recompute reported 69,780 Bing clicks for an actual 34,890.

### 2026-04-30: Cumulative vs monthly, always request the Month breakdown
A cumulative export averages all months together and can mislead on direction, while the monthly file disambiguates in seconds. The [Account: HIS] April CTR drop looked like Syndicated share growing in the cumulative file, but the monthly file showed Syndicated share had been declining all quarter and the real cause was Syndicated quality collapsing month-over-month (CTR 10.31% to 6.85%). If only the cumulative is available, frame directional findings as hypotheses pending monthly data.

### 2026-04-30: Syndicated Search Partners default-on is a recurring auction-quality issue
When Bing CTR softens, check the network split (MS sites vs Syndicated) before blaming match type or creative. Exclude Syndicated on non-brand campaigns and pair it with prosumer-AI Phrase negatives on any Phrase keyword that triggers consumer queries (the "ai coding / ai notes" cluster is the canonical example).

### 2026-04-30: Pressure-test single-cause CTR framings (v3 after user pushback)
The user pushed back on a single-cause "Syndicated grew" framing; the verified diagnosis was multi-factor (Syndicated quality collapse, campaign mix shift, Bing-specific branded softening, and daily-cap pacing). Always cross-check (a) campaign mix, (b) within-campaign CTR per program, (c) top-keyword CTR deltas, and (d) the Google brand parallel before shipping a single-cause story.

### 2026-04-26: Bing often has no conversion tracking, and copy mirrors Google ([Account: HIS])
[Account: HIS] Bing had no conversion tracking installed, so all Bing optimization is click-volume weighted and every deck or report slide using conversion data must footer "Google yes / Bing no." Bing RSAs were pushed over from Google wholesale, so single-RSA and empty-display-path findings from the Google ad-copy audit apply to Bing too: fix on Google, mirror to Bing. Future Bing data requests only need the Search Query Report.

## Standing preferences (apply every run)

- **Cross-check Bing CTR softening against Google for the same window.** If Google brand volume and CTR are steady or up, the issue is Bing-specific (Microsoft auction, competitor brand-bidding, daily-cap pacing), not external demand.
- **Consider daily-budget pacing as a CTR-quality factor.** If campaign daily caps exhaust before end of day, delivery front-loads and the auction may shift to cheaper Syndicated inventory; verify Standard (not Accelerated) delivery and rebalance daily caps within the monthly cap.
- **Bing column names differ from Google** (`Impressions` not `Impr.`, `Spend` not `Cost`, `Campaign name` not `Campaign`); Bing also has Quality Score, Impression Share, and Abs. Top Impression Rate %.
- **Never fabricate campaign or ad-group labels** and **do not name "DataForSEO"** in output: the same standing rules as the Google search skill.
