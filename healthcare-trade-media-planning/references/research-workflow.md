# Research workflow: inputs, search queries, output format, rep checklist, data schema

_Use when researching a NEW publication or building a fresh plan from scratch._

## 1. Inputs the skill should ask for

When starting a new research request, ask for these fields. If the user does not know, infer from product and business group.

```yaml
business_group: Dental | Health Information Systems | Medical Surgical | Purification & Filtration | Other
product_or_solution:
product_aliases:
region: United States | Canada | North America | EMEA | APAC | Global
primary_audience:
  - clinicians
  - specialists
  - nurses
  - perioperative leaders
  - infection preventionists
  - dental practice owners
  - dental hygienists
  - revenue cycle leaders
  - CIO / CMIO / health IT executives
  - supply chain / value analysis
campaign_goal:
  - awareness
  - qualified traffic
  - lead generation
  - webinar / education
  - sample request / demo
  - event alignment
preferred_channels:
  - newsletter
  - display banner
  - sponsored article
  - webinar
  - CE/CME/CNE
  - podcast
  - social post
  - print
budget:
timing:
exclusions:
```

---


## 5. Search query templates

Use these exact searches first:

```text
[publication name] 2026 media kit advertising
[publication name] advertise media kit contact
[publisher name] marketing solutions [audience]
[association name] sponsorship advertising media kit 2026
[product category] trade publication media kit 2026
[region] [specialty] journal advertising media kit
```

Business-group-specific templates:

```text
Dental:
2026 dental media kit restorative dentistry newsletter advertising
2026 dental hygiene media kit RDH prevention advertising
2026 dental CE sponsorship media kit general dentists
Dental Tribune International Media Kit 2026
BDJ In Practice advertising media kit

Health Information Systems:
healthcare IT media kit 2026 CIO advertising
revenue cycle media kit 2026 healthcare finance
HIMSS Media marketing solutions Healthcare IT News media kit
Becker's Healthcare request media kit health IT revenue cycle
HFMA hfm media kit revenue cycle 2026
HBMA 2026 media kit RCM Advisor

Medical Surgical:
critical care nursing media kit 2026 AACN CriticalCare Newsline advertising
perioperative nursing media kit 2026 AORN advertising
Periop Leader Network Product Spotlight OR Manager media kit
anesthesiology media kit 2026 ASA Monitor Anesthesiology News
CRNA media kit 2026 AANA Journal advertising
Beyond the Mask podcast sponsorship CRNA
infection prevention media kit 2026 APIC Infection Control Today
wound care media kit 2026 WoundSource HMP
Healthcare Purchasing News 2026 media kit supply chain
ORNAC Journal advertising rates eblast web ad

Biopharma / Purification & Filtration:
BioProcess International media kit 2026 sponsorship Informa Connect
European Pharmaceutical Manufacturer EPM media pack advertise Rapid News
Fierce Biotech advertise media kit Questex life sciences
BioPharma Dive advertise media kit Industry Dive
bioprocessing downstream purification media kit lead generation
GEN Genetic Engineering Biotechnology News media kit webinar
BioPharm International media kit MJH Life Sciences
Bioprocess Online VertMarkets content syndication lead gen
```

---

## 6. Output format for publication research

Every research output should use this format:

```markdown
# Publication Research: [Business Group] — [Product] — [Region]

## Recommended shortlist
| Rank | Publication | Fit | Audience | Recommended channel | Why it fits | Contact / media kit | Unknowns |
|---:|---|---|---|---|---|---|---|

## Exclusions / deprioritized
| Publication | Reason |
|---|---|

## Outreach draft notes
- Product claim guardrails:
- Audience hypothesis:
- Recommended ask to rep:
- Specs to request:
- Minimums to request:
- Added-value asks:

## Open questions
1.
2.
3.
```

---

## 7. Rep outreach checklist

Ask reps for:

1. 2026 media kit and rate card.
2. Net rates, minimums, and agency commission policy.
3. Newsletter list size, average open rate, CTR benchmarks, and segmentation options.
4. Web display placements, SOV, impressions, refresh policy, accepted tags, and viewability reporting.
5. Sponsored content process: editorial review, labeling, word count, revision rounds, and whether assets are gated.
6. Lead-gen rules: required fields, CPL, MQL definition, dedupe, delivery cadence, and consent language.
7. Healthcare/pharma/med device claim review process.
8. Competitive separation and category exclusivity.
9. Added value: social amplification, article inclusion in newsletters, bonus impressions, ROS banners, podcast mentions.
10. Reporting cadence and final proof of performance.

---


## 9. Data capture schema

Use this schema when building a publication database:

```yaml
publication_name:
publisher_or_association:
region:
business_group_fit:
product_fit:
audience:
channels:
media_kit_year:
media_kit_url:
advertise_url:
contact_name:
contact_role:
contact_email:
contact_phone:
known_rates:
known_minimums:
specs:
lead_gen_available:
newsletter_available:
web_display_available:
sponsored_content_available:
webinar_or_ce_available:
notes:
last_verified_date:
source_quality: official_media_kit | official_advertise_page | publisher_page | third_party | stale
```

---

