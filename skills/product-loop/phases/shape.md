# Phase 2: Shape

Two steps, Specify and Plan, for the proposals the user **accepted** or **changed** at checkpoint 1 (`<run>/decisions.json`). Rejected and parked proposals stay out. Then, after checkpoint 2, Apply. `<run>` is the run folder, `<skill>` this skill's folder.

## 6. Specify

For each accepted proposal, write the PRD change as **before / after** text against the PRD file the context pack names:
- a new or changed user story, in the PRD's own format and language,
- a changed requirement, product decision or out-of-scope line,
- an answered open point.

A proposal marked **bet** gets a PR-FAQ first ([../references/frameworks.md](../references/frameworks.md)), in the review doc. Its PRD change follows from it.

A proposal that is a test ("run test Z first") gets no PRD change. It gets a test card: the assumption, the test, who runs it, and what result would change the plan.

**Done when:** every accepted proposal has its PRD change or its test card.

## 7. Plan

1. **Roadmap:** the changes to the roadmap file, as before / after: an item moves between Now, Next and Later, a new item, an item dropped. Use the MoSCoW the user set.
2. **Linear preview:** write `<run>/actions.json`, one entry per action:
   ```json
   [{"id": "A1", "kind": "create_issue", "decision": "P3", "title": "…", "body": "…", "project": "…"},
    {"id": "A2", "kind": "move_status", "decision": "P5", "issue": "STE-214", "from": "Backlog", "to": "Todo"}]
   ```
   Kinds: `create_issue`, `update_project`, `move_status`, `set_priority`, `comment`. Before a `create_issue`, search Linear for an issue that already covers it; found: make it a `comment` or `update` on that issue instead. A new issue gets the label `needs-triage` and its evidence (item IDs and quotes) in the body. Refinement happens later in `define-work`.
3. Check: `python3 "<skill>/scripts/check.py" actions "<run>"`, then the makes-sense check on the whole change set ([../references/checks.md](../references/checks.md)).
4. Add the change set to the review doc: PRD before/after, roadmap before/after, the Linear actions as a table, and exactly what Apply will do. Set `phase` to `checkpoint-2`.

**Done when:** the change set is in the review doc and both checks are done.

## Apply (after checkpoint 2)

Only what the user approved, in this order:

1. **Linear:** each action through the Linear MCP. Check each result. Save the issue IDs in `actions.json`.
2. **Product repo:** edit the PRD and roadmap files. The working tree must be clean and on the default branch; otherwise stop and ask. Commit as `product-loop <run-id>: <one-line summary>`. Push when the user approved pushing at checkpoint 2.
3. **Claude Docs:** add the new input items to the input bank, apply the journey and tree changes, and add one line per decision to the decisions log (date, proposal, decision, evidence IDs).
4. Set `phase` to `retro`.

**Done when:** every approved action is done or reported as failed, with the reason.
