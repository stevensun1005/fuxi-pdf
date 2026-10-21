#!/usr/bin/env python3
"""Validate a study ledger, optionally against actual source-page counts."""
import argparse
import csv
import json
from pathlib import Path
from collections import Counter

COLUMNS = "source_id lecture_id page_or_slide topic concept_id importance disposition summary_location explanation_depth visual_check citation notes".split()
KINDS = {"covered", "duplicate", "administrative", "blank", "uncertain"}


def inspect_ledger(path, inventory=None):
    with Path(path).open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        absent = set(COLUMNS) - set(reader.fieldnames or [])
        if absent:
            return ["Missing columns: " + ", ".join(sorted(absent))], Counter()
        rows = list(reader)
    errors, seen, counts = [], set(), Counter()
    if not rows:
        errors.append("The ledger contains no pages.")
    for line, row in enumerate(rows, 2):
        if None in row or any(row.get(k) is None for k in COLUMNS):
            errors.append(f"Line {line}: malformed CSV row.")
            continue
        row = {k: v.strip() for k, v in row.items()}
        source, raw = row["source_id"], row["page_or_slide"]
        if not source or not raw.isdecimal() or int(raw) < 1:
            errors.append(f"Line {line}: source ID and positive integer page required.")
            continue
        key = source, int(raw)
        if key in seen:
            errors.append(f"Line {line}: repeated page {source}/{key[1]}.")
        seen.add(key)
        kind = row["disposition"].lower()
        counts[kind] += 1
        if kind not in KINDS or kind == "uncertain":
            errors.append(f"Line {line}: unresolved or invalid disposition {kind!r}.")
        if kind == "covered":
            for field in ["concept_id", "importance", "summary_location", "explanation_depth", "citation"]:
                if not row[field]:
                    errors.append(f"Line {line}: covered page needs {field}.")
        elif kind in {"duplicate", "administrative", "blank"} and not row["notes"]:
            errors.append(f"Line {line}: {kind} page needs a reason in notes.")
    if inventory is not None:
        if not isinstance(inventory, dict) or not inventory or any(
            not isinstance(k, str) or not k.strip() or type(v) is not int or v < 1
            for k, v in inventory.items()
        ):
            raise ValueError("Inventory must map source IDs to positive integer page counts.")
        expected = {(s, p) for s, n in inventory.items() for p in range(1, n + 1)}
        for label, diff in [("Missing page", expected - seen), ("Unexpected page", seen - expected)]:
            errors.extend(f"{label}: {s}/{p}" for s, p in sorted(diff))
    return errors, counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path)
    parser.add_argument("--inventory", type=Path, help="JSON object: source ID -> actual page count")
    args = parser.parse_args(argv)
    try:
        inventory = json.loads(args.inventory.read_text(encoding="utf-8-sig")) if args.inventory else None
        errors, counts = inspect_ledger(args.ledger, inventory)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(2, f"ERROR: {error}\n")
    if errors:
        print("FAIL\n" + "\n".join("- " + error for error in errors))
        return 1
    scope = "exact source-page coverage" if args.inventory else "ledger only; source completeness NOT checked"
    print(f"PASS: {scope}; {sum(counts.values())} rows; {dict(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
