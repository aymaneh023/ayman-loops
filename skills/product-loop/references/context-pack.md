# Context pack and first-time setup

The context pack is one Claude Doc per product. The loop reads it at the start of every run. It holds everything that differs between companies, so the loop itself stays the same.

## What the context pack holds

| Section | Content |
|---|---|
| **Product** | One paragraph: what it is, for whom |
| **Goal** | The outcome the product works toward now, with a measure if one exists. Impact is scored against it. |
| **Segments** | Users and buyers, with the names the team uses (for example student, parent, reseller) |
| **Chain** | The product's documents in order, from input to work, and where each lives: input bank, journey, opportunity tree, PRD, roadmap, open points, decisions (ADRs, decisions log), Linear |
| **Linear** | Team, the projects the loop may touch, the triage label |
| **Repo** | Local path of the product repo, default branch, PRD and roadmap file paths |
| **Language** | Output language. Quotes always stay in the source language. |
| **Reviewers** | Who decides at the checkpoints |

## First-time setup

Runs when `~/.claude/loop-runs/<product>/product.json` does not exist.

1. Ask for the product repo path. Read its PRD, roadmap, README, glossary and agent docs (`AGENTS.md`, `CLAUDE.md`, `docs/agents/`) to find the Linear team and the documents of the chain.
2. Draft the context pack from what you read. Mark every line you inferred, rather than read, as `(inferred)`. The goal is often not written down: draft it from the PRD's problem and the roadmap's current phase, marked `(inferred)`.
3. Create the docs in Claude Docs: "<Product>: product context", "<Product>: input bank" (a table: ID, type, speaker, quote, observation, source, date, run), and, when the chain has none yet, "<Product>: journey", "<Product>: opportunity tree", "<Product>: decisions log". The journey and tree start empty; the first run proposes their first versions.
4. Open the context pack with the Artifact tool's `open` action and ask the user to correct it, especially the lines marked `(inferred)`.
5. Write `product.json` once the user confirms:

```json
{"product": "<product>", "context_pack": "<doc link>", "input_bank": "<doc link>",
 "journey": "<doc link>", "opportunity_tree": "<doc link>", "decisions_log": "<doc link>",
 "repo": "/path/to/repo", "prd": "docs/SPEC.md", "roadmap": "docs/ROADMAP.md"}
```

`product.json` only points at things. Business content stays in the docs.
