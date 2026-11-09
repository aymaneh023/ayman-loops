# Phase 1: Sense

Five steps, in order: Capture, Understand, Map, Explore, Assess. Only the end results are saved: the input items, the review doc, and proposed changes to the product picture. `<run>` is the run folder, `<skill>` this skill's folder.

## 1. Capture

1. Save every input as plain text in `<run>/sources/`, one file each (`01-interview-teacher.md`, …). A Drive link: read it with the Google Drive connector. A Wispr Flow meeting: its transcript. Pasted text: as pasted. Audio without a transcript: stop and ask for the transcript.
2. Read the input bank doc and save its items to `<run>/bank.json` (same fields as below). New IDs continue after its highest `I<n>`.
3. Read every source end to end and split it into **input items**, typed as [../references/input-types.md](../references/input-types.md) says. One observation per item.
4. Replace every person's name with role + code. Keep the key in `<run>/people.json`.
5. Write `<run>/items.json`.
6. Check: `python3 "<skill>/scripts/check.py" quotes "<run>"`. Each failure: copy the quote again from the source, or drop the item.

**Done when:** every source is read to its last line, every item has a type, and the quote check is green.

## 2. Understand (blind)

Start **one** subagent (Agent tool, `model: sonnet`, `description: understand <run-id>`). Give it `items.json` and `bank.json` as text, and this task:

> These are input items about one product: what customers, buyers and the team said or found. Find the **opportunities**: problems or unmet needs, in the words of the people who have them. Not features. For each: a one-sentence statement, who has it (segment or role), the item IDs that support it, and the item IDs that contradict it. Also list items that fit no opportunity, and tensions between items. Use only these items. Cite IDs for every statement. Return JSON: `{"opportunities":[{"id":"O1","statement":"…","who":"…","supports":["I3"],"contradicts":[],"new_items":["I3"]}],"unplaced":["I9"],"tensions":["…"]}`.

Give it nothing else: no PRD, roadmap, journey or context pack. It must not see what the product already plans. Save its answer to `<run>/opportunities.json`. Opportunity IDs already in the opportunity tree doc keep their ID when the statement matches; match them in step 3, not here.

**Done when:** `opportunities.json` exists and every cited ID exists in `items.json` or `bank.json`.

## 3. Map

Now read the product documents the context pack lists: journey, opportunity tree, PRD, roadmap, open points, and the titles of the decisions (ADRs, decisions log).

For each opportunity:
- **Compare:** `confirms` (the product already plans for it: say where), `contradicts` (the evidence goes against a plan or decision: say which), or `new`.
- **Journey:** which moment of whose journey it touches. Propose the change to the journey doc. No journey doc yet: propose a first version for the segments the items cover, marked as a draft.
- **Tree:** where it hangs under the goal in the opportunity tree. Propose the change. No tree yet: propose a first version.

**Done when:** every opportunity has a comparison, a journey place and a tree place.

## 4. Explore

For each opportunity that is `new`, `contradicts`, or gained support in this run: list the **options** that could solve it. Include:
- options that already exist in the roadmap or PRD,
- options from items of type `own_idea` and `tech_research` (they belong here, not as evidence),
- "do nothing" or "solve it elsewhere",
- your own options when they add a real alternative.

As many as make sense. Two options that differ only in detail are one option.

**Done when:** every opportunity in scope has its options, each with one line on what it is.

## 5. Assess

For each option, using [../references/frameworks.md](../references/frameworks.md):
- **Assumptions:** what must be true, sorted by the four risks (value, usability, feasibility, viability). The riskiest one first.
- **Confidence** 0–10, from the type and number of supporting items, with a one-line reason.
- **Impact** 1–10 on the goal in the context pack, with a one-line reason.
- **Cheapest test** of the riskiest assumption.
- **Ease**: left empty for the user.

Turn the results into **proposals** in `<run>/proposals.md`, in the format of [../references/review-doc.md](../references/review-doc.md). A proposal is one decision the user can make: take option X for opportunity Y, run test Z first, move or drop a roadmap item, update the journey or tree.

Check, as [../references/checks.md](../references/checks.md) says:
1. `python3 "<skill>/scripts/check.py" citations "<run>"`.
2. The makes-sense check on every proposal.

Then publish the review doc as [../references/review-doc.md](../references/review-doc.md) says. Set `state.json` `phase` to `checkpoint-1` and save the doc link in `review_doc`.

**Done when:** the review doc is published, the citation check is green, and every proposal shows its makes-sense verdict.
