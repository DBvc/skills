#!/usr/bin/env python3
"""Static lint for agent skill packages."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

from eval_schema import validate_eval_data

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    fm: dict[str, str] = {}
    for line in text[4:end].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, text[end + 4:]


def lint(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.exists():
        return {"ok": False, "errors": [f"Path does not exist: {path}"], "warnings": []}
    skill_files = list(path.rglob("SKILL.md"))
    if len(skill_files) != 1:
        errors.append(f"Expected exactly one SKILL.md, found {len(skill_files)}")
        return {"ok": False, "errors": errors, "warnings": warnings}
    text = skill_files[0].read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    name = fm.get("name", "")
    desc = fm.get("description", "")
    if not NAME_RE.match(name):
        errors.append("frontmatter name must be lowercase ASCII letters/numbers/hyphens and <=64 chars")
    if not desc:
        errors.append("frontmatter description is required")
    elif len(desc) > 1024:
        errors.append("description exceeds 1024 chars")
    body_lower = body.lower()
    required_terms = {
        "when not": "Non-use boundary is required",
        "hard gates": "Hard gates are required",
        "ir": "IR guidance is required",
        "workflow": "Workflow guidance is required",
        "output contract": "Output contract is required",
        "eval": "Eval guidance is required",
    }
    for term, msg in required_terms.items():
        if term not in body_lower:
            errors.append(msg)
    line_count = len(body.splitlines())
    if line_count > 500:
        warnings.append(f"SKILL.md body has {line_count} lines; ideal is under 500")
    if "```yaml" not in body_lower and "```json" not in body_lower:
        warnings.append("No schema-like block found")

    if name == "dbx-skill-architect":
        for term in (
            "route:",
            "operation:",
            "compatibility matrix",
            "needs_clarification",
            "eval_artifact_present",
            "eval kind single source",
            "patch-first",
            "runner-compatible",
            "check_architect_output.py",
        ):
            if term not in body_lower:
                errors.append(f"dbx-skill-architect missing required protocol term: {term}")
        # Do not teach the model invented eval kinds inside the main skill body.
        if 'invented alias as a `kind`' in body_lower:
            errors.append('dbx-skill-architect should list canonical kinds, not invented aliases')

    eval_path = path / "evals" / "evals.json"
    if not eval_path.exists():
        errors.append("Missing evals/evals.json")
    else:
        try:
            data = json.loads(eval_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid evals.json: {exc}")
        else:
            e, w = validate_eval_data(data if isinstance(data, dict) else {})
            errors.extend(e)
            warnings.extend(w)

    refs = path / "references"
    if refs.exists():
        for ref in refs.rglob("*.md"):
            rel = ref.relative_to(path)
            if len(rel.parts) > 3:
                warnings.append(f"Deeply nested reference: {rel}")
            ref_text = ref.read_text(encoding="utf-8")
            if len(ref_text.splitlines()) > 300 and "contents" not in ref_text.lower():
                warnings.append(f"Long reference without contents marker: {rel}")
    return {"ok": not errors, "errors": errors, "warnings": warnings}


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    result = lint(path)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
