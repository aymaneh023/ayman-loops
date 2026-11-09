#!/usr/bin/env python3
"""Exact checks for a product-loop run folder.

    check.py quotes    <run-dir>   every quote in items.json is in its source file
    check.py citations <run-dir>   every proposal cites items that exist
    check.py actions   <run-dir>   every Linear action points to an accepted proposal

Exit 0 when green, 1 with one line per failure. Standard library only.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

QUOTE_REQUIRED = {"customer_voice", "buyer"}
TYPES = {"customer_voice", "buyer", "tech_research", "own_idea", "usage_data"}
ACTION_KINDS = {"create_issue", "update_project", "move_status", "set_priority", "comment"}
ACCEPTED = {"accept", "change"}
GAP = re.compile(r"\s*(?:\.\.\.|…)\s*")
CITE = re.compile(r"\[(I\d+)\]")


def normalise(text):
    text = unicodedata.normalize("NFKC", text)
    for chars, plain in (("‘’‚‛`´", "'"), ("“”„‟«»", '"'), ("‐‑‒–—―−", "-")):
        for c in chars:
            text = text.replace(c, plain)
    return re.sub(r"\s+", " ", text).strip().casefold()


def load_json(path, default=None):
    if not path.exists():
        if default is not None:
            return default
        sys.exit(f"missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def quote_found(quote, source):
    """Each part of the quote (split on '...') appears in the source, in order."""
    pos = 0
    for part in GAP.split(quote):
        part = normalise(part).strip(" \"'")
        if not part:
            continue
        at = source.find(part, pos)
        if at < 0:
            return False
        pos = at + len(part)
    return True


def check_quotes(run):
    items = load_json(run / "items.json")
    errors, seen, sources = [], set(), {}
    for item in items:
        iid = item.get("id", "?")
        if iid in seen:
            errors.append(f"{iid}: duplicate id")
        seen.add(iid)
        if item.get("type") not in TYPES:
            errors.append(f"{iid}: unknown type {item.get('type')!r}")
        quote = item.get("quote")
        if not quote:
            if item.get("type") in QUOTE_REQUIRED:
                errors.append(f"{iid}: {item.get('type')} needs a quote")
            continue
        src = item.get("source")
        if not src or not (run / src).exists():
            errors.append(f"{iid}: source file not found: {src}")
            continue
        if src not in sources:
            sources[src] = normalise((run / src).read_text(encoding="utf-8"))
        if not quote_found(quote, sources[src]):
            errors.append(f"{iid}: quote not found word for word in {src}: {quote[:80]!r}")
    return errors, []


def proposals(run):
    """{proposal id: section text} from proposals.md."""
    text = (run / "proposals.md").read_text(encoding="utf-8") if (run / "proposals.md").exists() else ""
    parts = re.split(r"^###\s+(P\d+)\b.*$", text, flags=re.M)
    return dict(zip(parts[1::2], parts[2::2]))


def check_citations(run):
    known = {i["id"]: i.get("type") for i in load_json(run / "items.json") + load_json(run / "bank.json", [])}
    props = proposals(run)
    if not props:
        return ["no proposals found (expected '### P<n>: …' headings in proposals.md)"], []
    errors, warnings = [], []
    for pid, body in props.items():
        line = next((l for l in body.splitlines() if l.startswith("**Evidence:**")), None)
        if line is None:
            errors.append(f"{pid}: no **Evidence:** line")
            continue
        cited = CITE.findall(body)
        if not cited:
            errors.append(f"{pid}: cites no item")
        missing = [c for c in cited if c not in known]
        if missing:
            errors.append(f"{pid}: cites unknown items {', '.join(missing)}")
        support = CITE.findall(line.split("Against:")[0])
        if support and all(known.get(c) == "own_idea" for c in support):
            warnings.append(f"{pid}: rests only on own_idea items (a hypothesis, not evidence)")
    return errors, warnings


def check_actions(run):
    actions = load_json(run / "actions.json")
    decisions = load_json(run / "decisions.json")
    props = proposals(run)
    errors = []
    for a in actions:
        aid = a.get("id", "?")
        if a.get("kind") not in ACTION_KINDS:
            errors.append(f"{aid}: unknown kind {a.get('kind')!r}")
        pid = a.get("decision")
        if not pid:
            errors.append(f"{aid}: no decision")
        elif pid not in props:
            errors.append(f"{aid}: decision {pid} is not a proposal")
        elif decisions.get(pid, {}).get("decision") not in ACCEPTED:
            errors.append(f"{aid}: proposal {pid} was not accepted")
    return errors, []


CHECKS = {"quotes": check_quotes, "citations": check_citations, "actions": check_actions}


def main(argv):
    if len(argv) != 3 or argv[1] not in CHECKS:
        sys.exit(__doc__)
    errors, warnings = CHECKS[argv[1]](Path(argv[2]))
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(e)
    print(f"{argv[1]}: {'red' if errors else 'green'} ({len(errors)} failures, {len(warnings)} warnings)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
