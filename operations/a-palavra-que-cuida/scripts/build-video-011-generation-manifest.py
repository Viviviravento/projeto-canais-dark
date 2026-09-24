from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHANNEL_ROOT = ROOT / "operations" / "a-palavra-que-cuida"
PERFORMANCE = CHANNEL_ROOT / "02_roteiros" / "video-011-performance-v1.json"
SCRIPT = CHANNEL_ROOT / "02_roteiros" / "video-011-roteiro-v1.md"
OUTPUT = CHANNEL_ROOT / "02_roteiros" / "video-011-generation-manifest-v1.json"


def main() -> None:
    manifest = json.loads(PERFORMANCE.read_text(encoding="utf-8"))
    source = SCRIPT.read_text(encoding="utf-8")
    sections = re.split(r"(?m)^##\s+\d{2}\s+-\s+", source)[1:]
    if len(sections) != len(manifest["blocks"]):
        raise RuntimeError(f"Expected {len(manifest['blocks'])} sections, found {len(sections)}")

    blocks = []
    for block, section in zip(manifest["blocks"], sections):
        _, _, body = section.partition("\n")
        cleaned_lines = []
        for line in body.splitlines():
            cleaned_lines.append(line[2:] if line.startswith("> ") else line)
        text = "\n".join(cleaned_lines).strip()
        if not text:
            raise RuntimeError(f"Empty text for {block['id']}")
        blocks.append({**block, "text": text})

    output = {**manifest, "version": "video-011-generation-manifest-v1", "blocks": blocks}
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(OUTPUT), "blocks": len(blocks), "characters": sum(len(block["text"]) for block in blocks)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
