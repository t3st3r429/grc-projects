#!/usr/bin/env python3
"""Builds dashboard.html (self-contained) from the data in projects 01 and 03.

Usage:  python build_dashboard.py [--as-of YYYY-MM-DD]
Standard library only. Open dashboard.html in a browser, or publish with GitHub Pages.
"""
import argparse, csv, datetime as dt, html, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
P1 = os.path.join(HERE, "..", "01-exception-tracker", "exceptions.csv")
P3 = os.path.join(HERE, "..", "03-risk-register-hygiene")

def load(p):
    with open(p, newline="") as f:
        return list(csv.DictReader(f))

def band(l, i):
    s = int(l) * int(i)
    return "High" if s >= 15 else "Medium" if s >= 8 else "Low"

def bars(counts, colors=None, order=None):
    keys = order or list(counts)
    mx = max([counts.get(k, 0) for k in keys] + [1])
    out = []
    for k in keys:
        v = counts.get(k, 0)
        c = (colors or {}).get(k, "#2f5d8a")
        out.append(f'<div class="row"><span class="lab">{html.escape(k)}</span>'
                   f'<span class="track"><span class="fill" style="width:{v/mx*100:.0f}%;background:{c}"></span></span>'
                   f'<span class="val">{v}</span></div>')
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", default=dt.date.today().isoformat())
    a = ap.parse_args()
    asof = dt.date.fromisoformat(a.as_of)
    risks, issues, exc = load(os.path.join(P3, "register.csv")), load(os.path.join(P3, "issues.csv")), load(P1)

    open_risks = [r for r in risks if r["status"] != "Closed"]
    by_rating = Counter(band(r["likelihood"], r["impact"]) for r in open_risks)
    by_cat = Counter(r["category"] for r in open_risks)
    open_issues = [i for i in issues if i["status"] != "Closed"]
    overdue = [i for i in open_issues if dt.date.fromisoformat(i["due_date"]) < asof]
    by_status = Counter(i["status"] for i in issues)

    buckets = Counter()
    unverified = 0
    for e in exc:
        if e["status"] == "Closed":
            continue
        if e["controls_verified"] == "N":
            unverified += 1
        if not e["expiry_date"]:
            buckets["In progress"] += 1; continue
        days = (dt.date.fromisoformat(e["expiry_date"]) - asof).days
        key = "Expired" if days < 0 else "Due in 30 days" if days <= 30 else "Due in 60 days" if days <= 60 else "Due in 90 days" if days <= 90 else "On track"
        buckets[key] += 1
    urgent = buckets["Expired"] + buckets["Due in 30 days"]

    kpis = [("Open risks", len(open_risks), ""), ("High risks", by_rating["High"], "warn"),
            ("Open issues", len(open_issues), ""), ("Overdue issues", len(overdue), "bad"),
            ("Exceptions expired or due in 30 days", urgent, "bad"), ("Controls not yet verified", unverified, "warn")]
    kpi_html = "".join(f'<div class="kpi {c}"><div class="n">{n}</div><div class="t">{html.escape(t)}</div></div>' for t, n, c in kpis)
    rows = "".join(
        f'<tr><td>{html.escape(i["issue_id"])}</td><td>{html.escape(i["title"])}</td><td>{html.escape(i["owner"])}</td>'
        f'<td>{html.escape(i["severity"])}</td><td>{(asof - dt.date.fromisoformat(i["due_date"])).days}</td></tr>'
        for i in sorted(overdue, key=lambda i: i["due_date"]))
    cat_sorted = dict(by_cat.most_common())
    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cyber Risk Dashboard (fictional data)</title>
<style>
:root{{--bg:#f6f4ef;--card:#fff;--ink:#14202e;--mute:#5b6573;--line:#ddd8cc}}
@media (prefers-color-scheme:dark){{:root{{--bg:#101826;--card:#182235;--ink:#eceff4;--mute:#9aa6b6;--line:#2b3850}}}}
*{{box-sizing:border-box}}body{{margin:0;padding:32px;background:var(--bg);color:var(--ink);font-family:Arial,Helvetica,sans-serif}}
h1{{margin:0 0 4px;font-size:28px}}.sub{{color:var(--mute);margin:0 0 24px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-bottom:24px}}
.kpi{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px}}
.kpi .n{{font-size:38px;font-weight:700}}.kpi .t{{color:var(--mute);font-size:14px}}
.kpi.bad .n{{color:#c0392b}}.kpi.warn .n{{color:#d68910}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:14px;margin-bottom:24px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:20px}}
.card h2{{margin:0 0 14px;font-size:17px}}
.row{{display:flex;align-items:center;gap:10px;margin:8px 0;font-size:14px}}
.lab{{width:150px;flex:none}}.track{{flex:1;background:var(--line);border-radius:6px;height:14px;overflow:hidden}}
.fill{{display:block;height:100%;border-radius:6px}}.val{{width:28px;text-align:right;font-weight:700}}
.wide{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-size:14px}}
th,td{{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line)}}th{{color:var(--mute);font-weight:600}}
.foot{{color:var(--mute);font-size:13px;margin-top:20px}}
</style></head><body>
<h1>Cyber Risk Dashboard</h1>
<p class="sub">Northwind Payments (fictional) &middot; as of {asof.isoformat()} &middot; built from the register, issues and exceptions in this repo</p>
<div class="kpis">{kpi_html}</div>
<div class="grid">
<div class="card"><h2>Open risks by rating</h2>{bars(by_rating, {"High":"#c0392b","Medium":"#d68910","Low":"#2e8b57"}, ["High","Medium","Low"])}</div>
<div class="card"><h2>Issues by status</h2>{bars(by_status, {"Open":"#2f5d8a","In Progress":"#d68910","Closed":"#2e8b57"}, ["Open","In Progress","Closed"])}</div>
<div class="card"><h2>Exceptions by expiry</h2>{bars(buckets, {"Expired":"#c0392b","Due in 30 days":"#d35400","Due in 60 days":"#d68910","Due in 90 days":"#b7950b","On track":"#2e8b57","In progress":"#7f8c8d"}, ["Expired","Due in 30 days","Due in 60 days","Due in 90 days","On track","In progress"])}</div>
<div class="card"><h2>Open risks by category</h2>{bars(cat_sorted)}</div>
</div>
<div class="card wide"><h2>Overdue issues ({len(overdue)})</h2>
<table><tr><th>ID</th><th>Issue</th><th>Owner</th><th>Severity</th><th>Days late</th></tr>{rows}</table></div>
<p class="foot">All data is fictional. Risk rating = likelihood x impact (High 15+, Medium 8-14, Low 1-7). Regenerate with build_dashboard.py.</p>
</body></html>"""
    with open(os.path.join(HERE, "dashboard.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("Wrote dashboard.html")

if __name__ == "__main__":
    main()
