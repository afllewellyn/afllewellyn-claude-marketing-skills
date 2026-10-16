"""Self-contained regression tests for scripts/linkedin_compute.py (synthetic data).

The fixture writes a small UTF-16 tab-delimited export in Campaign Manager's shape:
a preamble, then one row per ad per day. Two ads deliberately share a name, and one
ad set name repeats under two campaigns, the two keying traps the script guards against.

Run from paid-media-analyst-skills/: `python -m pytest tests` or `python -m unittest discover tests`
"""

import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import linkedin_compute as lc  # noqa: E402

HEADER = ["Campaign Name", "Campaign ID", "Ad Set Name", "Ad Set ID", "Ad Name", "Ad ID",
          "Start Date (in UTC)", "Impressions", "Clicks", "Total Spent", "Leads",
          "Ad Set Start Date", "Ad Set End Date", "Total Budget", "Ad Status", "Currency"]

# (campaign, campaign_id, ad_set, ad_set_id, ad_name, ad_id, per-day (impr, clicks, spend, leads))
ADS = [
    ("Camp A", "C1", "Single Image - Nurses", "S1", "brand-alpha-ad-v1", "1001", (1000, 20, 50.0, 1)),
    ("Camp A", "C1", "Single Image - Nurses", "S1", "brand-alpha-ad-v1", "1002", (500, 5, 25.0, 0)),
    ("Camp B", "C2", "Single Image - Nurses", "S2", "brand-beta-ad-v1", "2001", (800, 8, 40.0, 0)),
]
DAYS = ["10/1/2026", "10/2/2026", "10/3/2026"]


def write_export(path):
    lines = ['"Report Start: October 1, 2026, 12:00 AM"',
             '"Report End: October 3, 2026, 12:00 AM"',
             '"Date Generated: October 5, 2026, 9:00 AM"', "", ""]
    lines.append("\t".join(HEADER))
    for day in DAYS:
        for camp, cid, aset, sid, name, ad_id, (impr, clk, spend, leads) in ADS:
            row = [camp, cid, aset, sid, name, ad_id, day, impr, clk, spend, leads,
                   "10/1/2026", "10/10/2026", "1000.00", "ACTIVE", "USD"]
            lines.append("\t".join(str(c) for c in row))
    Path(path).write_bytes(("\n".join(lines) + "\n").encode("utf-16"))


class SyntheticExportTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.path = Path(cls._tmp.name) / "export.csv"
        write_export(cls.path)
        cls.m = lc.build(cls.path)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_totals_reconcile(self):
        s = self.m["summary"]
        self.assertEqual(s["impressions"], 3 * (1000 + 500 + 800))
        self.assertEqual(s["clicks"], 3 * 33)
        self.assertAlmostEqual(s["spend"], 3 * 115.0, places=2)

    def test_ads_are_keyed_by_id_and_sum_to_total(self):
        self.assertEqual(len(self.m["ads"]), 3)
        self.assertEqual(sum(a["clicks"] for a in self.m["ads"]), self.m["summary"]["clicks"])
        self.assertAlmostEqual(sum(a["spend"] for a in self.m["ads"]), self.m["summary"]["spend"], places=2)

    def test_ads_sharing_a_name_stay_separate(self):
        self.assertEqual(sorted(sum(self.m["duplicate_ad_names"].values(), [])), ["1001", "1002"])
        labels = [a["label"] for a in self.m["ads"]]
        self.assertEqual(len(set(labels)), len(labels))

    def test_ad_set_names_reused_across_campaigns_stay_separate(self):
        nurses = [a for a in self.m["ad_sets"] if a["name"] == "Single Image - Nurses"]
        self.assertEqual(len(nurses), 2)
        for pace in self.m["ad_set_pacing"].values():
            self.assertLessEqual(pace["pct_spent"], 1.0001)

    def test_leads_detected_and_cpl_present(self):
        self.assertTrue(self.m["has_leads"])
        self.assertEqual(self.m["summary"]["leads"], 3)
        self.assertAlmostEqual(self.m["summary"]["cpl"], 345.0 / 3)

    def test_granularity_and_date_range(self):
        self.assertEqual(self.m["granularity"], "daily")
        self.assertEqual(self.m["date_range"], ["2026-10-01", "2026-10-03"])

    def test_per_ad_daily_rows_sum_to_each_ad(self):
        for ad in self.m["ads"]:
            self.assertEqual(sum(d["clicks"] for d in self.m["ads_daily"][ad["ad_id"]]), ad["clicks"])

    def test_missing_required_column_exits(self):
        bad = Path(self._tmp.name) / "bad.csv"
        bad.write_bytes("\n".join(["a", "b", "c", "d", "e", "Campaign Name\tAd ID", "x\t1"]).encode("utf-16"))
        with self.assertRaises(SystemExit):
            lc.build(bad)


class AdLabelTest(unittest.TestCase):

    def test_suffix_lengthens_when_ad_ids_share_their_last_four_digits(self):
        ads = [{"ad_id": "1551234", "name": "warmth", "ad_set_id": "A"},
               {"ad_id": "1561234", "name": "warmth", "ad_set_id": "A"}]
        lc.ad_labels(ads)
        self.assertEqual([a["label"] for a in ads], ["warmth #51234", "warmth #61234"])

    def test_blank_names_use_the_headline_then_get_an_id(self):
        ads = [{"ad_id": "1001", "name": "", "headline": "Keep patients warm", "ad_set_id": "A"},
               {"ad_id": "1002", "name": " ", "headline": "", "ad_set_id": "A"},
               {"ad_id": "1003", "name": "", "headline": "", "ad_set_id": "A"}]
        lc.ad_labels(ads)
        self.assertEqual([a["label"] for a in ads], ["Keep patients warm", "ad #1002", "ad #1003"])

    def test_single_blank_ad_still_gets_a_readable_label(self):
        ads = [{"ad_id": "9871", "name": "", "ad_set_id": "A"}]
        lc.ad_labels(ads)
        self.assertEqual(ads[0]["label"], "ad #9871")

    def test_labels_stay_unique_and_short(self):
        name = "2392362-05-brand-product-patient-transition-brochure-a4-rgb-en-uk-v1f"
        ads = [{"ad_id": "1", "name": name, "ad_set_id": "A"},
               {"ad_id": "2", "name": name, "ad_set_id": "A"}]
        lc.ad_labels(ads)
        labels = [a["label"] for a in ads]
        self.assertEqual(len(set(labels)), 2)
        for label in labels:
            self.assertLessEqual(len(re.sub(r" #\d+$", "", label)), lc.LABEL_MAX)

    def test_generated_suffix_never_lands_on_an_existing_label(self):
        ads = [{"ad_id": "1111234", "name": "warmth", "ad_set_id": "A"},
               {"ad_id": "2221235", "name": "warmth", "ad_set_id": "A"},
               {"ad_id": "5", "name": "warmth #1235", "ad_set_id": "A"},
               {"ad_id": "9991234", "name": "", "ad_set_id": "A"},
               {"ad_id": "7", "name": "ad #1234", "ad_set_id": "A"}]
        lc.ad_labels(ads)
        labels = [a["label"] for a in ads]
        self.assertEqual(len(set(labels)), len(labels), labels)

    def test_short_names_are_left_alone(self):
        ads = [{"ad_id": "1001", "name": "carmix", "ad_set_id": "A"},
               {"ad_id": "1002", "name": "admix", "ad_set_id": "A"}]
        lc.ad_labels(ads)
        self.assertEqual([a["label"] for a in ads], ["carmix", "admix"])


class DateKeyTest(unittest.TestCase):

    def test_month_day_year_sorts_chronologically(self):
        dates = ["9/2/2026", "10/1/2026", "6/26/2026"]
        self.assertEqual(sorted(dates, key=lc._date_key), ["6/26/2026", "9/2/2026", "10/1/2026"])


if __name__ == "__main__":
    unittest.main()
