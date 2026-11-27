import json
import fcntl
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class FactoryLeaseRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        shutil.copytree(ROOT / "scripts", self.repo / "scripts")
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        (self.repo / ".gitignore").write_text(".work/\n")
        subprocess.run(["git", "-C", str(self.repo), "add", ".gitignore"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "-c", "user.name=test", "-c", "user.email=test@example.invalid", "commit", "-qm", "init"], check=True)
        self.graph = self.repo / ".work/graphs/recovery.json"
        self.plan = self.repo / ".work/plan.json"
        node = {
            "id": "N1", "domain": "application", "owner": "writer", "mode": "WRITE",
            "task": "test", "depends_on": [], "requires": [], "produces": ["result"],
            "write_set": ["src/"], "verifies": [], "gate": "none",
            "delegation": {
                "A": {"nodes": [{"id": "do", "domain": "application", "inputs": [], "outputs": ["result"]}], "edges": []},
                "E": [{"at": "do", "kind": "wrong_context", "mitigation": "stop"}],
                "R": {"method": "test", "verification": [["true"]], "why": "test", "inputs": ["fixture"]},
            },
        }
        self.plan.parent.mkdir(parents=True)
        reviewer = {
            "id": "N2", "domain": "quality", "owner": "reviewer", "mode": "RUN",
            "task": "review", "depends_on": ["N1"], "requires": [{"from": "N1", "output": "result"}],
            "produces": ["review"], "write_set": [], "verifies": ["N1"], "gate": "review",
            "delegation": {
                "A": {"nodes": [{"id": "review", "domain": "quality", "inputs": ["result"], "outputs": ["review"]}], "edges": []},
                "E": [{"at": "review", "kind": "missing_input", "mitigation": "stop"}],
                "R": {"method": "test", "verification": [["true"]], "why": "test", "inputs": ["N1.result"]},
            },
        }
        self.plan.write_text(json.dumps({"schema_version": 3, "planned_nodes": [node, reviewer]}))
        self.factory("init", "--plan", str(self.plan), "--graph", str(self.graph))
        self.state = self.graph.parent / "recovery.evidence/N1.state.json"
        self.state.parent.mkdir(parents=True, exist_ok=True)
        self.state.write_text(json.dumps({"id": "N1", "status": "failed", "worktree": str(self.repo), "start_order": 1, "started_utc": "now"}))
        self.lease = Path(subprocess.check_output(["git", "-C", str(self.repo), "rev-parse", "--path-format=absolute", "--git-dir"], text=True).strip()) / "mimir-factory/active"
        self.lease.parent.mkdir(parents=True, exist_ok=True)
        self.lease.write_text(f"{self.graph}:N1\n")

    def tearDown(self):
        self.tmp.cleanup()

    def factory(self, *args, ok=True):
        result = subprocess.run(["bash", str(self.repo / "scripts/factory"), *map(str, args)], cwd=self.repo, text=True, capture_output=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0)
        return result

    def recover(self, *args):
        return self.factory("recover", "--graph", self.graph, "--node", "N1", *args, ok=False)

    def test_requires_explicit_stopped_confirmation(self):
        self.recover()
        self.assertTrue(self.lease.exists())

    def test_owner_checked_and_idempotent_recovery(self):
        self.factory("recover", "--graph", self.graph, "--node", "N1", "--confirm-worker-stopped")
        self.assertFalse(self.lease.exists())
        self.factory("recover", "--graph", self.graph, "--node", "N1", "--confirm-worker-stopped")

    def test_refuses_unknown_lease_owner_without_mutation(self):
        self.lease.write_text("/other/graph.json:N2\n")
        self.recover("--confirm-worker-stopped")
        self.assertEqual(self.lease.read_text(), "/other/graph.json:N2\n")

    def test_requires_terminal_state(self):
        self.state.write_text(self.state.read_text().replace('"failed"', '"running"'))
        self.recover("--confirm-worker-stopped")
        self.assertTrue(self.lease.exists())

    def test_recovery_waits_for_stable_worktree_lease_lock(self):
        lock_path = self.lease.parent / ".lock"
        with lock_path.open("w") as lock_file:
            fcntl.flock(lock_file, fcntl.LOCK_EX)
            proc = subprocess.Popen(
                ["bash", str(self.repo / "scripts/factory"), "recover", "--graph", str(self.graph),
                 "--node", "N1", "--confirm-worker-stopped"],
                cwd=self.repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            )
            try:
                with self.assertRaises(subprocess.TimeoutExpired):
                    proc.communicate(timeout=0.15)
            finally:
                fcntl.flock(lock_file, fcntl.LOCK_UN)
            stdout, stderr = proc.communicate(timeout=5)
            self.assertEqual(proc.returncode, 0, stderr)
            self.assertIn("RECOVERED: N1", stdout)


if __name__ == "__main__":
    unittest.main()
