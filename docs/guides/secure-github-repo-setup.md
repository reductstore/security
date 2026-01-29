# Secure GitHub Repository Setup (Maintainer Guide)

This guide describes a practical security baseline for ReductStore repositories (public and private). It targets supply-chain risks in areas **1–5** of the threat model: contributors, GitHub controls, GitHub Actions, runner execution, dependencies, and publishing.

Reference: [Threat Modeling & Risk Assessment](../threat-modeling/threat-model-risk-assessment.md).

## 1) Repository + Org Baseline
- Require org-wide **2FA** and least-privilege team membership.
- Keep a small set of **repo admins**; prefer teams over individual grants.
- Review org/repo **audit logs** weekly

## 2) Branch Protection / Rulesets (P0)
Apply rulesets to `main` and any `release/*` branches:
- Require **pull requests** (no direct pushes).
- Require **1 approval**  and **CODEOWNERS** for:
  - `.github/workflows/**`, `.github/actions/**`
  - release scripts and packaging (e.g., `Dockerfile*`, build scripts)
- Require **status checks** (CI, lint, tests) before merge.
- Block force-pushes/deletions; require linear history if it fits your workflow.

Create `CODEOWNERS` with explicit ownership for CI/CD and release paths.

## 3) Tags, Releases, and Versioning (P0)
- Restrict who can **create tags** and **publish releases** (maintainers only).
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
- Treat fork PRs as untrusted: **no secrets**, no publish, no deployments.
- Keep this enforceable via separate workflows:
  - `pull_request` = build/test only
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
- [ ] Fork PRs run tests only; no secrets; no publish
- [ ] Least-privilege `GITHUB_TOKEN` permissions
- [ ] Pinned actions (SHA) and reviewed third-party actions
- [ ] Publishing uses environment approval + isolated secrets
- [ ] Prefer OIDC (AWS/Azure); rotate remaining secrets
