#!/usr/bin/env python3
"""Regression tests for the saved-output eval runner."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from run_skill_evals import score_single_case  # noqa: E402


def pure_must_not_case() -> dict[str, object]:
    return {
        "id": "negative-pure-must-not",
        "kind": "negative",
        "checks": {
            "trigger": [],
            "process": [],
            "output": [
                {
                    "type": "must_not_contain",
                    "value": "forbidden route",
                    "required": True,
                    "quality": "behavior",
                }
            ],
            "safety": [],
        },
        "pass_criteria": {"all_required": True, "min_score": 1.0},
    }


def positive_evidence_case() -> dict[str, object]:
    case = pure_must_not_case()
    case["id"] = "negative-with-positive-reroute"
    checks = case["checks"]
    assert isinstance(checks, dict)
    checks["process"] = [
        {
            "type": "regex",
            "value": "(?i)(direct answer|outside the skill boundary)",
            "required": True,
            "quality": "behavior",
        }
    ]
    return case


class CapturedOutputTests(unittest.TestCase):
    def score(self, text: str, *, schema_version: int = 7, case: dict[str, object] | None = None) -> dict[str, object]:
        selected_case = case or pure_must_not_case()
        data = {
            "schema_version": schema_version,
            "pass_threshold": 0.85,
            "evals": [selected_case],
        }
        with tempfile.TemporaryDirectory() as tmp_dir:
            output = Path(tmp_dir) / "captured.md"
            output.write_text(text, encoding="utf-8")
            return score_single_case(data, str(selected_case["id"]), output)

    def test_empty_captured_output_fails_instead_of_passing_vacuously(self) -> None:
        result = self.score("")

        self.assertFalse(result["ok"])
        self.assertEqual(result["pass_rate"], 0.0)
        scored = result["results"][0]
        self.assertFalse(scored["passed"])
        self.assertEqual(scored["score"], 0.0)
        self.assertEqual(scored["details"][0]["type"], "non_empty_output")

    def test_whitespace_or_bom_only_captured_output_fails(self) -> None:
        result = self.score("\ufeff \n\t")

        self.assertFalse(result["ok"])
        self.assertFalse(result["results"][0]["passed"])

    def test_legacy_non_empty_output_can_still_pass_a_pure_must_not_case(self) -> None:
        result = self.score("This request belongs to a direct answer.\n")

        self.assertTrue(result["ok"])
        self.assertEqual(result["pass_rate"], 1.0)
        self.assertTrue(result["results"][0]["passed"])

    def test_v8_arbitrary_non_empty_output_fails_pure_must_not_case(self) -> None:
        result = self.score("arbitrary text\n", schema_version=8)

        self.assertFalse(result["ok"])
        scored = result["results"][0]
        self.assertFalse(scored["passed"])
        self.assertEqual(scored["score"], 0.0)
        self.assertEqual(scored["details"][0]["type"], "positive_evidence_required")

    def test_v8_case_passes_only_when_positive_behavior_is_observed(self) -> None:
        case = positive_evidence_case()

        missing_behavior = self.score("harmless arbitrary text\n", schema_version=8, case=case)
        observed_behavior = self.score(
            "This is outside the skill boundary; provide a direct answer.\n",
            schema_version=8,
            case=case,
        )

        self.assertFalse(missing_behavior["ok"])
        self.assertTrue(observed_behavior["ok"])


if __name__ == "__main__":
    unittest.main()
