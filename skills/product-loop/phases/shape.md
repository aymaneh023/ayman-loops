# Phase 2: Shape

Three steps, Refine, Specify and Plan, for the proposals the user **accepted** or **changed** at checkpoint 1 (`<run>/decisions.json`). Rejected and parked proposals stay out. Then, after checkpoint 2, Apply. `<run>` is the run folder, `<skill>` this skill's folder.

## 5b. Refine

Before writing any change, check the picture with the user. A decision on a proposal says yes or no; it does not say what the thing looks like.

1. Ask short rounds of two or three questions, one topic per round: what each user gets, what the content is, what the other roles see, what is in the first version and what comes later. Ask about anything the loop filled in itself. Give a recommendation when the user asks which option is better.
2. Save the answers word for word as a source in `<run>/sources/` and add them as input items.
3. Write the picture back in plain words, as short lists per user, and say which points the loop filled in itself. Go on only when the user confirms it.

**Done when:** the user confirmed the picture.

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
   The preview covers the whole board, not only new issues:
   - the text of the initiative, when the goal or the scope changed (`update_project`, with the initiative named in `project`);
   - the text of each project that changes (`update_project`);
   - the status of projects: planned for what is needed now, backlog for later (`update_project`);
   - the status of issues: to do for what is needed now, backlog for later (`move_status`);
   - new issues (`create_issue`).

   Check who made each project and issue the preview touches. List the ones that belong to someone other than the user and ask about each by name; leave them alone until the user says yes.

   Kinds: `create_issue`, `update_project`, `move_status`, `set_priority`, `comment`. Before a `create_issue`, search Linear for an issue that already covers it; found: make it a `comment` or `update` on that issue instead. A new issue gets the label `needs-triage` and its evidence (item IDs and quotes) in the body. Refinement happens later in `define-work`.
3. Check: `python3 "<skill>/scripts/check.py" actions "<run>"`, then the makes-sense check on the whole change set ([../references/checks.md](../references/checks.md)).
4. Add the change set to the review doc: PRD before/after, roadmap before/after, the Linear actions as a table, and exactly what Apply will do. Also list the other places that describe the plan and that this run does not change (project descriptions, an architecture document, a published overview), so the user knows what goes out of date. Set `phase` to `checkpoint-2`.

**Done when:** the change set is in the review doc and both checks are done.

## Apply (after checkpoint 2)

Only what the user approved, in this order:

1. **Linear:** each action through the Linear MCP. Check each result. Save the issue IDs in `actions.json`.
2. **Product repo:** edit the PRD and roadmap files. The working tree must be clean and on the default branch; otherwise stop and ask. Commit as `product-loop <run-id>: <one-line summary>`. Push when the user approved pushing at checkpoint 2.
3. **Claude Docs:** add the new input items to the input bank, apply the journey and tree changes, and add one line per decision to the decisions log (date, proposal, decision, evidence IDs).
4. Set `phase` to `retro`.

**Done when:** every approved action is done or reported as failed, with the reason.
