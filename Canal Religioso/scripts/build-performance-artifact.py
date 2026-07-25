"""Build a TTS performance artifact from one canonical Markdown script."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SECTION_RE = re.compile(r"^###\s+(?P<number>\d+)\s*\|\s*(?P<title>.+?)\s*$", re.MULTILINE)


def clean_markdown(text: str) -> str:
    lines: list[str] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(">"):
            line = line[1:].strip()
        line = line.replace("**", "").replace("`", "")
        if line.startswith("#"):
            continue
        lines.append(line)
    return "\n\n".join(lines)


def script_sections(markdown: str) -> dict[str, dict[str, str]]:
    matches = list(SECTION_RE.finditer(markdown))
    sections: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(markdown)
        section_id = match.group("number")
        sections[section_id] = {
            "title": match.group("title").strip(),
            "text": clean_markdown(markdown[start:end]),
        }
    return sections


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    source_path = (args.spec.parent / spec["source_script"]).resolve()
    sections = script_sections(source_path.read_text(encoding="utf-8"))

    blocks = []
    for block_spec in spec["blocks"]:
        section_id = block_spec["source_section"]
        if section_id not in sections:
            raise ValueError(f"Missing script section: {section_id}")
        blocks.append(
            {
                "id": block_spec["id"],
                "source_section": section_id,
                "title": sections[section_id]["title"],
                "function": block_spec["function"],
                "text": sections[section_id]["text"],
            }
        )

    artifact = {
        "version": spec["version"],
        "source_script": str(source_path),
        "performance_contract": spec["performance_contract"],
        "api": spec["api"],
        "blocks": blocks,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
