# Incident Response Playbook

This playbook tells maintainers what to do when they receive or discover a security incident affecting
maintained ReductStore projects. It complements the
[Vulnerability Disclosure Policy](vulnerability-disclosure.md), the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md), the
[ENISA Vulnerability Reporting Procedure](enisa-reporting.md), the
[Security Advisory and Public Disclosure Process](security-advisory-process.md), and the
[Security Update Distribution and Patching Policy](security-update-policy.md).

## Status

- Owner: ReductSoftware UG
- Applies to: all maintained `reductstore/*` project repositories
- Review cadence: at least annually and after any incident
- CRA mapping: Article 11 and Annex I Part II, Requirements 2 and 6
- Related standards: ISO/IEC 27035 (incident management) and ISO/IEC 30111

## Scope

Use this playbook for security incidents involving:

- Product vulnerability exploitation: an actively exploited vulnerability in a shipped ReductStore
  product.
- Supply chain compromise: tampering or suspected tampering with dependencies, builds, packages,
  container images, or release artifacts.
- Infrastructure breach: compromise or suspected compromise of CI/CD, registries, maintainer
  accounts, release tokens, signing keys, or other project infrastructure.

If the report is only a suspected vulnerability and there is no incident yet, start with the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md).

## First Response

If you receive a vulnerability or incident report, do these steps first:

- [ ] Move the discussion to a private place, such as a GitHub Security Advisory, private issue, or
  encrypted email thread.
- [ ] Do not discuss the report in public issues, public pull requests, public chats, or social media.
- [ ] Record the report source, receipt time, affected product, affected version, and available
  evidence.
- [ ] Acknowledge external vulnerability reports within 48 hours under the
  [Vulnerability Disclosure Policy](vulnerability-disclosure.md#response-commitments).
- [ ] Assign an incident commander, triage owner, remediation owner, release manager, communications
  lead, and backup owner when required.
- [ ] Classify severity using the
  [triage policy](vulnerability-triage.md#severity-classification).
- [ ] Check whether the report shows
  [active exploitation](vulnerability-triage.md#criteria-for-actively-exploited).
- [ ] Escalate Critical, High, actively exploited, public, or potentially CRA-reportable incidents to
  ReductSoftware UG leadership.

One person may hold multiple roles when appropriate, but Critical and actively exploited
vulnerabilities require a backup owner under the triage policy.

## Severity and Timelines

Use the severity levels from the
[Vulnerability Triage and Severity Classification Policy](vulnerability-triage.md#severity-classification).

| Severity | First response | Containment target | Resolution target |
|----------|----------------|--------------------|-------------------|
| Critical | 1 hour | 4 hours | 24 hours |
| High | 4 hours | 24 hours | 72 hours |
| Medium | 24 hours | 72 hours | 7 days |
| Low | 48 hours | 7 days | Next release |

If a target cannot be met, record the reason, current risk, interim mitigation, owner, and new target
date in the private incident record.

## Response Runbook

### 1. Triage

- [ ] Confirm whether the report is credible.
- [ ] Identify affected products, versions, artifacts, repositories, and deployment assumptions.
- [ ] Assign severity, owner, backup owner, and target deadlines.
- [ ] Decide whether users are at immediate risk.
- [ ] Decide whether the
  [ENISA reporting trigger](vulnerability-triage.md#enisa-reporting-trigger) may apply.

### 2. Contain

- [ ] Restrict access to the incident details.
- [ ] Disable or rotate compromised credentials, tokens, deploy keys, and CI/CD secrets.
- [ ] Pull, quarantine, or mark affected artifacts when release integrity is uncertain.
- [ ] Disable vulnerable features, block abusive traffic, or provide temporary mitigation guidance when
  needed.
- [ ] Isolate compromised CI runners, release workflows, registries, or provider accounts.

### 3. Investigate

- [ ] Determine root cause, affected versions, affected artifacts, compromised accounts, and user
  impact.
- [ ] Build a timeline covering report, awareness, containment, remediation, release, notification,
  and closure.
- [ ] Preserve safe evidence such as logs, artifact hashes, image digests, build IDs, registry
  metadata, provider alerts, and indicators of compromise.

### 4. Remediate

- [ ] Prepare the fix, mitigation, dependency update, configuration change, or credential rotation.
- [ ] Validate the fix with review, tests, artifact checks, or provider verification.
- [ ] Keep remediation private until public disclosure is approved or users need immediate guidance.
- [ ] Use the
  [Security Update Distribution and Patching Policy](security-update-policy.md) for releases,
  packages, container images, checksums, release notes, and upgrade guidance.

### 5. Recover

- [ ] Restore normal operations only after containment and remediation are validated.
- [ ] Re-enable access and workflows with fresh secrets and reviewed permissions.
- [ ] Verify artifact integrity after recovery.
- [ ] Confirm that users have a fixed release, mitigation, or clear action to take.

### 6. Communicate

- [ ] Give internal updates every 4 hours for Critical incidents, daily for High incidents, and after
  material changes for Medium or Low incidents.
- [ ] Coordinate advisories and public disclosure through the
  [Security Advisory and Public Disclosure Process](security-advisory-process.md).
- [ ] Avoid publishing exploit details before users have a fix or mitigation unless early disclosure
  reduces risk.

## ENISA Reporting

Assess ENISA reporting immediately when a shipped ReductStore product vulnerability is actively
exploited or likely to be actively exploited.

The [ENISA Vulnerability Reporting Procedure](enisa-reporting.md) defines the full workflow. The key
deadlines are:

| Deadline | Action |
|----------|--------|
| Within 24 hours | Submit the early warning. |
| Within 72 hours | Submit or update the vulnerability notification. |
| Within 14 days after mitigation or corrective action is available | Submit the final report. |

Do not wait for a complete root cause analysis, fixed release, CVE, or public advisory before meeting
a required ENISA deadline.

## User Notification

Notify users when:

- Active exploitation is confirmed or likely.
- User data, credentials, release integrity, or deployment security may be affected.
- Users need to upgrade, rotate credentials, replace artifacts, verify image digests, change
  configuration, or take another action.

Use GitHub Security Advisories, release notes, changelog entries, package or registry metadata, direct
notification to known high-impact integrators, or project communication channels. Publish guidance
after containment when possible, but do not delay if users need immediate action to reduce risk.

## Post-Incident Review

Critical and High incidents require a review within 7 days of closure. Review Medium and Low
incidents when they reveal process gaps or repeated problems.

Record:

- What happened
- Who and what was affected
- Timeline
- Root cause
- What worked well
- What should improve
- Follow-up actions, owners, and deadlines

## Roles and Responsibilities

| Role | Responsibilities |
|------|------------------|
| Incident commander | Coordinate response, assign roles, maintain the incident record, run status updates, and confirm closure. |
| Triage owner | Validate impact, classify severity, assess active exploitation, and record technical rationale. |
| Remediation owner | Coordinate fixes, mitigations, credential rotations, tests, and validation. |
| Release manager | Coordinate fixed versions, artifacts, checksums, image digests, release notes, and publication. |
| Communications lead | Coordinate internal updates, advisories, user notifications, and approved public messaging. |
| Security maintainer | Review severity, containment decisions, CRA traceability, ENISA readiness, and evidence handling. |
| Legal or compliance reviewer | Advise on CRA obligations, ENISA reporting, personal-data handling, and regulator communication when available. |
| ReductSoftware UG leadership | Approve priorities, high-impact decisions, external communication posture, and closure. |

## Evidence and Audit Trail

Keep the private incident record up to date with:

- Report source, timestamps, category, severity, owners, and status
- Affected products, versions, artifacts, infrastructure, and users
- Severity rationale, active-exploitation assessment, ENISA assessment, and escalation decisions
- Containment actions, credential rotations, access changes, and recovery validation
- Root cause, timeline, logs, artifact hashes, image digests, build IDs, and provider alerts
- Fixes, commits, releases, advisories, CVE records, release notes, and user notifications
- Post-incident review notes and follow-up actions

Store incident evidence in a private, restricted-access location. Do not store secrets, exploit
payloads containing real user data, unnecessary personal data, or restricted incident evidence in
public documentation.
