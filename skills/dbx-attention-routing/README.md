# dbx-attention-routing

A DBX skill for recurring attention-allocation decisions across mixed inputs.

It is intentionally product-agnostic. Saved articles, notes, tasks, courses, tools, feeds, market messages, and project ideas all pass through the same kernel:

```text
What is this item asking from attention, and what should it become?
```

Canonical routes:

```text
act_now | build | test | track | store | incubate | drop | guard | clarify
```

Layer model:

```text
kernel     stable route logic and evidence/risk gates
profile    personal horizons, thresholds, source maps, vocabulary
adapter    optional mapping to external systems
tooling    scripts, schemas, validation, import/export mechanics
```

Default posture:

- classify from visible evidence only;
- keep the kernel independent from any specific app or productivity method;
- use user-approved profiles for personalization;
- propose profile updates from corrections instead of silently changing memory;
- produce dry-run adapter plans before any external write;
- avoid direct high-risk advice such as trading, medical, legal, or tax instructions.

Validation:

```bash
python3 skills/dbx-attention-routing/scripts/validate_attention_output.py \
  skills/dbx-attention-routing/examples/sample-output.json
```

This skill replaces product-shaped attention triage designs. Product names and methods should live in adapter manifests or personal profile config, not in the runtime kernel.
