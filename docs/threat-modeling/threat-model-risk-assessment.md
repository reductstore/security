# Threat Modeling & Risk Assessment (SDLC + Distribution)

- Implementation guide: [Secure GitHub Repository Setup (Maintainer Guide)](../guides/secure-github-repo-setup.md).
- Implementation guide: [GitHub User Management (Access + Authentication + Commit Trust)](../guides/github-user-management.md).

## Scope (Current)
This threat model covers the **software development lifecycle and release/distribution pipeline** for ReductStore, including:
- Source code hosted on **GitHub** (mix of public and private repositories)
- CI/CD using **GitHub Actions**
- Distribution via **Docker Hub** (public images), **AWS ECR** (cloud deployment), and **Azure Storage** (public binaries)
- The public download entry point (`reduct.store/download`) as a distribution surface
- Deployment of **Reduct Cloud (SaaS)** from images stored in **AWS ECR** (deployment pipeline and image promotion)

Out of scope for now: runtime/product deployment hardening and customer environments (can be modeled separately).

## Security Objectives
- **Integrity**: released images/binaries are built from intended source and are not tampered with.
- **Confidentiality**: publishing credentials and internal security materials are protected.
- **Availability**: releases remain publishable and artifacts remain accessible to users.

## Actors
- **Maintainers/Release managers**: approve changes and publish releases.
- **Developers**: contribute code and workflows.
- **External contributors** (public repos): propose changes via PRs (if enabled).
- **CI system**: GitHub Actions control plane and runners.
- **Service providers**: GitHub, Docker Hub, AWS, Azure.
- **Cloud operators**: operate Reduct Cloud (SaaS) infrastructure and deployments.
- **Consumers**: end users and downstream automation pulling images/downloading binaries.

## Key Assets (What We Protect)
- **Source integrity**
  - Git history, tags, releases, protected branches, CODEOWNERS/rulesets
  - GitHub Actions workflow files and reusable workflows
- **Publishing authority**
  - Credentials and tokens for Docker Hub, AWS ECR, Azure Storage
  - Any signing keys (container signing, binary signing) and checksum generation process
- **Build integrity**
  - Runner environment configuration (hosted/self-hosted), runner images, toolchains
  - Dependency manifests and lockfiles; base images and pinned digests
  - Build logs and provenance/SBOM artifacts (if produced)
- **Distributed artifacts**
  - Docker images (tags, digests, manifests), repository settings (immutability/retention)
  - Binaries hosted in Azure Storage, blob/container configuration, public access policies
  - Checksums/signatures published alongside artifacts (if used)
- **Operational control**
  - GitHub org membership, 2FA/SSO policy, audit logs
  - Registry/storage account access control and audit trails
  - DNS/TLS for `reduct.store` and the download page publishing workflow
  - Reduct Cloud deployment controls (image promotion policy, IAM roles, deployment logs)

## Trust Boundaries & Attack Surfaces

### 1. Contributor environment → GitHub
Developer workstations and credentials interact with GitHub repositories and organization settings.

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Stolen developer credentials | Phishing, token theft, compromised laptops |
| Local auth material | SSH keys, PATs, stored GitHub sessions |
| Privileged actions in GitHub | Direct pushes to protected branches (if misconfigured), abuse of elevated roles |

### 2. GitHub (repo/org controls) → GitHub Actions
Workflow definitions, permissions, and tokens cross into CI execution.

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Workflow file tampering | Changes under `.github/workflows/` alter build/publish behavior |
| Token/permission misuse | Overly broad `GITHUB_TOKEN` / workflow `permissions:` |
| Reusable/third-party actions | Composite actions and reusable workflows (internal or external) |
| Secrets exposure paths | Logs, artifacts, environment dumps, debug output |
| High-trust triggers | Differences between `pull_request`, `push`, `workflow_dispatch`, `pull_request_target` |

### 3. GitHub Actions control plane → Runner execution environment
Jobs run with ephemeral credentials/tokens on **GitHub-hosted runners** (no self-hosted runners).

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Runner compromise | Breakout/compromise of a job environment during a release workflow |
| Persistence/cross-job state | Cache poisoning / state reuse via dependency caches and artifacts |
| Credentialed execution | Network/filesystem access + injected creds during publish steps |
| Artifact/log access | Retention policies and access controls for logs/artifacts |

### 4. Runner execution environment → Supply chain inputs
CI fetches third-party actions, dependencies, base images, and build tooling from external sources.

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Third-party actions supply chain | Actions referenced by mutable tags instead of pinned SHAs |
| Dependency supply chain | Package registries, transitive deps, build scripts |
| Base images | Mutable tags vs pinned digests; upstream image compromise |
| Toolchain installers | Unverified binaries; `curl | sh` patterns |
| Naming attacks | Typosquatting, dependency confusion |

### 5. Runner execution environment → Distribution endpoints
CI pushes images to registries and uploads binaries to storage.

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Credentialed publish operations | Push/upload using Docker Hub/AWS/Azure credentials |
| Tag/release mutability | Overwriting tags (e.g., `latest`), inconsistent release metadata |
| Promotion without traceability | Artifacts published without clear mapping to commit/tag |
| Accidental leakage | Publishing internal/debug artifacts or sensitive build outputs |

### 6. Distribution endpoints → Deployments/Consumers
Artifacts are consumed by automated systems (deployments) and by end users.

#### 6.1 AWS ECR → Reduct Cloud (SaaS)
The SaaS deployment system pulls/promotes images from ECR into production.

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Image selection/promotion | Which digest is deployed; promotion workflow controls |
| Deployment pull permissions | IAM roles used by the deployment plane to pull from ECR |
| Cross-account/replication | Replication policies and access boundaries (if used) |

#### 6.2 Azure Storage account → Binary consumers
Users (and automation) download published binaries from public blob endpoints.

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Public access configuration | Container/blob ACL mistakes; unintended write permissions |
| Object tamper/overwrite risk | Risk depends on who can write and whether versions are immutable |
| Metadata/checksum mismatch | Incorrect/missing checksums or confusing naming |

#### 6.3 GitHub release pipeline → Docker consumers
CI publishes images to Docker Hub; consumers pull by tag/digest from the public registry.

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Docker Hub repository controls | Access control, tag mutability, retention settings |
| Namespace confusion | Lookalike images, unauthorized publishes to similarly named repos |

#### 6.4 Download page → Consumers
The website content and any redirects/links influence what users download.

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Website publishing pipeline | CMS/static site deployment; link generation and release automation |
| Link/redirect manipulation | Stale links, mixed content, redirect targets |
| DNS/TLS posture | Misconfiguration impacting where users are sent |

## Risk Scoring (Lightweight)
Scoring uses a simple **Likelihood (L) × Impact (I)** model:
- **L (1–5)**: 1=rare, 3=possible, 5=likely
- **I (1–5)**: 1=low, 3=high, 5=critical
- **Risk = L×I**: interpret as 1–5 low, 6–10 medium, 12–15 high, 16–25 critical (format in tables: `High (15)`)

This is an initial assessment to prioritize mitigations; adjust once the release process details are confirmed.

## Threats & Misuse Cases (No Mitigations Yet)
Threat IDs (`TM-*`) and mitigation controls below are cross-linked to make traceability easier during review.

### 1. Contributor environment → GitHub
| ID | Threat / misuse case | Primary impact | L | I | Risk | Mitigations |
|---|---|---|---:|---:|---:|---|
| <a id="tm-1"></a>TM-1 | Account takeover of a maintainer/developer | Malicious code/workflow changes; unauthorized releases | 3 | 5 | High (15) | [Restrict who can create tags/releases](#mit-tags-releases) |
| <a id="tm-2"></a>TM-2 | Malicious/compromised developer workstation | Unauthorized pushes, credential theft, backdoored changes | 3 | 4 | High (12) | TBD |
| <a id="tm-3"></a>TM-3 | Abuse of elevated GitHub permissions | Bypass review controls; change branch protection; hide malicious changes | 2 | 5 | Medium (10) | [Enforce branch protections + required reviews](#mit-branch-protections), [Restrict who can create tags/releases](#mit-tags-releases) |

### 2. GitHub (repo/org controls) → GitHub Actions
| ID | Threat / misuse case | Primary impact | L | I | Risk | Mitigations |
|---|---|---|---:|---:|---:|---|
| <a id="tm-4"></a>TM-4 | Workflow injection via PR/workflow edits | Build/publish steps altered to ship malicious artifacts | 4 | 5 | Critical (20) | [Enforce branch protections + required reviews](#mit-branch-protections), [Restrict who can create tags/releases](#mit-tags-releases) |
| <a id="tm-5"></a>TM-5 | Secrets exfiltration from CI | Publishing credential theft; lateral movement to registries/storage | 4 | 5 | Critical (20) | [Least-privilege `GITHUB_TOKEN` permissions](#mit-github-token-permissions), [Harden PR workflows for forks/untrusted code](#mit-pr-workflows-untrusted), [Prevent secrets exposure in CI (especially for public repos)](#mit-ci-secrets-exposure), [Prefer short-lived credentials (OIDC) for cloud publishes](#mit-oidc-cloud-publishes) |
| <a id="tm-6"></a>TM-6 | Malicious reusable workflow/composite/third-party action | Remote code execution in CI with job permissions | 3 | 5 | High (15) | [Pin third-party actions by commit SHA](#mit-pin-actions) |
| <a id="tm-7"></a>TM-7 | Permission escalation via mis-scoped `GITHUB_TOKEN` | Repo writes, tag creation, release edits beyond intended scope | 3 | 4 | High (12) | [Least-privilege `GITHUB_TOKEN` permissions](#mit-github-token-permissions) |
| <a id="tm-8"></a>TM-8 | Trigger confusion (PR vs trusted context) | Untrusted code runs with trusted permissions/secrets | 3 | 5 | High (15) | [Harden PR workflows for forks/untrusted code](#mit-pr-workflows-untrusted), [Prevent secrets exposure in CI (especially for public repos)](#mit-ci-secrets-exposure) |

### 3. Actions control plane → Runner execution environment
| ID | Threat / misuse case | Primary impact | L | I | Risk | Mitigations |
|---|---|---|---:|---:|---:|---|
| <a id="tm-9"></a>TM-9 | Runner compromise during release job | Artifact tampering; credential theft; persistent foothold (if self-hosted) | 3 | 5 | High (15) | [Use ephemeral, isolated runners for releases](#mit-ephemeral-runners) |
| <a id="tm-10"></a>TM-10 | Cross-job contamination (cache/workspace) | Build outputs influenced by prior untrusted job state | 2 | 4 | Medium (8) | [Use ephemeral, isolated runners for releases](#mit-ephemeral-runners) |
| <a id="tm-11"></a>TM-11 | Log/artifact exposure | Leaked tokens, internal paths, or security-relevant configuration | 3 | 3 | Medium (9) | TBD |

### 4. Runner execution environment → Supply chain inputs
| ID | Threat / misuse case | Primary impact | L | I | Risk | Mitigations |
|---|---|---|---:|---:|---:|---|
| <a id="tm-12"></a>TM-12 | Compromised dependency/action/base image | Backdoored builds; malicious runtime behavior | 3 | 5 | High (15) | [Pin third-party actions by commit SHA](#mit-pin-actions), [Dependency/base image pinning and verification](#mit-pin-dependencies) |
| <a id="tm-13"></a>TM-13 | Typosquatting/dependency confusion | Wrong package/action pulled into build and executed | 3 | 4 | High (12) | [Dependency/base image pinning and verification](#mit-pin-dependencies) |
| <a id="tm-14"></a>TM-14 | Toolchain tampering | Malicious compiler/build tool produces compromised artifacts | 2 | 5 | Medium (10) | [Dependency/base image pinning and verification](#mit-pin-dependencies) |

### 5. Runner execution environment → Distribution endpoints
| ID | Threat / misuse case | Primary impact | L | I | Risk | Mitigations |
|---|---|---|---:|---:|---:|---|
| <a id="tm-15"></a>TM-15 | Unauthorized publish using stolen credentials | Malicious images/binaries distributed from official channels | 3 | 5 | High (15) | [Prefer short-lived credentials (OIDC) for cloud publishes](#mit-oidc-cloud-publishes) |
| <a id="tm-16"></a>TM-16 | Tag overwrite / mutable release artifacts | Users pull different content than expected; rollback becomes unreliable | 3 | 4 | High (12) | [Prevent tag overwrite where possible](#mit-prevent-tag-overwrite), [Prefer digest-based references for Docker consumers docs](#mit-digest-based-docker-docs) |
| <a id="tm-17"></a>TM-17 | Publish wrong artifact or wrong target | Confusing/mismatched downloads; accidental leakage of non-release outputs | 3 | 3 | Medium (9) | TBD |

### 6. Distribution endpoints → Deployments/Consumers

#### 6.1 AWS ECR → Reduct Cloud (SaaS)
| ID | Threat / misuse case | Primary impact | L | I | Risk | Mitigations |
|---|---|---|---:|---:|---:|---|
| <a id="tm-18"></a>TM-18 | Deploy wrong image digest/tag | Production runs unintended or vulnerable code | 3 | 4 | High (12) | [Deploy by immutable image digest in Reduct Cloud](#mit-deploy-by-digest) |
| <a id="tm-19"></a>TM-19 | Unauthorized image promotion to production | Attackers introduce malicious image into SaaS | 2 | 5 | Medium (10) | [Deploy by immutable image digest in Reduct Cloud](#mit-deploy-by-digest) |

#### 6.2 Azure Storage account → Binary consumers
| ID | Threat / misuse case | Primary impact | L | I | Risk | Mitigations |
|---|---|---|---:|---:|---:|---|
| <a id="tm-20"></a>TM-20 | Binary replacement/tampering in storage | Users install a malicious binary believing it is official | 3 | 5 | High (15) | [Restrict write access to Azure binaries container](#mit-azure-binaries-write-access), [Publish checksums (and optionally signatures) for binaries](#mit-publish-checksums) |
| <a id="tm-21"></a>TM-21 | Confusing naming/metadata (wrong binary) | Users download wrong platform/version; increased support and security risk | 3 | 2 | Medium (6) | [Publish checksums (and optionally signatures) for binaries](#mit-publish-checksums) |

#### 6.3 GitHub release pipeline → Docker consumers
| ID | Threat / misuse case | Primary impact | L | I | Risk | Mitigations |
|---|---|---|---:|---:|---:|---|
| <a id="tm-22"></a>TM-22 | Malicious image published under official name | Consumers deploy compromised containers | 3 | 5 | High (15) | [Prefer digest-based references for Docker consumers docs](#mit-digest-based-docker-docs) |
| <a id="tm-23"></a>TM-23 | Lookalike/typosquatted image confusion | Users pull attacker-controlled images by mistake | 3 | 4 | High (12) | TBD |

#### 6.4 Download page → Consumers
| ID | Threat / misuse case | Primary impact | L | I | Risk | Mitigations |
|---|---|---|---:|---:|---:|---|
| <a id="tm-24"></a>TM-24 | Download links altered to attacker-controlled artifacts | Users receive malicious binaries/images | 2 | 5 | Medium (10) | [Publish checksums (and optionally signatures) for binaries](#mit-publish-checksums), [Protect the download page publishing pipeline](#mit-protect-download-pipeline) |
| <a id="tm-25"></a>TM-25 | DNS/TLS compromise or misconfiguration | Users redirected to malicious endpoints or served tampered content | 2 | 5 | Medium (10) | [Protect the download page publishing pipeline](#mit-protect-download-pipeline) |

## Mitigation Candidates (To Be Confirmed/Implemented)
These are candidate controls to reduce the risks above; implementation details and ownership are tracked in the next iteration.

### 1–2. GitHub (contributors + repo controls + Actions)
Priority is driven by the highest-risk threat(s) a control addresses.
`P0` = addresses at least one **Critical** risk, `P1` = highest addressed risk is **High**, `P2` = highest addressed risk is **Medium/Low**.

Status is the mitigation implementation status (across repos): `⬜ Not started` / `🟡 In progress` / `✅ Done`.

| Priority | Control | Addresses | Notes / evidence to capture | Status | Tracking (issue/PR) |
|---|---|---|---|---|---|
| P0 | <a id="mit-branch-protections"></a>Enforce branch protections + required reviews | [TM-3](#tm-3), [TM-4](#tm-4) | Rulesets/branch protection settings, CODEOWNERS (baseline export: `misc/protected_branches.json`) | ✅ Done | [#14](https://github.com/reductstore/security/issues/14) |
| P0 | <a id="mit-tags-releases"></a>Restrict who can create tags/releases | [TM-1](#tm-1), [TM-3](#tm-3), [TM-4](#tm-4) | Release permissions and protected tags (baseline export: `misc/tags.json`) | ✅ Done | [#15](https://github.com/reductstore/security/issues/15) |
| P0 | <a id="mit-github-token-permissions"></a>Least-privilege `GITHUB_TOKEN` permissions | [TM-7](#tm-7), [TM-5](#tm-5) | Workflow `permissions:` block per job | ⬜ Not started | [#16](https://github.com/reductstore/security/issues/16) |
| P0 | <a id="mit-pr-workflows-untrusted"></a>Harden PR workflows for forks/untrusted code | [TM-8](#tm-8), [TM-5](#tm-5) | Fork PRs require explicit maintainer approval before CI runs; do not expose secrets or trusted permissions to untrusted triggers | ⬜ Not started | [#17](https://github.com/reductstore/security/issues/17) |
| P0 | <a id="mit-ci-secrets-exposure"></a>Prevent secrets exposure in CI (especially for public repos) | [TM-5](#tm-5), [TM-8](#tm-8) | Internal branch PRs may follow normal CI; fork PRs run without secrets; avoid `pull_request_target` unless strictly reviewed; scrub logs/artifacts for tokens | ⬜ Not started | [#18](https://github.com/reductstore/security/issues/18) |
| P1 | <a id="mit-pin-actions"></a>Pin third-party actions by commit SHA | [TM-6](#tm-6), [TM-12](#tm-12) | Workflow diffs showing pinned SHAs | ⬜ Not started | [#22](https://github.com/reductstore/security/issues/22) |

### 3–5. CI runners, dependencies, and publishing
| Priority | Control | Addresses | Notes / evidence to capture | Status | Tracking (issue/PR) |
|---|---|---|---|---|---|
| P0 | <a id="mit-oidc-cloud-publishes"></a>Prefer short-lived credentials (OIDC) for cloud publishes | [TM-5](#tm-5), [TM-15](#tm-15) | AWS/Azure federation configs; secret inventory | ⬜ Not started | [#19](https://github.com/reductstore/security/issues/19) |
| P1 | <a id="mit-pin-dependencies"></a>Dependency/base image pinning and verification | [TM-12](#tm-12), [TM-13](#tm-13), [TM-14](#tm-14) | Lockfiles, digests, provenance/SBOM if available | ⬜ Not started | TODO |
| P1 | <a id="mit-ephemeral-runners"></a>Use ephemeral, isolated runners for releases | [TM-9](#tm-9), [TM-10](#tm-10) | Runner type, isolation model, cache policy | ⬜ Not started | TODO |
| P2 | <a id="mit-prevent-tag-overwrite"></a>Prevent tag overwrite where possible | [TM-16](#tm-16) | Registry policies; release immutability guidance | ⬜ Not started | TODO |

### 6.x Distribution endpoints and consumers
| Priority | Control | Addresses | Notes / evidence to capture | Status | Tracking (issue/PR) |
|---|---|---|---|---|---|
| P1 | <a id="mit-azure-binaries-write-access"></a>Restrict write access to Azure binaries container | [TM-20](#tm-20) | Storage RBAC/SAS usage and audit logs | ⬜ Not started | TODO |
| P1 | <a id="mit-publish-checksums"></a>Publish checksums (and optionally signatures) for binaries | [TM-20](#tm-20), [TM-21](#tm-21), [TM-24](#tm-24) | Checksum files and verification instructions | ⬜ Not started | TODO |
| P1 | <a id="mit-digest-based-docker-docs"></a>Prefer digest-based references for Docker consumers docs | [TM-22](#tm-22), [TM-16](#tm-16) | Documentation guidance; release notes | ⬜ Not started | TODO |
| P2 | <a id="mit-deploy-by-digest"></a>Deploy by immutable image digest in Reduct Cloud | [TM-18](#tm-18), [TM-19](#tm-19) | Deployment manifests/policies referencing digests | ⬜ Not started | TODO |
| P2 | <a id="mit-protect-download-pipeline"></a>Protect the download page publishing pipeline | [TM-24](#tm-24), [TM-25](#tm-25) | Site build/deploy controls; DNS/TLS controls | ⬜ Not started | TODO |

## Residual Risk (Initial)
Residual risk remains for sophisticated supply-chain attacks and account compromise; reassess after the controls above are implemented and evidenced, and after any incident affecting GitHub/CI/distribution accounts.

## Ownership & Review Cadence
| Area | Owner (role) | Review trigger |
|---|---|---|
| GitHub org/repo security settings | Security/Engineering owner (TBD) | Quarterly; after membership/permission changes |
| GitHub Actions workflows | Release engineering (TBD) | Any release workflow change; quarterly |
| CI runner security posture | Release engineering / DevOps (TBD) | Runner change; quarterly |
| Docker Hub publishing | Release engineering (TBD) | Credential rotation; quarterly |
| AWS ECR publishing + Reduct Cloud deployments | Cloud ops (TBD) | Deployment pipeline change; quarterly |
| Azure binaries publishing | Release engineering (TBD) | Storage policy change; quarterly |
| `reduct.store/download` publishing + DNS/TLS | Web ops (TBD) | Site pipeline/DNS change; quarterly |

## Assumptions & TBD (Context That Affects Risk)
Threat modeling depends heavily on process details. This section lists **unknowns** that can change likelihood/impact scores and the recommended control priorities; once clarified, we update the tables above.

- Reduct Cloud deployment mechanism (e.g., ECS/EKS), and how image promotion to production is controlled/audited.
