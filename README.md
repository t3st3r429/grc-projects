# grc-projects

# GRC Portfolio

Hands-on cyber risk and GRC projects by **Geoffrey Chege**. Each one mirrors a task from a day in a cyber risk team: taking in exceptions, writing risk statements, keeping risk data clean, reporting to leadership and controlling access to the tooling.

> **Everything here uses fictional data.** The company is "Northwind Payments", which does not exist. Nothing comes from a client or employer.

| # | Project | What it shows |
|---|---|---|
| 01 | [Exception and acceptance tracker](01-exception-tracker/) | Full lifecycle from intake to closure, expiry flags, compensating-control checks (Excel) |
| 02 | [Findings to risk statements](02-risk-statements/) | Technical findings turned into likelihood, impact and a leadership summary |
| 03 | [Risk register with hygiene checks](03-risk-register-hygiene/) | 42-risk register mapped to NIST CSF and ISO 27001, plus a Python script that finds duplicates, stale records and orphans |
| 04 | [Cyber risk dashboard](04-dashboard/) | A one-page leadership view built from the data in 01 and 03 |
| 05 | [GRC platform access model](05-access-model/) | Least-privilege role matrix and rules for API and AI-tool integrations |

## Skills these projects demonstrate

Risk assessment and treatment, exception and risk acceptance management, remediation tracking, NIST CSF 2.0 and ISO 27001:2022 mapping, data quality, reporting, access control design, Python (standard library only), Excel formulas.

## Run it yourself

- Project 03: `python 03-risk-register-hygiene/hygiene_check.py --as-of 2026-11-17`
- Project 04: `python 04-dashboard/build_dashboard.py --as-of 2026-11-17`, then open `dashboard.html`
- No installs needed beyond Python 3.8+.

## Contact

Geoffrey Chege 
