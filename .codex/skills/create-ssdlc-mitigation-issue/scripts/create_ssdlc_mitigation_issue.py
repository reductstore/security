#!/usr/bin/env python3

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


THREAT_MODEL_PATH = Path("docs/threat-modeling/threat-model-risk-assessment.md")
GUIDE_REPO_SETUP = Path("docs/guides/secure-github-repo-setup.md")
GUIDE_USER_MGMT = Path("docs/guides/github-user-management.md")

DEFAULT_REPOS = [
    "reductstore",
    "reduct-rs",
    "reduct-cpp",
    "reduct-js",
    "reduct-go",
    "reduct-py",
    "reduct-cli",
    "web-console",
    "reductstore-pro",
    "reduct-grafana",
    "reduct-bridge",
]


@dataclass(frozen=True)
class MitigationRow:
    line_index: int
    priority: str
    control: str
    addresses: str
    notes: str
    status: str
    tracking: str


def run(cmd: List[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a tracking issue for an SSDLC mitigation control and update the threat model table."
        )
    )
    parser.add_argument(
        "--control",
        required=True,
        help="Exact Control string as it appears in the mitigation candidates table.",
    )
    parser.add_argument(
        "--repos",
        nargs="+",
        default=[],
        help=(
            "Repos to implement the mitigation in. "
            "If omitted, uses the standard ReductStore repo list."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not create an issue or modify files; print the generated issue body.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow updating a row that already has a non-TODO tracking value.",
    )
    parser.add_argument(
        "--title-prefix",
        default="Mitigation:",
        help='Issue title prefix (default: "Mitigation:").',
    )
    return parser.parse_args()


def normalize_cell(value: str) -> str:
    value = value.strip()
    value = re.sub(r"<a\s+id=\"[^\"]+\"></a>", "", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return re.sub(r"\s+", " ", value)


def parse_markdown_table_row(line: str) -> Optional[Tuple[str, str, str, str, str, str]]:
    if not line.lstrip().startswith("|"):
        return None
    if re.match(r"^\|\s*-+\s*\|", line):
        return None
    cells = [normalize_cell(c) for c in line.strip().strip("|").split("|")]
    # Backwards-compatible parsing:
    # - legacy table format: Priority | Control | Addresses | Notes | Tracking
    # - current table format: Priority | Control | Addresses | Notes | Status | Tracking
    if len(cells) == 5:
        priority, control, addresses, notes, tracking = cells
        status = ""
    elif len(cells) == 6:
        priority, control, addresses, notes, status, tracking = cells
    else:
        return None
    if not priority or not control:
        return None
    return priority, control, addresses, notes, status, tracking


def find_mitigation_row(control_name: str, content: str) -> MitigationRow:
    wanted = normalize_cell(control_name)
    for idx, line in enumerate(content.splitlines()):
        parsed = parse_markdown_table_row(line)
        if not parsed:
            continue
        priority, control, addresses, notes, status, tracking = parsed
        if control == wanted:
            return MitigationRow(
                line_index=idx,
                priority=priority,
                control=control,
                addresses=addresses,
                notes=notes,
                status=status,
                tracking=tracking,
            )
    raise SystemExit(
        f'Control not found in mitigation tables: "{control_name}". '
        f'Check {THREAT_MODEL_PATH} and copy the Control cell exactly.'
    )


def build_issue_body(row: MitigationRow, repos: List[str]) -> str:
    tm_ids = [t.strip() for t in row.addresses.split(",") if t.strip()]
    tm_list = ", ".join(tm_ids) if tm_ids else row.addresses

    checklist = "\n".join(
        [f"- [ ] Apply mitigation in `{r}` (code/pipeline/settings as needed)" for r in repos]
    )

    guidance_links: List[str] = []
    if GUIDE_REPO_SETUP.exists():
        guidance_links.append(f"- [{GUIDE_REPO_SETUP}]({GUIDE_REPO_SETUP})")
    if GUIDE_USER_MGMT.exists():
        guidance_links.append(f"- [{GUIDE_USER_MGMT}]({GUIDE_USER_MGMT})")
    guidance_links.append(f"- [{THREAT_MODEL_PATH}]({THREAT_MODEL_PATH}) (Mitigation Candidates table)")

    evidence = row.notes if row.notes and row.notes != "TODO" else "TBD"

    return "\n".join(
        [
            "# SSDLC Mitigation",
            "",
            "## Control",
            f"- **Control:** {row.control}",
            "",
            "## Threat model coverage",
            f"- **Addresses:** {tm_list}",
            f"- **Priority (from threat model):** {row.priority}",
            "",
            "## Motivation / Context",
            f"This mitigation is proposed to reduce risk for: {tm_list}.",
            "",
            "## Implementation guidance",
            *guidance_links,
            "",
            "## Evidence to capture",
            f"- {evidence}",
            "",
            "## Affected repositories",
            "Apply the relevant changes (code/pipeline/settings) per repository:",
            "",
            checklist,
            "",
            "## Completion criteria",
            "- Table row tracking link updated in the threat model.",
            "- Each repo checklist item has a link to the implementing PR(s) or change record(s).",
            "",
        ]
    )


def create_issue(title: str, body: str) -> Tuple[int, str]:
    tmp = Path("/tmp/ssdlc_mitigation_issue.md")
    tmp.write_text(body, encoding="utf-8")

    output = run(["gh", "issue", "create", "--title", title, "--body-file", str(tmp)])
    match = re.search(r"/issues/(\d+)", output)
    if not match:
        raise SystemExit(f"Could not parse issue number from gh output: {output}")
    number = int(match.group(1))
    url = output.strip()
    return number, url


def update_tracking_cell(
    content: str, row: MitigationRow, issue_number: int, issue_url: str, force: bool
) -> str:
    if row.tracking != "TODO" and not force:
        raise SystemExit(
            f'Row already tracked (Tracking="{row.tracking}"). Re-run with --force to overwrite.'
        )

    lines = content.splitlines()
    original = lines[row.line_index]
    if not original.lstrip().startswith("|"):
        raise SystemExit("Internal error: expected table row line.")

    updated_tracking = f"[#{issue_number}]({issue_url})"

    cells = [c for c in original.strip().strip("|").split("|")]
    if len(cells) not in (5, 6):
        raise SystemExit("Internal error: unexpected table row cell count.")

    cells[-1] = f" {updated_tracking} "
    new_line = "|" + "|".join(cells) + "|"
    lines[row.line_index] = new_line
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()

    content = THREAT_MODEL_PATH.read_text(encoding="utf-8")
    row = find_mitigation_row(args.control, content)

    repos = args.repos or DEFAULT_REPOS

    issue_title = f"{args.title_prefix} {row.control}"
    issue_body = build_issue_body(row=row, repos=repos)

    if args.dry_run:
        print(issue_title)
        print("---")
        print(issue_body)
        return

    issue_number, issue_url = create_issue(title=issue_title, body=issue_body)
    updated = update_tracking_cell(
        content=content, row=row, issue_number=issue_number, issue_url=issue_url, force=args.force
    )
    THREAT_MODEL_PATH.write_text(updated, encoding="utf-8")

    print(f"Created issue: {issue_url}")
    print(f"Updated: {THREAT_MODEL_PATH}")


if __name__ == "__main__":
    main()
