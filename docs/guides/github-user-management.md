# GitHub User Management (Access + Authentication + Commit Trust)

This guide describes a practical baseline for managing **people and access** in GitHub organizations and
repositories used by ReductStore. It focuses on reducing account takeover, unauthorized changes, and privilege
abuse risks.

Reference: [Threat Modeling & Risk Assessment](../threat-modeling/threat-model-risk-assessment.md) (especially
TM-1, TM-2, TM-3, TM-5, TM-7, TM-8, TM-15).

Related guide: [Secure GitHub Repository Setup (Maintainer Guide)](./secure-github-repo-setup.md).

## 1) Principles
- Default to **least privilege**: grant the minimum role needed for a job function.
- Prefer **teams over individual grants** and keep teams small and purpose-based.
- Separate duties: avoid having the same person both approve and publish releases where feasible.
- Make access changes **reviewable**: require approvals for team membership and elevated roles.
- Keep a short paper trail: capture evidence for access reviews and permission changes.

## 2) Authentication Baseline (P0)
Goal: reduce likelihood of account takeover (TM-1, TM-2).

- Enforce org-wide **2FA** for all members (including outside collaborators where possible).
- Prefer **SSO/SAML** (if available) and disable legacy auth paths you do not need.
- Require **hardware security keys** (or passkeys) for maintainers and release managers when feasible.
- Keep recovery paths strict:
  - limit who can bypass SSO / recover accounts
  - document escalation steps for account lockout

### Personal Access Tokens (PATs)
- Prefer short-lived, scoped tokens (Fine-grained PATs) over classic PATs.
- Ban or heavily restrict classic PATs for maintainers/release managers if possible.
- Require an owner and expiry for any token used in automation.
- Rotate tokens after role change, offboarding, or any suspected exposure.

### SSH keys
- Require modern key types (e.g., ed25519) and disable weak/legacy keys where possible.
- Review and remove unused keys during periodic access reviews.

## 3) Commit Trust (P0/P1)
Goal: make it harder to land untrusted changes and easier to attribute authorship (TM-1, TM-2, TM-4).

- Require PRs + reviews for protected branches (see repo setup guide).
- Require **signed commits** for maintainers when feasible, especially for:
  - `.github/workflows/**`
  - release scripts and packaging files
  - CODEOWNERS/rulesets changes

Recommended options (choose one per repo/org policy):
- GitHub **vigilant mode** + require signed commits on protected branches (where supported)
- Require signed commits for maintainers only; allow unsigned commits from external contributors but keep them in
  PRs with mandatory review

Operational notes:
- Make “who can approve” explicit via CODEOWNERS for security-critical paths.
- Treat any workflow change as security-sensitive and subject to stricter review.

## 4) Permissions Model (P0)
Goal: minimize privilege abuse and reduce blast radius (TM-3, TM-7, TM-15).

### Organization roles
- Keep org **Owners** to the smallest possible set (ideally 2–3).
- Use a dedicated team for **security admins** (if available) rather than granting owner broadly.
- Require approval to add someone to any elevated role/team.

### Repository roles
- Prefer granting access via teams:
  - `maintainers` (admin/maintain, small)
  - `developers` (write, typical)
  - `triage` (triage on issues/PRs)
  - `readers` (read-only)
- Avoid long-lived **outside collaborators**; prefer inviting into the org with role-based teams.

### High-risk capabilities (control tightly)
- Create tags/releases
- Change branch protection/rulesets
- Edit Actions workflows or secrets
- Publish to Docker Hub/AWS/Azure

Implementation options:
- Separate `release-managers` team from `developers`.
- Require environment approvals for publish jobs (see repo setup guide).

## 5) Onboarding (P0)
Use a consistent checklist for every joiner.

- [ ] Add to org with the lowest role that works.
- [ ] Add to role-based teams (avoid direct repo grants).
- [ ] Confirm 2FA/SSO compliance.
- [ ] Confirm how they will authenticate (SSO + key/passkey; PAT policy).
- [ ] For maintainers/release managers: enable signed commits and confirm key custody expectations.

Evidence to capture (lightweight):
- Link to the onboarding request/approval (issue/ticket) and the final team memberships.

## 6) Offboarding and Role Changes (P0)
Goal: prevent lingering access (TM-3, TM-15).

- [ ] Remove from org teams and repo collaborator lists.
- [ ] Remove elevated roles (owner/admin/maintain) first, then remove general access.
- [ ] Revoke/rotate any automation tokens they owned or had access to.
- [ ] Rotate shared secrets affected by the role change (publish creds, environment secrets).
- [ ] Review recent sensitive events (releases/tags/workflow changes) in the audit log.

## 7) Access Reviews and Audit Logs (P1)
Goal: detect drift and unexpected access changes (TM-3, TM-5, TM-7, TM-8).

Suggested cadence for a small team:
- Weekly: 10–15 minute scan of high-signal audit events.
- Quarterly: full review of org membership, elevated roles, and repo access.

What to review:
- membership changes, role changes, team membership changes
- branch protection/ruleset changes
- secrets added/updated
- workflow permission changes and environment protection changes
- release/tag creation and publish workflow runs

Evidence to capture:
- A short log entry with date/reviewer and “no findings” or list of follow-ups.
- Track follow-ups as issues/PRs in the main engineering repo (or an internal tracker).

## Quick Checklist (Minimum)
- [ ] Org 2FA/SSO enforced; maintainers use keys/passkeys where feasible
- [ ] Teams-based access; minimal owners/admins; approvals for elevated membership
- [ ] PRs required; CODEOWNERS for CI/release paths; signed commits policy for maintainers
- [ ] Onboarding/offboarding checklists used; tokens/secrets rotated on role changes
- [ ] Regular audit log review and quarterly access review with evidence
