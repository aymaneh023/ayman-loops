---
name: product-loop
description: Turn raw input (interviews, GTM notes, technical research, your own ideas) into proposed changes to one product's journey, opportunity tree, PRD, roadmap and Linear, with you deciding at two checkpoints. /product-loop <product> [input]
disable-model-invocation: true
---

# Product loop

Take any input about one product and turn it into **proposed changes** to that product's documents and Linear. The user and their co-founders decide at two checkpoints. Nothing outside the run folder and the product's Claude Docs changes before checkpoint 2.

```
/product-loop <product> <file, pasted text, Drive link or Wispr Flow meeting>
/product-loop <product> resume
```

Run it in a main session. The checks start subagents, and a subagent cannot start its own.

## Where things live

| What | Where | Shared? |
|---|---|---|
| Context pack: the product's chain of documents, goal, segments, Linear team, repo path | Claude Doc "<Product>: product context" | Yes |
| Input bank: every input item of the product, over all runs | Claude Doc "<Product>: input bank" | Yes |
| Product picture: journey, opportunity tree, decisions log | Claude Docs, listed in the context pack | Yes |
| Review doc: one per run, the proposals and the change set | Claude Doc "<Product>: run <run-id>" | Yes |
| PRD and roadmap | The product repo, at the paths in the context pack | Yes, after checkpoint 2 |
| Work | Linear, the team in the context pack | Yes, after checkpoint 2 |
| Doc links per product | `~/.claude/loop-runs/<product>/product.json` | Local |
| Run folder: source copies, input items, proposals, decisions, state | `~/.claude/loop-runs/<product>/<run-id>/` (run-id = `YYYYMMDD-HHMM`) | Local |

Business information lives in Claude Docs, Linear, the product repo and the local run folder. The `ayman-loops` repo holds only the generic loop.

Use the Claude Docs connector for every doc, and follow its own instructions for loading and drawing. Use the Linear MCP for Linear.

## Start

1. **Product.** The first argument names it. Missing: ask.
2. **Resume.** A run folder of this product whose `state.json` has `phase` other than `done`: offer to resume it from its phase. `resume` as the argument: resume the newest one.
3. **Setup.** `product.json` missing: first-time setup, as [references/context-pack.md](references/context-pack.md) says. It ends with the user confirming the context pack.
4. **Read** the context pack doc. Make the run folder. Write `state.json`: `{"product", "run_id", "phase": "sense", "review_doc": null}`. Update `phase` at every change; a resumed run starts from it.
5. **Input.** Everything the user gave is the input. Nothing given: ask for it.

## The run

Read each phase file at the start of that phase, not earlier.

1. **Sense**: [phases/sense.md](phases/sense.md). Capture, Understand, Map, Explore, Assess. Ends with the review doc published.
2. **Checkpoint 1: decide.** See *Checkpoints*. For each proposal the user accepts, rejects, changes or parks it, sets **Ease** (1–10) and **MoSCoW**, and marks a big new idea as a **bet**.
3. **Shape**: [phases/shape.md](phases/shape.md). Specify, Plan. Ends with the change set and the Linear preview in the review doc.
4. **Checkpoint 2: approve.** The user approves the change set, or changes it.
5. **Apply**: the last section of [phases/shape.md](phases/shape.md).
6. **Retro**: [phases/retro.md](phases/retro.md).

Set `phase` to `done` and end with a short report: what changed where (with links), what is parked, and the cheapest tests the user chose to run.

## Checkpoints

1. Bring the review doc up to date and open it with the Artifact tool's `open` action.
2. Send a push notification: `<Product> run <run-id>: checkpoint <n> ready, <k> proposals, <f> flags.`
3. Wait. Decisions arrive as comments in the review doc or as chat messages, from the user or a co-founder. Answer a question in its comment thread.
4. Record each decision in `decisions.json` (`{"P3": {"decision": "accept", "ease": 6, "moscow": "Should", "bet": false, "note": "…"}}`) and in the review doc next to its proposal.
5. The checkpoint is passed when **every** proposal (checkpoint 1) or the whole change set (checkpoint 2) has a decision. An open item: ask about that item by its ID.

## Checks

Every step ends with its check, as [references/checks.md](references/checks.md) says: the script for what can be checked exactly, then the makes-sense check by three isolated cheap models. A step that fails gets at most 2 fix rounds, then goes on with the problem flagged in the review doc.

## Rules that hold in every step

- Every quote is copied word for word from its source. Where the input bank holds no evidence for a claim, the proposal says "no evidence yet".
- The user's own ideas and technical research are input items with their own type ([references/input-types.md](references/input-types.md)). An idea is a hypothesis until evidence supports it.
- People appear as role + code ("Teacher, P03"). Names stay in the run folder's `people.json`.
- Ease and MoSCoW come from the user. The loop proposes Impact and Confidence, each with a one-line reason.
- Frameworks, scales and templates: [references/frameworks.md](references/frameworks.md).
