"""Export human-readable upload sheets from canonical publication manifests."""

from __future__ import annotations

import json
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent


def description_with_cross_link(package: dict) -> str:
    description = package["description"]
    cross_link = package.get("cross_link", {})
    url = cross_link.get("youtube_url")
    if not url:
        return description
    line = cross_link["description_line_template"].replace("{YOUTUBE_URL}", url)
    paragraphs = description.split("\n\n")
    paragraphs.insert(2, line)
    return "\n\n".join(paragraphs)


def main() -> None:
    for manifest_path in sorted(PACKAGE_DIR.glob("*-publicacao-v1.json")):
        package = json.loads(manifest_path.read_text(encoding="utf-8"))
        output_path = PACKAGE_DIR / f"{package['video_id']}-copiar-e-colar-v1.txt"
        output = "\n".join(
            [
                "TÍTULO",
                package["title"],
                "",
                "DESCRIÇÃO",
                description_with_cross_link(package),
                "",
                "COMENTÁRIO FIXADO",
                package["pinned_comment"],
                "",
                "TAGS",
                ", ".join(package["tags"]),
                "",
            ]
        )
        output_path.write_text(output, encoding="utf-8")
        print(output_path)


if __name__ == "__main__":
    main()
