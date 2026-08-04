from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT))

from factory.core.metrics import ImmutableRecordStore  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Registra um snapshot bruto como MetricObservation imutavel.")
    parser.add_argument("raw_json", type=Path)
    parser.add_argument("--platform", required=True)
    parser.add_argument("--window", required=True, choices=["24h", "72h", "7d", "28d", "custom"])
    parser.add_argument("--source", required=True)
    parser.add_argument("--content-id", default="video-003")
    parser.add_argument("--channel-id", default="palavra-que-cuida")
    parser.add_argument("--store", type=Path, default=PROJECT_ROOT / "operations" / "a-palavra-que-cuida" / "09_metricas" / "video-003")
    args = parser.parse_args()

    raw = args.raw_json.read_bytes()
    values = json.loads(raw.decode("utf-8"))
    if not isinstance(values, dict):
        raise ValueError("O snapshot bruto deve ser um objeto JSON de metricas.")
    digest = hashlib.sha256(raw).hexdigest()
    payload = {
        "schema_version": "1.0.0",
        "observation_id": f"{args.channel_id}-{args.content_id}-{args.platform}-{args.window}-{digest[:12]}",
        "channel_id": args.channel_id,
        "content_id": args.content_id,
        "platform": args.platform,
        "window": args.window,
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "source": args.source,
        "values": values,
        "raw_hash": digest,
        "raw_artifact": str(args.raw_json.resolve()),
    }
    ImmutableRecordStore(args.store).append_observation(payload)
    print(payload["observation_id"])


if __name__ == "__main__":
    main()
