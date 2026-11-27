import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FactoryRetryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        shutil.copytree(ROOT / "scripts", self.repo / "scripts")
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / ".gitignore").write_text(".work/\n")
        subprocess.run(["git", "-C", str(self.repo), "add", ".gitignore"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "-c", "user.name=test", "-c", "user.email=test@example.invalid", "commit", "-qm", "init"], check=True)
        self.graph = self.repo / ".work/graphs/retry.json"
        self.plan = self.repo / ".work/plan.json"
        self.plan.parent.mkdir(parents=True)
        self.return_file = self.repo / ".work/return.json"
        self.write_node = {
            "id": "N1", "domain": "application", "owner": "runner", "mode": "RUN",
            "task": "test", "depends_on": [], "requires": [], "produces": ["result"],
            "write_set": [], "verifies": [], "gate": "none",
            "delegation": {"A": {"nodes": [{"id": "do", "domain": "application", "inputs": [], "outputs": ["result"]}], "edges": []},
                           "E": [{"at": "do", "kind": "wrong_context", "mitigation": "stop"}],
                           "R": {"method": "test", "verification": [["false"], ["true"]], "why": "test", "inputs": ["fixture"]}},
        }
        self.valid_return = {"node_id": "N1", "implemented": self.write_node["delegation"], "outputs": {"result": "done"}, "summary": "completed"}
        self.return_file.write_text(json.dumps(self.valid_return))
        self._init([self.write_node])

    def tearDown(self):
        self.tmp.cleanup()

    def _init(self, nodes):
        self.plan.write_text(json.dumps({"schema_version": 3, "planned_nodes": nodes}))
        result = self.factory("init", "--plan", self.plan, "--graph", self.graph)
        self.assertEqual(result.returncode, 0, result.stderr)

    def factory(self, *args):
        return subprocess.run(["bash", str(self.repo / "scripts/factory"), *map(str, args)], cwd=self.repo, text=True, capture_output=True)

    def test_retry_preserves_failed_submission_and_validates_new_attempt(self):
        evidence = self.graph.parent / "retry.evidence"
        state = evidence / "N1.state.json"
        failed = self.factory("run", "--graph", self.graph, "--node", "N1", "--return", self.return_file, "--", "false")
        self.assertNotEqual(failed.returncode, 0)
        old_state = state.read_bytes()
        blocked = self.factory("retry", "--graph", self.graph, "--node", "N1")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertFalse((evidence / "N1.retry.json").exists())
        authorized = self.factory("retry", "--graph", self.graph, "--node", "N1", "--confirm-worker-stopped")
        self.assertEqual(authorized.returncode, 0, authorized.stderr)
        record = json.loads((evidence / "N1.retry.json").read_text())
        attempt = record["attempt_id"]
        self.assertRegex(attempt, r"^[a-f0-9]{32}$")
        self.assertEqual(state.read_bytes(), old_state)
        ended = self.factory("run", "--graph", self.graph, "--node", "N1", "--return", self.return_file, "--", "true")
        self.assertEqual(ended.returncode, 0, ended.stderr)
        self.assertTrue((evidence / f"N1.{attempt}.state.json").exists())
        self.assertEqual(state.read_bytes(), old_state)
        valid = self.factory("validate", "--graph", self.graph)
        self.assertEqual(valid.returncode, 0, valid.stderr)

    def test_run_rejects_malformed_return_before_lease_or_state_mutation(self):
        run_node = dict(self.write_node)
        run_node.update({"mode": "RUN", "write_set": [], "task": "run", "produces": ["result"]})
        self.graph = self.repo / ".work/graphs/run.json"
        self._init([run_node])
        malformed = self.repo / ".work/malformed.json"
        malformed.write_text("{")
        result = self.factory("run", "--graph", self.graph, "--node", "N1", "--return", malformed, "--", "true")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR [RETURN]", result.stderr)
        evidence = self.graph.parent / "run.evidence"
        self.assertFalse((evidence / "N1.state.json").exists())
        gitdir = Path(subprocess.check_output(["git", "-C", str(self.repo), "rev-parse", "--path-format=absolute", "--git-dir"], text=True).strip())
        self.assertFalse((gitdir / "mimir-factory/active").exists())

    def test_run_rejects_stale_node_return_before_lease_or_state_mutation(self):
        run_node = dict(self.write_node)
        self.graph = self.repo / ".work/graphs/stale.json"
        self._init([run_node])
        stale = dict(self.valid_return)
        stale["node_id"] = "N9"
        self.return_file.write_text(json.dumps(stale))
        result = self.factory("run", "--graph", self.graph, "--node", "N1", "--return", self.return_file, "--", "false")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ERROR [RETURN]", result.stderr)
        evidence = self.graph.parent / "stale.evidence"
        self.assertFalse((evidence / "N1.state.json").exists())
        self.assertFalse((evidence / "N1.return.json").exists())
        gitdir = Path(subprocess.check_output(["git", "-C", str(self.repo), "rev-parse", "--path-format=absolute", "--git-dir"], text=True).strip())
        self.assertFalse((gitdir / "mimir-factory/active").exists())

    def test_retry_record_hash_tampering_fails_closed(self):
        failed = self.factory("run", "--graph", self.graph, "--node", "N1", "--return", self.return_file, "--", "false")
        self.assertNotEqual(failed.returncode, 0)
        self.factory("retry", "--graph", self.graph, "--node", "N1", "--confirm-worker-stopped")
        retry = self.graph.parent / "retry.evidence/N1.retry.json"
        value = json.loads(retry.read_text())
        value["attempt_id"] = "0" * 32
        retry.write_text(json.dumps(value))
        status = self.factory("status", "--graph", self.graph)
        self.assertNotEqual(status.returncode, 0)
        self.assertIn("retry record hash mismatch", status.stderr)


if __name__ == "__main__":
    unittest.main()
