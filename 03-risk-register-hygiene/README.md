# 03 · Risk register with hygiene checks

**Problem:** Risk registers rot. Over time they collect duplicates, risks with no owner, reviews that never happen, and issues that point at nothing. Once people stop trusting the data, the dashboards built on it mean nothing.

**What I built:**
- `register.csv`: 42 fictional risks mapped to NIST CSF 2.0 and ISO 27001:2022 controls.
- `issues.csv`: 25 remediation issues linked to risks.
- `hygiene_check.py`: a script (standard library only) that checks the data and writes `hygiene_report.md`.

**What the script checks**

| Check | Rule |
|---|---|
| Possible duplicates | Same category and similar wording, with common synonyms normalised (for example "multi-factor authentication" and "MFA") |
| Missing owner | Risk has no named owner |
| Missing mapping | No NIST CSF or ISO 27001 control |
| Stale reviews | High risks not reviewed in 90 days, others in 180 days |
| Rating mismatch | Stored rating differs from likelihood x impact |
| Orphaned issues | Issue links to a blank or non-existent risk |
| Overdue issues | Open and past its due date |
| Closed risk, open issue | A risk was closed while work is still open |

I planted defects in the data on purpose (two duplicate pairs, one missing owner, one missing mapping, two wrong ratings, two orphans, a closed risk with an open issue) so the output shows what a clean-up looks like. The sample result is in `hygiene_report.md`: 19 findings across 8 checks.

**Run it:** `python hygiene_check.py --as-of 2026-11-17`

**Where to look first:** `hygiene_report.md`.

**What I'd improve next:** let the script write fixes back as a change list for the risk owner to approve, instead of only reporting.
