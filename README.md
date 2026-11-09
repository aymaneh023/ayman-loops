# ayman-loops

Loops for Claude Code: skills that run a whole piece of work through fixed steps, check their own output, and stop at checkpoints where a person decides. The tech loop (plan, build, review) lives in [ayman-skills](https://github.com/aymaneh023/ayman-skills). This repo holds the loops for other kinds of work.

This repo holds only the generic loops. Company information (customer input, product context, decisions) lives in each company's own Claude Docs, Linear and product repo, never here.

## Loops

| Loop | What it does |
|---|---|
| `product-loop` | Turns raw input (interviews, buyer or GTM input, technical research, your own ideas) into proposed changes to one product's journey, opportunity tree, PRD, roadmap and Linear. You decide at two checkpoints. |

## product-loop

```
/product-loop <product> <file, pasted text, Drive link or Wispr Flow meeting>
/product-loop <product> resume
```

```
any input
  → Sense   capture → understand (blind to the roadmap) → map → explore → assess
  → checkpoint 1: you pick options, set Ease and MoSCoW, mark big bets
  → Shape   specify (PRD, PR-FAQ for a bet) → plan (roadmap, Linear preview)
  → checkpoint 2: you approve; then it writes to Linear and the product repo
  → Retro   proposes changes to the loop itself; you approve
```

A cheap test chosen in Assess runs in the real world; its result is new input for a later run.

The first run for a product sets up its context pack: one Claude Doc with the product's goal, segments, documents and Linear team. See `skills/product-loop/references/context-pack.md`.

Needs: the Claude Docs connector, the Linear MCP, the Google Drive connector for Drive links, and `python3` for the check script.

## Install

```bash
git clone https://github.com/aymaneh023/ayman-loops.git ~/dev/ayman-loops
~/dev/ayman-loops/install.sh      # macOS / Linux
```

On Windows: `install.ps1`. Both link each skill in `skills/` into `~/.claude/skills/` and skip links that exist. Run again after a pull.

## Tests

```bash
python3 -m unittest discover -s skills/product-loop/scripts
```
