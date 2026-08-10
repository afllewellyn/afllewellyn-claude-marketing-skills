# Memory: qa-review

Lessons from past runs and user feedback for this skill. Read this file when the
skill is triggered and apply anything relevant before you start. If a run surfaces a
new skill-specific lesson or preference, add a dated entry at the top of the log,
2-3 sentences. CLAUDE.md "Session Learnings" stays the central system-of-record;
this file is the skill-scoped view.

## Log (newest first)

### 2026-07-14: Run an independent from-scratch recompute pass alongside qa-reviewer, not just once ([Account: VAC] EMEA)
Before treating a client-facing deck as done, run a second agent that recomputes every figure directly from the raw exports without trusting the prior build's numbers — distinct from `qa_lint`/`qa-reviewer`, which validate structure, tone, and reconciliation against the same already-computed figures and can miss a miscalculation both would otherwise wave through together. This session ran the two-agent gate (qa-reviewer + independent completeness/eval agent) twice — once mid-build and once as a final pass after further manual edits — and the second pass is what caught the footnote-migration issue below. Re-run review after any further edit, not just once per session.

### 2026-07-14: A footnote resolving a nit can fail to migrate when the user manually relocates the content it was attached to ([Account: VAC] EMEA)
When a user hand-restructures a deck locally and re-uploads it, re-verify that any prior fix (a clarifying footnote, a caveat) living on content that got moved actually moved WITH it. A footnote resolving a "these two numbers don't visibly sum" nit didn't survive the user's manual relocation of that bullet onto a new slide, silently reintroducing the same nit — caught only on the second qa-review pass, reinforcing why review must re-run after any post-QA edit, including user-side manual restructuring.

### 2026-07-09: Two pipeline bugs from one session — exact-term matching and round-once discipline ([Account: Dental] Q2)
A thematic/segment keyword filter built on a loose substring match (`flow` instead of the literal `flowable`) swept in unrelated ad copy and inflated a baseline metric ~10x; match on the literal, most-specific term when segmenting by theme. A double-rounding bug (round to 2 decimals in compute, then round again to 1 decimal at display) flipped two CTR values by a full digit; store full float precision through the pipeline and round exactly once, at render. When a bug like this is fixed in one output (report/CSV), verify the fix touches the actual shared compute function feeding the deck too — a standalone patch script can leave the deck's auto-generated card wrong even after the report and CSV are hand-corrected.

### 2026-07-09: A `[:N]` top-N slice can silently break a slide's own internal consistency ([Account: Dental] Q2)
When a table is built from a `[:N]` slice of a dict/list, verify N covers every item that the SAME slide's other claims (subtitle text, KPI cards, headline totals) depend on. A `[:8]` slice of a 9-item Meta campaign dict dropped a row representing 13 of the stated 32 leads while the slide's subtitle/KPI tile still cited the full 32-lead total — distinct from the intentional top-N-plus-Total-row pattern, where the Total legitimately exceeds the visible sum by design.

### 2026-07-09: Uncorroborated client-reported figures need a "per the client" label, not silent trust ([Account: Dental] Q2)
Check any client-relayed figure (a lead count, a result mentioned verbally) against the platform's own export before it ships. If it can't be corroborated in the raw data, it must read "per the client" everywhere it appears rather than being presented as independently verified — flag the instrumentation gap (pixel/CRM matchback) that would let it be verified going forward.

### 2026-07-09: Re-check a carried-forward slide/table against its own original source before shipping ([Account: Dental] Q2)
When content is pulled forward from a prior deck into a new deliverable's appendix, don't copy it verbatim — re-verify it against its original source material. A carried-forward keyword table blended in a cluster the source workbook had explicitly labeled "out of scope" (a separate product line meant for negative-listing), which would have inverted the recommendation if the reviewer hadn't caught it and added a caveat.

### 2026-07-09: Reconcile a corrected exhibit against EVERY slide that rolls up the same total, not just the one being fixed ([Account: Dental] Q2)
A Display ad-group slide was corrected to a partial-quarter export before the true full-quarter file arrived, but the same deck's Program Overview KPI card and Platform Performance Breakdown table had already folded the partial numbers into their totals ($50,559 total spend, 1.9% blended CTR). Fixing the one exhibit the user asked about left the deck internally inconsistent until the user separately asked "does everything still match up." Whenever a channel's data is corrected, search the whole deck (and every report/CSV) for every OTHER slide/table that sums or blends that channel, and recheck all of them in the same pass — don't wait for the user to notice a total is now stale.

### 2026-07-09: A channel export's OWN embedded date-range header + `Month` values are the source of truth for period coverage — never trust the filename or the deck's stated period ([Account: Dental] Q2)
A file named with "Q2" or living inside a "Q2 final" deck is not proof it covers the full quarter. Two Display exports were named `Apr-May24` and their own header row (`"April 1, 2026 - May 24, 2026"`) confirmed the partial window — but it took an explicit user assertion ("I gave you reports through June 30th") to trigger a full re-check of every file across both branches before finding the file was genuinely missing (not just unfound). When a client insists fuller data was supplied, exhaustively re-search before concluding it wasn't — but also don't fabricate coverage a file's own header doesn't support.

### 2026-07-09: Respect an explicit "don't edit this file" boundary even when a later message asks you to verify/reconcile it — offer a standalone corrected exhibit instead of copying-then-editing ([Account: Dental] Q2)
After the user said not to edit their uploaded final deck, a later request to "make sure totals match up" does not implicitly lift that boundary. Copying the file to a new path and applying the identical edit is a workaround, not compliance — it was (correctly) blocked by the auto-mode classifier a second time. Instead, rebuild only the specific slide(s) needing correction as a new standalone file that exactly matches the original's layout, fonts, and cell positions (read them off the original via python-pptx first), and hand it back for the user to swap in themselves.

### 2026-07-08: Hash-compare embedded deck images before trusting an adjacent caption ([Account: MedSurg])
When a slide has a screenshot left unchanged from a prior version, cross-check that any nearby text callout describing the same data doesn't quote numbers from a newer, different source (for example a later chat-pasted image) than what the screenshot actually shows. Hash-compare each embedded picture's before/after bytes to positively confirm which slide images actually changed this session before trusting or writing any caption. A [Account: MedSurg] deck's "top companies" callout stated a later chat-pasted image's numbers next to a screenshot correctly left unchanged; this qa-reviewer pass caught the mismatch as BLOCKING.

### 2026-07-08: Recompute a stated weighted-average metric under its claimed method, don't eyeball it ([Account: MedSurg])
A report's program-level Abs Top% didn't reproduce under either impression- or click-weighting when checked exactly; recomputing click-weighted (matching the report's own approach elsewhere) fixed the figure. When two tables in the same report show the same metric on different weighting bases (here, a Campaign scorecard table using impression-weighted-per-campaign versus the program rollup's click-weighted), footnote both explicitly rather than letting the reader assume one basis applies throughout.

### 2026-07-08: A combined top-N table must be re-ranked from the full union, not concatenated per-segment ([Account: MedSurg])
A "top-10 ad groups by clicks" table hand-assembled by concatenating two per-program top-5 lists silently dropped a real 9th-place ad group (237 clicks) while keeping a lower-ranked row (211 clicks) that only made a per-program list. Always compute the ranking from the full combined row set, then take the top N; never concatenate or truncate per-segment top-N lists.

### 2026-07-08: Re-verify a qa-review fix didn't introduce its own regression ([Account: MedSurg])
A methodology-caveat sentence added to fix one finding pushed an already-near-capacity PPT card's body text past its shape bounds into the shape above (no autofit, so the overflow was silent, not clipped). Caught only because a second, targeted qa-reviewer pass specifically re-verified the prior round's fixes instead of assuming they were clean. Do a rough char-count-vs-usable-area check before adding text to an existing fixed-size card, and treat "verify the fix" as its own review step whenever a text edit is made in response to a finding.

### 2026-07-08: Spot-check the actual keyword-count numbers in change-history claims, not just the cited examples ([Account: MedTech] Q2)
A report can cite real, verifiable example keywords for a change-history event while still understating its true scope by 10x if the writer sampled examples instead of tallying every matching row's embedded count ([Account: MedTech] Q2: 6 cited examples vs. the true 62 keywords across 23 ad-group actions in 9 campaigns). When reviewing a change-history-derived claim, sum the keyword-count field across ALL matching rows for the cited date/event, not just spot-check the named examples.

### 2026-06-24: `chart-pct-format` has an inverse FALSE POSITIVE — sub-1% display CTRs in percentage-point space ([Account: IWFB]/TF)
The guard flagged the committed [Account: IWFB]/TF deck's slide-6 CTR bars, but those values (0.0637, 0.0239…) are **percentage-points**, not fractions — [DSP Platform] DISPLAY CTRs genuinely in the 0.01–0.06% range (Wine 0.063%, Ind. Water 0.024%→0.029%, matching the 2026-06-16 run log), correctly rendered by the literal `0.000"%"`. Converting them to the true `%` operator would render them 100× too HIGH. The guard cannot tell a sub-1% fraction from a sub-1% percentage-point value, so when it fires on a chart you believe is display CTRs, **cross-check the cached values against the source run-log numbers before "fixing"** — a literal-`"%"` flag is correct for a pp-space sub-1% rate. **To silence it WITHOUT changing the display: ÷100 the stored values (pp → fraction) AND set the true `%` operator together** (`0.000%`, 3 decimals for sub-0.1% CTRs) on the data labels, numCache and axis — never flip the format alone. The [Account: IWFB]/TF slide-6 chart was resolved this way (verified the six labels render identically: 0.064% / 0.008% / 0.024% / 0.063% / 0.013% / 0.029%). (Corrects the prior entry's claim that this was "the same latent bug.")

### 2026-06-24: Percent-format trap — never format a FRACTION with a literal `0.0"%"` ([Product Line A] EMEA v4)
CTR labels on the creative charts rendered ~100x too small because the line series stored fractions (0.0167) but used a literal quoted `0.0"%"` formatCode — a quoted `"%"` is a literal character, not the percent operator, so PowerPoint does not multiply by 100. Fix: use the true percent operator `0.0%`/`0.00%` (`sourceLinked=0`) on fraction values, OR percentage-point values (1.67) with the literal `0.0"%"` — pick ONE convention per chart and make the data-label numFmt, the secondary-axis numFmt, and the val numCache formatCode all agree; also relax any secondary-axis `max` that floors the line. **This supersedes the "feed CTR in the SAME value-space (fractions) with `0.0"%"`" line in the v3 combo-chart entry below — that exact combination IS the bug.** Now caught deterministically by `scripts/qa_lint.py` (`chart-pct-format`: a percent series with a literal-`"%"` formatCode on sub-1.0 values). It also fired on the committed [Account: IWFB]/TF deck's slide-6 CTR bars — but that one is a FALSE POSITIVE (see the entry above): those are display CTRs in percentage-point space, correctly formatted. Always re-run `qa_lint` after any chart edit, and cross-check a sub-1% flag against the source before treating it as a bug.

### 2026-06-24: Update a committed deck in place; never rebuild it ([Product Line A] EMEA v3)
When revising a deck that is already committed, UPDATE it: reorder and insert slides and edit tables, never regenerate from scratch (strong user preference). To reorder/insert, append the new slides then permute `prs.slides._sldIdLst` (appending an existing `<p:sldId>` MOVES it, so no delete+re-add, which avoids duplicate-partname corruption); map slide to sldId via `prs.part.related_part(rId)` vs `slide.part.partname`. Re-open and assert the title order plus `zipfile.testzip()` after saving.

### 2026-06-24: Add Total rows to per-market/audience exec tables ([Product Line A] EMEA v3)
User wants a Total row on every per-market and audience table in exec decks (Account Overview and Geo already had them; per-platform-market and Audience did not). Append one by `deepcopy`-ing the last `<a:tr>` into `tbl._tbl`, re-applying `style_table_cell` (setting `cell.text` wipes run formatting), then compressing all row heights to `frame_cy // nrows` to keep the original footprint. For a top-N table the Total is the platform total (greater than the visible sum) and must match Account-Overview/report; add a header note like "Top 8 of 13 markets (Total = platform)" so it is not misread.

### 2026-06-24: Reuse the combo chart by replacing the whole plotArea from a templated XML ([Product Line A] EMEA v3)
Faster reusable build for the link-clicks-bars + CTR-line combo: `add_chart(COLUMN_CLUSTERED, 2 series)` then replace the entire `<c:plotArea>` with a templated XML string copied off an existing working combo chart (`chartEl.replace(old, parse_xml(...))` + `new_pa.addnext(legend)`); keep `<c:externalData r:id="rId1">`. Feed CTR in the SAME value-space and formatCode as the reference chart so it renders identically (extends the relocate-`ser` technique). Front-load the Geo Performance slide near position 4 (right after Account Overview), not buried near the end; replicate the combo chart per platform with screenshot-placeholder slides after Meta/LinkedIn/TikTok; keep the TikTok combo even with only 2 creatives (compute CTR from impressions); add a separate Gantt flight/pacing slide alongside the pacing table (compare-both), do not replace the table.

### 2026-06-23: Trust platform in-flight reporting over IO dates for flight windows ([Product Line A] EMEA)
Use the platform's own in-platform fields for flight windows and pause status, not the IO/plan line items (they can disagree). For LinkedIn read `Campaign End Date` + `Ad Status` (Active/Paused). A campaign can be 99.5% budget-exhausted yet still inside its flight window, so frame it "spent out, in flight," not "finished."

### 2026-06-23: Dual-axis link-clicks-bars + CTR-line combo chart in python-pptx
Build it by relocating the 2nd `<c:ser>` from `<c:barChart>` into a new `<c:lineChart>` on a secondary value axis (`axPos=r`) plus a deleted secondary `<c:catAx>`; wire the lineChart's two `axId`s to them. Escape numFmt formatCode quotes (`0.0"%"`) to `&quot;` when injecting via `parse_xml`. This is the chart the standing "clicks with strong CTRs" preference calls for; reusable helper built at `/tmp/ppe/combo.py` this session.

### 2026-06-22: Paid-social export quirks and cross-platform geo normalization ([Product Line A] EMEA)
TikTok Ads exports carry a `Total of N results` footer row to filter (same doubling-trap class as the Bing Total row), and a TikTok pull can come back single-day, so re-request the date range. LinkedIn Campaign Manager exports are UTF-16 LE with about 5 preamble rows, tab-delimited, about 110 columns, geo in `Campaign Name`. Normalize geo names across platforms ("France- Meta", "Spain - Medical" with no "Ads", "Netherland", "Switzerland (French)" vs "(FR)") before any cross-platform geo rollup.

### 2026-06-22: First 3-platform paid-social blended deck on MSD master ([Product Line A] EMEA)
The [Product Line A] "Personalized Precision" deck blended Meta + LinkedIn + TikTok (all USD) into an 11-slide [Client] MSD-master deck via `scripts/ppt_helpers.py`; [Account: MedSurg] uses the MSD master. qa_lint caught one "wasted" forbidden token in the actions CSV (reframe to efficiency). User arc preference: what ran and performance vs plan, then the insight that drove a pause, then next steps; condense many geos into a single cross-platform table with no per-country slides; primary deliverable is the [Client]-template PPT.

### 2026-06-21: For sparse-conversion accounts, reconcile narrative against Salesforce, not Google conversions ([Account: MOEM])
For sparse-conversion accounts the client Salesforce export is the lead source of truth ([Account: MOEM]: 25 SF leads vs 6 Google conv this period). Reconcile the narrative against SF, not the Google conversion count, and frame the story as demand-capture. Do not flag the narrative for "ignoring" the low Google conversion count when SF is the authoritative lead source.

### 2026-06-16: Replace a mid-deck slide in place, never delete+add
python-pptx delete-slide + add-slide can produce a DUPLICATE slide partname (e.g. slide8.xml) that corrupts the file (zip "Duplicate name" warning on save). To replace a mid-deck slide's content, edit it IN PLACE: keep the title placeholder, remove the other shapes via `sh._element.getparent().remove(sh._element)`, then rebuild.

### 2026-06-16: A [Acquiring Co] brand template exists; qa_lint forbidden-hex is [Client]-only
A [Acquiring Co] template now exists at `templates/acquiring_co_template.pptx` (red #E71315, indigo #262160, cyan #9AD3DC, gold #F0B234, orange #EA7600, near-black #222222; Arial; 17 layouts). Both templates are kept ([Client] teal `report_template.pptx` + TF) and chosen per team. qa_lint's forbidden-hex checks are [Client]-specific, so do not flag TF red/indigo/orange as violations when the deck is intentionally Thermo-Fisher-branded.

### 2026-06-16: XML-escape quotes when injecting a numFmt into chart XML
When injecting a numFmt formatCode that contains quotes (e.g. `0.0"%"`) into chart XML via `parse_xml` for a dual-axis combo chart, XML-escape the quotes to `&quot;` first or lxml raises an attribute construct error. This applies to the data-label number formats the standing preference already calls for.

### 2026-06-01: Report .md headers need an explicit Agent/spec attribution line
The first live `/qa-review` flagged report headers that had a data-source line but no agent attribution, so add an `**Agent:** Agent N <name> (prompts/<platform>/<spec>.md)` line to every report header. A card-format [Client]-teal deck built from `scripts/ppt_helpers.py` cleared the mechanical linter; only the report headers drew the nit.

### 2026-05-07: Reconcile totals against the performance export, filtering the Bing Total row
Filter the Bing `Month = "Total"` footer row before summing, since it doubles clicks and impressions. A report figure higher than the Search Terms Report sum is expected (the ST report undercounts), so reconcile against the campaign-performance export before flagging a mismatch; flag only a figure that matches no performance export.

### 2026-05-06: Never fabricate campaign or ad-group display labels ([Account: HIS] Q1 decks)
Use only names that exist in the platform export; do not invent contrast suffixes like "(Manual)" to pair with a real "(Auto)" sibling. A prior deck's invented "(Manual)" label matched an old paused campaign and briefly worried the client on the call. Cross-check every display label against the live campaign-name list before introducing it.

## Standing preferences (apply every run)

- **Forbidden tokens:** hex `#003DA5` (electric blue) and `#FF6B35` (alert orange); accent green `#05DD4D` used as a fill (it is a 1-pt rule only); and the words "waste" and "consider" in deliverables.
- **Never blend CAD and USD** in any total; always add a per-table conversion footnote.
- **Single-RSA and empty-display-path** are appendix items, not exec-deck findings, unless there is a structural blocker.
- **Judge ads/campaigns by clicks with strong CTRs, not spend.** Do not build spend-only bar charts unless the user asks. Put link clicks on every table and chart. For the "full metrics" visual use a single account-overview-by-channel table (one row per channel + total: spend/impr/clicks/CTR/CPC/CPM); on other slides lean on rich tables plus a few select dual-axis link-clicks-bars + CTR-line combo charts, not spend bars.
- **Chart data labels:** set `number_format` by context (IS/CTR `0.0"%"`, CPC `$#,##0.00`, spend `$#,##0`, conversions/clicks/impressions `#,##0`); detect by value range, not series name alone.
- **Advisory, not blocking.** Surface findings; the curator proposes CLAUDE.md edits and the user confirms before applying.
