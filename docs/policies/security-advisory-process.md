# Security Advisory and Public Disclosure Process

This policy defines how ReductSoftware UG publishes security advisories and coordinates public
disclosure for fixed vulnerabilities affecting ReductStore projects. It complements the
[Vulnerability Disclosure Policy](vulnerability-disclosure.md), which defines intake and coordinated
disclosure expectations, and the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md), which defines
classification, remediation SLAs, escalation, and evidence requirements.

## Status

- Owner: ReductSoftware UG
- Applies to: all maintained `reductstore/*` project repositories
- Review cadence: at least annually and after any material security incident
- CRA mapping: Article 11 and Annex I Part II, Requirement 4 (public disclosure of fixed
  vulnerabilities, advisory publication, and user notification)
- Related standards: ISO/IEC 29147 (vulnerability disclosure) and FIRST CVSS v3.1

## Scope

This policy applies to public disclosure of fixed vulnerabilities in maintained ReductStore software,
release artifacts, and official project infrastructure that can affect the security of users or
downstream systems.

In-scope repositories match the [Vulnerability Disclosure Policy](vulnerability-disclosure.md).

This policy governs advisory publication, CVE assignment, embargo coordination, release-note
integration, and downstream notification. It does not replace vulnerability reporting, validation,
classification, or remediation tracking, which are handled by the disclosure and triage policies.

## GitHub Security Advisories as Primary Mechanism

ReductStore maintainers publish security advisories through GitHub Security Advisories in the
affected repository. The repository-level advisory is the canonical public record for affected
versions, fixed versions, severity, CVE assignment, mitigations, credits, and references.

Maintainers should use GitHub Security Advisories to keep remediation private before disclosure:

1. Create or update a private draft advisory in the affected repository.
2. Add the triage owner, remediation maintainers, release manager, and security maintainer as
   collaborators when they need access.
3. Use the advisory private fork or another restricted remediation branch for fixes when public
   pull requests would disclose technical details before release.
4. Review advisory content, affected versions, fixed versions, CVSS v3.1 scoring, credits, and
   references before publication.
5. Publish the advisory after fixed releases, packages, images, or mitigations are available and
   disclosure timing has been approved.

The normal advisory lifecycle is draft, review, and publish. Drafts remain private to maintainers
and approved collaborators. Review confirms technical accuracy, CVSS scoring, upgrade guidance, and
CRA traceability. Publishing makes the advisory public and triggers GitHub notifications to affected
users and dependent projects where GitHub can determine impact.

When a vulnerability affects one repository, publish the advisory in that repository. When a
vulnerability affects multiple repositories, designate a primary repository for the canonical
advisory and link related advisories, releases, and upgrade instructions from each affected
repository. Organization-level coordination should be tracked privately until all affected releases
are ready for public disclosure.

## CVE Assignment via GitHub CNA

GitHub acts as a CVE Numbering Authority (CNA) for GitHub Security Advisories. Maintainers should
request a CVE through the GitHub advisory workflow when a validated, in-scope vulnerability has a
credible security impact on supported ReductStore users or official artifacts.

Request a CVE when the finding is:

- A validated product, dependency, release-integrity, or official-artifact vulnerability
- In scope for a maintained ReductStore repository
- Security-relevant for supported users or downstream systems
- Suitable for public tracking as a distinct vulnerability

A CVE is usually not needed for:

- Informational findings without a concrete security impact
- Defense-in-depth hardening that does not remediate a specific vulnerability
- Configuration mistakes limited to an unsupported deployment
- Issues that affect only development, test, example, or CI code without release-integrity impact
- Duplicate reports already covered by another advisory or upstream CVE

CVE identifiers must use the `CVE-YYYY-NNNN` format. Published advisories, changelog entries,
release notes, and downstream notifications should link to the CVE record when it is available. If
the advisory is published before the CVE record is populated, update references after the CVE becomes
public.

## Advisory Content Template

Every published security advisory must include enough information for users to determine exposure,
upgrade safely, and understand residual mitigations.

| Field | Requirement |
|-------|-------------|
| Title | Short, descriptive summary of the vulnerability and affected component. |
| Description | Vulnerability type, root cause, affected behavior, and security impact. |
| Affected versions | Semver ranges, packages, container images, binaries, SDKs, or other artifacts. |
| Fixed versions | Corrected versions and the recommended upgrade path. |
| CVSS v3.1 | Base score and vector string reviewed under the triage policy. |
| Severity | Critical, High, Medium, or Low, consistent with the triage classification. |
| Credits | Reporter attribution when permitted by the reporter and appropriate for disclosure. |
| Workarounds or mitigations | Temporary guidance when users cannot immediately upgrade or no full fix exists. |
| References | Related commits, pull requests, releases, CWE entries, upstream advisories, and CVE. |
| Timeline | Reported, acknowledged, fixed, released, and disclosed dates where appropriate. |

Advisory content must avoid secrets, customer data, unnecessary personal data, and exploit details
that are not needed for users to assess and remediate exposure.

## Embargo and Coordination Window

The default embargo pattern is to prepare the fix privately, publish corrected artifacts, and publish
the advisory at the coordinated disclosure point. Disclosure timing must respect the coordinated
disclosure window defined in the [Vulnerability Disclosure Policy](vulnerability-disclosure.md) and
the remediation deadlines defined in the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md).

When feasible, maintainers should provide at least 24 hours between availability of fixed binaries,
packages, container images, or documented mitigations and publication of full technical advisory
details. This upgrade window may be shortened when users need immediate public guidance.

For vulnerabilities spanning multiple repositories, such as server and SDK changes, all required
releases should ship before any advisory goes public. The primary advisory should link to each
affected repository, release, package, image, and upgrade instruction.

Early disclosure may be required when:

- The vulnerability is actively exploited.
- The vulnerability has leaked or is already publicly known.
- An upstream advisory, dependency advisory, or third-party advisory is already public.
- Users need mitigation guidance before a complete fix is available.

Embargoes may be extended only when the extension is justified and documented, such as when a fix is
complex, validation is incomplete, downstream coordination is still in progress, or premature
disclosure would materially increase user risk. Extensions must identify an owner, revised target
date, interim mitigation plan, and communication plan.

## Changelog and Release Notes Integration

Every security fix must be documented in the affected repository `CHANGELOG.md` or equivalent release
history. The entry should identify the change as a security fix and reference the advisory and CVE
when available.

Release notes for fixed versions must:

- Reference the published or pending security advisory.
- Link to upgrade instructions and fixed versions.
- Identify affected packages, binaries, SDKs, or container images.
- Include mitigation guidance when users cannot immediately upgrade.

For container images, release notes and advisories must provide tag-based upgrade guidance, including
the fixed tag and any affected tags or ranges that users should replace.

## Downstream Notification Process

Published GitHub Security Advisories provide the primary notification mechanism for repository
watchers, dependent repositories, and Dependabot alerts where GitHub can map affected packages or
versions.

Maintainers should add additional notification when the vulnerability is high impact, likely to
affect known integrators, or requires coordinated changes across server and client components.

Notification options include:

- Direct notification to known high-impact downstream users or integrators when appropriate and
  permitted.
- GitHub release notes and repository discussions that link to the advisory and fixed release.
- Package, SDK, or container registry release metadata where supported.
- Coordinated advisories for SDK or client libraries when the vulnerability spans server and client
  behavior.

Notifications should provide practical upgrade or mitigation instructions and avoid disclosing
unnecessary exploit detail beyond what users need to assess exposure.

## Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| Triage owner | Draft advisory, confirm affected versions, collect timeline evidence, and contact reporter. |
| Release manager | Coordinate fixed releases, packages, images, changelog, release notes, and publication timing. |
| Security maintainer | Review CVSS v3.1 scoring, severity, CVE request, embargo decisions, and CRA traceability. |
| Reporter | Confirm credit preference, disclosure constraints, and advisory details when invited. |

One person may hold multiple roles when appropriate, but Critical and actively exploited
vulnerabilities require a separate backup owner under the triage policy.

## Evidence and Audit Trail

For each published advisory, maintainers should retain:

- Advisory identifier, CVE identifier, and affected repository
- Advisory draft creation timestamp, review decisions, and publication timestamp
- CVE request timestamp, CVE assignment, and CVE publication status
- Affected versions, fixed versions, packages, images, and artifacts
- CVSS v3.1 score, vector string, severity, and scoring rationale
- Embargo decisions, early disclosure decisions, extensions, and approval records
- Release notes, changelog entries, commits, pull requests, tags, packages, and image references
- Reporter credit decision and relevant disclosure communications
- Downstream notification records and public announcement links

These records supplement the evidence requirements in the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md). Do not store
secrets, exploit payloads containing real user data, unnecessary personal data, or restricted
incident evidence in public documentation.
