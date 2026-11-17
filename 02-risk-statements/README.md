# 02 · From technical finding to risk statement

**Problem:** Pentest reports describe vulnerabilities. Leadership needs to know what could happen to the business, how likely it is, and what to do about it.

**What I built:** `risk-statements.md` takes five common web application findings and turns each into a risk statement, a score, a treatment decision and a recommendation, plus a one-page summary for leadership.

**The lab:** OWASP Juice Shop, a deliberately vulnerable app that anyone can run locally (`docker run -p 3000:3000 bkimminich/juice-shop`). I treat it as the stand-in for the customer portal of the fictional Northwind Payments.

**Before you publish this:** reproduce each finding yourself in your own Juice Shop instance and drop a screenshot into an `evidence/` folder. Screenshots turn this from a write-up into proof of work. Only the findings you have personally reproduced should stay in.

**Where to look first:** the summary table at the top, then Finding 1.
