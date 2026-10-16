---
name: nppes-npi-registry
description: Count and list US healthcare providers from the public NPPES NPI Registry API, by taxonomy (specialty), state, city, or postal code. Use for audience sizing in trade media plans, sanity-checking a publisher's claimed reach, or pulling provider lists for a geography. Needs no API key, only network access to npiregistry.cms.hhs.gov.
---

# NPPES NPI Registry

Query the public NPPES NPI Registry to see how many registered US providers exist for a specialty and place. It gives a real-world denominator for audience claims. Pairs with `../healthcare-trade-media-planning/`, but works on its own.

## When to use

- Provider counts by specialty, state, city, or postal code.
- Audience sizing for a trade media plan (for example, general dentists in Texas).
- Sanity-checking a publisher's reach claim against the number of providers that exist.
- Pulling a provider list for one geography as CSV or JSON.

## How to run

The script is `scripts/nppes_query.py`. It needs Python 3 and `requests`.

```bash
# Count general dentists per state
python3 scripts/nppes_query.py --taxonomy "Dentist" --state VT,NH,ME --count-only

# List dental hygienists in one city as CSV
python3 scripts/nppes_query.py --taxonomy "Dental Hygienist" --state MN --city Duluth --out hygienists.csv

# Organizations only (NPI-2), JSON to stdout
python3 scripts/nppes_query.py --taxonomy "General Acute Care Hospital" --state OH --entity org --format json
```

Flags:

- `--taxonomy`: taxonomy description text, sent as the API field `taxonomy_description`. Use the descriptions in `references/taxonomy-codes.md`. The API matches on the text, so try the broad term first.
- `--state`: two-letter code. Repeat the flag or pass a comma list.
- `--city`, `--postal`: optional filters. Postal accepts a 5-digit ZIP.
- `--entity individual|org`: individual providers (NPI-1) or organizations (NPI-2). Default is both.
- `--limit-pages`: stop after this many 200-record pages.
- `--count-only`: report a count per state instead of records.
- `--format csv|json`, `--out path`: output format and file. Default is CSV to stdout.

`--taxonomy` or `--postal` is required. The API rejects searches that use only state or city, so add `--state` and `--city` to narrow a taxonomy search.

## Limits

The API returns at most 200 records per call and allows a skip of at most 1,000, so one query reaches about 1,200 records. When a query hits that ceiling the count is a floor, not a total, and the script says so. Split the query by state, then city, then taxonomy until each piece comes in under the ceiling, and add the pieces up.

## Caveats

- An NPI is a registered provider, not an active ad audience. Many registered providers are retired, not practicing, or not reachable in any trade publication.
- The data is a point-in-time snapshot of the live registry. Record the run date next to any number you quote.
- Individuals (NPI-1) and organizations (NPI-2) are separate counts. Do not add them together as people.
- A provider can list several taxonomies and several locations, so counts by taxonomy can overlap.
- The state filter matches a practice or mailing address on the record, not where the person works today.

## Network

The script needs outbound HTTPS to `npiregistry.cms.hhs.gov`. There is no API key. In a sandbox, add that host to the allowed domains. On a network failure the script prints a clear message to stderr and exits 1.

## Alternative for nationwide totals

CMS publishes a monthly NPPES bulk data file with every NPI. It is the better source for nationwide totals or counts that would need hundreds of split queries. It is large and is not bundled here.

## Reference files

- `references/taxonomy-codes.md`: starter table of common healthcare trade audiences mapped to NUCC taxonomy descriptions and codes.
