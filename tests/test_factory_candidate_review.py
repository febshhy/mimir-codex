import json
import shutil
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FactoryCandidateReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        shutil.copytree(ROOT / "scripts", self.repo / "scripts")
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / ".gitignore").write_text(".work/\n")
        subprocess.run(["git", "-C", str(self.repo), "add", ".gitignore"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "-c", "user.name=test", "-c", "user.email=test@example.invalid", "commit", "-qm", "init"], check=True)
        self.graph = self.repo / ".work/graphs/candidate.json"
        self.plan = self.repo / ".work/plan.json"
        self.plan.parent.mkdir(parents=True)
        self.write_return = self.repo / ".work/write-return.json"
        self.review_return = self.repo / ".work/review-return.json"
        write = self.node("N1", "application", "writer", "WRITE", "write", [], [], ["implementation"], ["src/"], [], "none",
                          {"A": {"nodes": [{"id": "write", "domain": "application", "inputs": [], "outputs": ["implementation"]}], "edges": []},
                           "E": [{"at": "write", "kind": "wrong_context", "mitigation": "preserve candidate"}],
                           "R": {"method": "write", "verification": [["true"]], "why": "create candidate", "inputs": ["task"]}})
        review = self.node("N2", "quality", "reviewer", "RUN", "review", ["N1"], [{"from": "N1", "output": "implementation"}], ["review"], [], ["N1"], "review",
                           {"A": {"nodes": [{"id": "review", "domain": "quality", "inputs": ["implementation"], "outputs": ["review"]}], "edges": []},
                            "E": [{"at": "review", "kind": "missing_input", "mitigation": "inspect exact candidate"}],
                            "R": {"method": "independent review", "verification": [["true"]], "why": "review candidate", "inputs": ["N1.implementation"]}})
        self.write_node, self.review_node = write, review
        self.plan.write_text(json.dumps({"schema_version": 3, "planned_nodes": [write, review]}))
        self.assertEqual(self.factory("init", "--plan", self.plan, "--graph", self.graph).returncode, 0)
        self.write_return.write_text(json.dumps({"node_id": "N1", "implemented": write["delegation"], "outputs": {"implementation": "created"}, "summary": "created"}))
        self.review_return.write_text(json.dumps({"node_id": "N2", "implemented": review["delegation"], "outputs": {"review": "reviewed"}, "summary": "reviewed"}))

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def node(node_id, domain, owner, mode, task, deps, requires, produces, writes, verifies, gate, delegation):
        return {"id": node_id, "domain": domain, "owner": owner, "mode": mode, "task": task, "depends_on": deps,
                "requires": requires, "produces": produces, "write_set": writes, "verifies": verifies, "gate": gate,
                "delegation": delegation}

    def factory(self, *args):
        return subprocess.run(["bash", str(self.repo / "scripts/factory"), *map(str, args)], cwd=self.repo, text=True, capture_output=True)

    def write_candidate(self):
        self.assertEqual(self.factory("begin", "--graph", self.graph, "--node", "N1").returncode, 0)
        (self.repo / "src").mkdir()
        (self.repo / "src/candidate.py").write_text("candidate\n")
        result = self.factory("end", "--graph", self.graph, "--node", "N1", "--return", self.write_return)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_review_receipt_binds_candidate_and_graph_validates(self):
        self.write_candidate()
        started = self.factory("run", "--graph", self.graph, "--node", "N2", "--return", self.review_return, "--review-note", "independent review", "--", "true")
        self.assertEqual(started.returncode, 0, started.stderr)
        receipt = json.loads((self.graph.parent / "candidate.evidence/N2.receipt.json").read_text())
        candidate = json.loads((self.graph.parent / "candidate.evidence/N1.receipt.json").read_text())["candidate_sha256"]
        self.assertEqual(receipt["reviewed_candidates"]["N1"], candidate)
        valid = self.factory("validate", "--graph", self.graph)
        self.assertEqual(valid.returncode, 0, valid.stderr)

    def test_review_rejects_changed_candidate(self):
        sentinel = self.repo / "review-command-ran"
        command = self.repo / ".work/review.sh"
        command.write_text(f"#!/bin/sh\ntouch '{sentinel}'\n")
        command.chmod(0o755)
        self.review_node["delegation"]["R"]["verification"] = [[str(command)]]
        plan = json.loads(self.plan.read_text())
        plan["planned_nodes"][1] = self.review_node
        self.plan.write_text(json.dumps(plan))
        # Reinitialize from an equivalent fresh graph because plans become immutable at init.
        self.graph.unlink()
        shutil.rmtree(self.graph.parent / "candidate.evidence")
        self.assertEqual(self.factory("init", "--plan", self.plan, "--graph", self.graph).returncode, 0)
        self.write_return.write_text(json.dumps({"node_id": "N1", "implemented": self.write_node["delegation"], "outputs": {"implementation": "created"}, "summary": "created"}))
        self.review_return.write_text(json.dumps({"node_id": "N2", "implemented": self.review_node["delegation"], "outputs": {"review": "reviewed"}, "summary": "reviewed"}))
        self.write_candidate()
        (self.repo / "src/candidate.py").write_text("changed after candidate\n")
        result = self.factory("run", "--graph", self.graph, "--node", "N2", "--return", self.review_return, "--review-note", "review", "--", str(command))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("candidate_mismatch", result.stderr)
        self.assertFalse(sentinel.exists(), "review command must not run for a mismatched candidate")

    def test_review_rechecks_candidate_after_command(self):
        candidate = self.repo / "src/candidate.py"
        command = self.repo / ".work/review-mutates-candidate.sh"
        command.write_text(f"#!/bin/sh\nprintf 'changed during review\\n' > '{candidate}'\n")
        command.chmod(0o755)
        self.review_node["delegation"]["R"]["verification"] = [[str(command)]]
        plan = json.loads(self.plan.read_text())
        plan["planned_nodes"][1] = self.review_node
        self.plan.write_text(json.dumps(plan))
        self.graph.unlink()
        shutil.rmtree(self.graph.parent / "candidate.evidence")
        self.assertEqual(self.factory("init", "--plan", self.plan, "--graph", self.graph).returncode, 0)
        self.write_return.write_text(json.dumps({"node_id": "N1", "implemented": self.write_node["delegation"], "outputs": {"implementation": "created"}, "summary": "created"}))
        self.review_return.write_text(json.dumps({"node_id": "N2", "implemented": self.review_node["delegation"], "outputs": {"review": "reviewed"}, "summary": "reviewed"}))
        self.write_candidate()
        result = self.factory("run", "--graph", self.graph, "--node", "N2", "--return", self.review_return, "--review-note", "review", "--", str(command))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("candidate_mismatch", result.stderr)

    def test_candidate_change_before_lease_is_rejected_before_command(self):
        candidate = self.repo / "src/candidate.py"
        sentinel = self.repo / "review-command-ran"
        command = self.repo / ".work/review.sh"
        command.write_text(f"#!/bin/sh\ntouch '{sentinel}'\n")
        command.chmod(0o755)
        self.review_node["delegation"]["R"]["verification"] = [[str(command)]]
        plan = json.loads(self.plan.read_text())
        plan["planned_nodes"][1] = self.review_node
        self.plan.write_text(json.dumps(plan))
        self.graph.unlink()
        shutil.rmtree(self.graph.parent / "candidate.evidence")
        self.assertEqual(self.factory("init", "--plan", self.plan, "--graph", self.graph).returncode, 0)
        self.write_return.write_text(json.dumps({"node_id": "N1", "implemented": self.write_node["delegation"], "outputs": {"implementation": "created"}, "summary": "created"}))
        self.review_return.write_text(json.dumps({"node_id": "N2", "implemented": self.review_node["delegation"], "outputs": {"review": "reviewed"}, "summary": "reviewed"}))
        self.write_candidate()

        factory_script = self.repo / "scripts/factory"
        source = factory_script.read_text()
        hook = f"        printf 'changed in lease window\n' > {shlex.quote(str(candidate))}\n        start_node EXEC\n"
        self.assertIn("        start_node EXEC\n", source)
        factory_script.write_text(source.replace("        start_node EXEC\n", hook, 1))

        result = self.factory("run", "--graph", self.graph, "--node", "N2", "--return", self.review_return, "--review-note", "review", "--", str(command))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("candidate_mismatch", result.stderr)
        self.assertFalse(sentinel.exists(), "review command must not run for a candidate changed before lease acquisition")
        state = json.loads((self.graph.parent / "candidate.evidence/N2.state.json").read_text())
        receipt = json.loads((self.graph.parent / "candidate.evidence/N2.receipt.json").read_text())
        self.assertEqual(state["status"], "failed")
        self.assertEqual(receipt["status"], "failed")
        self.assertIn("candidate_mismatch", [error["code"] for error in receipt["errors"]])
        self.assertIn("command not run", (self.graph.parent / "candidate.evidence/N2.log").read_text())
        self.assertFalse((self.repo / ".git/mimir-factory/active").exists(), "failed pre-command review must release the lease")


if __name__ == "__main__":
    unittest.main()
