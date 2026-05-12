#!/usr/bin/env python3
"""Produce a heuristic first-pass placement analysis from a skill inventory.

This script is intentionally conservative. It does not prove value or usage; it
creates a review queue and draft recommendations from observable metadata plus
optional usage evidence supplied by the user.
"""
from __future__ import annotations

import argparse
import csv
import itertools
import json
import re
import sys
from pathlib import Path
from typing import Any

GENERIC_WORDS = re.compile(r"\b(help|helps|assistant|general|anything|everything|all|improve|better)\b", re.I)
PROJECT_WORDS = re.compile(
    r"\b(repo|project|workspace|monorepo|service|module|team|company|client|internal|work|frontend|backend|ios|android|react|vue|next|node|go|rust|python)\b",
    re.I,
)
META_WORDS = re.compile(
    r"\b(skill|audit|architect|installer|inventory|governance|routing|eval|evaluation|migration|release|incident|security|policy)\b",
    re.I,
)
ASCII_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_+-]{2,}", re.I)
CJK_RUN_RE = re.compile(r"[\u4e00-\u9fff]+")
STOP_WORDS = {
    "and",
    "are",
    "can",
    "codex",
    "for",
    "from",
    "have",
    "help",
    "helps",
    "into",
    "not",
    "the",
    "this",
    "use",
    "used",
    "user",
    "when",
    "without",
    "with",
    "audit",
    "review",
    "skill",
    "skills",
    "agent",
    "agents",
    "task",
    "tasks",
}

RISKY_FLAGS = {
    "network_reference",
    "dependency_install",
    "destructive_operation",
    "secret_or_credential_reference",
    "skill_md_mentions_credentials",
}


def tokenize(text: str) -> set[str]:
    tokens = {token.lower() for token in ASCII_TOKEN_RE.findall(text) if token.lower() not in STOP_WORDS}
    for run in CJK_RUN_RE.findall(text):
        if len(run) == 1:
            tokens.add(run)
        else:
            tokens.update(run[index : index + 2] for index in range(0, len(run) - 1))
    return tokens


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def top_shared_terms(left: set[str], right: set[str], limit: int = 12) -> list[str]:
    shared = left & right
    return sorted(shared, key=lambda token: (-len(token), token))[:limit]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_usage(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix.lower() == ".json":
        data = load_json(path)
        if isinstance(data, dict) and "skill_usage" in data and isinstance(data["skill_usage"], dict):
            return {str(k): dict(v) if isinstance(v, dict) else {"notes": v} for k, v in data["skill_usage"].items()}
        if isinstance(data, dict):
            return {str(k): dict(v) if isinstance(v, dict) else {"notes": v} for k, v in data.items()}
    if path.suffix.lower() in {".csv", ".tsv"}:
        delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
        result: dict[str, dict[str, Any]] = {}
        with path.open("r", encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh, delimiter=delimiter)
            for row in reader:
                name = row.get("skill_name") or row.get("name")
                if name:
                    result[str(name)] = dict(row)
        return result
    raise ValueError(f"Unsupported usage evidence file: {path}")


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except Exception:
        return default


def usage_signal(name: str, usage: dict[str, dict[str, Any]]) -> tuple[str, int, list[str]]:
    item = usage.get(name, {})
    notes: list[str] = []
    count = max(
        as_int(item.get("explicit_invocations")),
        as_int(item.get("uses")),
        as_int(item.get("count")),
        as_int(item.get("manual_value")),
    )
    if not item:
        return "unknown", 0, ["no_usage_evidence"]
    if count >= 10:
        label = "frequent"
        score = 3
    elif count >= 3:
        label = "occasional"
        score = 2
    elif count >= 1:
        label = "tried_or_rare"
        score = 1
    else:
        label = "user_provided_no_count"
        score = 1
    if item.get("notes"):
        notes.append(str(item["notes"]))
    if item.get("project_scope"):
        notes.append(f"project_scope={item['project_scope']}")
    return label, score, notes


def case_expected_trigger(case: dict[str, Any]) -> bool:
    expected = case.get("expected")
    if expected == "trigger":
        return True
    if expected == "do_not_trigger":
        return False
    expected_trigger = case.get("expected_trigger")
    if isinstance(expected_trigger, bool):
        return expected_trigger
    return str(case.get("kind", "")) in {"positive", "failure_mode", "safety"}


def activation_profile(item: dict[str, Any]) -> dict[str, Any]:
    name = str(item.get("name", ""))
    desc = str(item.get("frontmatter", {}).get("description", ""))
    positive_texts = [name, desc]
    negative_texts: list[str] = []
    positive_cases: list[str] = []
    negative_cases: list[str] = []

    for case in item.get("trigger_evals", {}).get("cases", []):
        if not isinstance(case, dict):
            continue
        prompt = str(case.get("prompt", ""))
        if not prompt:
            continue
        label = str(case.get("id") or case.get("kind") or "case")
        if case_expected_trigger(case):
            positive_texts.append(prompt)
            positive_cases.append(label)
        else:
            negative_texts.append(prompt)
            negative_cases.append(label)

    implicit = item.get("agents_openai", {}).get("allow_implicit_invocation", "unknown")
    return {
        "name": name,
        "path": item.get("path"),
        "implicit": implicit,
        "positive_tokens": tokenize(" ".join(positive_texts)),
        "description_tokens": tokenize(desc),
        "negative_tokens": tokenize(" ".join(negative_texts)),
        "positive_cases": positive_cases[:5],
        "negative_cases": negative_cases[:5],
    }


def overlap_severity(positive_score: float, boundary_score: float, description_score: float, both_implicit: bool) -> str:
    if positive_score >= 0.34 or boundary_score >= 0.30:
        return "high"
    if both_implicit and (positive_score >= 0.22 or boundary_score >= 0.20):
        return "high"
    if positive_score >= 0.22 or boundary_score >= 0.20 or description_score >= 0.28:
        return "medium"
    return "low"


def overlap_action(severity: str, conflict_type: str) -> str:
    if severity == "high":
        if conflict_type == "boundary_conflict":
            return "Review trigger boundaries; add near-miss evals or explicit routing so one skill's positive case is not another skill's rejection case."
        return "Review for merge_or_refactor or add an explicit routing rule that names the canonical skill."
    if conflict_type == "boundary_conflict":
        return "Compare positive and near-miss trigger evals; document precedence if both skills remain installed."
    return "Review shared trigger terms and add a routing note only if users actually confuse these skills."


def find_trigger_overlaps(skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    profiles = [activation_profile(item) for item in skills]
    pairs: list[dict[str, Any]] = []
    for left, right in itertools.combinations(profiles, 2):
        # Same-name duplicates are handled by duplicate detection; overlap review
        # is for distinct skills whose triggers may collide.
        if left["name"] == right["name"]:
            continue
        positive_score = jaccard(left["positive_tokens"], right["positive_tokens"])
        description_score = jaccard(left["description_tokens"], right["description_tokens"])
        left_boundary = jaccard(left["positive_tokens"], right["negative_tokens"])
        right_boundary = jaccard(right["positive_tokens"], left["negative_tokens"])
        boundary_score = max(left_boundary, right_boundary)

        if max(positive_score, description_score, boundary_score) < 0.18:
            continue

        both_implicit = left["implicit"] is not False and right["implicit"] is not False
        if boundary_score >= 0.20 and boundary_score >= max(positive_score, description_score):
            conflict_type = "boundary_conflict"
            if left_boundary >= right_boundary:
                shared_terms = top_shared_terms(left["positive_tokens"], right["negative_tokens"])
            else:
                shared_terms = top_shared_terms(right["positive_tokens"], left["negative_tokens"])
        elif positive_score >= 0.22:
            conflict_type = "trigger_overlap"
            shared_terms = top_shared_terms(left["positive_tokens"], right["positive_tokens"])
        else:
            conflict_type = "description_overlap"
            shared_terms = top_shared_terms(left["description_tokens"], right["description_tokens"])

        severity = overlap_severity(positive_score, boundary_score, description_score, both_implicit)
        pairs.append(
            {
                "skills": [left["name"], right["name"]],
                "severity": severity,
                "conflict_type": conflict_type,
                "positive_overlap": round(positive_score, 3),
                "boundary_overlap": round(boundary_score, 3),
                "description_overlap": round(description_score, 3),
                "both_implicit_or_unknown": both_implicit,
                "shared_terms": shared_terms,
                "left_positive_cases": left["positive_cases"],
                "right_positive_cases": right["positive_cases"],
                "recommended_action": overlap_action(severity, conflict_type),
            }
        )
    return sorted(
        pairs,
        key=lambda pair: (
            {"high": 0, "medium": 1, "low": 2}.get(str(pair["severity"]), 3),
            -float(pair["positive_overlap"]),
            -float(pair["boundary_overlap"]),
            pair["skills"],
        ),
    )


def classify(item: dict[str, Any], usage: dict[str, dict[str, Any]], duplicate_names: set[str]) -> dict[str, Any]:
    name = str(item.get("name", ""))
    desc = str(item.get("frontmatter", {}).get("description", ""))
    issues = set(item.get("issues", []))
    risks = set(item.get("risk_flags", []))
    scope = str(item.get("scope_guess", ""))
    dirs = set(item.get("optional_dirs", []))
    line_count = int(item.get("skill_md", {}).get("line_count", 0) or 0)
    desc_chars = int(item.get("frontmatter", {}).get("description_chars", 0) or 0)
    implicit = item.get("agents_openai", {}).get("allow_implicit_invocation", "unknown")

    usage_label, usage_score, usage_notes = usage_signal(name, usage)
    evidence: list[str] = [f"usage={usage_label}"] + usage_notes
    risk_notes: list[str] = []
    confidence = "medium" if usage_score > 0 else "low"

    if name in duplicate_names or "duplicate_name" in issues:
        recommendation = "merge_or_refactor"
        reason = "Duplicate skill name creates routing ambiguity."
        risk_notes.append("duplicate_name")
        confidence = "high"
    elif risks & RISKY_FLAGS:
        recommendation = "disable_pending_review"
        reason = "Risk flags require review before keeping active."
        risk_notes.extend(sorted(risks & RISKY_FLAGS))
        confidence = "medium"
    elif "missing_skill_md" in issues or "missing_name" in issues or "missing_description" in issues:
        recommendation = "disable_pending_review"
        reason = "Invalid active skill package metadata."
        risk_notes.extend(sorted(issues))
        confidence = "high"
    elif implicit is False:
        recommendation = "explicit_only"
        reason = "Already configured for explicit invocation only."
        confidence = "high"
    elif META_WORDS.search(name + " " + desc) and usage_score <= 1:
        recommendation = "explicit_only"
        reason = "Meta/governance/rare workflow should usually avoid implicit trigger."
    elif usage_score >= 2 and scope in {"codex_user_current", "codex_user_legacy_or_custom", "cursor_user", "claude_user"} and not risks:
        recommendation = "global_keep"
        reason = "Usage evidence plus user/global scope suggests cross-project value."
        confidence = "medium"
    elif PROJECT_WORDS.search(desc) and usage_score <= 2:
        recommendation = "project_scope"
        reason = "Description suggests project/team/stack specificity."
    elif usage_score == 0 and (GENERIC_WORDS.search(desc) or desc_chars < 60 or line_count > 400):
        recommendation = "explicit_only"
        reason = "Unknown usage plus trigger/context risk; reversible explicit-only is safer than deletion."
    elif usage_score == 0:
        recommendation = "needs_more_evidence"
        reason = "No usage evidence; inventory alone is insufficient."
    else:
        recommendation = "needs_more_evidence"
        reason = "Signals are mixed; use interview or observation window."

    if "evals" not in dirs:
        risk_notes.append("missing_evals")
    if desc_chars > 700:
        risk_notes.append("long_description")
    if line_count > 500:
        risk_notes.append("large_skill_md")

    return {
        "skill": name,
        "current_scope": scope,
        "recommendation": recommendation,
        "confidence": confidence,
        "reason": reason,
        "evidence": evidence,
        "risk_notes": sorted(set(risk_notes)),
        "path": item.get("path"),
        "suggested_next_action": next_action(recommendation, name),
    }


def next_action(recommendation: str, name: str) -> str:
    if recommendation == "global_keep":
        return "Keep installed globally; verify trigger evals and remove duplicates."
    if recommendation == "project_scope":
        return "Move or copy to the relevant repo .agents/skills path; remove from user/global after testing."
    if recommendation == "explicit_only":
        return "Add agents/openai.yaml policy.allow_implicit_invocation=false or keep disabled until explicit use."
    if recommendation == "disable_pending_review":
        return "Disable or quarantine first; review scripts/source/trust before re-enabling."
    if recommendation == "uninstall_or_archive":
        return "Archive with rollback path, then remove from active discovery after approval."
    if recommendation == "merge_or_refactor":
        return "Pick one canonical skill name; archive or rename duplicates and update routing docs."
    return "Collect usage evidence or ask targeted interview questions."


def has_unknown_usage(row: dict[str, Any]) -> bool:
    evidence = row.get("evidence", [])
    return any(str(item) in {"usage=unknown", "no_usage_evidence"} for item in evidence)


def build_executive_decision(
    rows: list[dict[str, Any]], counts: dict[str, int], overlap_pairs: list[dict[str, Any]]
) -> dict[str, Any]:
    high_overlaps = [pair for pair in overlap_pairs if pair.get("severity") == "high"]
    medium_overlaps = [pair for pair in overlap_pairs if pair.get("severity") == "medium"]
    unknown_usage_count = sum(1 for row in rows if has_unknown_usage(row))
    blocking_count = counts.get("disable_pending_review", 0) + counts.get("merge_or_refactor", 0)

    if blocking_count or high_overlaps:
        recommendation = "Conservative cleanup: review risky, invalid, duplicate, or high-overlap skills before moving or uninstalling anything."
    elif counts.get("explicit_only", 0) or medium_overlaps:
        recommendation = "Scope reduction: make narrow or sensitive skills explicit-only and document overlap boundaries."
    elif unknown_usage_count:
        recommendation = "Evidence collection: inventory alone is insufficient for removal decisions."
    else:
        recommendation = "No urgent cleanup from available evidence."

    confidence = "high"
    if unknown_usage_count:
        confidence = "low" if unknown_usage_count == len(rows) else "medium"
    if blocking_count or high_overlaps:
        confidence = "medium" if unknown_usage_count else "high"

    do_now: list[str] = []
    if counts.get("disable_pending_review"):
        do_now.append(f"Review or quarantine {counts['disable_pending_review']} skill(s) with metadata, trust, script, or safety risk.")
    if counts.get("merge_or_refactor"):
        do_now.append(f"Resolve {counts['merge_or_refactor']} duplicate or merge/refactor candidate(s) before judging usage value.")
    if high_overlaps:
        do_now.append(f"Review {len(high_overlaps)} high-severity trigger-overlap pair(s) and add routing or near-miss evals.")
    if counts.get("explicit_only"):
        do_now.append(f"Consider explicit-only policy for {counts['explicit_only']} narrow, rare, sensitive, or costly skill(s).")
    if unknown_usage_count:
        do_now.append(f"Collect usage evidence for {unknown_usage_count} skill(s) before uninstall/archive decisions.")
    if not do_now:
        do_now.append("Keep current placement and rerun after new usage or routing evidence appears.")

    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "evidence_quality": "usage evidence missing" if unknown_usage_count else "usage evidence provided or not required",
        "unknown_usage_count": unknown_usage_count,
        "high_overlap_count": len(high_overlaps),
        "medium_overlap_count": len(medium_overlaps),
        "do_now": do_now[:5],
        "do_not_do_automatically": [
            "Do not uninstall or archive skills based only on inventory metadata.",
            "Do not inspect private chat, shell, browser, or log history without explicit consent.",
            "Do not merge skills on lexical overlap alone; confirm with trigger examples or user confusion evidence.",
        ],
    }


def build_high_leverage_changes(
    rows: list[dict[str, Any]], overlap_pairs: list[dict[str, Any]], limit: int = 5
) -> list[str]:
    changes: list[str] = []
    seen: set[str] = set()

    def add(key: str, text: str) -> None:
        if len(changes) >= limit or key in seen:
            return
        seen.add(key)
        changes.append(text)

    for row in rows:
        if row["recommendation"] == "disable_pending_review":
            add(
                f"disable:{row['skill']}",
                f"Review or quarantine `{row['skill']}`: {row['reason']} Risk notes: {', '.join(row['risk_notes']) or 'none'}.",
            )
    for row in rows:
        if row["recommendation"] == "merge_or_refactor":
            add(
                f"merge:{row['skill']}",
                f"Resolve duplicate or merge/refactor candidate `{row['skill']}` before making placement decisions.",
            )
    for pair in overlap_pairs:
        if pair.get("severity") in {"high", "medium"}:
            skills = " <-> ".join(pair["skills"])
            add(
                f"overlap:{skills}",
                f"Review `{skills}` trigger overlap ({pair['conflict_type']}); shared terms: {', '.join(pair['shared_terms'][:6]) or 'none'}.",
            )
    explicit_count = sum(1 for row in rows if row["recommendation"] == "explicit_only")
    if explicit_count:
        add(
            "explicit_only_batch",
            f"Apply or verify explicit-only policy for {explicit_count} low-frequency, sensitive, or meta-level skill(s).",
        )
    unknown_count = sum(1 for row in rows if has_unknown_usage(row))
    if unknown_count:
        add("usage_evidence", f"Collect usage evidence for {unknown_count} skill(s) before deletion or archive decisions.")
    if not changes:
        changes.append("No high-leverage cleanup is justified from this inventory alone; keep monitoring usage and trigger mistakes.")
    return changes


def analyze(data: dict[str, Any], usage: dict[str, dict[str, Any]]) -> dict[str, Any]:
    duplicate_names = set(data.get("duplicates", {}).get("by_name", {}).keys())
    skills = data.get("skills", [])
    rows = [classify(item, usage, duplicate_names) for item in skills]
    overlap_pairs = find_trigger_overlaps(skills)
    overlap_by_skill: dict[str, list[str]] = {}
    for pair in overlap_pairs:
        if pair["severity"] == "low":
            continue
        left, right = pair["skills"]
        overlap_by_skill.setdefault(str(left), []).append(str(right))
        overlap_by_skill.setdefault(str(right), []).append(str(left))
    for row in rows:
        related = sorted(set(overlap_by_skill.get(row["skill"], [])))
        if related:
            row["risk_notes"] = sorted(set(row["risk_notes"] + [f"trigger_overlap_review:{','.join(related[:3])}"]))
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["recommendation"]] = counts.get(row["recommendation"], 0) + 1
    executive_decision = build_executive_decision(rows, counts, overlap_pairs)
    high_leverage_changes = build_high_leverage_changes(rows, overlap_pairs)
    return {
        "schema_version": "1.0",
        "source_inventory_generated_at_utc": data.get("generated_at_utc"),
        "skill_count": len(rows),
        "executive_decision": executive_decision,
        "recommendation_counts": counts,
        "high_leverage_changes": high_leverage_changes,
        "recommendations": sorted(rows, key=lambda r: (r["recommendation"], r["skill"])),
        "trigger_overlap_pairs": overlap_pairs,
        "limitations": [
            "This is a heuristic first pass, not a final audit.",
            "Usage is unknown unless provided through --usage-evidence.",
            "Trigger overlap scores are lexical heuristics over descriptions and trigger eval prompts; review high/medium pairs before merging skills.",
            "Do not delete or edit skills without reviewing the proposed action and keeping rollback paths.",
        ],
    }


def esc(value: Any) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def to_markdown(report: dict[str, Any]) -> str:
    decision = report.get("executive_decision", {})
    lines = [
        "# Skill Portfolio Heuristic Analysis",
        "",
        f"Skills analyzed: `{report['skill_count']}`",
        "",
        "## Executive decision",
        "",
        f"Recommendation: {esc(decision.get('recommendation', 'Review inventory before acting.'))}",
        f"Confidence: `{esc(decision.get('confidence', 'unknown'))}`",
        f"Evidence quality: {esc(decision.get('evidence_quality', 'unknown'))}",
        f"Trigger overlap review: `{esc(decision.get('high_overlap_count', 0))}` high, `{esc(decision.get('medium_overlap_count', 0))}` medium",
        "",
        "Do now:",
    ]
    for index, item in enumerate(decision.get("do_now", []), start=1):
        lines.append(f"{index}. {esc(item)}")
    lines.extend(["", "Do not do automatically:"])
    for item in decision.get("do_not_do_automatically", []):
        lines.append(f"- {esc(item)}")
    lines.extend(
        [
            "",
            "## Recommendation counts",
            "",
            "| Recommendation | Count |",
            "|---|---:|",
        ]
    )
    for key, count in sorted(report["recommendation_counts"].items()):
        lines.append(f"| `{esc(key)}` | {count} |")
    lines.extend(
        [
            "",
            "## Top high-leverage changes",
            "",
        ]
    )
    for index, item in enumerate(report.get("high_leverage_changes", []), start=1):
        lines.append(f"{index}. {esc(item)}")
    lines.extend(
        [
            "",
            "## Recommendations",
            "",
            "| Skill | Current scope | Recommendation | Confidence | Evidence | Reason | Risk notes | Next action |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for row in report["recommendations"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{esc(row['skill'])}`",
                    esc(row["current_scope"]),
                    f"`{esc(row['recommendation'])}`",
                    esc(row["confidence"]),
                    esc(", ".join(row.get("evidence", [])) or "none"),
                    esc(row["reason"]),
                    esc(", ".join(row["risk_notes"]) or "none"),
                    esc(row["suggested_next_action"]),
                ]
            )
            + " |"
        )
    overlap_pairs = report.get("trigger_overlap_pairs", [])
    lines.extend(
        [
            "",
            "## Trigger overlap review",
            "",
        ]
    )
    if overlap_pairs:
        actionable_pairs = [pair for pair in overlap_pairs if pair.get("severity") in {"high", "medium"}]
        low_count = len(overlap_pairs) - len(actionable_pairs)
        if low_count:
            lines.append(f"Low-severity pairs omitted from Markdown: `{low_count}`. Use JSON output for the full list.")
        if actionable_pairs:
            lines.extend(
                [
                    "| Skills | Severity | Type | Positive | Boundary | Description | Shared terms | Recommended action |",
                    "|---|---|---|---:|---:|---:|---|---|",
                ]
            )
        for pair in actionable_pairs:
            lines.append(
                "| "
                + " | ".join(
                    [
                        esc(" <-> ".join(pair["skills"])),
                        esc(pair["severity"]),
                        esc(pair["conflict_type"]),
                        esc(pair["positive_overlap"]),
                        esc(pair["boundary_overlap"]),
                        esc(pair["description_overlap"]),
                        esc(", ".join(pair["shared_terms"]) or "none"),
                        esc(pair["recommended_action"]),
                    ]
                )
                + " |"
            )
        if not actionable_pairs:
            lines.append("No high/medium trigger-overlap pairs crossed the Markdown reporting threshold.")
    else:
        lines.append("No trigger-overlap pairs crossed the heuristic review threshold.")
    lines.extend(["", "## Limitations", ""])
    for item in report.get("limitations", []):
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Heuristically classify skills from an inventory into global/project/explicit/disable review buckets."
    )
    parser.add_argument("inventory", help="Inventory JSON produced by inventory_installed_skills.py.")
    parser.add_argument(
        "--usage-evidence",
        help="Optional JSON/CSV/TSV file with usage evidence keyed by skill name. Columns: skill_name, explicit_invocations, notes, project_scope.",
    )
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Output format.")
    parser.add_argument("--output", help="Write output to a file instead of stdout.")
    args = parser.parse_args()

    inventory = load_json(Path(args.inventory))
    usage = load_usage(Path(args.usage_evidence)) if args.usage_evidence else {}
    report = analyze(inventory, usage)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n" if args.format == "json" else to_markdown(report)
    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
