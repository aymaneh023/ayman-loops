# Review doc

One Claude Doc per run, "<Product>: run <run-id>". The user and co-founders read it, comment and decide in it. Pictures first, details below. Write it in the context pack's language, in plain words.

## Layout

1. **Lead:** one or two sentences: what came in, the main finding, how many proposals wait for a decision.
2. **At a glance** (drawn, not as rows):
   - the opportunity tree with this run's changes highlighted,
   - the journey with the touched moments highlighted,
   - the options ranked by Impact × Confidence (a chart; Ease added after checkpoint 1).
3. **Proposals:** one section per proposal, in the format below.
4. **Flags:** makes-sense flags and checks still failing.
5. **Spot check:** three random items next to their source lines.
6. **Change set** (added in Shape): PRD before/after, roadmap before/after, test cards, PR-FAQs, the Linear actions as a table, and exactly what Apply will do.

## A proposal in `proposals.md` and in the doc

```markdown
### P3: Weekly practice e-mail to the parent (test first)

**Opportunity:** O2, "The parent does not know whether their child practises enough." (new)
**Option:** a weekly e-mail with practice time. Other options for O2: P4, P5.
**Evidence:** [I14], [I22], [I31]: three parents (P03, P07, P09). Against: [I18].
**Confidence:** 3, several interviews, no usage data. **Impact:** 7, practice frequency is the goal.
**Riskiest assumption:** value: parents read the e-mail.
**Cheapest test:** hand-made e-mail to 5 pilot parents for 3 weeks; fewer than 2 replies drops it.
**Makes sense:** 3 of 3.
**Decision:** _open_
```

Every proposal has the `**Evidence:**` line with at least one `[I<n>]`; the citation check reads it. A proposal without evidence says `**Evidence:** none yet` and cites the `own_idea` item it comes from.

The example above is made up. It shows the format, not real data.
