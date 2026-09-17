#!/usr/bin/env python3
"""Deterministic publication-gate regression tests."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(SCRIPT_DIR))

from validate_change_manifest import collect_changed_paths, validate_manifest  # noqa: E402


def release(mode: str = "isolated_manual_prototype", **overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "mode": mode,
        "changes_default_routing": False,
        "removes_existing_path": False,
        "registers_stable": False,
        "claims_improvement": False,
        "manual_entry_point": "Explicit manual invocation" if mode == "isolated_manual_prototype" else None,
        "removal_without_migration": "Delete this isolated package" if mode == "isolated_manual_prototype" else None,
        "replacement_unit_id": None,
    }
    value.update(overrides)
    return value


def command(*argv: str, expected_exit: int = 0) -> dict[str, object]:
    return {"argv": list(argv), "expected_exit": expected_exit}


def rollback(*, executable: bool = True) -> dict[str, object]:
    value: dict[str, object] = {
        "trigger": "A targeted regression fails",
        "steps": ["Restore this independent unit from the pre-publication baseline"],
    }
    if executable:
        value["commands"] = [
            command("git", "restore", "--source=HEAD", "--", "skills/example-a")
        ]
    return value


def evidence() -> list[dict[str, str]]:
    return [
        {
            "kind": "user_session",
            "ref": "skills/dbx-skill-architect/tests/test_validate_change_manifest.py#session-evidence",
            "summary": "Observed the known-bad default failure repeatedly.",
        }
    ]


def release_validation(kind: str = "before_after") -> dict[str, object]:
    test_ref = "skills/dbx-skill-architect/tests/test_validate_change_manifest.py"
    baseline_ref = f"{test_ref}#baseline-fixture"
    candidate_ref = f"{test_ref}#candidate-fixture"
    outcome: dict[str, object] = {
        "kind": kind,
        "ref": candidate_ref,
        "summary": "The candidate rejects the baseline bypass and accepts the complete proof contract.",
        "baseline_ref": baseline_ref if kind == "before_after" else None,
        "candidate_ref": candidate_ref if kind == "before_after" else None,
        "check": command(
            "python3",
            "skills/dbx-skill-architect/tests/test_validate_change_manifest.py",
        ),
    }
    return {
        "baseline": {
            "ref": baseline_ref,
            "summary": "The old contract accepted narrative evidence and prose rollback.",
            "check": command(
                "python3",
                "skills/dbx-skill-architect/tests/test_validate_change_manifest.py",
            ),
        },
        "outcomes": [outcome],
        "costs": [
            {
                "metric": "publication gate regression command",
                "value": 1,
                "unit": "test command",
                "ref": f"{test_ref}#cost-fixture",
                "check": command(
                    "python3",
                    "skills/dbx-skill-architect/tests/test_validate_change_manifest.py",
                ),
            }
        ],
    }


def unit(
    unit_id: str,
    patterns: list[str],
    *,
    kind: str = "prototype",
    net_value: str = "uncertain",
    release_value: dict[str, object] | None = None,
    evidence_value: list[dict[str, str]] | None = None,
    surfaces: dict[str, list[str]] | None = None,
    validation_value: dict[str, object] | None = None,
    rollback_value: dict[str, object] | None = None,
) -> dict[str, object]:
    value: dict[str, object] = {
        "id": unit_id,
        "kind": kind,
        "net_value": net_value,
        "path_patterns": patterns,
        "surfaces": surfaces
        or {
            "cross_skill_protocol": [],
            "cross_skill_state": [],
            "execution_authority": [],
            "routing": [],
        },
        "release": release_value or release(),
        "evidence": evidence_value or [],
        "rollback": rollback_value or rollback(),
    }
    if validation_value is not None:
        value["validation"] = validation_value
    return value


class ChangeManifestGateTests(unittest.TestCase):
    def validate(self, units: list[dict[str, object]], paths: list[str]) -> dict[str, object]:
        return validate_manifest({"schema_version": 2, "change_units": units}, paths, REPO_ROOT)

    def test_uncertain_three_skill_unit_can_only_remain_isolated(self) -> None:
        paths = [
            "skills/example-a/SKILL.md",
            "skills/example-b/SKILL.md",
            "skills/example-c/SKILL.md",
        ]
        result = self.validate([unit("prototype", ["skills/example-*/**"])], paths)

        self.assertTrue(result["ok"], result["errors"])
        self.assertTrue(result["unit_reports"][0]["broad"])
        self.assertEqual(len(result["unit_reports"][0]["affected_skill_roots"]), 3)

    def test_schema_v2_exposes_release_validation_and_executable_rollback(self) -> None:
        schema_path = REPO_ROOT / "skills/dbx-skill-architect/assets/change-manifest.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))

        self.assertEqual(schema["properties"]["schema_version"]["const"], 2)
        self.assertEqual(
            set(schema["$defs"]["release_validation"]["required"]),
            {"baseline", "outcomes", "costs"},
        )
        rollback = schema["$defs"]["change_unit"]["properties"]["rollback"]["properties"]
        self.assertIn("commands", rollback)

    def test_uncertain_broad_unit_cannot_change_default_or_claim_improvement(self) -> None:
        paths = [
            "skills/example-a/SKILL.md",
            "skills/example-b/SKILL.md",
            "skills/example-c/SKILL.md",
        ]
        bad_release = release(changes_default_routing=True, claims_improvement=True)
        result = self.validate([unit("prototype", ["skills/example-*/**"], release_value=bad_release)], paths)

        self.assertFalse(result["ok"])
        self.assertTrue(any("cannot enable release flags" in error for error in result["errors"]))
        self.assertTrue(any("improvement claim requires" in error for error in result["errors"]))

    def test_three_skill_publication_cannot_evade_gate_by_splitting_units(self) -> None:
        paths = [
            "skills/example-a/SKILL.md",
            "skills/example-b/SKILL.md",
            "skills/example-c/SKILL.md",
        ]
        units = [
            unit(
                "a",
                ["skills/example-a/**"],
                kind="standard_change",
                release_value=release("candidate", claims_improvement=True),
            ),
            unit("b", ["skills/example-b/**"]),
            unit("c", ["skills/example-c/**"]),
        ]

        result = self.validate(units, paths)

        self.assertFalse(result["ok"])
        self.assertTrue(result["publication_broad"])
        self.assertTrue(any("broad uncertain unit must remain" in error for error in result["errors"]))

    def test_declared_cross_skill_protocol_makes_two_skill_unit_broad(self) -> None:
        paths = ["skills/example-a/SKILL.md", "skills/example-b/SKILL.md"]
        surfaces = {
            "cross_skill_protocol": ["skills/example-a/SKILL.md"],
            "cross_skill_state": [],
            "execution_authority": [],
            "routing": [],
        }
        result = self.validate([unit("protocol", ["skills/example-*/**"], surfaces=surfaces)], paths)

        self.assertTrue(result["ok"], result["errors"])
        self.assertTrue(result["unit_reports"][0]["broad"])
        self.assertEqual(result["unit_reports"][0]["surface_counts"]["cross_skill_protocol"], 1)

    def test_known_bad_default_removal_is_separate_positive_unit(self) -> None:
        paths = [
            "skills/example-a/SKILL.md",
            "skills/example-b/SKILL.md",
            "skills/example-c/SKILL.md",
            "docs/skill-routing.md",
        ]
        prototype = unit("prototype", ["skills/example-*/**"])
        removal = unit(
            "remove-default",
            ["docs/skill-routing.md"],
            kind="known_bad_default_removal",
            net_value="positive",
            release_value=release(
                "candidate",
                changes_default_routing=True,
                removes_existing_path=True,
                claims_improvement=True,
            ),
            evidence_value=evidence(),
            validation_value=release_validation(),
            surfaces={
                "cross_skill_protocol": [],
                "cross_skill_state": [],
                "execution_authority": [],
                "routing": ["docs/skill-routing.md"],
            },
        )

        result = self.validate([prototype, removal], paths)

        self.assertTrue(result["ok"], result["errors"])

    def test_known_bad_removal_cannot_use_uncertain_prototype_as_replacement(self) -> None:
        paths = ["skills/example-a/SKILL.md", "docs/skill-routing.md"]
        prototype = unit("prototype", ["skills/example-a/**"])
        removal_release = release(
            "candidate",
            changes_default_routing=True,
            removes_existing_path=True,
            claims_improvement=True,
            replacement_unit_id="prototype",
        )
        removal = unit(
            "remove-default",
            ["docs/skill-routing.md"],
            kind="known_bad_default_removal",
            net_value="positive",
            release_value=removal_release,
            evidence_value=evidence(),
            validation_value=release_validation(),
            surfaces={
                "cross_skill_protocol": [],
                "cross_skill_state": [],
                "execution_authority": [],
                "routing": ["docs/skill-routing.md"],
            },
        )

        result = self.validate([prototype, removal], paths)

        self.assertFalse(result["ok"])
        self.assertTrue(any("cannot use an uncertain" in error for error in result["errors"]))

    def test_broad_positive_rejects_narrative_evidence_and_prose_rollback(self) -> None:
        paths = [
            "skills/example-a/SKILL.md",
            "skills/example-b/SKILL.md",
            "skills/example-c/SKILL.md",
        ]
        positive = unit(
            "positive",
            ["skills/example-*/**"],
            kind="standard_change",
            net_value="positive",
            release_value=release("candidate", claims_improvement=True),
            evidence_value=evidence(),
            rollback_value=rollback(executable=False),
        )

        result = self.validate([positive], paths)

        self.assertFalse(result["ok"])
        self.assertTrue(any("machine-checkable baseline" in error for error in result["errors"]))
        self.assertTrue(any("rollback.commands argv" in error for error in result["errors"]))

    def test_broad_positive_rejects_nonexistent_proof_ref(self) -> None:
        paths = [
            "skills/example-a/SKILL.md",
            "skills/example-b/SKILL.md",
            "skills/example-c/SKILL.md",
        ]
        validation_value = release_validation()
        validation_value["baseline"]["ref"] = "evidence/does-not-exist.json#baseline"  # type: ignore[index]
        positive = unit(
            "positive",
            ["skills/example-*/**"],
            kind="standard_change",
            net_value="positive",
            release_value=release("candidate", claims_improvement=True),
            evidence_value=evidence(),
            validation_value=validation_value,
        )

        result = self.validate([positive], paths)

        self.assertFalse(result["ok"])
        self.assertTrue(any("does not resolve to an existing repository file" in error for error in result["errors"]))

    def test_narrative_evidence_ref_must_be_repository_local_and_existing(self) -> None:
        bad_evidence = [
            {
                "kind": "other",
                "ref": "https://example.invalid/self-authored-proof",
                "summary": "An arbitrary URL must not satisfy the evidence contract.",
            }
        ]
        result = self.validate(
            [unit("prototype", ["skills/example-a/**"], evidence_value=bad_evidence)],
            ["skills/example-a/SKILL.md"],
        )

        self.assertFalse(result["ok"])
        self.assertTrue(any("repository-relative" in error for error in result["errors"]))

    def test_broad_positive_rejects_unavailable_check_executable(self) -> None:
        paths = [
            "skills/example-a/SKILL.md",
            "skills/example-b/SKILL.md",
            "skills/example-c/SKILL.md",
        ]
        validation_value = release_validation()
        validation_value["outcomes"][0]["check"]["argv"][0] = "definitely-not-a-real-command"  # type: ignore[index]
        positive = unit(
            "positive",
            ["skills/example-*/**"],
            kind="standard_change",
            net_value="positive",
            release_value=release("candidate", claims_improvement=True),
            evidence_value=evidence(),
            validation_value=validation_value,
        )

        result = self.validate([positive], paths)

        self.assertFalse(result["ok"])
        self.assertTrue(any("not available on PATH" in error for error in result["errors"]))

    def test_broad_positive_accepts_before_after_proof_cost_and_rollback(self) -> None:
        paths = [
            "skills/example-a/SKILL.md",
            "skills/example-b/SKILL.md",
            "skills/example-c/SKILL.md",
        ]
        positive = unit(
            "positive",
            ["skills/example-*/**"],
            kind="standard_change",
            net_value="positive",
            release_value=release("candidate", claims_improvement=True),
            evidence_value=evidence(),
            validation_value=release_validation("before_after"),
        )

        result = self.validate([positive], paths)

        self.assertTrue(result["ok"], result["errors"])

    def test_broad_positive_accepts_operational_proof_cost_and_rollback(self) -> None:
        paths = [
            "skills/example-a/SKILL.md",
            "skills/example-b/SKILL.md",
            "skills/example-c/SKILL.md",
        ]
        positive = unit(
            "positive",
            ["skills/example-*/**"],
            kind="standard_change",
            net_value="positive",
            release_value=release("candidate", claims_improvement=True),
            evidence_value=evidence(),
            validation_value=release_validation("operational"),
        )

        result = self.validate([positive], paths)

        self.assertTrue(result["ok"], result["errors"])

    def test_detected_routing_path_must_be_declared(self) -> None:
        path = "skills/example-a/agents/openai.yaml"
        result = self.validate([unit("routing", ["skills/example-a/**"])], [path])

        self.assertFalse(result["ok"])
        self.assertTrue(any("omits detected routing paths" in error for error in result["errors"]))

    def test_working_tree_collection_includes_tracked_and_untracked_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = Path(tmp_dir)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
            subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
            tracked = repo / "tracked.txt"
            tracked.write_text("one\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "tracked.txt"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "initial"], check=True)
            tracked.write_text("two\n", encoding="utf-8")
            (repo / "untracked.txt").write_text("new\n", encoding="utf-8")

            paths = collect_changed_paths(repo, "working-tree")

        self.assertEqual(paths, ["tracked.txt", "untracked.txt"])


if __name__ == "__main__":
    unittest.main()
