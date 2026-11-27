#!/usr/bin/env python3
"""Verify accepted candidate identity against observed GitHub and remote Git evidence."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def reject(message):
    raise ValueError(message)


def git(repo, *args):
    result = subprocess.run(["git", "-C", str(repo), *args], text=True, capture_output=True)
    if result.returncode:
        reject(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def load(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError) as exc:
        reject(f"cannot read JSON evidence {path}: {exc}")


def verify(repo, candidate, pr, remote, branch):
    commit, tree, base = (candidate.get(k) for k in ("commit", "tree", "base"))
    if not all(isinstance(v, str) and v for v in (commit, tree, base)):
        reject("candidate must name commit, tree, and base SHAs")
    if not all(re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", value) for value in (commit, tree, base)):
        reject("candidate commit, tree, and base must be full hexadecimal SHAs")
    if git(repo, "rev-parse", f"{commit}^{{commit}}") != commit:
        reject("candidate commit is stale or unavailable")
    if git(repo, "rev-parse", f"{commit}^{{tree}}") != tree:
        reject("candidate tree does not match accepted tree SHA")
    if git(repo, "rev-parse", f"{base}^{{commit}}") != base:
        reject("accepted base commit is unavailable")
    if subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", base, commit]).returncode:
        reject("accepted base is not an ancestor of candidate commit")

    head = (pr.get("head") or {}).get("sha")
    merge = pr.get("merge_commit_sha")
    if not pr.get("merged_at") or not merge:
        reject("GitHub PR evidence does not show a completed merge")
    if head != commit:
        reject("GitHub PR head does not equal accepted candidate commit")
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", head or ""):
        reject("GitHub PR head must be a full hexadecimal SHA")
    if (pr.get("base") or {}).get("ref") != branch:
        reject("GitHub PR targets a different integration branch")
    if pr.get("base", {}).get("sha") and not re.fullmatch(
            r"(?:[0-9a-f]{40}|[0-9a-f]{64})", pr["base"]["sha"]):
        reject("GitHub PR base must be a full hexadecimal SHA")
    if git(repo, "rev-parse", f"{merge}^{{commit}}") != merge:
        reject("reported merge commit is unavailable")
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", merge):
        reject("reported merge commit must be a full hexadecimal SHA")
    if not isinstance(remote, dict) or remote.get("name") != branch or not isinstance(remote.get("sha"), str):
        reject("remote trunk evidence must name the expected branch and observed SHA")
    if not re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", remote["sha"]):
        reject("remote trunk SHA must be a full hexadecimal SHA")
    live = git(repo, "ls-remote", "origin", f"refs/heads/{branch}").split()
    if not live or live[0] != remote["sha"]:
        reject("remote trunk moved since its SHA was observed")
    if subprocess.run(["git", "-C", str(repo), "merge-base", "--is-ancestor", merge, remote["sha"]]).returncode:
        reject("remote trunk does not contain the reported merge commit")
    return {"candidate_commit": commit, "candidate_tree": tree, "candidate_base": base,
            "pr_head": head, "merge_commit": merge, "remote_trunk": remote["sha"],
            "remote_branch": branch, "merged_at": pr["merged_at"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--candidate", required=True, help="accepted record JSON: commit, tree, base")
    parser.add_argument("--pr", required=True, help="GitHub PR JSON response")
    parser.add_argument("--remote", required=True, help="observed remote ref JSON: name, sha")
    parser.add_argument("--branch", default="main")
    args = parser.parse_args()
    try:
        result = verify(args.repo, load(args.candidate), load(args.pr), load(args.remote), args.branch)
    except ValueError as exc:
        print(f"delivery verification failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
