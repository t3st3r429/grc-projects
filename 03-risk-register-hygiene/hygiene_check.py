#!/usr/bin/env python3
"""Risk register data-hygiene checker.

Reads register.csv and issues.csv (same folder by default) and reports:
duplicates, missing owners, missing framework mappings, stale reviews,
rating mismatches, orphaned issues, overdue issues, and closed risks with open issues.

Usage:  python hygiene_check.py [--as-of YYYY-MM-DD] [--out hygiene_report.md]
Uses only the Python standard library.
"""
import argparse, csv, datetime as dt, os, re
from difflib import SequenceMatcher

HERE = os.path.dirname(os.path.abspath(__file__))
STOP = {"a","an","the","on","in","of","to","for","by","and","or","with","without","at","not","no","than","from"}

def band(l, i):
    s = int(l) * int(i)
    return "High" if s >= 15 else "Medium" if s >= 8 else "Low"

SYNONYMS = {"multi-factor authentication": "mfa", "multifactor authentication": "mfa", "two-factor authentication": "mfa", "2fa": "mfa"}

def norm(title):
    t = title.lower()
    for k, v in SYNONYMS.items():
        t = t.replace(k, v)
    return t

def tokens(title):
    return {w for w in re.findall(r"[a-z0-9]+", norm(title)) if w not in STOP}

def load(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--register", default=os.path.join(HERE, "register.csv"))
    ap.add_argument("--issues", default=os.path.join(HERE, "issues.csv"))
    ap.add_argument("--as-of", default=dt.date.today().isoformat())
    ap.add_argument("--out", default=os.path.join(HERE, "hygiene_report.md"))
    a = ap.parse_args()
    asof = dt.date.fromisoformat(a.as_of)
    risks, issues = load(a.register), load(a.issues)
    ids = {r["risk_id"] for r in risks}
    findings = {}

    # 1. possible duplicates (same category, similar wording)
    dup = []
    for i, x in enumerate(risks):
        for y in risks[i+1:]:
            if x["category"] != y["category"]:
                continue
            ratio = SequenceMatcher(None, norm(x["title"]), norm(y["title"])).ratio()
            tx, ty = tokens(x["title"]), tokens(y["title"])
            jac = len(tx & ty) / max(1, len(tx | ty))
            if ratio >= 0.8 or jac >= 0.5:
                dup.append(f'{x["risk_id"]} and {y["risk_id"]}: "{x["title"]}" / "{y["title"]}"')
    findings["Possible duplicate risks"] = dup

    # 2. missing owner, 3. missing control mapping
    findings["Risks with no owner"] = [f'{r["risk_id"]}: {r["title"]}' for r in risks if not r["owner"].strip()]
    findings["Risks with no NIST CSF / ISO 27001 mapping"] = [
        f'{r["risk_id"]}: {r["title"]} (NIST: {r["nist_csf"] or "-"}, ISO: {r["iso27001"] or "-"})'
        for r in risks if not r["nist_csf"].strip() or not r["iso27001"].strip()]

    # 4. stale reviews (High: 90 days, others: 180 days)
    stale = []
    for r in risks:
        if r["status"] == "Closed":
            continue
        age = (asof - dt.date.fromisoformat(r["last_reviewed"])).days
        limit = 90 if band(r["likelihood"], r["impact"]) == "High" else 180
        if age > limit:
            stale.append(f'{r["risk_id"]}: {r["title"]} (last reviewed {age} days ago, limit {limit})')
    findings["Stale reviews"] = stale

    # 5. stored rating does not match likelihood x impact
    findings["Rating does not match likelihood x impact"] = [
        f'{r["risk_id"]}: stored {r["rating"]}, calculated {band(r["likelihood"], r["impact"])} ({int(r["likelihood"])*int(r["impact"])})'
        for r in risks if r["rating"] != band(r["likelihood"], r["impact"])]

    # 6. orphaned issues, 7. overdue issues, 8. closed risk with open issue
    findings["Orphaned issues (no valid linked risk)"] = [
        f'{i["issue_id"]}: {i["title"]} (risk_id: {i["risk_id"] or "blank"})' for i in issues if i["risk_id"] not in ids]
    findings["Overdue issues"] = [
        f'{i["issue_id"]} ({i["severity"]}): {i["title"]}, due {i["due_date"]}, {(asof - dt.date.fromisoformat(i["due_date"])).days} days late'
        for i in issues if i["status"] != "Closed" and dt.date.fromisoformat(i["due_date"]) < asof]
    closed = {r["risk_id"] for r in risks if r["status"] == "Closed"}
    findings["Closed risks that still have open issues"] = [
        f'{i["issue_id"]} on {i["risk_id"]}: {i["title"]}' for i in issues if i["risk_id"] in closed and i["status"] != "Closed"]

    total = sum(len(v) for v in findings.values())
    lines = [f"# Risk register hygiene report", "", f"As-of date: {asof.isoformat()}  ",
             f"Risks checked: {len(risks)}  |  Issues checked: {len(issues)}  |  Findings: {total}", "",
             "| Check | Findings |", "|---|---|"]
    lines += [f"| {k} | {len(v)} |" for k, v in findings.items()]
    for k, v in findings.items():
        lines += ["", f"## {k} ({len(v)})", ""]
        lines += [f"- {x}" for x in v] if v else ["None found."]
    report = "\n".join(lines) + "\n"
    with open(a.out, "w") as f:
        f.write(report)
    print(report)

if __name__ == "__main__":
    main()
