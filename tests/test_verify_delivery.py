import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("verify_delivery", Path(__file__).resolve().parents[1] / "scripts/verify_delivery.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
verify = module.verify


def run(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, text=True, capture_output=True).stdout.strip()


class DeliveryEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.repo = self.root / "repo"
        self.origin = self.root / "origin.git"
        self.repo.mkdir()
        run(self.repo, "init", "-q", "-b", "main")
        run(self.repo, "config", "user.name", "Test")
        run(self.repo, "config", "user.email", "test@example.invalid")
        (self.repo / "file").write_text("base\n")
        run(self.repo, "add", "file")
        run(self.repo, "commit", "-qm", "base")
        self.base = run(self.repo, "rev-parse", "HEAD")
        run(self.repo, "checkout", "-qb", "task")
        (self.repo / "file").write_text("candidate\n")
        run(self.repo, "commit", "-qam", "candidate")
        self.commit = run(self.repo, "rev-parse", "HEAD")
        self.tree = run(self.repo, "rev-parse", "HEAD^{tree}")
        run(self.repo, "checkout", "-q", "main")
        run(self.repo, "merge", "--no-ff", "-m", "merge task", "task")
        self.merge = run(self.repo, "rev-parse", "HEAD")
        run(self.root, "init", "--bare", "-q", str(self.origin))
        run(self.repo, "remote", "add", "origin", str(self.origin))
        run(self.repo, "push", "-q", "origin", "main")
        self.candidate = {"commit": self.commit, "tree": self.tree, "base": self.base}
        self.pr = {"merged_at": "2026-11-27T00:00:00Z", "head": {"sha": self.commit},
                   "base": {"ref": "main", "sha": self.base}, "merge_commit_sha": self.merge}
        self.remote = {"name": "main", "sha": self.merge}

    def tearDown(self):
        self.tmp.cleanup()

    def test_accepts_matching_candidate_pr_and_remote_trunk(self):
        result = verify(self.repo, self.candidate, self.pr, self.remote, "main")
        self.assertEqual(result["candidate_commit"], self.commit)
        self.assertEqual(result["merge_commit"], self.merge)

    def test_rejects_stale_head_even_when_tree_is_identical(self):
        run(self.repo, "checkout", "-qb", "same-tree", self.commit)
        run(self.repo, "commit", "--allow-empty", "-qm", "new commit, same tree")
        stale = run(self.repo, "rev-parse", "HEAD")
        self.assertEqual(run(self.repo, "rev-parse", "HEAD^{tree}"), self.tree)
        self.pr["head"]["sha"] = stale
        with self.assertRaisesRegex(ValueError, "PR head"):
            verify(self.repo, self.candidate, self.pr, self.remote, "main")

    def test_rejects_new_candidate_commit_with_same_tree(self):
        run(self.repo, "checkout", "-qb", "same-tree", self.commit)
        run(self.repo, "commit", "--allow-empty", "-qm", "new commit, same tree")
        self.candidate["commit"] = run(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "PR head"):
            verify(self.repo, self.candidate, self.pr, self.remote, "main")

    def test_rejects_moving_remote_trunk_after_observation(self):
        run(self.repo, "checkout", "main")
        run(self.repo, "commit", "--allow-empty", "-qm", "trunk advanced")
        run(self.repo, "push", "-q", "origin", "main")
        with self.assertRaisesRegex(ValueError, "trunk moved"):
            verify(self.repo, self.candidate, self.pr, self.remote, "main")

    def test_rejects_abbreviated_candidate_sha(self):
        self.candidate["commit"] = self.commit[:12]
        with self.assertRaisesRegex(ValueError, "full hexadecimal SHAs"):
            verify(self.repo, self.candidate, self.pr, self.remote, "main")

    def test_rejects_abbreviated_pr_base_sha(self):
        self.pr["base"]["sha"] = self.base[:12]
        with self.assertRaisesRegex(ValueError, "PR base must be a full"):
            verify(self.repo, self.candidate, self.pr, self.remote, "main")

    def test_accepts_advanced_pr_base_when_live_trunk_contains_merge(self):
        run(self.repo, "checkout", "main")
        run(self.repo, "commit", "--allow-empty", "-qm", "trunk advanced after merge")
        advanced = run(self.repo, "rev-parse", "HEAD")
        run(self.repo, "push", "-q", "origin", "main")
        self.pr["base"]["sha"] = advanced
        self.remote["sha"] = advanced
        result = verify(self.repo, self.candidate, self.pr, self.remote, "main")
        self.assertEqual(result["candidate_base"], self.base)
        self.assertEqual(result["remote_trunk"], advanced)

    def test_rejects_wrong_pr_base_ref(self):
        self.pr["base"]["ref"] = "release"
        with self.assertRaisesRegex(ValueError, "different integration branch"):
            verify(self.repo, self.candidate, self.pr, self.remote, "main")


if __name__ == "__main__":
    unittest.main()
