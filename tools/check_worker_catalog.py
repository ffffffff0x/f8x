#!/usr/bin/env python3
"""Check f8x's development-time Worker profile against a capability catalog."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


_PROFILE_RE = re.compile(r'^F8X_WORKER_CAPABILITIES="\n(?P<body>.*?)\n"$', re.MULTILINE | re.DOTALL)
_RESOURCE_RE = re.compile(r'^F8X_WORKER_RESOURCES="\n(?P<body>.*?)\n"$', re.MULTILINE | re.DOTALL)


def _profile_entries(script: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    match = _PROFILE_RE.search(script)
    if not match:
        return {}, ["F8X_WORKER_CAPABILITIES block is missing"]

    entries: dict[str, dict[str, Any]] = {}
    invalid: list[str] = []
    for line_number, raw_line in enumerate(match.group("body").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 5)
        if len(parts) != 6:
            invalid.append(f"line {line_number}: expected 6 fields")
            continue
        name, bins, function, dependencies, policy, reason = (part.strip() for part in parts)
        if not name or not bins or policy not in {"install", "skip"}:
            invalid.append(f"line {line_number}: invalid name, bins, or policy")
            continue
        if name in entries:
            invalid.append(f"line {line_number}: duplicate capability {name}")
            continue
        if policy == "install" and (not function or function == "-"):
            invalid.append(f"line {line_number}: install entry {name} has no function")
            continue
        if policy == "skip" and (function != "-" or not reason):
            invalid.append(f"line {line_number}: skip entry {name} needs '-' and a reason")
            continue
        entries[name] = {
            "bins": [item.strip() for item in bins.split(",") if item.strip()],
            "function": function,
            "dependencies": dependencies,
            "policy": policy,
            "reason": reason,
        }
    return entries, invalid


def _resource_entries(script: str) -> tuple[dict[str, dict[str, Any]], list[str]]:
    match = _RESOURCE_RE.search(script)
    if not match:
        return {}, ["F8X_WORKER_RESOURCES block is missing"]

    entries: dict[str, dict[str, Any]] = {}
    invalid: list[str] = []
    for line_number, raw_line in enumerate(match.group("body").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("|", 4)
        if len(parts) != 5:
            invalid.append(f"resource line {line_number}: expected 5 fields")
            continue
        name, paths, function, policy, reason = (part.strip() for part in parts)
        if not name or not paths or policy not in {"install", "skip"}:
            invalid.append(f"resource line {line_number}: invalid name, paths, or policy")
            continue
        if name in entries:
            invalid.append(f"resource line {line_number}: duplicate resource {name}")
            continue
        if policy == "install" and (not function or function == "-"):
            invalid.append(f"resource line {line_number}: install entry {name} has no function")
            continue
        if policy == "skip" and (function != "-" or not reason):
            invalid.append(f"resource line {line_number}: skip entry {name} needs '-' and a reason")
            continue
        entries[name] = {
            "paths": [item.strip() for item in paths.split(",") if item.strip()],
            "function": function,
            "policy": policy,
            "reason": reason,
        }
    return entries, invalid


def check_catalog(catalog: dict[str, Any], script: str) -> dict[str, Any]:
    profile, invalid_entries = _profile_entries(script)
    resources, invalid_resources = _resource_entries(script)
    invalid_entries.extend(invalid_resources)
    catalog_tools = {
        str(entry.get("name") or "").strip(): entry
        for entry in catalog.get("tools") or []
        if isinstance(entry, dict) and str(entry.get("name") or "").strip()
    }

    missing = sorted(set(catalog_tools) - set(profile))
    unknown = sorted(set(profile) - set(catalog_tools))
    bin_mismatches: dict[str, list[str]] = {}
    missing_functions: list[str] = []
    skipped: dict[str, str] = {}
    catalog_resources = {
        str(entry.get("name") or "").strip(): entry
        for category in ("wordlists", "resources")
        for entry in (catalog.get(category) or [])
        if isinstance(entry, dict) and str(entry.get("name") or "").strip()
    }
    missing_resources = sorted(set(catalog_resources) - set(resources))
    unknown_resources = sorted(set(resources) - set(catalog_resources))
    resource_path_mismatches: dict[str, list[str]] = {}

    for name in sorted(set(catalog_tools) & set(profile)):
        expected_bins = {
            str(binary).strip()
            for binary in (catalog_tools[name].get("bins") or [name])
            if str(binary).strip()
        }
        missing_bins = sorted(expected_bins - set(profile[name]["bins"]))
        if missing_bins:
            bin_mismatches[name] = missing_bins

        if profile[name]["policy"] == "skip":
            skipped[name] = profile[name]["reason"]
            continue
    for entry in profile.values():
        if entry["policy"] != "install":
            continue
        function = entry["function"]
        if not re.search(rf"^{re.escape(function)}\(\)\s*\{{", script, re.MULTILINE):
            missing_functions.append(function)

    for name in sorted(set(catalog_resources) & set(resources)):
        expected_paths = {
            str(path).strip()
            for path in (catalog_resources[name].get("candidates") or [])
            if str(path).strip()
        }
        if expected_paths and not expected_paths.intersection(resources[name]["paths"]):
            resource_path_mismatches[name] = sorted(expected_paths)
    for entry in resources.values():
        if entry["policy"] != "install":
            continue
        function = entry["function"]
        if not re.search(rf"^{re.escape(function)}\(\)\s*\{{", script, re.MULTILINE):
            missing_functions.append(function)

    return {
        "catalog_count": len(catalog_tools),
        "installed_count": sum(entry["policy"] == "install" for entry in profile.values()),
        "resource_count": len(catalog_resources),
        "installed_resource_count": sum(entry["policy"] == "install" for entry in resources.values()),
        "missing": missing,
        "unknown": unknown,
        "missing_resources": missing_resources,
        "unknown_resources": unknown_resources,
        "bin_mismatches": bin_mismatches,
        "resource_path_mismatches": resource_path_mismatches,
        "missing_functions": sorted(set(missing_functions)),
        "invalid_entries": invalid_entries,
        "skipped": skipped,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("--f8x", type=Path, default=Path(__file__).resolve().parents[1] / "f8x")
    args = parser.parse_args()

    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    report = check_catalog(catalog, args.f8x.read_text(encoding="utf-8"))
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    failures = (
        report["missing"]
        or report["unknown"]
        or report["bin_mismatches"]
        or report["missing_resources"]
        or report["unknown_resources"]
        or report["resource_path_mismatches"]
        or report["missing_functions"]
        or report["invalid_entries"]
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
