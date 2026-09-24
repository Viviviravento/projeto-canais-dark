"""Validate a draft ACF citation manifest against the channel safety cap."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def unique_direct_references(manifest: dict) -> list[str]:
    references = []
    for item in manifest.get("direct_acf_citations", []):
        reference = str(item.get("reference", "")).strip()
        if not reference:
            raise ValueError("Every direct ACF citation needs a reference.")
        if reference not in references:
            references.append(reference)
    return references


def published_total(registry: dict) -> int:
    total = 0
    for output in registry.get("published_outputs", []):
        count = output.get("quoted_verse_count")
        if count is None:
            count = len(set(output.get("direct_acf_references", [])))
        total += int(count)
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(__file__).with_name("registro-citacoes-acf.json"),
    )
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    registry = load_json(args.registry)
    references = unique_direct_references(manifest)
    current = published_total(registry)
    cap = int(registry["project_policy"]["published_channel_cap"])
    projected = current + len(references)

    print(f"Published ACF verse units: {current}")
    print(f"Draft direct ACF verse units: {len(references)}")
    print(f"Projected total: {projected}/{cap}")
    print("Draft references: " + ", ".join(references))

    if projected > cap:
        print("BLOCKED: projected total exceeds the internal ACF cap.")
        return 2
    if projected >= cap - 100:
        print("WARNING: projected total enters the 100-verse safety margin.")
    else:
        print("PASS: projected total remains below the internal ACF cap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
