# ENISA Vulnerability Reporting Procedure

This procedure defines how ReductSoftware UG reports actively exploited vulnerabilities affecting
ReductStore products to ENISA under the Cyber Resilience Act (CRA). It complements the
[Vulnerability Disclosure Policy](vulnerability-disclosure.md), the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md), and the
[Security Advisory and Public Disclosure Process](security-advisory-process.md).

## Status

- Owner: ReductSoftware UG
- Applies to: all maintained `reductstore/*` project repositories and shipped ReductStore products,
  SDKs, packages, binaries, and container images
- Review cadence: at least annually, after any reportable vulnerability, and when ENISA reporting
  platform requirements materially change
- CRA mapping: Article 11 and Annex I Part II, Requirement 6 (mandatory reporting of actively
  exploited vulnerabilities)
- Related standards: ISO/IEC 30111 (vulnerability handling) and ISO/IEC 29147 (vulnerability
  disclosure)

## Scope

This procedure applies when ReductSoftware UG becomes aware of a validated, actively exploited
vulnerability affecting a shipped ReductStore product, SDK, package, binary, container image, or
other official artifact within the scope of the
[Vulnerability Disclosure Policy](vulnerability-disclosure.md).

The procedure starts when the triage owner determines that the ENISA reporting trigger may apply
under the [Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md). It
covers internal escalation, ENISA single reporting platform registration and use, the 24-hour early
warning, the 72-hour vulnerability notification, the 14-day final report, and the required evidence
trail.

This procedure does not replace private intake, validation, severity classification, remediation,
public advisory publication, CVE assignment, or user notification. Those activities remain governed
by the sibling policies linked above.

## ENISA Single Reporting Platform

ReductSoftware UG uses the ENISA single reporting platform as the primary channel for CRA mandatory
vulnerability reporting when the platform is available and applicable to the report.

The security maintainer is responsible for maintaining platform readiness:

- Register the organization account or equivalent legal-entity profile before it is needed for an
  emergency submission.
- Assign at least two authorized reporting contacts with access to submit and update vulnerability
  reports.
- Record which internal roles have platform access and review access after personnel or role changes.
- Verify that contact details, legal entity information, and notification email addresses are current
  at least annually.
- Preserve platform confirmation identifiers, submission receipts, and timestamps in the private
  vulnerability tracking record.

When the ENISA platform is unavailable, inaccessible, or does not yet support the required workflow,
the security maintainer must record the outage or limitation, use any official fallback channel
identified by ENISA or the competent authority, and update the platform submission as soon as
practical.

## Trigger Criteria

ENISA reporting is required when all of the following conditions are met:

- The vulnerability has been validated under the ReductStore triage process.
- The affected component is a shipped ReductStore product, SDK, package, binary, container image, or
  official artifact used by supported users.
- There is credible evidence that the vulnerability is actively exploited or being used against real
  systems outside a controlled test environment.
- The vulnerability falls within ReductSoftware UG's CRA reporting obligations.

The criteria for active exploitation are defined in the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md#criteria-for-actively-exploited).
The triage owner must also follow that policy's
[ENISA reporting trigger](vulnerability-triage.md#enisa-reporting-trigger) and escalation path.

### CRA Reporting Obligation Assessment

For this procedure, a vulnerability falls within ReductSoftware UG's CRA reporting obligations when
all of the following are true:

- The affected product or component is a ReductSoftware UG product with digital elements made
  available to users, including products made available on the EU market.
- The affected version, SDK, package, binary, container image, or official artifact has been shipped,
  published, distributed, or otherwise made available outside ReductSoftware UG.
- ReductSoftware UG is the manufacturer, publisher, or responsible maintainer for the affected
  product or official artifact.
- The vulnerability affects the security of the product, its users, or downstream systems in a
  supported deployment or supported integration scenario.
- The vulnerability is actively exploited under the criteria in the triage policy.

The following cases do not normally fall within the ENISA reporting obligation unless legal or
compliance review determines otherwise:

- Vulnerabilities limited to internal development systems, test environments, or unreleased code.
- Test-only, example-only, CI-only, or development-only dependencies that are not present in shipped
  artifacts and do not affect release integrity.
- Unsupported third-party modifications, forks, deployments, or configurations outside
  ReductSoftware UG control.
- Upstream dependency vulnerabilities that are not present in shipped ReductStore artifacts, are not
  reachable in supported configurations, or do not affect supported users.
- Findings without a concrete product-security impact, such as purely informational scanner output or
  defense-in-depth hardening that does not remediate a specific vulnerability.

When the obligation assessment is uncertain, the triage owner must escalate for leadership and legal
or compliance review, preserve the awareness timestamp and evidence, and continue preparing the
24-hour early warning so that a mandatory deadline is not missed.

Speculation, scanner output without manual validation, or proof-of-concept code without evidence of
real-world use does not automatically trigger reporting. The triage owner may still escalate for
legal and compliance review when exploitation is likely, exposure is broad, or delaying the decision
could risk missing a CRA reporting deadline.

The reporting decision must be made by the triage owner, security maintainer, and ReductSoftware UG
leadership. If legal or compliance counsel is available, they should review the reporting decision,
but their unavailability must not delay a mandatory 24-hour early warning.

## Reporting Timeline

The reporting clock starts when ReductSoftware UG becomes aware that a vulnerability is actively
exploited and may be reportable under the CRA. The triage owner must record this awareness timestamp
in the private vulnerability tracking record.

| Deadline | Required action | Owner |
|----------|-----------------|-------|
| Without undue delay | Escalate internally, assign owners, restrict technical details, and preserve evidence | Triage owner |
| Within 24 hours | Submit the early warning through the ENISA reporting platform | Security maintainer |
| Within 72 hours | Submit or update the vulnerability notification with available technical and impact details | Security maintainer |
| Within 14 days after mitigation or corrective action is available | Submit the final report | Security maintainer and triage owner |

When exact information is not yet available, submit the best verified information by the deadline and
clearly mark unknown or pending fields. Do not delay a required submission to wait for complete root
cause analysis, full patch availability, CVE assignment, or advisory publication.

## 24-Hour Early Warning

The early warning alerts ENISA that an actively exploited vulnerability may affect a shipped
ReductStore product or artifact. It should be concise, factual, and limited to verified information.

Use this template for the early warning content:

| Field | Required content |
|-------|------------------|
| Reporter organization | ReductSoftware UG and the authorized reporting contact. |
| Awareness timestamp | Date and time when ReductSoftware UG became aware of active exploitation. |
| Affected product or artifact | Product, repository, SDK, package, binary, container image, or release line believed to be affected. |
| Vulnerability summary | Short description of the suspected vulnerability class and affected component. |
| Active exploitation basis | Evidence category, such as reporter evidence, customer report, telemetry, public exploitation, upstream confirmation, CERT, CSIRT, or regulator notice. |
| Known impact | Confirmed or suspected confidentiality, integrity, availability, or safety impact. |
| Exposure scope | Known affected versions, deployment assumptions, and whether default configurations are affected. |
| Immediate actions | Containment, mitigation, private remediation, user guidance, or investigation actions already started. |
| Disclosure status | Whether the vulnerability is private, publicly known, under embargo, or already disclosed. |
| Next update | Planned 72-hour notification target and responsible ReductSoftware UG contact. |

Before submission, the triage owner must verify that the content does not include secrets, customer
data, exploit payloads, unnecessary personal data, or unvalidated claims. The security maintainer
submits the early warning and records the platform confirmation identifier and submission timestamp.

## 72-Hour Vulnerability Notification

The vulnerability notification updates the early warning with a fuller technical and impact
assessment. It must be submitted within 72 hours of awareness even if remediation is still in
progress.

Use this template for the 72-hour notification content:

| Field | Required content |
|-------|------------------|
| Report reference | ENISA platform identifier, early warning reference, and internal tracking identifier. |
| Affected products | Products, repositories, versions, packages, SDKs, binaries, images, and supported deployment assumptions. |
| Technical description | Vulnerability type, affected component, prerequisites, attack vector, and root cause if known. |
| Severity | CVSS v3.1 score, vector, severity, operational priority, and rationale from the triage policy. |
| Exploitation status | Evidence of active exploitation, indicators of compromise when safe to share, and known exploitation scope. |
| Impact assessment | Confirmed or likely impact on confidentiality, integrity, availability, users, or downstream systems. |
| Corrective actions | Patches, mitigations, configuration guidance, release targets, and temporary containment measures. |
| User communication | Advisory, release note, direct notification, or embargo status, including planned timing. |
| Open items | Unknowns, pending validation, pending releases, and planned follow-up updates. |
| Contact and owner | Triage owner, security maintainer, and authorized reporting contact. |

The 72-hour notification may reference a CVE, GitHub Security Advisory, release, or public advisory
only when those records are already available or safe to disclose. If public disclosure would
increase user risk before a fix or mitigation is available, the notification should explain the
embargo status and planned disclosure path without publishing exploit-enabling detail.

## 14-Day Final Report

The final report closes the mandatory reporting flow after mitigation or corrective action is
available. It must summarize what happened, what was affected, what was fixed, and what residual risk
remains.

Use this template for the final report content:

| Field | Required content |
|-------|------------------|
| Report reference | ENISA platform identifier, prior submission references, CVE, and advisory identifiers when available. |
| Final affected scope | Confirmed affected products, repositories, versions, packages, SDKs, binaries, images, and unsupported or unaffected versions where relevant. |
| Root cause | Technical and process root cause at the level appropriate for regulatory reporting. |
| Exploitation summary | Confirmed exploitation timeline, scope, observed indicators, and any known user impact. |
| Corrective actions completed | Fixed versions, patches, mitigations, configuration guidance, release notes, advisories, and user notifications. |
| Verification evidence | Tests, review evidence, release validation, dependency validation, or mitigation validation. |
| Residual risk | Remaining exposure, unsupported versions, temporary mitigations, known limitations, and follow-up work. |
| Lessons learned | Process improvements, monitoring updates, documentation changes, or future preventive actions. |
| Closure owner | Person responsible for confirming final report accuracy and retaining evidence. |

The final report should align with the advisory fields defined in the
[Security Advisory and Public Disclosure Process](security-advisory-process.md#advisory-content-template),
but it may include private regulatory context that is not suitable for the public advisory. Public
advisory text must continue to avoid unnecessary exploit detail, secrets, customer data, and personal
data.

## Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| Triage owner | Confirm the ENISA trigger assessment, record the awareness timestamp, coordinate technical validation, maintain the private tracking record, and provide report content. |
| Security maintainer | Maintain ENISA platform readiness, submit early warning, notification, and final report, record platform receipts, and review CRA traceability. |
| Remediation owner | Coordinate fixes, mitigations, tests, release artifacts, and technical evidence for report updates. |
| Release manager | Coordinate fixed versions, packages, container images, changelog entries, release notes, and publication timing. |
| ReductSoftware UG leadership | Approve reportability decisions, resource prioritization, external communication posture, and final report closure. |
| Legal or compliance reviewer | Advise on CRA obligations, personal-data handling, regulator communication, and fallback reporting channels when available. |

One person may hold multiple roles when appropriate, but actively exploited vulnerabilities require a
backup owner under the [Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md#triage-owner).

## Checklist and Runbook

Use this checklist for every suspected reportable vulnerability:

- [ ] Confirm the report is tracked in a private location with restricted access.
- [ ] Record the initial report receipt timestamp and the active-exploitation awareness timestamp.
- [ ] Assign the triage owner, security maintainer, remediation owner, release manager, and backup
  owner.
- [ ] Validate affected products, versions, artifacts, deployment assumptions, and supported-user
  impact.
- [ ] Assess active exploitation using the triage policy criteria and record the evidence basis.
- [ ] Escalate to ReductSoftware UG leadership and legal or compliance review when available.
- [ ] Decide whether the CRA ENISA reporting trigger applies and record the decision rationale.
- [ ] Prepare the 24-hour early warning using verified information only.
- [ ] Submit the early warning through the ENISA reporting platform or approved fallback channel.
- [ ] Record the submission timestamp, confirmation identifier, submitter, and content snapshot.
- [ ] Continue validation, severity classification, remediation planning, and user-risk assessment.
- [ ] Prepare the 72-hour vulnerability notification with technical, impact, and corrective-action
  details.
- [ ] Submit or update the 72-hour notification and record the confirmation evidence.
- [ ] Prepare patches, mitigations, releases, advisories, CVE request, and user notifications under
  the sibling policies.
- [ ] Submit interim updates through the ENISA platform if material facts, impact, or corrective
  actions change before the final report.
- [ ] Prepare the 14-day final report after mitigation or corrective action is available.
- [ ] Submit the final report and record the confirmation evidence.
- [ ] Retain the audit trail and update lessons learned, process improvements, or follow-up work.

## Evidence and Audit Trail

For each ENISA reporting assessment or submission, maintainers should retain:

- Report receipt timestamp and active-exploitation awareness timestamp
- ENISA reporting trigger assessment, reporting decision, and decision approvers
- Triage owner, security maintainer, remediation owner, release manager, and backup owner
- ENISA platform account or fallback channel used for submission
- Early warning, 72-hour notification, final report, and any interim update content snapshots
- Platform confirmation identifiers, submission timestamps, receipt emails, and submitter identity
- Affected products, versions, packages, SDKs, binaries, container images, and deployment assumptions
- Severity, CVSS v3.1 score, exploitability assessment, and impact analysis
- Evidence supporting active exploitation and any safe-to-retain indicators of compromise
- Remediation plans, mitigation guidance, fixed versions, release notes, advisories, and CVE records
- Internal approval records, disclosure decisions, user notification decisions, and lessons learned

Store ENISA reporting evidence in the private vulnerability tracking location. Do not store secrets,
exploit payloads containing real user data, unnecessary personal data, customer data, or restricted
incident evidence in public documentation.
