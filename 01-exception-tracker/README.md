# 01 · Risk exception and acceptance tracker

**Problem:** Exceptions and risk acceptances are easy to approve and easy to forget. They expire quietly, the compensating controls drift, and nobody checks whether the original reason still holds.

**What I built:** An Excel tracker (`exception-tracker.xlsx`) with 15 fictional records that follow the full lifecycle: Intake, Assessment, Approved, Renewal Review, Closed.

- **Scoring:** likelihood x impact, with High / Medium / Low bands.
- **Expiry flags:** EXPIRED, due in 30, 60 or 90 days, calculated from an as-of date.
- **Control check:** flags any open exception whose compensating controls have not been verified, so nobody recommends renewal on trust.
- **Summary sheet:** counts by flag and severity, updated by formulas.
- `exceptions.csv` holds the same data for scripts. `procedure.md` documents the process and includes a 30-day outreach email.

**Where to look first:** the `Tracker` sheet, filtered on Flag = EXPIRED or Due in 30 days, then the Control Check column.

**What I'd improve next:** connect it to the risk register (project 03) so a closed risk automatically prompts closure of its exceptions.
