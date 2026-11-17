# 05 · GRC platform access model

**Problem:** A GRC platform holds the organization's most candid view of its weaknesses. Too much access leaks that, and too little stops the work. Integrations with reporting tools, APIs and AI assistants add new doors.

**What I built:**
- `role-matrix.csv`: nine roles (seven human, two service accounts) against the platform's functions, using None / View / Create / Edit / Approve / Admin.
- `integration-register.csv`: an example inventory of integrations with scope, owner, data exposed and review dates.
- The standards below.

This is a design pattern and is not tied to one vendor's product. Names of permissions would be mapped to the specific platform.

## Principles

1. **Least privilege.** Start from None and add only what the role needs.
2. **Separation of duties.** The person who requests an exception cannot approve it. The person who administers the platform does not approve risks.
3. **Roles, not individuals.** Grant access through roles. No one-off permissions.
4. **Time-box elevated access.** Admin rights are granted for a task and removed afterwards.
5. **Review regularly.** Quarterly access review by the platform owner. Remove leavers the same day.

## Joiner, mover, leaver

- **Joiner:** manager requests a named role. Platform admin grants it. Ticket is the evidence.
- **Mover:** old role is removed before the new one is added.
- **Leaver:** access removed at offboarding. Any records they own are reassigned.

## Standards for API and AI-tool integrations

- One service account per integration, never a person's credentials.
- **Read-only by default.** Write access needs a written reason and owner approval.
- Scope to the specific modules and fields needed. Exclude personal data and unredacted findings unless required.
- Tokens expire and are rotated every 90 days, stored in a secrets manager.
- Every call is logged. Alert on unusual volume or off-hours use.
- Each integration has a named owner and a way to switch it off quickly.
- **AI assistants** get the same rules: read-only, limited to approved record types, no ability to approve, close or delete, and a human reviews anything it drafts before it is saved.
- Test every configuration or workflow change in a sandbox before production, and keep the test notes.

## Quarterly access review checklist

- [ ] Export all users and roles
- [ ] Confirm each user still needs their role (manager sign-off)
- [ ] Remove users who left or changed teams
- [ ] Check admin accounts against the approved list
- [ ] Review integration tokens: owner, scope, last rotation
- [ ] Record the review date and the changes made
