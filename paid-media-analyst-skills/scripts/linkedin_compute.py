"""LinkedIn Campaign Manager export -> reconciled metrics JSON.

The deterministic layer under `prompts/linkedin/agent_1_campaign_analyst.md`: every
figure the agent reports comes from this file's output, never from ad-hoc parsing.

Export shape (every export seen so far): UTF-16, tab-delimited, ~5 preamble rows,
one row per ad per day. Level names follow Campaign Manager's current naming:
`Campaign Name` (the old campaign group) > `Ad Set Name` (the old campaign) > ad.

Rules encoded here, each from a past miss:
  * Every level is keyed by its ID (`Campaign ID`, `Ad Set ID`, `Ad ID`), never its name:
    two ads can share a name (one export had two ads named "Warmth Matters";
    keying by name showed 3 of 4), and ad set names repeat across campaigns (one program runs
    "Single Image Ads - Nurses" under two campaigns; keying by name merged their spend
    and paired it with one budget). Names are kept as labels.
  * `Impressions` is read by exact name. `Card Impressions` / `Viral Impressions`
    are different metrics and must never stand in for it.
  * Flight windows and pause state come from the export's own `Ad Set End Date` /
    `Campaign End Date` and `Ad Status`, not the IO.
  * `Reach` and `Average Frequency` are not additive across rows; they are reported
    per row-set only where the export carries them, never summed.
  * Rates are stored at full precision; round once, at render time.
  * `trend` compares periods over EQUAL numbers of days. `granularity` says what the export
    is: daily, weekly, monthly (rows dated at the period start) or aggregate (one to-date total
    per ad, no trend). Daily exports get ISO-week and calendar-month comparisons (newest
    period vs the adjacent prior, over the same number of in-flight days) plus optional
    `--compare-days N` trailing windows. Weekly/monthly exports cannot be sliced, so they are
    compared per day and by rate with `equal_days` false. For non-daily exports `date_range`
    comes from the flights and the report window, not the row dates. Periods clip to the
    flight start and end; a day a live flight delivered nothing counts as a zero day.

Usage:
    python scripts/linkedin_compute.py <export.csv> [-o metrics.json]
    python scripts/linkedin_compute.py <export.csv> -o - | ...   # JSON on stdout, summary on stderr
    python scripts/linkedin_compute.py <export.csv> -o data/processed/linkedin_acct_{end}.json
        # `{end}` becomes the last data day (YYYY-MM-DD), so one run computes and names the file
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_loaders import _decode, log_stream, num, read_linkedin_with_layout, write_json  # noqa: E402

# Additive metrics: output key -> exact export column.
METRICS = {
    "spend": "Total Spent",
    "impressions": "Impressions",
    "clicks": "Clicks",
    "lp_clicks": "Clicks to Landing Page",
    "engagements": "Total Engagements",
    "leads": "Leads",
    "lead_forms_opened": "Lead Forms Opened",
    "conversions": "Conversions",
    "video_views": "Video Views",
    "video_completions": "Video Completions",
}
REQUIRED = ("Ad ID", "Total Spent", "Impressions", "Clicks", "Start Date (in UTC)")


def rates(m: dict) -> dict:
    spend, impr, clicks = m["spend"], m["impressions"], m["clicks"]
    out = dict(m)
    out["ctr"] = clicks / impr if impr else 0.0
    out["cpc"] = spend / clicks if clicks else None
    out["cpm"] = spend / impr * 1000 if impr else None
    out["engagement_rate"] = m["engagements"] / impr if impr else 0.0
    if m.get("leads"):
        out["cpl"] = spend / m["leads"]
        out["lead_form_completion"] = m["leads"] / m["lead_forms_opened"] if m.get("lead_forms_opened") else None
    if m.get("video_views"):
        out["view_rate"] = m["video_views"] / impr if impr else 0.0
        out["completion_rate"] = m["video_completions"] / m["video_views"]
    return out


def detect_granularity(dates: set[date]) -> str:
    """daily | weekly | monthly | aggregate, from the spacing of the export's row dates.

    LinkedIn can export one row per ad per day, per week, per month, or a single row per ad
    covering the whole range (a to-date total, dated at the range start).
    """
    ds = sorted(dates)
    if len(ds) < 2:
        return "aggregate"
    gaps = [(y - x).days for x, y in zip(ds, ds[1:])]
    if sum(g == 1 for g in gaps) / len(gaps) >= 0.6:
        return "daily"
    if all(d.day == 1 for d in ds):
        return "monthly"
    if all(d.weekday() == 0 for d in ds) and all(g % 7 == 0 for g in gaps):
        return "weekly"
    return "daily" if len(ds) >= 4 else "aggregate"


def _span(a: date, b: date) -> list[date]:
    return [a + timedelta(days=i) for i in range((b - a).days + 1)]


def _sum(days: list[date], daily: dict[date, dict]) -> dict:
    tot = {k: 0.0 for k in METRICS}
    for d in days:  # a day the flight ran but delivered nothing has no row and counts as zeros
        for k, v in daily.get(d, {}).items():
            tot[k] += v
    return tot


def _summ(tot: dict, days: list[date]) -> dict:
    n = len(days)
    r = rates(tot)
    r.update(days=n, start=days[0].isoformat(), end=days[-1].isoformat(),
             spend_per_day=r["spend"] / n, impressions_per_day=r["impressions"] / n,
             clicks_per_day=r["clicks"] / n, leads_per_day=r["leads"] / n)
    return r


def _delta(cur: dict, prev: dict) -> dict:
    """Relative change (fraction) per metric; None when the prior value is zero or absent."""
    out = {}
    for k in ("spend_per_day", "impressions_per_day", "clicks_per_day", "ctr", "cpc", "cpm",
              "engagement_rate", "leads_per_day", "cpl", "view_rate"):
        a, b = cur.get(k), prev.get(k)
        out[k] = (a - b) / b if a is not None and b else None
    return out


def _comparison(cur_days, prior_days, daily, note=None) -> dict:
    """Compare two windows: equal length unless the export's own grain forbids slicing."""
    cur, prior = _summ(_sum(cur_days, daily), cur_days), _summ(_sum(prior_days, daily), prior_days)
    equal = len(cur_days) == len(prior_days)
    out = {"equal_days": equal, "days_compared": len(cur_days) if equal else [len(prior_days), len(cur_days)],
           "current": cur, "prior": prior, "delta": _delta(cur, prior)}
    if note:
        out["note"] = note
    return out


def _period_bounds(d: date, grain: str) -> tuple[date, date]:
    if grain == "week":
        start = d - timedelta(days=d.weekday())
        return start, start + timedelta(days=6)
    start = d.replace(day=1)
    nxt = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
    return start, nxt - timedelta(days=1)


def _period_row(daily, pstart, pend, covered_from, fs, fe, last_full) -> dict | None:
    eff_start = max(pstart, fs) if fs else pstart
    flight_pend = min(pend, fe) if fe else pend
    eff_end = min(flight_pend, last_full)
    if eff_end < eff_start:
        return None
    days = _span(eff_start, eff_end)
    r = _summ(_sum(days, daily), days)
    r.update(period_start=pstart.isoformat(), period_end=pend.isoformat(), days_in_flight=len(days),
             complete=eff_start >= covered_from and flight_pend <= last_full,
             open=eff_start >= covered_from and flight_pend > last_full)
    r["_days"] = days
    return r


def build_trend(daily: dict[date, dict], gran: str, covered_from: date, fs: date | None, fe: date | None,
                last: date, last_partial: bool, windows: tuple[int, ...] = ()) -> dict:
    """Period-over-period comparisons, over equal numbers of days wherever the grain allows.

    * daily export: ISO weeks (Mon-Sun) and calendar months. The newest period (complete, or
      open = still running) is compared with the adjacent prior period over the SAME number
      of in-flight days (the first n days of each, n = the shorter). Optional trailing
      `windows` (e.g. 5, 10) compare the last N complete days with the N before them.
    * weekly / monthly export: the export's own rows are the periods and cannot be sliced, so
      the comparison is per-day and rate based, with `equal_days` false when lengths differ.
    * aggregate export (one row per ad for the whole range): no trend.
    Periods clip to the flight start/end; days a flight ran with no row count as zero days;
    the partial last day is never used. A period is `complete` only when its in-flight days
    all fall inside the export's report window.
    """
    if gran == "aggregate":
        return {"available": False, "granularity": gran,
                "reason": "one total per ad for the whole range (to-date export); no period breakdown"}
    last_full = last - timedelta(days=1) if last_partial else last
    lo = fs or min(daily)
    grains = ("week", "month") if gran == "daily" else (("month",) if gran == "monthly" else ("week",))
    out: dict = {"available": True, "granularity": gran}
    for grain in grains:
        if gran == "daily":
            starts, cursor = [], _period_bounds(lo, grain)[0]
            while cursor <= last_full:
                starts.append(cursor)
                cursor = _period_bounds(cursor, grain)[1] + timedelta(days=1)
        else:
            starts = sorted({_period_bounds(d, grain)[0] for d in daily})
        rows = [r for st in starts if (r := _period_row(
            daily, st, _period_bounds(st, grain)[1], covered_from, fs, fe, last_full))]
        usable = [r for r in rows if r["complete"] or r["open"]]
        cmp_ = None
        if len(usable) >= 2 and usable[-2]["complete"]:
            cur, prev = usable[-1], usable[-2]
            if gran == "daily":
                n = min(len(cur["_days"]), len(prev["_days"]))
                cd, pd = cur["_days"][:n], prev["_days"][:n]
                note = (f"current period trimmed to its first {n} in-flight days to match the prior period"
                        if n < len(cur["_days"]) else None)
            else:
                cd, pd = cur["_days"], prev["_days"]
                note = (f"export is pre-aggregated by {grain}; per-day and rate comparison only, totals not compared"
                        if len(cd) != len(pd) else None)
            cmp_ = _comparison(cd, pd, daily, note)
            cmp_["periods"] = [prev["period_start"], cur["period_start"]]
        for r in rows:
            r.pop("_days")
        out[grain] = {"periods": rows, "complete_periods": sum(r["complete"] for r in rows), "comparison": cmp_}
    if gran == "daily":
        end = min(last_full, fe) if fe else last_full
        floor = max(covered_from, fs) if fs else covered_from
        out["windows"] = {}
        for n in windows:
            cur = _span(end - timedelta(days=n - 1), end)
            prior = [d - timedelta(days=n) for d in cur]
            out["windows"][str(n)] = (_comparison(cur, prior, daily) if prior[0] >= floor else
                                      {"available": False,
                                       "reason": f"fewer than {2 * n} in-flight days inside the export"})
    return out


def _add(bucket: dict, bucket_key, row_metrics: dict, **labels) -> None:
    entry = bucket.setdefault(bucket_key, {**labels, **{k: 0.0 for k in METRICS}})
    for k, v in row_metrics.items():
        entry[k] += v


def _finalize(bucket: dict, sort_by: str = "clicks") -> list[dict]:
    rows = [rates(v) for v in bucket.values()]
    return sorted(rows, key=lambda r: (-r[sort_by], str(r.get("name") or r.get("key") or "")))


LABEL_MAX = 36
TOP_ADS = 10
# Filename tokens that never tell two ads apart: job numbers, sizes, market/locale codes.
_NOISE_TOKEN = re.compile(r"^(\d{4,}|\d+x\d+|ms|mt|st|en|us|uk|rgb|a4|social)$", re.I)


def _words(name: str) -> tuple[list[str], str]:
    """Split a name into words and the joiner to rebuild it: spaced names split on
    whitespace (hyphenated words and lone ` - ` dividers handled), filenames on `-`/`_`."""
    if re.search(r"\s", name):
        return [w for w in name.split() if re.search(r"\w", w)], " "
    return [w for w in re.split(r"[-_]", name) if w], "-"


def ad_labels(ads: list[dict]) -> None:
    """Add a short, table-ready `label` to each ad, in place.

    Ad names are usually asset filenames
    (`brand-warmth-matters-social-ad-1080x1080-en`) and the
    headline is often identical across every ad, so the label comes from the name:
      1. Among the DISTINCT names longer than 24 characters (when there are at least 2),
         drop the leading and trailing words they ALL share (brand prefix, format
         suffix). Copies of one name therefore keep their whole name.
      2. Drop words that never tell ads apart: leading numbers and any number of 4+
         digits (job codes, asset IDs; a short `-1` version mark stays), sizes such as
         `1080x1080`, and locale/file codes (`ms`, `en`, `uk`, `rgb`, `a4`, `social`).
         If that leaves nothing (names that differ only by size), keep the words.
      3. Over 36 characters, cut whole words from the MIDDLE (`-…-`, or ` … ` for names
         with spaces), so words stay whole and a version suffix (`v2fv-1` vs `v2fv-2`)
         survives. Short names (`carmix`) stay as they are.
      4. A blank name falls back to the headline, then to `ad`.
      5. Two ads anywhere in the export with the same label get ` #` + the last 4
         digits of their Ad ID (more digits if those match), so a table row always
         points at one ad. An `ad` label always gets the suffix.
    """
    named = {}
    for a in ads:
        name = a["name"].strip()
        if len(name) > 24 and name not in named:
            named[name] = _words(name)
    head = tail = 0
    if len(named) >= 2:
        word_lists = [w for w, _ in named.values()]
        shortest = min(len(w) for w in word_lists)
        while head < shortest - 1 and len({w[head] for w in word_lists}) == 1:
            head += 1
        while (tail < shortest - head - 1
               and len({w[len(w) - 1 - tail] for w in word_lists}) == 1):
            tail += 1
    forced = set()
    for a in ads:
        name = a["name"].strip()
        if not name:
            name = " ".join((a.get("headline") or "").split())
            if not name:
                a["label"] = "ad"
                forced.add(a["ad_id"])
                continue
        elif len(name) > 24:
            words, joiner = named[name]
            if len(named) >= 2:
                words = words[head:len(words) - tail]
            kept = list(words)
            while kept and kept[0].isdigit():
                kept = kept[1:]
            kept = [w for w in kept if not _NOISE_TOKEN.match(w)]
            name = joiner.join(kept or words) or name
        a["label"] = _middle_cut(name)
        if not a["label"].strip("-_ "):
            a["label"] = "ad"
            forced.add(a["ad_id"])
    seen: dict[str, list] = {}
    for a in ads:
        seen.setdefault(a["label"], []).append(a)
    needs_id = [g for g in seen.values() if len(g) > 1 or g[0]["ad_id"] in forced]
    # Labels that stay as they are: a suffix must not land on one of them.
    taken = {g[0]["label"] for g in seen.values() if len(g) == 1 and g[0]["ad_id"] not in forced}
    for group in needs_id:
        # Last 4 digits, lengthened until they differ from each other and from any label
        # already in use (IDs can share an ending; a name can look like `ad #1234`).
        longest = max(len(a["ad_id"]) for a in group)
        n = 4
        while n < longest and (len({a["ad_id"][-n:] for a in group}) < len(group)
                               or any(f"{a['label']} #{a['ad_id'][-n:]}" in taken for a in group)):
            n += 1
        for a in group:
            a["label"] = f"{a['label']} #{a['ad_id'][-n:]}"
            taken.add(a["label"])


def _middle_cut(text: str, limit: int = LABEL_MAX) -> str:
    """Shorten from the middle on whole words: keep the last word (usually the version
    mark) and as many leading words as fit. A lone oversized word falls back to a
    character cut."""
    if len(text) <= limit:
        return text
    joiner = " " if " " in text else "-"
    marker = f"{joiner}…{joiner}"
    words = text.split(joiner)
    if len(words) > 1:
        head, tail = [], words[-1]
        for word in words[:-1]:
            if len(joiner.join(head + [word])) + len(marker) + len(tail) > limit:
                break
            head.append(word)
        if head:
            return joiner.join(head) + marker + tail
    keep_tail = (limit - 1) // 3
    return text[:limit - 1 - keep_tail].rstrip("-_ ") + "…" + text[-keep_tail:].lstrip("-_ ")


def _parse_mdy(text) -> date | None:
    try:
        return datetime.strptime(str(text).strip(), "%m/%d/%Y").date()
    except ValueError:
        return None


def read_preamble(path: Path) -> dict:
    """Report window and generation time from the export's preamble rows."""
    out = {}
    for line in _decode(path).splitlines()[:6]:
        m = re.match(r'"?(Report Start|Report End|Date Generated):\s*([^"\t]+)', line.strip())
        if m:
            try:
                out[m.group(1)] = datetime.strptime(m.group(2).strip(), "%B %d, %Y, %I:%M %p")
            except ValueError:
                out[m.group(1)] = None
    return {"report_start": out.get("Report Start"), "report_end": out.get("Report End"),
            "generated": out.get("Date Generated")}


def pacing(flight: dict, spent: float, last_day: date | None, last_day_partial: bool) -> dict | None:
    """Budget vs flight elapsed for one ad set. Elapsed counts whole days of data only.

    The flight runs Ad Set Start Date through Ad Set End Date inclusive. Days elapsed
    run from the start through the last COMPLETE day in the export: a final day the
    export was generated on is partial and excluded, so the run-rate is not understated.
    """
    budget = flight.get("budget")
    start, end = _parse_mdy(flight.get("start")), _parse_mdy(flight.get("end"))
    if not budget or not start or not end or not last_day:
        return None
    complete = last_day - timedelta(days=1) if last_day_partial else last_day
    days_total = (end - start).days + 1
    days_elapsed = max(0, min((complete - start).days + 1, days_total))
    days_left = days_total - days_elapsed
    remaining = budget - spent
    return {
        "budget": budget, "spent": spent, "pct_spent": spent / budget,
        "days_total": days_total, "days_elapsed": days_elapsed, "pct_elapsed": days_elapsed / days_total,
        "remaining": remaining, "days_left": days_left,
        "required_per_day": remaining / days_left if days_left else None,
        "elapsed_basis": f"{start.isoformat()} to {complete.isoformat()} (whole days of data)",
    }


def build(path: Path, windows: tuple[int, ...] = ()) -> dict:
    rows, encoding, header_idx = read_linkedin_with_layout(path)
    if not rows:
        raise SystemExit(f"{path}: no rows after the preamble")
    missing = [c for c in REQUIRED if c not in rows[0]]
    if missing:
        raise SystemExit(f"{path}: missing required columns {missing}")
    present = [k for k, col in METRICS.items() if col in rows[0]]

    total = {k: 0.0 for k in METRICS}
    campaigns, ad_sets, ads, days = {}, {}, {}, {}
    ad_status, ad_set_flight, campaign_end, campaign_budget = {}, {}, {}, {}
    ads_daily: dict[str, dict] = {}
    program_by_date: dict[date, dict] = {}
    ad_set_by_date: dict[str, dict[date, dict]] = {}
    skipped = 0
    for row in rows:
        if not str(row.get("Ad ID") or "").strip():
            skipped += 1  # spacer / footer rows carry no ad
            continue
        m = {k: num(row.get(col)) for k, col in METRICS.items() if col in row}
        for k, v in m.items():
            total[k] += v
        campaign = row.get("Campaign Name") or "Unknown"
        campaign_id = str(row.get("Campaign ID") or "").strip() or campaign
        ad_set = row.get("Ad Set Name") or "Unknown"
        ad_set_id = str(row.get("Ad Set ID") or "").strip() or f"{campaign_id}/{ad_set}"
        ad_id = str(row["Ad ID"]).strip()
        _add(campaigns, campaign_id, m, campaign_id=campaign_id, name=campaign)
        _add(ad_sets, ad_set_id, m, ad_set_id=ad_set_id, name=ad_set, campaign=campaign,
             campaign_id=campaign_id)
        _add(ads, ad_id, m, ad_id=ad_id, name=row.get("Ad Name") or "", ad_set=ad_set,
             ad_set_id=ad_set_id, campaign=campaign, format=row.get("Sponsored Update Type") or "",
             headline=row.get("Ad Headline") or "",
             intro_text=(row.get("Ad Introduction Text") or "")[:120])
        _add(ads_daily.setdefault(ad_id, {}), row["Start Date (in UTC)"], m, key=row["Start Date (in UTC)"])
        _add(days, row["Start Date (in UTC)"], m, key=row["Start Date (in UTC)"])
        day = _parse_mdy(row["Start Date (in UTC)"])
        if day:
            for target in (program_by_date, ad_set_by_date.setdefault(ad_set_id, {})):
                slot = target.setdefault(day, {k: 0.0 for k in METRICS})
                for k, v in m.items():
                    slot[k] += v
        if row.get("Ad Status"):
            ad_status[ad_id] = row["Ad Status"]
        ad_set_flight[ad_set_id] = {"name": ad_set, "campaign": campaign, "start": row.get("Ad Set Start Date"), "end": row.get("Ad Set End Date"),
                                 "status": row.get("Ad Set Status"),
                                 "budget": num(row.get("Total Budget")) or None,
                                 "daily_budget": num(row.get("Daily Budget")) or None}
        if num(row.get("Campaign Total Budget")):
            campaign_budget[campaign_id] = {"name": campaign, "budget": num(row["Campaign Total Budget"])}
        if row.get("Campaign End Date"):
            campaign_end[campaign_id] = {"name": campaign, "end": row["Campaign End Date"]}

    for ad_id, entry in ads.items():
        entry["status"] = ad_status.get(ad_id, "")
    ad_labels(list(ads.values()))
    names = {}
    for entry in ads.values():
        if entry["name"].strip():
            names.setdefault(entry["name"].strip(), []).append(entry["ad_id"])
    pre = read_preamble(path)
    data_days = sorted(filter(None, (_parse_mdy(d) for d in days)))
    gran = detect_granularity(set(data_days)) if data_days else "aggregate"
    starts = {k: _parse_mdy(f.get("start")) for k, f in ad_set_flight.items()}
    ends = {k: _parse_mdy(f.get("end")) for k, f in ad_set_flight.items()}
    first_day = data_days[0] if data_days else None
    last_day = data_days[-1] if data_days else None
    rs = pre["report_start"].date() if pre["report_start"] else None
    re_ = pre["report_end"].date() if pre["report_end"] else None
    if gran != "daily" and data_days:
        # Rows are dated at their period start (a month, a week, or the whole range), so the
        # covered range comes from the flights and the report window, not from the row dates.
        ks, ke = [d for d in starts.values() if d], [d for d in ends.values() if d]
        first_day = max(rs, min(ks)) if rs and ks else (min(ks) if ks else rs or first_day)
        last_day = min(re_, max(ke)) if re_ and ke else (max(ke) if ke else re_ or last_day)
    last_day_partial = bool(pre["generated"] and last_day and pre["generated"].date() == last_day)
    spent_by_ad_set = {k: v["spend"] for k, v in ad_sets.items()}
    ad_set_pacing = {}
    for k, f in ad_set_flight.items():
        pace = pacing(f, spent_by_ad_set.get(k, 0.0), last_day, last_day_partial)
        ad_set_pacing[k] = pace and {"name": f["name"], "campaign": f["campaign"], **pace}
    status_counts = {}
    for s in ad_status.values():
        status_counts[s] = status_counts.get(s, 0) + 1

    trend = None
    if data_days:
        covered_from = min(rs, first_day) if rs else first_day
        known, known_ends = [d for d in starts.values() if d], [d for d in ends.values() if d]
        fe_all = max(known_ends) if len(known_ends) == len(ends) else None
        trend = {"program": build_trend(program_by_date, gran, covered_from, min(known) if known else None,
                                        fe_all, last_day, last_day_partial, windows),
                 "ad_sets": {k: {"name": ad_set_flight[k]["name"], "campaign": ad_set_flight[k]["campaign"],
                                 **build_trend(v, gran, covered_from, starts.get(k), ends.get(k), last_day,
                                               last_day_partial, windows)}
                             for k, v in ad_set_by_date.items()}}

    return {
        "platform": "LinkedIn",
        "source_file": Path(path).name,
        "encoding": encoding,
        "header_row_index": header_idx,
        "row_count": len(rows),
        "skipped_rows": skipped,
        "currency": sorted({r.get("Currency") for r in rows if r.get("Currency")}),
        "metrics_present": present,
        "has_leads": total["leads"] > 0,
        "has_conversions": total["conversions"] > 0,
        "has_video": total["video_views"] > 0,
        "granularity": gran,
        "date_range": [first_day.isoformat(), last_day.isoformat()] if data_days else None,
        "report_window": {k: v.isoformat() if v else None for k, v in pre.items()},
        "last_day_partial": last_day_partial,
        "summary": rates(total),
        "campaigns": _finalize(campaigns),
        "ad_sets": _finalize(ad_sets),
        "ads": _finalize(ads),
        "daily": sorted((rates(v) for v in days.values()), key=lambda r: _date_key(r["key"])),
        "ads_daily": {ad: sorted((rates(v) for v in d.values()), key=lambda r: _date_key(r["key"]))
                      for ad, d in ads_daily.items()},
        "trend": trend,
        "ad_set_flight": ad_set_flight,
        "ad_set_pacing": ad_set_pacing,
        "campaign_budgets": campaign_budget,
        "campaign_end_dates": campaign_end,
        "ad_status_counts": status_counts,
        "duplicate_ad_names": {n: ids for n, ids in names.items() if len(ids) > 1},
    }


def _date_key(text: str):
    """M/D/YYYY -> (Y, M, D); anything else sorts as-is after real dates."""
    parts = str(text).split("/")
    if len(parts) == 3 and all(p.isdigit() for p in parts):
        return (0, int(parts[2]), int(parts[0]), int(parts[1]))
    return (1, str(text))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", type=Path)
    ap.add_argument("--compare-days", type=int, action="append", default=[], metavar="N",
                    help="also compare the last N complete days with the N days before (repeatable, "
                         "e.g. --compare-days 5 --compare-days 10); daily exports only")
    ap.add_argument("-o", "--out", help="write metrics JSON here; `-` writes it to stdout "
                                        "(the summary then goes to stderr); `{end}` in the path "
                                        "becomes the last data day, YYYY-MM-DD")
    args = ap.parse_args(argv)
    metrics = build(args.export, tuple(args.compare_days))
    log = log_stream(args.out)
    out = args.out
    if out and "{end}" in out:
        if not metrics["date_range"]:
            print("error: `{end}` in -o needs dated rows, and the export has none", file=sys.stderr)
            return 2
        out = out.replace("{end}", metrics["date_range"][1])
    s = metrics["summary"]
    print(f"{metrics['source_file']}: {metrics['date_range']} | ${s['spend']:,.2f} | "
          f"{s['impressions']:,.0f} impr | {s['clicks']:,.0f} clicks | CTR {s['ctr']:.2%} | "
          f"{len(metrics['ads'])} ads | leads {s['leads']:,.0f}", file=log)
    if metrics["duplicate_ad_names"]:
        dup = metrics["duplicate_ad_names"]
        print(f"  {len(dup)} ad name(s) shared by several Ad IDs, kept separate "
              f"({sum(len(v) for v in dup.values())} ads)", file=log)
    top = metrics["ads"][:TOP_ADS]
    width = max(len(a["label"]) for a in top) if top else 0
    for a in top:
        print(f"  {a['label']:<{width}} | {a['ad_set'][:30]:<30} | {a['clicks']:>6,.0f} clicks | "
              f"CTR {a['ctr']:.2%}", file=log)
    if len(metrics["ads"]) > TOP_ADS:
        print(f"  ... {len(metrics['ads']) - TOP_ADS} more ads in the JSON", file=log)
    written = write_json(metrics, out)
    if written:
        print(f"  wrote {written}", file=log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
