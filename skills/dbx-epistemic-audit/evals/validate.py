#!/usr/bin/env python3
"""Offline package checks only. Does not execute models or prove semantic quality."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True
NAME = 'dbx-epistemic-audit'
KINDS = {'positive', 'negative', 'near_miss', 'failure_mode', 'safety'}
BUCKETS = ('trigger', 'process', 'output', 'safety')
TYPES = {'must_contain', 'must_not_contain', 'must_start_with', 'regex'}
QUALITIES = {'structural', 'behavior', 'artifact', 'specificity', 'domain',
             'safety', 'validation', 'placement', 'state', 'collection'}
ID_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
REQUIRED = (
    'SKILL.md', 'README.md', 'agents/openai.yaml',
    'references/evidence-checks.md', 'references/examples.md',
    'evals/triggers.json', 'evals/evals.json', 'evals/metamorphic.json',
    'evals/human-rubric.md', 'evals/README.md', 'evals/design-notes.md',
)


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def fraction(value: Any) -> bool:
    return (type(value) in (int, float) and math.isfinite(value)
            and 0 < value <= 1)


def weak_marker(value: str) -> bool:
    norm = ' '.join(value.strip().lower().split())
    exact = {'skill.md', 'evals/evals.json', 'evals/triggers.json', 'scripts/',
             'references/', 'assets/', 'evals/', 'checks', 'pass_threshold',
             'skill_shape', 'dominant_failure_modes', 'domain_substance_gates',
             'patch_hypothesis', 'control_surface_map', 'placement_decision',
             'mode:', 'route:', 'operation:'}
    return (norm in exact or bool(re.match(r'^#{1,6}\s', norm))
            or bool(re.match(r'^(mode|route|operation):\s*[-_a-z0-9]+$', norm))
            or norm.startswith('```'))


def validate(skill_dir: Path) -> dict[str, Any]:
    root = skill_dir.resolve()
    errors: list[str] = []
    counts: dict[str, int] = {}
    if not root.is_dir():
        return {'ok': False, 'errors': ['Skill directory does not exist.'], 'counts': {}}
    # Reject symlink payloads before reading any content.
    symlinks = [str(p.relative_to(root)) for p in root.rglob('*') if p.is_symlink()]
    if symlinks:
        return {'ok': False, 'errors': ['Symlinks are not accepted: ' + ', '.join(symlinks)], 'counts': {}}
    for name in REQUIRED:
        if not (root/name).is_file():
            errors.append(f'Missing required file: {name}')
    if errors:
        return {'ok': False, 'errors': errors, 'counts': counts}

    def read(name: str) -> str:
        try:
            return (root/name).read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{name}: cannot read UTF-8: {exc}')
            return ''

    def obj(name: str) -> dict[str, Any]:
        try:
            data = json.loads(read(name))
        except (ValueError, TypeError) as exc:
            errors.append(f'{name}: invalid JSON: {exc}')
            return {}
        if not isinstance(data, dict):
            errors.append(f'{name}: root must be an object')
            return {}
        if data.get('skill_name') != NAME:
            errors.append(f'{name}: wrong skill_name')
        return data

    text = read('SKILL.md')
    front = re.match(r'\A---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not front:
        errors.append('SKILL.md: strict YAML frontmatter required')
    else:
        block = front.group(1)
        n = re.search(r'^name:\s*([^\n]+)$', block, re.M)
        if not n or n.group(1).strip() != NAME or root.name != NAME:
            errors.append('SKILL.md: name must equal directory and expected skill name')
        d = re.search(r'^description:\s*(.*)', block, re.M | re.S)
        if not d or not 25 <= len(d.group(1).strip()) <= 1024:
            errors.append('SKILL.md: invalid/missing description')
    counts['skill_lines'] = len(text.splitlines())
    if counts['skill_lines'] > 500:
        errors.append('SKILL.md: exceeds the 500-line package budget')
    yaml = read('agents/openai.yaml')
    if not re.search(r'(?m)^policy:\s*\n\s+allow_implicit_invocation:\s*false\s*$', yaml):
        errors.append('agents/openai.yaml: explicit-only invocation policy missing')
    for key in ('display_name', 'short_description', 'default_prompt'):
        if not re.search(rf'(?m)^\s+{key}:\s*".+"\s*$', yaml):
            errors.append(f'agents/openai.yaml: missing quoted {key}')
    if '$'+NAME not in yaml:
        errors.append('agents/openai.yaml: default_prompt must name the skill')

    def case_array(data: dict[str, Any], key: str, file: str) -> list[dict[str, Any]]:
        seq = data.get(key)
        if not isinstance(seq, list) or not seq:
            errors.append(f'{file}: {key} must be a non-empty array')
            return []
        ids: set[str] = set()
        accepted = []
        for item in seq:
            if not isinstance(item, dict):
                errors.append(f'{file}: case must be an object')
                continue
            ident = item.get('id')
            if not isinstance(ident, str) or not ID_RE.fullmatch(ident):
                errors.append(f'{file}: invalid case id')
            elif ident in ids:
                errors.append(f'{file}: duplicate id {ident}')
            else:
                ids.add(ident)
            if not isinstance(item.get('kind'), str) or item.get('kind') not in KINDS:
                errors.append(f'{file}: {ident}: invalid kind')
            if not nonempty(item.get('prompt')):
                errors.append(f'{file}: {ident}: missing prompt')
            accepted.append(item)
        counts[file] = len(accepted)
        return accepted

    triggers = case_array(obj('evals/triggers.json'), 'cases', 'triggers')
    for c in triggers:
        if type(c.get('expected_trigger')) is not bool:
            errors.append(f'triggers: {c.get("id")}: expected_trigger must be bool')
        if not nonempty(c.get('rationale')):
            errors.append(f'triggers: {c.get("id")}: missing rationale')
    if not {'positive','negative','near_miss'} <= {c.get('kind') for c in triggers if isinstance(c.get('kind'), str)}:
        errors.append('triggers: missing positive/negative/near_miss coverage')

    edata = obj('evals/evals.json')
    if not fraction(edata.get('pass_threshold')):
        errors.append('evals: invalid pass_threshold')
    evaluations = case_array(edata, 'evals', 'evals')
    for c in evaluations:
        prefix = f'evals: {c.get("id")}'
        if not nonempty(c.get('expected_behavior')):
            errors.append(prefix + ': missing expected_behavior')
        buckets = c.get('checks')
        if not isinstance(buckets, dict):
            errors.append(prefix + ': checks must be an object')
            continue
        strong = 0
        for bucket in BUCKETS:
            checks = buckets.get(bucket)
            if not isinstance(checks, list):
                errors.append(prefix + f': missing array checks.{bucket}')
                continue
            for ch in checks:
                if not isinstance(ch, dict):
                    errors.append(prefix + ': check must be an object')
                    continue
                value = ch.get('value')
                typ = ch.get('type')
                quality = ch.get('quality')
                required = ch.get('required')
                if not isinstance(typ, str) or typ not in TYPES or not nonempty(value):
                    errors.append(prefix + ': invalid check type/value')
                if type(required) is not bool or not isinstance(quality, str) or quality not in QUALITIES:
                    errors.append(prefix + ': invalid required/quality')
                if isinstance(value, str):
                    if typ == 'regex':
                        try:
                            re.compile(value)
                        except re.error:
                            errors.append(prefix + ': invalid regex')
                    if isinstance(quality, str) and quality in QUALITIES-{'structural'} and weak_marker(value):
                        errors.append(prefix + ': mislabeled marker-only assertion')
                    if required is True and isinstance(quality, str) and quality in QUALITIES-{'structural'} and not weak_marker(value):
                        strong += 1
        if not strong:
            errors.append(prefix + ': required non-marker assertion missing')
        pc = c.get('pass_criteria')
        if not isinstance(pc, dict) or type(pc.get('all_required')) is not bool or not fraction(pc.get('min_score')):
            errors.append(prefix + ': invalid pass_criteria')
    kinds = [c.get('kind') for c in evaluations if isinstance(c.get('kind'), str)]
    if kinds.count('positive') < 2 or not {'negative','near_miss'} <= set(kinds) or not {'failure_mode','safety'} & set(kinds):
        errors.append('evals: insufficient kind coverage')

    pairdata = obj('evals/metamorphic.json')
    pairs = pairdata.get('pairs')
    if not isinstance(pairs, list) or not pairs:
        errors.append('metamorphic: pairs must be a non-empty array')
        pairs = []
    case_ids = {c.get('id') for c in evaluations if isinstance(c.get('id'), str)}
    seen_pairs: set[str] = set()
    for p in pairs:
        if not isinstance(p, dict):
            errors.append('metamorphic: pair must be an object')
            continue
        pid = p.get('id')
        if not isinstance(pid, str) or not ID_RE.fullmatch(pid) or pid in seen_pairs:
            errors.append('metamorphic: invalid/duplicate pair id')
        else:
            seen_pairs.add(pid)
        members = p.get('case_ids')
        if (not isinstance(members, list) or len(members) != 2
            or not all(isinstance(i,str) for i in members)
            or len(set(members)) != 2 or not set(members) <= case_ids):
            errors.append(f'metamorphic: {pid}: missing/duplicate/invalid case references')
        for f in ('controlled_change','review_rule'):
            if not nonempty(p.get(f)):
                errors.append(f'metamorphic: {pid}: missing {f}')
        for f in ('must_remain','expected_change'):
            values = p.get(f)
            if not isinstance(values,list) or not values or not all(nonempty(v) for v in values):
                errors.append(f'metamorphic: {pid}: invalid {f}')
    counts['metamorphic_pairs'] = len(pairs)

    for doc in root.rglob('*.md'):
        body = read(str(doc.relative_to(root)))
        for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',body):
            if re.match(r'^[a-z]+:',target) or target.startswith('#'):
                continue
            path = (doc.parent/target.split('#')[0]).resolve()
            if not path.is_relative_to(root):
                errors.append(f'{doc.relative_to(root)}: local link escapes skill: {target}')
            elif not path.exists():
                errors.append(f'{doc.relative_to(root)}: broken link: {target}')
    return {'ok': not errors, 'errors': errors, 'counts': counts,
            'scope': 'Offline package/fixture structure only; no LLM or semantic eval executed.'}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('skill_dir', nargs='?', default=str(Path(__file__).resolve().parents[1]))
    args = ap.parse_args()
    result = validate(Path(args.skill_dir))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
