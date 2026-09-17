#!/usr/bin/env python3
"""Versioned eval-schema regression tests."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from eval_schema import validate_eval_file  # noqa: E402


def case(case_id: str, kind: str, check: dict[str, object]) -> dict[str, object]:
    return {
        "id": case_id,
        "kind": kind,
        "prompt": f"Real prompt for {case_id}",
        "expected_behavior": f"Observable result for {case_id}",
        "checks": {"trigger": [], "process": [check], "output": [], "safety": []},
        "pass_criteria": {"all_required": True, "min_score": 1.0},
    }


def suite(schema_version: int, negative_check: dict[str, object]) -> dict[str, object]:
    positive = {
        "type": "regex",
        "value": "(?i)(observable behavior|validated result)",
        "required": True,
        "quality": "behavior",
    }
    return {
        "schema_version": schema_version,
        "skill_name": "example-skill",
        "pass_threshold": 0.85,
        "evals": [
            case("positive-one", "positive", positive),
            case("positive-two", "positive", positive),
            case("negative-one", "negative", negative_check),
            case("near-miss-one", "near_miss", positive),
            case("failure-one", "failure_mode", positive),
        ],
    }


class EvalSchemaVersionTests(unittest.TestCase):
    def validate(self, data: dict[str, object]):
        with tempfile.TemporaryDirectory() as tmp_dir:
            path = Path(tmp_dir) / "evals.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return validate_eval_file(path, "example-skill")

    def test_v8_rejects_case_with_only_required_absence_assertion(self) -> None:
        result = self.validate(
            suite(
                8,
                {
                    "type": "must_not_contain",
                    "value": "forbidden workflow",
                    "required": True,
                    "quality": "behavior",
                },
            )
        )

        self.assertFalse(result.ok)
        self.assertTrue(any("positive-evidence" in error for error in result.errors))

    def test_v8_accepts_negative_case_with_observable_reroute(self) -> None:
        result = self.validate(
            suite(
                8,
                {
                    "type": "regex",
                    "value": "(?i)(direct answer|outside the skill boundary)",
                    "required": True,
                    "quality": "behavior",
                },
            )
        )

        self.assertTrue(result.ok, result.errors)

    def test_unversioned_v7_suite_remains_compatible(self) -> None:
        data = suite(
            7,
            {
                "type": "must_not_contain",
                "value": "forbidden workflow",
                "required": True,
                "quality": "behavior",
            },
        )
        data.pop("schema_version")

        result = self.validate(data)

        self.assertTrue(result.ok, result.errors)


if __name__ == "__main__":
    unittest.main()
