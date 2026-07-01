# Security Update Distribution and Patching Policy

This policy defines how ReductSoftware UG provides security updates, publishes official artifacts,
and communicates upgrade guidance for ReductStore projects. It complements the
[Vulnerability Disclosure Policy](vulnerability-disclosure.md), the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md), and the
[Security Advisory and Public Disclosure Process](security-advisory-process.md).

## Status

- Owner: ReductSoftware UG
- Applies to: all maintained `reductstore/*` project repositories
- Review cadence: at least annually and after any material security incident
- CRA mapping: Article 11 and Annex I Part II, Requirements 7 and 8
- Related standards: ISO/IEC 30111 (vulnerability handling) and ISO/IEC 29147
  (vulnerability disclosure)

## Scope

This policy applies to security updates for supported ReductStore server, SDK, CLI/tooling,
bridge, and web-console projects, including official packages, binaries, container images, and
release metadata.

In-scope repositories match the [Vulnerability Disclosure Policy](vulnerability-disclosure.md).

This policy covers official distribution channels maintained by ReductSoftware UG or the affected
project maintainers. It does not cover unsupported forks, modified third-party redistributions,
unofficial mirrors, or deployment-specific packaging maintained outside the ReductStore project.

## Supported Versions Matrix

Security updates are provided for supported versions according to the following support windows,
unless a repository-specific `SECURITY.md` states a broader or more specific support window.

| Project type | Support window |
|--------------|----------------|
| Server (`reductstore`, `reductstore-pro`) | Latest minor version |
| SDKs (`reduct-rs`, `reduct-py`, `reduct-js`, `reduct-go`, `reduct-cpp`) | Latest minor version |
| CLI tools (`reduct-cli`) | Latest minor version |
| Bridge (`reduct-bridge`) | Latest minor version |
| Web console (`web-console`) | Latest minor version |

For example, when `1.20.3` is the latest stable release, the supported window is `1.20.x` and
`1.19.x` is not supported by default. Users should upgrade to the latest stable version when a
security update is published, consistent with the supported-version statement in the
[Vulnerability Disclosure Policy](vulnerability-disclosure.md#supported-versions).

## Free-of-Charge Security Updates

ReductSoftware UG provides security updates free of charge for supported ReductStore versions. This
commitment applies to fixes, mitigations, or upgrade guidance published through official project
channels and supports CRA Annex I Part II, Requirement 8.

Commercial licensing, support contracts, or access controls for private repositories do not change
the obligation to make security updates available for supported versions through the appropriate
official channel.

## Distribution Channels

Official security updates are distributed through the release channels maintained by each project.
Public projects are also available as source through their public GitHub repositories.

| Project | Channel(s) |
|---------|------------|
| Server CE (`reductstore`) | Docker Hub, GitHub Releases, Azure Storage, Git (public) |
| Server Pro (`reductstore-pro`) | Docker Hub, Azure Storage (private repository) |
| `reduct-rs` | crates.io, GitHub Releases, Git (public) |
| `reduct-py` | PyPI, GitHub Releases, Git (public) |
| `reduct-js` | npm, GitHub Releases, Git (public) |
| `reduct-go` | Go module proxy, GitHub Releases, Git (public) |
| `reduct-cpp` | Conan, GitHub Releases, Git (public) |
| `reduct-cli` | GitHub Releases, crates.io, Git (public) |
| `reduct-bridge` | Docker Hub, GitHub Releases, Git (public) |
| `web-console` | GitHub Releases, Git (public) |

Exact package names, registry namespaces, image names, storage paths, and release automation are
maintained in each repository's release configuration.

## Integrity Verification

Maintainers should publish SHA-256 checksums alongside binary release artifacts distributed through
GitHub Releases or Azure Storage. Users should verify downloaded binaries against the published
checksum before installation or deployment.

For container images, security advisories and release notes must provide digest-based references so
users can pin or verify the corrected image content. This supports the threat model mitigations to
[publish checksums](../threat-modeling/threat-model-risk-assessment.md#mit-publish-checksums) and
[prefer digest-based Docker references](../threat-modeling/threat-model-risk-assessment.md#mit-digest-based-docker-docs).

Binary and container image signing is a planned capability tracked with the checksum mitigation. This
policy does not treat signatures as a current guarantee unless the affected repository's release
documentation states that signatures are published and supported for that artifact.

## Expedited Release Process for Critical Security Fixes

Critical and actively exploited vulnerabilities may bypass the normal release cadence, including
feature batching, non-security release freezes, or scheduled release windows, when an expedited fix
is needed to reduce user risk.

The expedited release target must align with the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md#triage-slas). For
Critical or actively exploited vulnerabilities, maintainers should publish a corrected release,
mitigation, or upgrade guidance as fast as practical, targeting the 7-day remediation SLA from
severity classification.

Expedited security releases should be minimal-change, security-only releases where practical to
reduce regression risk and simplify user upgrades. Release communication must follow the
[Security Advisory and Public Disclosure Process](security-advisory-process.md), including advisory,
changelog, release-note, and downstream notification requirements.

  ## Backport Policy

Security fixes are backported according to severity, supported-version scope, and the risk of the
backport itself.

| Severity | Backport expectation |
|----------|----------------------|
| Critical | Backport to all supported versions. |
| High | Backport to all supported versions. |
| Medium | Include in the next scheduled release of the latest minor version. |
| Low | Include in the next scheduled release; expedited release is not mandatory. |

Because the default support window is the latest minor version, backporting primarily applies to
patch releases within the current minor version. Backport exceptions must be documented with
rationale, residual risk, affected versions, and user guidance, and communicated in the relevant
security advisory when users are affected.

## Notification and Communication

Every security fix must be documented in the affected repository's changelog or equivalent release
history. Release notes must identify the corrected version, affected artifacts, upgrade path, and any
temporary mitigations users need before upgrading.

Security advisory publication, CVE references, embargo coordination, changelog requirements, and
downstream notification are governed by the
[Security Advisory and Public Disclosure Process](security-advisory-process.md). For container image
users, advisories and release notes must include tag-based upgrade guidance and digest-based image
references.

## Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| Release manager | Coordinate security releases, backports, channel publication, changelog, and release notes. |
| Security maintainer | Review patch scope, confirm integrity artifacts, and align release communication with the advisory process. |
| Triage owner | Confirm severity, remediation SLA, affected scope, and backport requirements. |

One person may hold multiple roles when appropriate, but Critical and actively exploited
vulnerabilities require backup ownership under the triage policy.

## Evidence and Audit Trail

For each security update, maintainers should retain:

- Release artifacts, package references, container image references, and registry metadata
- SHA-256 checksums, digest references, and other integrity verification artifacts
- Backport decisions, exception rationale, residual-risk notes, and approval records
- Changelog entries, release notes, advisory links, CVE references, and notification timestamps
- Pull requests, commits, tags, release automation logs, and publication records

These records supplement the evidence requirements in the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md) and the
[Security Advisory and Public Disclosure Process](security-advisory-process.md). Do not store
secrets, exploit payloads containing real user data, unnecessary personal data, or restricted
incident evidence in public documentation.
