"""Tests for check.py. Run: python3 -m unittest discover -s skills/product-loop/scripts"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check.py")


def run(check, run_dir):
    p = subprocess.run([sys.executable, str(SCRIPT), check, str(run_dir)],
                       capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


class RunDir:
    def __init__(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name)
        (self.path / "sources").mkdir()

    def write(self, name, content):
        f = self.path / name
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(content if isinstance(content, str) else json.dumps(content), encoding="utf-8")


SOURCE = ("Interviewer: Hoe gaat het?\n"
          "P03: Ouders vragen mij  steeds:\n“oefent mijn kind wel genoeg?” "
          "Dat weet ik eerlijk gezegd niet - het systeem laat dat niet zien.\n")


class Quotes(unittest.TestCase):
    def setUp(self):
        self.r = RunDir()
        self.addCleanup(self.r.tmp.cleanup)
        self.r.write("sources/a.md", SOURCE)

    def items(self, *quotes, type_="customer_voice"):
        self.r.write("items.json", [
            {"id": f"I{i}", "type": type_, "source": "sources/a.md", "quote": q}
            for i, q in enumerate(quotes, 1)])

    def test_exact_quote_with_different_spaces_quotes_and_case_passes(self):
        self.items('ouders vragen mij steeds: "oefent mijn kind wel genoeg?"')
        code, out = run("quotes", self.r.path)
        self.assertEqual(code, 0, out)

    def test_dash_variants_match(self):
        self.items("Dat weet ik eerlijk gezegd niet — het systeem")
        self.assertEqual(run("quotes", self.r.path)[0], 0)

    def test_gap_marked_with_dots_passes_when_parts_are_in_order(self):
        self.items("Ouders vragen mij steeds ... het systeem laat dat niet zien")
        self.assertEqual(run("quotes", self.r.path)[0], 0)

    def test_parts_out_of_order_fail(self):
        self.items("het systeem laat dat niet zien ... Ouders vragen mij")
        code, out = run("quotes", self.r.path)
        self.assertEqual(code, 1)
        self.assertIn("I1", out)

    def test_invented_quote_fails_and_names_the_item(self):
        self.items("Ouders vragen mij steeds", "Ouders willen een dashboard")
        code, out = run("quotes", self.r.path)
        self.assertEqual(code, 1)
        self.assertIn("I2", out)
        self.assertNotIn("I1:", out)

    def test_customer_voice_without_quote_fails(self):
        self.r.write("items.json", [{"id": "I1", "type": "customer_voice", "source": "sources/a.md"}])
        self.assertEqual(run("quotes", self.r.path)[0], 1)

    def test_own_idea_without_quote_passes(self):
        self.r.write("items.json", [{"id": "I1", "type": "own_idea", "observation": "x"}])
        self.assertEqual(run("quotes", self.r.path)[0], 0)

    def test_missing_source_file_fails(self):
        self.r.write("items.json", [{"id": "I1", "type": "buyer", "source": "sources/nope.md", "quote": "x"}])
        code, out = run("quotes", self.r.path)
        self.assertEqual(code, 1)
        self.assertIn("nope.md", out)

    def test_duplicate_ids_fail(self):
        self.items("Ouders vragen mij steeds", "het systeem")
        data = json.loads((self.r.path / "items.json").read_text())
        data[1]["id"] = "I1"
        self.r.write("items.json", data)
        self.assertEqual(run("quotes", self.r.path)[0], 1)


PROPOSALS = """# Proposals

### P1: Weekly e-mail

**Evidence:** [I1], [I2]. Against: [I9].

### P2: Idea only

**Evidence:** none yet, from [I3].
"""


class Citations(unittest.TestCase):
    def setUp(self):
        self.r = RunDir()
        self.addCleanup(self.r.tmp.cleanup)
        self.r.write("items.json", [{"id": "I1", "type": "customer_voice"},
                                    {"id": "I3", "type": "own_idea"}])
        self.r.write("bank.json", [{"id": "I2", "type": "customer_voice"},
                                   {"id": "I9", "type": "buyer"}])

    def test_known_ids_pass_and_idea_only_proposal_warns(self):
        self.r.write("proposals.md", PROPOSALS)
        code, out = run("citations", self.r.path)
        self.assertEqual(code, 0, out)
        self.assertIn("warning", out.lower())
        self.assertIn("P2", out)

    def test_unknown_id_fails(self):
        self.r.write("proposals.md", PROPOSALS.replace("[I9]", "[I42]"))
        code, out = run("citations", self.r.path)
        self.assertEqual(code, 1)
        self.assertIn("I42", out)

    def test_proposal_without_evidence_line_fails(self):
        self.r.write("proposals.md", "### P1: Something\n\nNo evidence here.\n")
        code, out = run("citations", self.r.path)
        self.assertEqual(code, 1)
        self.assertIn("P1", out)

    def test_no_proposals_fails(self):
        self.r.write("proposals.md", "# Proposals\n")
        self.assertEqual(run("citations", self.r.path)[0], 1)


class Actions(unittest.TestCase):
    def setUp(self):
        self.r = RunDir()
        self.addCleanup(self.r.tmp.cleanup)
        self.r.write("proposals.md", PROPOSALS)
        self.r.write("decisions.json", {"P1": {"decision": "accept"}, "P2": {"decision": "reject"}})

    def test_action_on_accepted_proposal_passes(self):
        self.r.write("actions.json", [{"id": "A1", "kind": "create_issue", "decision": "P1"}])
        self.assertEqual(run("actions", self.r.path)[0], 0)

    def test_action_on_rejected_proposal_fails(self):
        self.r.write("actions.json", [{"id": "A1", "kind": "create_issue", "decision": "P2"}])
        code, out = run("actions", self.r.path)
        self.assertEqual(code, 1)
        self.assertIn("A1", out)

    def test_unknown_kind_and_missing_decision_fail(self):
        self.r.write("actions.json", [{"id": "A1", "kind": "delete_project", "decision": "P1"},
                                      {"id": "A2", "kind": "comment"}])
        code, out = run("actions", self.r.path)
        self.assertEqual(code, 1)
        self.assertIn("A1", out)
        self.assertIn("A2", out)


if __name__ == "__main__":
    unittest.main()
