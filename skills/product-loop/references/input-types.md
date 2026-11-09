# Input types

Input can be anything. Each **input item** gets one type, and the type decides where it enters the opportunity tree and how much it counts.

| Type | Examples | Enters the tree at | Counts as | Quote |
|---|---|---|---|---|
| `customer_voice` | Interview with a user, a support ticket, a survey answer | Opportunities: the problems | Evidence of a need | Required |
| `buyer` | A go-to-market partner, a sales call, a buyer's requirement | The goal and Impact: what sells, what a buyer needs before buying | Evidence about the buyer | Required |
| `tech_research` | A finding about a technology, a library, a cost | Options and feasibility: what becomes possible or cheaper | A fact about feasibility, as strong as its source | When it comes from a document |
| `own_idea` | The user's or a co-founder's own thought | Options: an idea to test | A hypothesis: confidence ≈ 0.1 until other items support it | Not needed |
| `usage_data` | Analytics, the result of a test the loop proposed earlier | Confidence of an option or opportunity | The strongest evidence | Not needed; give the numbers and the source |

## Fields in `items.json`

```json
{"id": "I14", "type": "customer_voice", "source": "sources/01-interview-teacher.md",
 "speaker": "Teacher, P03", "quote": "Ouders vragen mij steeds: oefent mijn kind wel genoeg?",
 "observation": "Parents don't know whether their child practises enough.", "date": "2026-11-10"}
```

- `quote`: copied word for word, in the source's language. A gap inside a quote is written `...`. The check script compares it with the source.
- `observation`: one sentence in the output language of the context pack. Says what the quote shows, nothing more.
- `speaker`: role + code. A new person gets the next free code in the product (`P01`, `P02`, …), found in the input bank; the name goes only into `people.json` in the run folder.
- One observation per item. A quote that shows two things is two items with the same quote.
