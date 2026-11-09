# Phase 3: Retro

Improve the loop itself from what the user changed. `<run>` is the run folder.

1. **Compare** what the loop proposed with what the user decided (`proposals.md`, `decisions.json`, comments in the review doc):
   - proposals accepted as they were, changed, rejected, parked;
   - options the user added that Explore missed;
   - Impact or Confidence scores the user disagreed with;
   - makes-sense flags that turned out right, and ones that were noise;
   - checks that failed, and fix rounds used.
2. **Save the golden case:** write `<run>/golden.json` with each proposal, the user's decision and the reason. Later retros read earlier golden cases to see whether a change to the loop helped.
3. **Propose** at most five changes to the loop's own files in `~/dev/ayman-loops/skills/product-loop/`. Each one: the file, the change, and the evidence from this run (and earlier golden cases when they show the same pattern). Example: "Explore missed a 'do nothing' option in 3 of 4 opportunities → sense.md step 4: list it first."
4. Ask the user per change. Make only the approved ones, and commit them in `~/dev/ayman-loops` as `retro <product> <run-id>: <summary>`. Ask before pushing: the repo is public. No product names, quotes or business facts go into the repo: write each change in generic terms.
5. Set `phase` to `done`.

**Done when:** `golden.json` is written and every proposed change is approved and made, or declined.
