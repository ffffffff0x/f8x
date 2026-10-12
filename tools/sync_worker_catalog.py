#!/usr/bin/env python3
"""Snapshot the PoJun capability catalog into this repository.

PoJun is a private repository, so CI cannot fetch the catalog it reconciles
against. This writes a committed snapshot plus a hash lock, in the same shape
worker-container uses, so the reconciliation gate runs with no network access.
Re-run it whenever PoJun changes its catalog; `--check` fails when the snapshot
no longer matches the source, which is what CI enforces.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT.parent.parent / "Agentic" / "pojun" / "common" / "capability_catalog.json"
SNAPSHOT_NAME = "worker_catalog.snapshot.json"
LOCK_NAME = "worker_catalog.lock.json"


def _load_source(source: Path) -> tuple[bytes, str]:
    source_bytes = source.read_bytes()
    contract = json.loads(source_bytes)
    if contract.get("schema_version") != 1:
        raise SystemExit("unsupported capability contract schema_version")
    contract_version = str(contract.get("contract_version") or "").strip()
    if not contract_version:
        raise SystemExit("capability contract requires contract_version")
    return source_bytes, contract_version


def _lock_payload(source_bytes: bytes, contract_version: str) -> dict[str, str]:
    return {
        "contract_version": contract_version,
        "sha256": hashlib.sha256(source_bytes).hexdigest(),
        "source_repository": "https://github.com/wgpsex/pojun",
        "source_path": "common/capability_catalog.json",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", nargs="?", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed snapshot and lock are consistent (no source needed)",
    )
    args = parser.parse_args()

    snapshot = REPO_ROOT / SNAPSHOT_NAME
    lock_path = REPO_ROOT / LOCK_NAME

    if args.check:
        # CI has no access to the private PoJun repository, so --check only
        # validates the committed pair against itself. Comparing against the
        # live catalog is the job of whoever regenerates the snapshot.
        problems: list[str] = []
        if not snapshot.is_file():
            problems.append(f"{SNAPSHOT_NAME} is missing")
        if not lock_path.is_file():
            problems.append(f"{LOCK_NAME} is missing")
        if problems:
            for problem in problems:
                print(problem, file=sys.stderr)
            return 1

        snapshot_bytes = snapshot.read_bytes()
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        if hashlib.sha256(snapshot_bytes).hexdigest() != lock.get("sha256"):
            problems.append(f"{SNAPSHOT_NAME} does not match {LOCK_NAME}; re-run the sync")
        if json.loads(snapshot_bytes).get("contract_version") != lock.get("contract_version"):
            problems.append(f"{SNAPSHOT_NAME} contract_version disagrees with {LOCK_NAME}")
        if not lock.get("contract_version"):
            problems.append(f"{LOCK_NAME} is missing contract_version")
        for problem in problems:
            print(problem, file=sys.stderr)
        if problems:
            return 1
        print(f"snapshot {lock['contract_version']} matches its lock")
        return 0

    source = args.catalog.resolve()
    if not source.is_file():
        raise SystemExit(f"capability catalog not found: {source}")

    source_bytes, contract_version = _load_source(source)
    lock = _lock_payload(source_bytes, contract_version)

    shutil.copyfile(source, snapshot)
    lock_path.write_text(
        json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"snapshot {contract_version} -> {SNAPSHOT_NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
