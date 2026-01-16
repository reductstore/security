# Repository Guidelines

## Purpose
This repository contains documentation for Cyber Resilience Act (CRA) compliance and security standards for the ReductStore project. Keep changes focused on documentation quality, correctness, and traceability.

## Project Structure & Module Organization
- `README.md`: entry point and high-level overview.
- `docs/`: place new documentation here (create as needed), grouped by area (e.g., `docs/policies/`, `docs/threat-models/`, `docs/checklists/`).
- `.idea/`: local IDE settings; avoid committing user-specific workspace files where possible.

## Build, Test, and Development Commands
This is a documentation-only repository; there is no build output or runtime.
- `rg "<term>" .`: fast search across docs.
- `git diff`: review changes before opening a PR.
- Optional (if installed): `markdownlint "**/*.md"` to catch common Markdown issues.

## Coding Style & Naming Conventions
- Markdown: use ATX headings (`#`, `##`), blank lines between sections, and fenced code blocks with a language tag (e.g., ```bash).
- Keep lines reasonably short (aim ~100 chars) and prefer lists/checklists for requirements.
- File naming: use kebab-case and stable paths (e.g., `docs/policies/vulnerability-disclosure.md`).
- When referencing identifiers, use consistent patterns (e.g., `CVE-YYYY-NNNN`, “CRA Article X”, “ISO/IEC 27001”).

## Testing Guidelines
No automated tests are currently configured. Validate documentation manually:
- Ensure links are correct and relative links resolve within the repo.
- Prefer reproducible “how to verify” steps (commands, expected outputs) in security checklists.

## Commit & Pull Request Guidelines
- Commits: keep messages short and imperative (the existing history uses messages like “add README”). If helpful, prefix by area (e.g., `docs: update threat model`).
- PRs: describe the intent, scope, and any impacted documents; link relevant issues/requirements; call out breaking doc reorganizations (moves/renames).

## Security & Compliance Notes
- Do not commit secrets, credentials, internal URLs, or customer data—use placeholders and examples.
- Cite sources for standards/regulatory claims and avoid pasting licensed text verbatim unless permitted.

## Agent-Specific Instructions
- Keep changes minimal and avoid repo-wide reformatting unless explicitly requested.
- Prefer adding new docs under `docs/` over expanding `README.md` with long content.
