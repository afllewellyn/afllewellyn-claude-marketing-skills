"""TypeSafe judgments for landing-page audit Gap A / Gap C.

Fetches the page with Firecrawl (scripts/firecrawl_fetch.py) and asks Jev
(scripts/jev_judge.py) one narrow question per judgment:
  - Gap C: Noul per keyword, "does the page address what this search is looking for?"
  - Gap A: Choice per ad claim, supported / contradicted / absent
Also prints a word-boundary literal-match baseline for each keyword.

Usage: python3 -I scripts/lp_judgments.py <page_url> --keywords k1,k2 --claims "c1|c2"
Key: TYPESAFE_API_KEY (environment, else gitignored .env); never printed.
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev_judge import MAX_STATE_CHARS, JevError, choice, have_key, judge, noul  # noqa: E402

CLAIM_LABELS = {
    "supported": "The page states the same fact or figure.",
    "contradicted": "The page states a different figure or fact on the same point.",
    "absent": "The page does not address this claim.",
}


def page_text(url):
    from firecrawl_fetch import fetch_page
    return fetch_page(url) or sys.exit(f"firecrawl returned nothing for {url}")


def literal_match(keyword, text):
    """True when every word of `keyword` appears in `text` on word boundaries."""
    low = text.lower()
    return all(re.search(r"\b" + re.escape(w) + r"\b", low) for w in keyword.lower().split())


def keyword_question(keyword):
    return noul(f'Does `landing_page_text` address what someone searching for "{keyword}" is '
                "looking for, including the product or topic named in that search?")


def claim_question(claim):
    return choice(f'Compare this ad claim to `landing_page_text`: "{claim}"', CLAIM_LABELS)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url")
    ap.add_argument("--keywords", default="", help="comma-separated keywords (Gap C)")
    ap.add_argument("--claims", default="", help="pipe-separated ad claims (Gap A)")
    a = ap.parse_args()
    kws = [k.strip() for k in a.keywords.split(",") if k.strip()]
    claims = [c.strip() for c in a.claims.split("|") if c.strip()]

    if (kws or claims) and not have_key():
        sys.exit("jev: TYPESAFE_API_KEY is not set; skipping before any Firecrawl credits are spent")
    text = page_text(a.url)
    print(f"page text: {len(text):,} chars (sending first {MAX_STATE_CHARS:,})")
    qs = {f"kw{i}": keyword_question(k) for i, k in enumerate(kws)}
    qs.update({f"claim{i}": claim_question(c) for i, c in enumerate(claims)})
    ans = {}
    if qs:
        try:
            ans = judge({"landing_page_text": text[:MAX_STATE_CHARS]}, qs)
        except JevError as exc:
            sys.exit(f"jev: {exc}")
    for i, k in enumerate(kws):
        n = (ans.get(f"kw{i}") or {}).get("noul")
        score = f"{n:.2f}" if isinstance(n, (int, float)) else "missing"
        print(f"[Gap C] {k!r}: noul={score}  literal_match={literal_match(k, text)}")
    for i, c in enumerate(claims):
        print(f"[Gap A] {c!r}:\n   {json.dumps(ans.get(f'claim{i}', 'missing'))}")


if __name__ == "__main__":
    main()
