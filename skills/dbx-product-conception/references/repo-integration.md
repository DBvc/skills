# DBX Repository Integration

The package includes an idempotent installer. This file documents the exact collection-level additions for manual review or installation.

## Boundary

```text
dbx-product-conception
  discover/reframe/generate/select what an undefined product should be
  -> selected but unvalidated product thesis

dbx-product-judgment
  judge whether a defined direction is valuable, coherent, viable, trustworthy, or worth building
  -> evidence-bounded verdict and validation plan

dbx-crystallize
  turn a chosen direction into precise requirements, scope, non-goals, acceptance criteria, and handoff
  -> requirement contract

dbx-design-judgment
  judge or shape a concrete design surface after product intent is sufficiently fixed
  -> design findings or handoff
```

## README row

```markdown
| [`dbx-product-conception`](skills/dbx-product-conception/) | 从技术/行为变化、弱信号、人类张力或竞争构想中发现、重构并选择产品方向，通过结构化分歧、体验样本和 creative selection 形成产品 thesis、kill list 与验证交接。Discover and select not-yet-defined product directions before product judgment. |
```

## DBX_SKILL_INDEX row

```markdown
| `dbx-product-conception` | Discover, reframe, generate, and select not-yet-defined product directions from weak signals, enabling changes, human tensions, or competing concepts. | product conception + creative selection + taste calibration | L5 | Fluent but derivative concepts, lone-genius role-play, novelty inflation, and overlap with product judgment or requirement crystallization. | Use before `dbx-product-judgment` when direction itself is unknown; route selected concepts to product judgment and chosen requirements to `dbx-crystallize`. | Add real before/after conception cases and a durable judgment-ledger adapter after 10 uses. |
```

## Routing primary-intent row

Insert before the product-judgment row:

```markdown
| Discover, invent, reframe, or select what a not-yet-defined product should be from enabling changes, weak signals, human tensions, or competing concepts | `dbx-product-conception` | `dbx-product-judgment` when a defined direction already exists and needs a correctness verdict; `dbx-crystallize` when direction is chosen and requirements need precision; generic idea lists or market summaries when no product-conception task exists. |
```

## Skill graph relationship

```markdown
| `dbx-product-conception` precedes product judgment and requirement crystallization when product direction is not yet selected | Generate structurally distinct product logics, make serious candidates experiential, select a thesis, and state explicit kill decisions. Hand the selected but unvalidated concept to `dbx-product-judgment`; hand a chosen direction to `dbx-crystallize` only when requirement precision becomes primary. |
```

## Routing subsection

```markdown
### Product conception

Use `dbx-product-conception` when the primary task is discovering, inventing, reframing, or selecting what a product should fundamentally be before a stable product object or PRD exists. It turns weak signals, enabling changes, human tensions, or competing concepts into distinct product logics and concrete experience specimens, then performs creative selection without claiming that the winner is product-correct. Route a selected direction to `dbx-product-judgment` for evidence-bounded product correctness, to `dbx-crystallize` for requirement precision after direction is chosen, and to `dbx-design-judgment` only after product intent is sufficiently fixed.
```

## Related frontmatter clarifications

`dbx-product-judgment`:

```text
Prefer dbx-product-conception when inventing or reframing an undefined direction; prefer dbx-design-judgment when product intent and rules are fixed and the concrete design surface dominates.
```

`dbx-crystallize`:

```text
Prefer dbx-product-conception when the product direction itself must still be invented or selected.
```

These are routing controls only. Do not duplicate the conception kernel in either downstream skill.

## Collection-level regression boundary

```text
“What should this new capability become?”       -> dbx-product-conception
“Is this proposed product worth building?”      -> dbx-product-judgment
“Turn this chosen idea into buildable scope.”   -> dbx-crystallize
```

For routing evals, expose candidate descriptions and preload no skill body before selection.
