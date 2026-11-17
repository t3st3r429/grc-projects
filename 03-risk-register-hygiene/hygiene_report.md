# Risk register hygiene report

As-of date: 2026-11-17  
Risks checked: 42  |  Issues checked: 25  |  Findings: 19

| Check | Findings |
|---|---|
| Possible duplicate risks | 2 |
| Risks with no owner | 1 |
| Risks with no NIST CSF / ISO 27001 mapping | 1 |
| Stale reviews | 5 |
| Rating does not match likelihood x impact | 2 |
| Orphaned issues (no valid linked risk) | 2 |
| Overdue issues | 5 |
| Closed risks that still have open issues | 1 |

## Possible duplicate risks (2)

- R-004 and R-039: "No MFA on legacy admin console" / "No multi-factor authentication on legacy admin console"
- R-011 and R-040: "Application log retention shorter than policy" / "Log retention on application tier below policy"

## Risks with no owner (1)

- R-041: Shadow IT tools adopted without review

## Risks with no NIST CSF / ISO 27001 mapping (1)

- R-042: Customer data exported to spreadsheets (NIST: -, ISO: -)

## Stale reviews (5)

- R-006: Weak password policy on internal wiki (last reviewed 200 days ago, limit 180)
- R-018: Backups not restore-tested (last reviewed 210 days ago, limit 180)
- R-020: No formal access recertification for finance systems (last reviewed 300 days ago, limit 180)
- R-024: Incident response plan not tested in 12 months (last reviewed 260 days ago, limit 180)
- R-037: Business continuity plan out of date (last reviewed 330 days ago, limit 180)

## Rating does not match likelihood x impact (2)

- R-006: stored Medium, calculated Low (6)
- R-030: stored High, calculated Medium (12)

## Orphaned issues (no valid linked risk) (2)

- ISS-021: Update vendor security questionnaire (risk_id: R-099)
- ISS-022: Patch lobby kiosk machines (risk_id: blank)

## Overdue issues (5)

- ISS-001 (High): Enable MFA on legacy admin console, due 2026-10-18, 30 days late
- ISS-005 (High): Migrate reporting server to a supported OS, due 2026-10-03, 45 days late
- ISS-009 (Medium): Complete overdue supplier security reviews, due 2026-11-07, 10 days late
- ISS-011 (High): Run access recertification for finance systems, due 2026-09-18, 60 days late
- ISS-015 (High): Enable session recording for vendor access, due 2026-11-12, 5 days late

## Closed risks that still have open issues (1)

- ISS-013 on R-012: Replace self-signed certificates
