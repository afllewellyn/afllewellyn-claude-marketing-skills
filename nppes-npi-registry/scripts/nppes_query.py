#!/usr/bin/env python3
"""Query the public NPPES NPI Registry API (v2.1) for provider counts and lists.

No API key is needed. Network access to npiregistry.cms.hhs.gov is required.

Usage:
    python3 nppes_query.py --taxonomy "Dentist" --state VT,NH --count-only
    python3 nppes_query.py --taxonomy "Dental Hygienist" --state MN --city Duluth --out out.csv
    python3 nppes_query.py --taxonomy "General Acute Care Hospital" --state OH \
        --entity org --format json

Flags:
    --taxonomy      taxonomy description text (API field taxonomy_description)
    --state         two-letter state; repeat or comma-separate for several
    --city, --postal
    --entity        individual (NPI-1) or org (NPI-2); default both
    --limit-pages   max number of 200-record pages per query
    --count-only    print a count per state instead of records
    --format        csv (default) or json
    --out           output file; default stdout

Limits: the API returns at most 200 records per call and a skip of at most
1000, so one query reaches about 1,200 records. A query that hits that ceiling
returns a floor, not a total; split by state, city, or taxonomy.

Exit codes: 0 success, 1 network or API failure, 2 bad arguments.
"""
import argparse
import csv
import io
import json
import sys
import time

try:
    import requests
except ImportError:  # pragma: no cover
    sys.stderr.write("The 'requests' package is required: pip install requests\n")
    sys.exit(1)

API_URL = "https://npiregistry.cms.hhs.gov/api/?version=2.1"
PAGE_SIZE = 200
MAX_SKIP = 1000
CEILING = PAGE_SIZE + MAX_SKIP  # about 1,200 records per query
DELAY = 0.3
RETRIES = 4
TIMEOUT = 30


class QueryError(Exception):
    """Raised for network or API failures."""


def fetch_page(params, session_get=None):
    """GET one page, retrying on 429 and 5xx. Returns the decoded JSON dict."""
    get = session_get or requests.get
    last = "unknown error"
    for attempt in range(RETRIES):
        try:
            resp = get(API_URL, params=params, timeout=TIMEOUT)
        except requests.RequestException as exc:
            last = "network error: %s" % exc
        else:
            if resp.status_code == 429 or resp.status_code >= 500:
                last = "HTTP %s" % resp.status_code
            elif resp.status_code != 200:
                raise QueryError("HTTP %s from NPPES API" % resp.status_code)
            else:
                try:
                    data = resp.json()
                except ValueError:
                    raise QueryError("NPPES API returned non-JSON content")
                if isinstance(data, dict) and data.get("Errors"):
                    msgs = "; ".join(str(e.get("description", e)) for e in data["Errors"])
                    raise QueryError("NPPES API error: %s" % msgs)
                return data
        time.sleep(min(2 ** attempt, 8))
    raise QueryError("giving up after %d attempts (%s)" % (RETRIES, last))


def run_query(base, limit_pages=None, fetch=fetch_page, delay=DELAY):
    """Page through one query. Returns (records, capped).

    capped is True when the query reached the ~1,200 record ceiling and the
    last page was full, so more records may exist.
    """
    records = []
    capped = False
    skip = 0
    pages = 0
    while True:
        params = dict(base, limit=PAGE_SIZE, skip=skip)
        data = fetch(params)
        batch = data.get("results") or []
        records.extend(batch)
        pages += 1
        if len(batch) < PAGE_SIZE:
            break
        if limit_pages and pages >= limit_pages:
            break
        if skip >= MAX_SKIP:
            capped = True
            break
        skip += PAGE_SIZE
        time.sleep(delay)
    return records, capped


def flatten(rec):
    """Reduce an API record to a flat dict for CSV output."""
    basic = rec.get("basic", {}) or {}
    addrs = rec.get("addresses", []) or []
    loc = next((a for a in addrs if a.get("address_purpose") == "LOCATION"),
               addrs[0] if addrs else {})
    tax = next((t for t in rec.get("taxonomies", []) or [] if t.get("primary")),
               (rec.get("taxonomies") or [{}])[0])
    name = basic.get("organization_name") or " ".join(
        x for x in (basic.get("first_name"), basic.get("last_name")) if x)
    return {
        "npi": rec.get("number", ""),
        "type": rec.get("enumeration_type", ""),
        "name": name,
        "credential": basic.get("credential", ""),
        "taxonomy_code": tax.get("code", ""),
        "taxonomy": tax.get("desc", ""),
        "city": loc.get("city", ""),
        "state": loc.get("state", ""),
        "postal_code": loc.get("postal_code", ""),
    }


def split_states(values):
    out = []
    for v in values or []:
        out.extend(s.strip().upper() for s in v.split(",") if s.strip())
    return out


def build_base(args, state):
    base = {}
    if args.taxonomy:
        base["taxonomy_description"] = args.taxonomy
    if state:
        base["state"] = state
    if args.city:
        base["city"] = args.city
    if args.postal:
        base["postal_code"] = args.postal
    if args.entity:
        base["enumeration_type"] = "NPI-1" if args.entity == "individual" else "NPI-2"
    return base


def parse_args(argv):
    p = argparse.ArgumentParser(
        description="Query the NPPES NPI Registry for provider counts and lists.")
    p.add_argument("--taxonomy", help="taxonomy description text")
    p.add_argument("--state", action="append",
                   help="two-letter state; repeat or comma-separate")
    p.add_argument("--city")
    p.add_argument("--postal")
    p.add_argument("--entity", choices=["individual", "org"])
    p.add_argument("--limit-pages", type=int, dest="limit_pages")
    p.add_argument("--count-only", action="store_true", dest="count_only")
    p.add_argument("--format", choices=["csv", "json"], default="csv")
    p.add_argument("--out")
    args = p.parse_args(argv)
    if not (args.taxonomy or args.postal):
        p.error("give --taxonomy or --postal (the API rejects state-only or city-only searches); add --state/--city to narrow")
    return args


def main(argv=None, fetch=fetch_page, delay=DELAY):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    states = split_states(args.state) or [None]
    results = []  # (state, records, capped)
    try:
        for i, st in enumerate(states):
            if i:
                time.sleep(delay)
            recs, capped = run_query(build_base(args, st), args.limit_pages,
                                     fetch=fetch, delay=delay)
            results.append((st, recs, capped))
    except QueryError as exc:
        sys.stderr.write("Error: %s\n" % exc)
        return 1

    any_capped = False
    if args.count_only:
        rows = []
        for st, recs, capped in results:
            any_capped = any_capped or capped
            rows.append({"state": st or "ALL",
                         "count": len(recs),
                         "capped": "yes" if capped else "no"})
        text = render(rows, args.format)
    else:
        rows = []
        for st, recs, capped in results:
            any_capped = any_capped or capped
            rows.extend(flatten(r) for r in recs)
        text = render(rows, args.format)

    if any_capped:
        sys.stderr.write(
            "Warning: a query hit the ~%d record ceiling (200 per call, skip max "
            "%d). Counts are a floor. Split by state, city, or taxonomy.\n"
            % (CEILING, MAX_SKIP))
    try:
        if args.out:
            with open(args.out, "w", newline="", encoding="utf-8") as fh:
                fh.write(text)
        else:
            sys.stdout.write(text)
    except OSError as exc:
        sys.stderr.write("Error: cannot write output: %s\n" % exc)
        return 1
    return 0


def render(rows, fmt):
    if fmt == "json":
        return json.dumps(rows, indent=2) + "\n"
    if not rows:
        return ""
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


if __name__ == "__main__":
    sys.exit(main())
