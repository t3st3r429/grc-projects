# 04 · Cyber risk dashboard

**Problem:** Leadership wants to know where risk stands without reading a spreadsheet.

**What I built:** `build_dashboard.py` reads the register, issues and exceptions from projects 01 and 03 and produces `dashboard.html`: a single self-contained page with six headline numbers, four charts (risks by rating, issues by status, exceptions by expiry, risks by category) and a table of overdue issues. It works in light and dark mode.

**Run it:** `python build_dashboard.py --as-of 2026-11-17`, then open `dashboard.html`.

**Publish it:** In your GitHub repo go to Settings, Pages, deploy from the main branch, then open `/04-dashboard/dashboard.html`. Add a screenshot to this folder and link it above.

**Why one source of truth matters:** the dashboard has no numbers of its own. Fix a record in the register and the dashboard changes on the next run. That is the same reason GRC platforms exist.

**What I'd improve next:** trend lines (this month versus last month) and a section for control test results.
