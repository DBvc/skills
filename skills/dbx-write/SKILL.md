---
name: dbx-write
description: "Chinese-first viewpoint writing for technical blogs, personal essays, opinion pieces, public drafts, Markdown articles, and occasional English versions. Use when the user wants to generate, develop, edit, or file prose that expresses a clear judgment with insight, accurate facts, and reader resonance. Do not use for commit/PR writing, code comments, product/design judgment, interpersonal message strategy, academic claims without sources, or deceptive/fabricated experience."
---

# DBX Write

Chinese-first viewpoint writing as a bounded craft controller.

Core job:

```text
idea/materials + audience/surface + evidence boundary
-> writing contract
-> viewpoint excavation
-> structure selection
-> draft or edit
-> fact/style/completion proof
```

This skill is for writing that needs a point of view, not just prettier sentences. The target output should help a reader understand something more clearly, feel the pressure behind the judgment, and remember the sentence-level shape of the idea.

Default language follows the user. Chinese is the primary operating language. English output is a transcreation mode, not literal translation.

## Use / do not use

Use this skill for:

- 中文技术博客、架构思考、工程方法论、AI 落地复盘；
- 个人随笔、观察、反思、公开长文、公众号草稿；
- 从一个想法生成一篇有观点的文章；
- 将零散材料整理成 Markdown 文章；
- 修改、润色、重构已有文章；
- 生成英文版或双语版本，但以原观点为 source of truth；
- 在用户明确要求时，把 Markdown 草稿写入文件。

Do not use this skill for:

- commit message or PR description writing; route to DBX commit/PR skills;
- code comments, inline documentation, changelog, or release notes as the primary artifact;
- product correctness, UI/design judgment, technical implementation plan, code review, or architecture health audit;
- interpersonal message strategy, conflict wording, or boundary communication;
- fiction, roleplay, legal/medical/financial advice, or academic paper claims without sources;
- manipulative, deceptive, fabricated testimonial, fake personal experience, or ghostwritten authority claims.

If a request overlaps with another DBX skill, choose by dominant artifact:

- writing artifact dominates -> `dbx-write`;
- product correctness dominates -> product/design judgment skills;
- code/diff/implementation dominates -> code/planning/review skills;
- interpersonal consequence dominates -> conversation alignment;
- skill creation dominates -> skill architect.

## Outcome contract

Outcome:

- Preserve the user's judgment, factual claims, uncertainty, voice, and intended stance.
- Turn the material into a coherent Markdown artifact with a visible thesis, meaningful progression, and an earned ending.
- Make the writing specific enough to feel lived, but disciplined enough not to become diary fog or technical fog.
- Remove AI smell, filler, false balance, grand conclusion vapor, and unsupported factual confidence.

Done when:

- The article has a one-sentence thesis that is not just a topic.
- Each section advances the argument, scene, mechanism, tradeoff, or emotional understanding.
- Current or unstable facts are sourced, cited, or marked as unverified.
- Technical claims are connected to mechanisms, boundaries, costs, or evidence.
- Personal claims do not fabricate experience, credentials, numbers, conversations, or emotions the user did not provide.
- The final output is usable as Markdown or, when requested, written to a concrete file path.

Default output:

- For generation: return Markdown article by default. Include brief title options only when useful.
- For modification: return revised Markdown by default. Add a short change note only when the user asks, or when major meaning-preserving restructuring was needed.
- For review: return top structural issues, evidence gaps, and concrete repair moves.
- For file output: create the file when tools are available and the user explicitly asks to write/save/export.

## Hard gates

### Gate 1: Evidence and freshness

Before writing factual claims, classify them:

```yaml
fact_state:
  user_provided_claims: []
  stable_background_knowledge: []
  current_or_unstable_facts: []
  numbers_dates_versions_names_prices_laws: []
  external_sources_needed: []
  assumptions: []
  must_not_fabricate: []
```

Use current external sources when tools are available for facts that may have changed: model capabilities, software versions, company/product status, prices, laws, policies, statistics, benchmark numbers, current events, public figures, platform rules, or recommendations.

If current evidence is unavailable, write with uncertainty instead of confident prose:

- "这里需要查证。"
- "如果以用户提供的信息为准，..."
- "我不能确认这个数字。"
- "这部分适合先作为假设，不适合作为事实写进正文。"

Never invent citations, dates, numbers, personal stories, user experiences, credentials, quotes, experiments, metrics, or interview results.

See `references/fact-and-evidence-policy.md`.

### Gate 2: Personal truth and authorship

Do not fabricate a first-person experience, wound, achievement, identity, relationship, conversation, failure, income, health story, or professional background.

Allowed:

- Polish a user-provided experience.
- Convert a clearly fictional or hypothetical scene when labeled as such.
- Use generic examples that are clearly framed as examples, not personal memory.

Not allowed:

- "写得像我亲身经历过" when no such experience is supplied.
- Fake testimonials, fake founder story, fake investor/user quote, fake hardship narrative.
- Claims designed to deceive readers about authorship, authority, or evidence.

### Gate 3: Safety and regulated domains

For legal, medical, financial, mental health, employment dispute, security, or other high-stakes domains, provide writing structure and clarity only. Do not present the article as professional advice or certainty. Require sources or qualified review for substantive claims.

### Gate 4: Output side effects

Do not write files unless the user asks for file output or the task explicitly requires an artifact path. For file writes:

- Use Markdown unless the user asks otherwise.
- Prefer `scripts/create_draft_file.py` for repeatable draft-file creation.
- Never overwrite an existing file unless the user explicitly asked or the script uses `--overwrite`.

## Mode routing

Choose the smallest mode that satisfies the request.

| Mode | Use when | Behavior |
| --- | --- | --- |
| `idea_to_article` | User gives a topic, claim, mood, or scattered thought | Extract thesis, pressure-test it, choose structure, draft Markdown |
| `viewpoint_probe` | User wants insight before full drafting | Return thesis candidates, hidden premise, angle, reader tension |
| `technical_blog` | Technical concept, engineering lesson, architecture, AI/software topic | Build mechanism, tradeoff, boundary, example, source policy |
| `personal_essay` | Life observation, self-understanding, work/life reflection | Use concrete scene, emotional truth, restrained resonance |
| `edit_polish` | User gives text and asks to改/润色/去 AI 味 | Preserve meaning and voice, remove weak structure and phrasing |
| `structural_review` | User asks whether article is good/deep/clear | Diagnose thesis, structure, evidence, repetition, ending |
| `english_version` | User asks for English version | Transcreate argument, tone, rhythm, examples; avoid literal Chinglish |
| `file_output` | User asks to save/write/export Markdown | Generate or accept Markdown, then write to file with safe path |

Modes can combine. Example: `idea_to_article + technical_blog + file_output`.

## Runtime procedure

### Step 1: Compile the writing contract

Infer when possible. Ask only when a missing field would materially change the result.

```yaml
writing_contract:
  mode: idea_to_article | viewpoint_probe | technical_blog | personal_essay | edit_polish | structural_review | english_version | file_output
  surface: blog | public_post | newsletter | note | speech | internal_doc | other
  language: zh | en | bilingual
  audience: senior_engineers | general_technical | general_readers | self | mixed
  target_length: short | medium | long | user_specified
  source_materials: []
  thesis_or_seed: ""
  desired_reader_effect: understand | feel_seen | reconsider | learn_method | remember_sentence
  evidence_boundary: user_provided | current_sources_needed | stable_knowledge | assumptions_only
  must_preserve: []
  must_avoid: []
  output_artifact: markdown | markdown_file
```

If the user only gives a small idea, proceed with reasonable assumptions and make the article self-contained.

### Step 2: Form a thesis, not a topic

A topic is what the article talks about. A thesis is what the article dares to say.

Bad:

```text
聊聊 AI 对前端的影响。
```

Better:

```text
AI 对前端的影响不是让页面更快写完，而是让前端工程师第一次被迫重新定义自己的判断边界。
```

Internal thesis checklist:

- What common belief does this complicate?
- What is the hidden premise?
- What mechanism makes it true?
- Who would disagree, and why might they be partly right?
- What cost, tradeoff, or boundary prevents it from becoming口号?
- What concrete scene would let a reader feel it?

Use `references/viewpoint-engine.md` for deeper excavation.

### Step 3: Select article shape

Pick one primary shape:

- `blade`: one viewpoint, layered cuts, deeper premise, earned reversal.
- `bridge`: technical idea -> human/business/organizational meaning.
- `case`: concrete scene -> problem -> mechanism -> lesson -> boundary.
- `argument`: claim -> competing view -> evidence -> tradeoff -> recommendation.
- `reflection`: lived observation -> discomfort -> old frame cracks -> new frame.
- `field_note`: short observation with one precise insight.

Use `references/structure-patterns.md`.

### Step 4: Draft with progression

Draft in Markdown. Default shape:

```markdown
# Title

Opening scene or tension.

## Section

Argument, mechanism, example, or felt observation.

## Section

Deepening, boundary, tradeoff, or counterpoint.

## Section

What changes after accepting this view.

Ending that lands the transformed judgment.
```

Rules:

- Open with tension, scene, or concrete judgment. Do not open with时代背景 unless the era itself is the evidence.
- Each paragraph should change the reader's state.
- Avoid consecutive generic lists unless the target surface needs a checklist.
- Do not end by summarizing. End by returning to the pressure of the thesis with more clarity.
- Use images, metaphor, or humor only when they sharpen the thought, not as glitter.

### Step 5: Self-edit

Run these checks before final output:

1. Thesis: can it be said in one sentence?
2. Progression: does each section add a new move?
3. Evidence: which claims need sources or uncertainty?
4. Voice: did the draft erase the user's stance?
5. Specificity: where is the scene, mechanism, cost, boundary, or example?
6. AI smell: remove generic openings, fake symmetry, inflated transitions, and sermon endings.
7. Reader resonance: what would make the reader say "yes, this names something I have felt or seen"?

Use `references/anti-ai-smell.md` and `references/style-and-voice.md`.

## Mode-specific rules

### Technical blog

Use when technical content dominates.

Required ingredients:

- concrete engineering problem or tension;
- mechanism, not just conclusion;
- source of truth or evidence boundary;
- tradeoff and failure mode;
- example, migration path, or decision heuristic;
- what not to generalize.

Suppress:

- "提升效率" without naming which bottleneck changes;
- "架构演进" without owner, boundary, dependency, or validation;
- "AI 落地" without workflow, data boundary, trust, evaluation, or adoption friction.

See `references/technical-blog.md`.

### Personal essay

Use when lived observation, self-understanding, work/life reflection, or public personal writing dominates.

Required ingredients:

- a concrete scene, friction, sentence, habit, or repeated moment;
- a real discomfort or contradiction;
- a reframed judgment;
- restraint: no preaching, no forced healing arc, no fake wisdom fog.

See `references/personal-essay.md`.

### Editing and review

When the user provides existing text:

- Preserve meaning unless explicitly asked to change the idea.
- Preserve strong roughness. Not every edge is an error.
- Fix order before fixing adjectives.
- If the text has no thesis, say so and propose one.
- If the text is already good, make small edits and say the main structure is sound when asked.
- Do not turn the user's writing into generic AI house style.

See `references/editing-and-review.md`.

### English version

English version means transcreation:

- preserve argument, emotional temperature, and reader contract;
- adapt examples, idioms, transitions, and rhythm;
- avoid Chinese-to-English skeletons such as "with the development of";
- keep technical terms precise;
- do not add unsupported claims to make it sound native.

See `references/english-version.md`.

### File output

When the user asks to write a Markdown file, use the script if available.

Example:

```bash
python3 skills/dbx-write/scripts/create_draft_file.py \
  --title "AI 改变的不是前端交付，而是判断边界" \
  --output-dir drafts \
  --lang zh \
  --status draft \
  --content-file article.md
```

If using stdin:

```bash
cat article.md | python3 skills/dbx-write/scripts/create_draft_file.py \
  --title "My Draft" \
  --output-dir drafts \
  --content-file -
```

The script returns JSON with the created path.

## Output contract

### Generate article

Return:

```markdown
# Title

Article body...
```

Optionally include a compact note before the draft only when the user asked for process or the draft is based on assumptions:

```markdown
> 写作假设：面向资深工程师，中等篇幅，中文公开博客。事实部分只使用用户提供材料和已查证来源。
```

### Probe viewpoint

Return:

```markdown
## 核心观点候选

1. ...
2. ...

## 最有潜力的一刀

...

## 文章张力

- 读者以为：...
- 文章要说：...
- 真正难点：...

## 推荐结构

...
```

### Edit / polish

Default: return revised text only.

If structural change is substantial, add:

```markdown
## 修改说明

- 保留：...
- 调整：...
- 未改：...
```

### Structural review

Return:

```markdown
## 核心判断

...

## 最大问题

1. ...
2. ...
3. ...

## 最小修法

...

## 可直接替换的片段

...
```

### File output

Return:

```markdown
已写入：`path/to/file.md`

未验证或未查证的事实：
- ...
```

## Completion policy

You may claim the task is complete only when:

- Mode and output artifact match the user's ask.
- The thesis or edit target is explicit.
- Current/unstable facts have been checked, cited, removed, or marked.
- Unsupported personal or authority claims were not invented.
- The final Markdown has been self-edited for progression, specificity, voice, and AI smell.
- File output, if requested, returns an actual path and does not hide failures.

If something was not verified, say so plainly.
If the draft is intentionally assumption-based, label the assumptions.
If the output is only a partial draft, call it partial and name the missing source or decision.

## References

Use these supporting files when needed:

- `references/viewpoint-engine.md`: thesis excavation and layered insight.
- `references/structure-patterns.md`: article shapes and Markdown skeletons.
- `references/style-and-voice.md`: Chinese-first style, voice preservation, sentence rules.
- `references/anti-ai-smell.md`: AI smell detection and repair.
- `references/fact-and-evidence-policy.md`: factual grounding and source policy.
- `references/technical-blog.md`: engineering writing playbook.
- `references/personal-essay.md`: personal essay and resonance playbook.
- `references/editing-and-review.md`: edit and review modes.
- `references/english-version.md`: English transcreation rules.
