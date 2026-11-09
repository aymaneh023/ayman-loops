# Checks

Two layers. The script checks what can be checked exactly. The makes-sense check judges whether a proposal holds up.

## The script

`python3 "<skill>/scripts/check.py" <check> "<run>"`. Exit 0 is green; exit 1 prints every failure.

| Check | When | What it checks |
|---|---|---|
| `quotes` | After Capture | Every quote in `items.json` appears in its source file, word for word (spaces, quote marks, dashes and case are normalised; `...` marks a gap) |
| `citations` | After Assess | Every proposal in `proposals.md` cites at least one item, and every cited `I<n>` exists in `items.json` or `bank.json`. Warns when a proposal rests only on `own_idea` items. |
| `actions` | After Plan | Every Linear action in `actions.json` has a known kind and points to a proposal the user accepted or changed |

## The makes-sense check

Three subagents check the same thing, each on its own: Agent tool, `model: haiku`, started in one message so they run in parallel, none sees another's answer. Give each the proposal(s), the items they cite (with quotes), the goal from the context pack, and this task:

> You review a product proposal. Read the evidence and the goal. Answer for each proposal: does it make sense? Check: (1) does the cited evidence really support it, or does it stretch it; (2) is there evidence in the list that goes against it; (3) does it serve the goal; (4) is there a clearly smaller or cheaper way to get the same answer. Return JSON per proposal: `{"id": "P3", "verdict": "makes_sense" | "doubtful" | "no", "reason": "one sentence"}`.

- Two or three say `makes_sense`: it passes.
- Otherwise: flag it in the review doc with each reviewer's reason. A flag is information for the user, not a block.
- A proposal the reviewers call `no` gets one fix round from you first: change it, or keep it and say why. Then check it again once.

## Stop rule

A step whose check fails gets at most 2 fix rounds. Then it goes on, and the review doc lists what is still failing.

## Spot check

Each review doc shows three random input items next to the source lines they came from, so the user can see Capture still works.
