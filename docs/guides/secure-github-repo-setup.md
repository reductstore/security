# Secure GitHub Repository Setup (Maintainer Guide)

This guide describes a practical security baseline for ReductStore repositories (public and private). It targets supply-chain risks in areas **1–5** of the threat model: contributors, GitHub controls, GitHub Actions, runner execution, dependencies, and publishing.

Reference: [Threat Modeling & Risk Assessment](../threat-modeling/threat-model-risk-assessment.md).
Related guide: [GitHub User Management (Access + Authentication + Commit Trust)](./github-user-management.md).

## 1) Repository + Org Baseline
- Require org-wide **2FA** and least-privilege team membership.
- Keep a small set of **repo admins**; prefer teams over individual grants.
- Review org/repo **audit logs** weekly

## 2) Branch Protection / Rulesets (P0)
Apply rulesets to `main` and any `release/*` branches:
- Default approach: start from the exported baseline ruleset in `misc/protected_branches.json` and adapt:
  - extend the `include` list to cover your release branches (e.g., `refs/heads/release/*`) if used
  - add required status checks appropriate to the repo (CI/lint/tests)
- Require **pull requests** (no direct pushes).
- Exception for releases: allow **org admins** to bypass rules only to synchronize `main` and `stable`
  with a **non-squash merge** when required by the release process. Treat this as break-glass:
  - do not use for normal feature delivery
  - document the reason in the PR/release notes and verify in audit logs
- Require **1 approval**  and **CODEOWNERS** for:
  - `.github/workflows/**`, `.github/actions/**`
  - release scripts and packaging (e.g., `Dockerfile*`, build scripts)
- Require **status checks** before merge, but keep the required set small and reliable:
  - make “must-pass” checks cover safety-critical guarantees (build + unit tests + lint)
  - keep flaky or “nice-to-have” checks (e.g., code coverage thresholds) informational, not required
- Block force-pushes/deletions; require linear history if it fits your workflow.

Create `CODEOWNERS` with explicit ownership for CI/CD and release paths.

## 3) Tags, Releases, and Versioning (P0)
- Default approach: start from the exported tag ruleset in `misc/tags.json` and adapt as needed.
- Restrict who can **create tags** and **publish releases** (maintainers only).
- Verify the tag ruleset does what you intend for **tag creation** (not just update/delete); if not, enforce this
  via repo permissions (e.g., only `release-managers`/maintainers can create tags).
- Prefer immutable release identifiers:
  - Build/publish by **git tag** and record the **commit SHA** in release notes.
  - Avoid reusing tags; treat “latest” as convenience only.

## 4) GitHub Actions Hardening (P0/P1)
Assumption: workflows run on **GitHub-hosted runners** (no self-hosted runners).

### Workflow permissions
- Default to least privilege:
  - set `permissions: read-all` at workflow top-level
  - grant write permissions only per-job (e.g., `contents: write` for releases)
- Avoid `pull_request_target` unless you have a documented review gate.

Example (baseline permissions):
```yaml
permissions: read-all

jobs:
  test:
    permissions: {}
    runs-on: ubuntu-latest
```

Example (release job with scoped writes):
```yaml
jobs:
  release:
    if: startsWith(github.ref, 'refs/tags/')
    permissions:
      contents: write
    runs-on: ubuntu-latest
```

### Fork PR policy (confirmed)
- This aligns with **GitHub default behavior** for fork pull requests: first-time/untrusted fork workflows
  require maintainer approval (based on repo/org settings), and secrets are not exposed by default.
- Treat PRs from repository branches as trusted team changes when only maintainers/team members can create them.
- Treat fork PRs as untrusted: require explicit maintainer approval before CI runs, and do not expose secrets,
  publish steps, or deployment credentials to those runs.
- Keep this enforceable via workflow/job conditions:
  - trusted branch PRs = normal CI
  - fork PRs = maintainer-approved build/test only
  - `push`/`workflow_dispatch` on protected branches/tags = release/publish

### Third-party actions (P1)
- Pin external actions to a **commit SHA** (not a mutable tag).
- Prefer GitHub-maintained actions; review any new action before adoption.

### Environments and approvals (recommended)
- Use GitHub **Environments** for publishing jobs (Docker Hub/AWS/Azure), with required reviewers and scoped secrets.

## 5) Secrets and Credentials (P0)
- Never print secrets: avoid `set -x`, `printenv`, and debug logs in publish jobs.
- Prefer **short-lived credentials** where possible (GitHub **OIDC** for AWS/Azure).
- Rotate any remaining long-lived secrets on a schedule and after incidents.
- Use separate credentials per destination (Docker Hub vs AWS vs Azure) and per environment.

## 6) Dependency and Build Input Controls (P1)
- Pin dependencies with lockfiles (where applicable) and review updates.
- Pin container **base images by digest** for release builds (recommended).
- Avoid unverified installers (`curl | sh`); prefer pinned checksums/signatures.

## 7) Publishing Safety (P1/P2)
- Make publish jobs explicit and gated (tag-based + environment approval).
- Prevent cache poisoning: do not share caches/artifacts between PR jobs and release jobs.
- Record evidence: link workflow run IDs to releases (release notes or a release manifest).

## Quick Checklist (Minimum)
- [ ] Branch protections + CODEOWNERS on CI/release files
- [ ] Internal branch PRs follow normal CI; fork PRs require maintainer approval and run without secrets/publish
- [ ] Least-privilege `GITHUB_TOKEN` permissions
- [ ] Pinned actions (SHA) and reviewed third-party actions
- [ ] Publishing uses environment approval + isolated secrets
- [ ] Prefer OIDC (AWS/Azure); rotate remaining secrets

## Threat Model Coverage Notes (Repository Rulesets)
The exported rulesets (`misc/protected_branches.json`, `misc/tags.json`) help mitigate GitHub-repo threats, but
are not sufficient on their own.

In particular:
- They contribute to TM-3 and TM-4 by enforcing PR-based changes and signed updates to protected refs.
- They contribute to TM-16 by discouraging tag overwrites, but you still need process + release automation
  controls to ensure immutability end-to-end.

Important boundary:
- GitHub rulesets do not (and cannot) fully mitigate account takeover (TM-1), CI secrets exfiltration (TM-5),
  `GITHUB_TOKEN` permission scoping (TM-7), or trigger-context confusion (TM-8). Those require a combination of
  org access controls (see the user management guide), workflow design, and environment/secret governance.

Common gaps to check for in each repo:
- Required status checks are configured and match your CI job names.
- Workflow/release paths are protected with CODEOWNERS and required reviews.
- Only a small set of users can change rulesets, secrets, and release settings (see the user management guide).
