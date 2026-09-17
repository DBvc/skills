"""Mutation tests for the offline package validator, not tests of LLM behavior."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate import validate


class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)/'dbx-epistemic-audit'
        shutil.copytree(Path(__file__).resolve().parents[1], self.root,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

    def tearDown(self):
        self.tmp.cleanup()

    def edit_json(self, name, fn):
        p = self.root/'evals'/name
        data = json.loads(p.read_text(encoding='utf-8'))
        fn(data)
        p.write_text(json.dumps(data,ensure_ascii=False), encoding='utf-8')

    def rejected(self):
        self.assertFalse(validate(self.root)['ok'])

    def test_valid_package(self):
        self.assertTrue(validate(self.root)['ok'])

    def test_missing_file(self):
        (self.root/'references/examples.md').unlink()
        self.rejected()

    def test_missing_frontmatter(self):
        (self.root/'SKILL.md').write_text('# No metadata\n')
        self.rejected()

    def test_wrong_name(self):
        p=self.root/'SKILL.md'
        p.write_text(p.read_text().replace('name: dbx-epistemic-audit','name: other',1))
        self.rejected()

    def test_implicit_policy_drift(self):
        p=self.root/'agents/openai.yaml'
        p.write_text(p.read_text().replace('allow_implicit_invocation: false','allow_implicit_invocation: true'))
        self.rejected()

    def test_bad_json(self):
        (self.root/'evals/evals.json').write_text('{')
        self.rejected()

    def test_duplicate_trigger(self):
        self.edit_json('triggers.json',lambda d:d['cases'].append(d['cases'][0].copy()))
        self.rejected()

    def test_non_boolean_trigger(self):
        self.edit_json('triggers.json',lambda d:d['cases'][0].update(expected_trigger=1))
        self.rejected()

    def test_invalid_kind(self):
        self.edit_json('evals.json',lambda d:d['evals'][0].update(kind='happy'))
        self.rejected()

    def test_bad_regex(self):
        self.edit_json('evals.json',lambda d:d['evals'][0]['checks']['output'][0].update(value='['))
        self.rejected()

    def test_marker_only(self):
        def patch(d):
            d['evals'][0]['checks']['output']=[{'type':'must_contain','value':'## Summary','required':True,'quality':'behavior'}]
        self.edit_json('evals.json',patch)
        self.rejected()

    def test_no_required_check(self):
        def patch(d):
            for c in d['evals'][0]['checks']['output']:
                c['required']=False
        self.edit_json('evals.json',patch)
        self.rejected()

    def test_missing_bucket(self):
        self.edit_json('evals.json',lambda d:d['evals'][0]['checks'].pop('process'))
        self.rejected()

    def test_nan_threshold(self):
        self.edit_json('evals.json',lambda d:d.update(pass_threshold=float('nan')))
        self.rejected()

    def test_pair_unknown_member(self):
        self.edit_json('metamorphic.json',lambda d:d['pairs'][0].update(case_ids=['not-a-case','stance-pro']))
        self.rejected()

    def test_pair_same_member(self):
        self.edit_json('metamorphic.json',lambda d:d['pairs'][0].update(case_ids=['stance-pro','stance-pro']))
        self.rejected()

    def test_broken_link(self):
        p=self.root/'README.md'
        p.write_text(p.read_text()+'\n[Missing](absent.md)\n')
        self.rejected()

    def test_link_escape(self):
        p=self.root/'README.md'
        p.write_text(p.read_text()+'\n[Outside](../../outside.md)\n')
        self.rejected()

    def test_kind_wrong_type(self):
        self.edit_json('evals.json',lambda d:d['evals'][0].update(kind=[]))
        self.rejected()

    def test_check_type_wrong_type(self):
        self.edit_json('evals.json',lambda d:d['evals'][0]['checks']['output'][0].update(type=[]))
        self.rejected()

    def test_quality_wrong_type(self):
        self.edit_json('evals.json',lambda d:d['evals'][0]['checks']['output'][0].update(quality=[]))
        self.rejected()

    def test_symlink(self):
        p=self.root/'references/examples.md'
        p.unlink()
        p.symlink_to(self.root/'README.md')
        self.rejected()


if __name__ == '__main__':
    unittest.main()
