# Threat Modeling & Risk Assessment (SDLC + Distribution)

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
Jobs run with ephemeral credentials/tokens and a specific runner security posture (TBD: GitHub-hosted vs self-hosted).

| Attack surface / entrypoint | Notes / examples |
|---|---|
| Runner compromise | Breakout/compromise; highest impact if any self-hosted runners exist |
| Persistence/cross-job state | Reused workspaces, caches, long-lived runner state (self-hosted) |
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

### 1. Contributor environment → GitHub
| ID | Threat / misuse case | Primary impact | L | I | Risk |
|---|---|---|---:|---:|---:|
| TM-1 | Account takeover of a maintainer/developer | Malicious code/workflow changes; unauthorized releases | 3 | 5 | High (15) |
| TM-2 | Malicious/compromised developer workstation | Unauthorized pushes, credential theft, backdoored changes | 3 | 4 | High (12) |
| TM-3 | Abuse of elevated GitHub permissions | Bypass review controls; change branch protection; hide malicious changes | 2 | 5 | Medium (10) |

### 2. GitHub (repo/org controls) → GitHub Actions
| ID | Threat / misuse case | Primary impact | L | I | Risk |
|---|---|---|---:|---:|---:|
| TM-4 | Workflow injection via PR/workflow edits | Build/publish steps altered to ship malicious artifacts | 4 | 5 | Critical (20) |
| TM-5 | Secrets exfiltration from CI | Publishing credential theft; lateral movement to registries/storage | 4 | 5 | Critical (20) |
| TM-6 | Malicious reusable workflow/composite/third-party action | Remote code execution in CI with job permissions | 3 | 5 | High (15) |
| TM-7 | Permission escalation via mis-scoped `GITHUB_TOKEN` | Repo writes, tag creation, release edits beyond intended scope | 3 | 4 | High (12) |
| TM-8 | Trigger confusion (PR vs trusted context) | Untrusted code runs with trusted permissions/secrets | 3 | 5 | High (15) |

### 3. Actions control plane → Runner execution environment
| ID | Threat / misuse case | Primary impact | L | I | Risk |
|---|---|---|---:|---:|---:|
| TM-9 | Runner compromise during release job | Artifact tampering; credential theft; persistent foothold (if self-hosted) | 3 | 5 | High (15) |
| TM-10 | Cross-job contamination (cache/workspace) | Build outputs influenced by prior untrusted job state | 2 | 4 | Medium (8) |
| TM-11 | Log/artifact exposure | Leaked tokens, internal paths, or security-relevant configuration | 3 | 3 | Medium (9) |

### 4. Runner execution environment → Supply chain inputs
| ID | Threat / misuse case | Primary impact | L | I | Risk |
|---|---|---|---:|---:|---:|
| TM-12 | Compromised dependency/action/base image | Backdoored builds; malicious runtime behavior | 3 | 5 | High (15) |
| TM-13 | Typosquatting/dependency confusion | Wrong package/action pulled into build and executed | 3 | 4 | High (12) |
| TM-14 | Toolchain tampering | Malicious compiler/build tool produces compromised artifacts | 2 | 5 | Medium (10) |

### 5. Runner execution environment → Distribution endpoints
| ID | Threat / misuse case | Primary impact | L | I | Risk |
|---|---|---|---:|---:|---:|
| TM-15 | Unauthorized publish using stolen credentials | Malicious images/binaries distributed from official channels | 3 | 5 | High (15) |
| TM-16 | Tag overwrite / mutable release artifacts | Users pull different content than expected; rollback becomes unreliable | 3 | 4 | High (12) |
| TM-17 | Publish wrong artifact or wrong target | Confusing/mismatched downloads; accidental leakage of non-release outputs | 3 | 3 | Medium (9) |

### 6. Distribution endpoints → Deployments/Consumers

#### 6.1 AWS ECR → Reduct Cloud (SaaS)
| ID | Threat / misuse case | Primary impact | L | I | Risk |
|---|---|---|---:|---:|---:|
| TM-18 | Deploy wrong image digest/tag | Production runs unintended or vulnerable code | 3 | 4 | High (12) |
| TM-19 | Unauthorized image promotion to production | Attackers introduce malicious image into SaaS | 2 | 5 | Medium (10) |

#### 6.2 Azure Storage account → Binary consumers
| ID | Threat / misuse case | Primary impact | L | I | Risk |
|---|---|---|---:|---:|---:|
| TM-20 | Binary replacement/tampering in storage | Users install a malicious binary believing it is official | 3 | 5 | High (15) |
| TM-21 | Confusing naming/metadata (wrong binary) | Users download wrong platform/version; increased support and security risk | 3 | 2 | Medium (6) |

#### 6.3 GitHub release pipeline → Docker consumers
| ID | Threat / misuse case | Primary impact | L | I | Risk |
|---|---|---|---:|---:|---:|
| TM-22 | Malicious image published under official name | Consumers deploy compromised containers | 3 | 5 | High (15) |
| TM-23 | Lookalike/typosquatted image confusion | Users pull attacker-controlled images by mistake | 3 | 4 | High (12) |

#### 6.4 Download page → Consumers
| ID | Threat / misuse case | Primary impact | L | I | Risk |
|---|---|---|---:|---:|---:|
| TM-24 | Download links altered to attacker-controlled artifacts | Users receive malicious binaries/images | 2 | 5 | Medium (10) |
| TM-25 | DNS/TLS compromise or misconfiguration | Users redirected to malicious endpoints or served tampered content | 2 | 5 | Medium (10) |

## Mitigation Candidates (To Be Confirmed/Implemented)
These are candidate controls to reduce the risks above; implementation details and ownership are tracked in the next iteration.

### 1–2. GitHub (contributors + repo controls + Actions)
| Control | Addresses | Notes / evidence to capture |
|---|---|---|
| Enforce branch protections + required reviews | TM-3, TM-4 | Rulesets/branch protection settings, CODEOWNERS |
| Restrict who can create tags/releases | TM-1, TM-3, TM-4 | Release permissions and protected tags |
| Pin third-party actions by commit SHA | TM-6, TM-12 | Workflow diffs showing pinned SHAs |
| Least-privilege `GITHUB_TOKEN` permissions | TM-7, TM-5 | Workflow `permissions:` block per job |
| Harden PR workflows for forks/untrusted code | TM-8, TM-5 | Avoid secret exposure on untrusted triggers |

### 3–5. CI runners, dependencies, and publishing
| Control | Addresses | Notes / evidence to capture |
|---|---|---|
| Use ephemeral, isolated runners for releases | TM-9, TM-10 | Runner type, isolation model, cache policy |
| Dependency/base image pinning and verification | TM-12, TM-13, TM-14 | Lockfiles, digests, provenance/SBOM if available |
| Prefer short-lived credentials (OIDC) for cloud publishes | TM-5, TM-15 | AWS/Azure federation configs; secret inventory |
| Prevent tag overwrite where possible | TM-16 | Registry policies; release immutability guidance |

### 6.x Distribution endpoints and consumers
| Control | Addresses | Notes / evidence to capture |
|---|---|---|
| Deploy by immutable image digest in Reduct Cloud | TM-18, TM-19 | Deployment manifests/policies referencing digests |
| Restrict write access to Azure binaries container | TM-20 | Storage RBAC/SAS usage and audit logs |
| Publish checksums (and optionally signatures) for binaries | TM-20, TM-21, TM-24 | Checksum files and verification instructions |
| Prefer digest-based references for Docker consumers docs | TM-22, TM-16 | Documentation guidance; release notes |
| Protect the download page publishing pipeline | TM-24, TM-25 | Site build/deploy controls; DNS/TLS controls |

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

## Open Context Items (To Confirm)
- Whether PRs from forks are accepted for public repos, and how CI is permissioned for them.
- Runner model: GitHub-hosted only vs any self-hosted runners.
- Release process trigger: tag-based, manual approval, or scheduled; who can publish.
- Artifact integrity posture: checksums/signatures (e.g., cosign/GPG) and whether they are required.
- Reduct Cloud deployment mechanism (e.g., ECS/EKS), and how image promotion to production is controlled/audited.
