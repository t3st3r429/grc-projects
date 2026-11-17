# Web portal risk statements: Northwind Payments (fictional)

**Scope:** customer portal, using OWASP Juice Shop as a stand-in. **Method:** findings scored 1-5 for likelihood and impact. High is 15+, Medium 8-14, Low 1-7. Existing controls below are assumptions for the scenario.

## Summary for leadership

Our customer portal has two weaknesses that could let an outsider read other customers' data or take over administrator functions. Both are quick to exploit and both are fixable within a month. We recommend fixing all five findings, starting with the three High items. None of them should be accepted as risk: the cost of fixing is small compared with the cost of a customer data incident for a payments business.

| # | Finding | Likelihood | Impact | Score | Rating | Treatment | Target |
|---|---|---|---|---|---|---|---|
| 1 | Login can be bypassed through injection | 4 | 5 | 20 | High | Mitigate | 14 days |
| 2 | Customers can view other customers' baskets | 4 | 4 | 16 | High | Mitigate | 30 days |
| 3 | Users can register themselves as administrators | 3 | 5 | 15 | High | Mitigate | 14 days |
| 4 | Confidential files exposed in a public directory | 4 | 3 | 12 | Medium | Mitigate | 30 days |
| 5 | Script injection through the search box | 3 | 3 | 9 | Medium | Mitigate | 60 days |

---

## Finding 1: Login can be bypassed through injection

**Technical finding.** The login form passes user input to the database without safe handling, so specially crafted input can sign an attacker in without a valid password.

**Risk statement.** Because login input is not handled safely, an attacker could sign in as any user, including an administrator. This could lead to exposure of customer data, fraudulent transactions and regulatory reporting obligations.

**Business impact.** Customer data breach, fraud losses, loss of payment partner trust, possible regulator notification.

**Existing controls (assumed).** A web application firewall in monitor-only mode. No secure coding standard enforced in code review.

**Why this score.** Likelihood 4: the weakness is well known and easy to test, and the portal is internet-facing. Impact 5: access to administrator accounts exposes all customer records.

**Recommendation.** Use parameterized queries for all database access. Add automated tests for injection to the build pipeline. Put the firewall into blocking mode for known injection patterns as a stopgap. Owner: Head of Engineering. Target: 14 days. Residual risk after fix: Low (1x5 = 5).

**Acceptance?** Not recommended. A fix is cheaper than the exposure.

---

## Finding 2: Customers can view other customers' baskets

**Technical finding.** The application checks that you are logged in but not that the basket you request belongs to you. Changing an identifier in the request returns another customer's data.

**Risk statement.** Because the application does not verify record ownership, any signed-in customer could read other customers' order data. This could lead to privacy breaches and loss of customer trust.

**Business impact.** Personal data exposure, complaints, potential data protection penalties.

**Existing controls (assumed).** Authentication is required. No ownership checks and no alerting on unusual access patterns.

**Why this score.** Likelihood 4: any customer can try it with a single changed value. Impact 4: personal data of many customers, but no direct financial access.

**Recommendation.** Enforce ownership checks on the server for every record request. Use non-guessable identifiers. Add alerts for one account requesting many different records. Owner: Head of Engineering. Target: 30 days. Residual: Low (1x4 = 4).

---

## Finding 3: Users can register themselves as administrators

**Technical finding.** The registration request accepts a role value supplied by the user, so a new account can be created with administrator rights.

**Risk statement.** Because the registration process trusts a role value sent by the user, anyone could create an administrator account. This could lead to full control over customer data and application settings.

**Business impact.** Complete loss of access control, data manipulation, fraud.

**Existing controls (assumed).** None specific. Administrator actions are not separately logged.

**Why this score.** Likelihood 3: it requires knowing the request structure, which is easy to find. Impact 5: full administrative control.

**Recommendation.** Ignore any role value from the client and assign roles only on the server. Review existing accounts for unexpected administrators. Log all administrator actions. Owner: Head of Engineering with IAM Lead. Target: 14 days. Residual: Low (1x5 = 5).

---

## Finding 4: Confidential files exposed in a public directory

**Technical finding.** A directory listing is publicly reachable and contains internal documents.

**Risk statement.** Because internal files are stored in a publicly reachable folder, anyone could download confidential company documents. This could lead to disclosure of business plans or credentials and give attackers material for follow-up attacks.

**Business impact.** Disclosure of internal information, reputational damage, reconnaissance for further attacks.

**Existing controls (assumed).** None. No periodic review of what is stored on the web server.

**Why this score.** Likelihood 4: directory listings are found by automated scanners. Impact 3: depends on the content, which here is internal but not customer data.

**Recommendation.** Disable directory listing. Move the files off the web server. Review what else is exposed. Add a quarterly check of public content. Owner: IT Ops Manager. Target: 30 days. Residual: Low (1x3 = 3).

---

## Finding 5: Script injection through the search box

**Technical finding.** Search input is displayed back to the user without being made safe, so a crafted link can run a script in the victim's browser.

**Risk statement.** Because search input is shown back without being sanitized, an attacker could craft a link that runs malicious script in a customer's browser. This could lead to session theft or fraudulent actions on a customer's behalf.

**Business impact.** Account takeover of individual customers, fraud, phishing that uses our own domain.

**Existing controls (assumed).** Session cookies lack the strictest protection flags. No Content Security Policy.

**Why this score.** Likelihood 3: the attacker must get a victim to click a link. Impact 3: affects individual accounts, not all data.

**Recommendation.** Encode output safely, add a Content Security Policy, and set protective cookie flags. Owner: Head of Engineering. Target: 60 days. Residual: Low (1x3 = 3).

---

*Residual scores assume fixes are verified by retest. Retest evidence should be attached before any finding is closed.*
