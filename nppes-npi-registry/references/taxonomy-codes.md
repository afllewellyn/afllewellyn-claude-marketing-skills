# Taxonomy codes for common trade audiences

Starter table mapping trade audiences to NUCC Health Care Provider Taxonomy descriptions. Pass the description text to `--taxonomy`. The NPPES API matches on the description, not the code, so the code column is for cross-checking against other data.

Only entries marked "confirmed" are codes I am certain of. Anything marked "verify" must be checked against the current NUCC code set at https://nucc.org before you rely on it. NUCC revises the set twice a year.

| Audience | NUCC description (use in `--taxonomy`) | Code | Status |
|---|---|---|---|
| General dentist | Dentist (classification), General Practice (specialization) | 1223G0001X | confirmed |
| Dentist, any specialty | Dentist | none (classification level) | use the description only |
| Dental hygienist | Dental Hygienist | 124Q00000X | confirmed |
| Registered nurse | Registered Nurse | 163W00000X | confirmed |
| Perioperative nurse | Registered Nurse, Perioperative (specialization) | 163WP0200X | verify |
| General surgeon | Surgery (classification), Surgery (specialization) | 208600000X | verify |
| Pharmacist | Pharmacist | 183500000X | verify |
| Hospital organizations | General Acute Care Hospital | 282N00000X | verify |
| Clinic and group organizations | Clinic/Center | 261Q00000X | verify |

## Notes

- Hospital and clinic rows are organization taxonomies. Use them with `--entity org`.
- Health IT buyers (CIOs, informatics leads, revenue cycle staff) do not have their own taxonomy. Size that audience by counting hospitals and clinics in the target geography, then apply your own estimate of buyers per organization. Label it as an estimate.
- Individual specialties are often split into several sub-specialty codes. If a broad description undercounts, check the NUCC set for sub-specialties and add them up.
