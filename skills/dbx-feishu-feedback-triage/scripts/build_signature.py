#!/usr/bin/env python3
"""Build deterministic duplicate signatures for feedback cases."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


def read_json(path: str | None) -> Any:
    raw = sys.stdin.read() if not path or path == "-" else Path(path).read_text(encoding="utf-8")
    return json.loads(raw)


def normalize_text(value: Any) -> str:
    text = "" if value is None else str(value)
    text = text.lower()
    text = re.sub(r"https?://\S+", " URL ", text)
    text = re.sub(r"om_[a-z0-9_\-]+|oc_[a-z0-9_\-]+", " ID ", text, flags=re.I)
    text = re.sub(r"\b\d{6,}\b", " NUM ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:300]


def case_signature(case: dict[str, Any]) -> dict[str, Any]:
    facts = case.get("extracted_facts") or {}
    if not isinstance(facts, dict):
        facts = {}
    components = {
        "module": normalize_text(case.get("module") or facts.get("module")),
        "category": normalize_text(case.get("category")),
        "symptom": normalize_text(facts.get("symptom")),
        "expected": normalize_text(facts.get("expected")),
        "actual": normalize_text(facts.get("actual")),
        "error_codes": ",".join(sorted(str(x) for x in facts.get("error_codes", []) if x)),
        "requested_change": normalize_text(facts.get("requested_change")),
    }
    base = "|".join(components[k] for k in sorted(components))
    digest = hashlib.sha256(base.encode("utf-8")).hexdigest()[:16]
    return {"signature": f"fb:{digest}", "components": components}


def iter_cases(obj: Any) -> list[dict[str, Any]]:
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        if isinstance(obj.get("cases"), list):
            return [x for x in obj["cases"] if isinstance(x, dict)]
        return [obj]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description="Build feedback duplicate signatures from case JSON.")
    parser.add_argument("input", nargs="?", default="-", help="Feedback case/digest JSON path, or stdin")
    parser.add_argument("--all", action="store_true", help="Output signatures for all cases")
    parser.add_argument("--case-index", type=int, default=0, help="Case index when input is a digest")
    parser.add_argument("--text", action="store_true", help="Print signature only")
    args = parser.parse_args()

    cases = iter_cases(read_json(args.input))
    if not cases:
        print(json.dumps({"ok": False, "error": "no case found"}, ensure_ascii=False, indent=2))
        return 1

    if args.all:
        output = [dict(case_id=c.get("case_id", ""), **case_signature(c)) for c in cases]
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return 0

    if args.case_index < 0 or args.case_index >= len(cases):
        print(json.dumps({"ok": False, "error": "case index out of range"}, ensure_ascii=False, indent=2))
        return 1
    result = case_signature(cases[args.case_index])
    if args.text:
        print(result["signature"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
