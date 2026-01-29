---
name: create-ssdlc-mitigation-issue
description: Create a tracking GitHub issue for an SSDLC mitigation control listed in docs/threat-modeling/threat-model-risk-assessment.md (Mitigation Candidates), including TM IDs addressed, motivation, links to docs/guides, and a per-repo implementation checklist; then update the mitigation table Tracking column with the created issue link.
---

# Create SSDLC Mitigation Issue

## Workflow

### 1) Preconditions
- Be on the branch where you want to record tracking links.
- Ensure `gh auth status` is logged in.

### 2) Pick the mitigation control name (exact match)
Choose a **Control** value from:
`docs/threat-modeling/threat-model-risk-assessment.md` → “Mitigation Candidates (To Be Confirmed/Implemented)”.

### 3) Create the issue and update the table
Run the helper script with a list of repos where the mitigation must be implemented:

```bash
python3 .codex/skills/create-ssdlc-mitigation-issue/scripts/create_ssdlc_mitigation_issue.py \
  --control "Enforce branch protections + required reviews" \
  --repos reductstore/reductstore reductstore/security
```

If the control name contains backticks (e.g., ``Least-privilege `GITHUB_TOKEN` permissions``), use single quotes:

```bash
python3 .codex/skills/create-ssdlc-mitigation-issue/scripts/create_ssdlc_mitigation_issue.py \
  --control 'Least-privilege `GITHUB_TOKEN` permissions' \
  --repos reductstore/reductstore reductstore/security
```

The script will:
- Look up the mitigation row (Priority, TM IDs, evidence notes).
- Create a GitHub issue in the current repo with:
  - TM(s) addressed
  - motivation/context
  - links to `docs/guides/*` and the threat model
  - a per-repo implementation checklist
- Update the mitigation row’s “Tracking (issue/PR)” cell from `TODO` to an issue link.

### 4) Review and commit (no push unless asked)
```bash
git diff
git add docs/threat-modeling/threat-model-risk-assessment.md
git commit -m "docs: track mitigation <short control name>"
```

## Notes
- If the table row is already tracked (not `TODO`), re-run with `--force`.
- Use `--dry-run` to preview the issue body and table edit without creating anything.
