from __future__ import annotations

import csv
import hashlib
import io
import mimetypes
import re
import zipfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


MAX_FILE_BYTES = 25 * 1024 * 1024
MAX_ARCHIVE_MEMBERS = 2_000
MAX_ARCHIVE_UNCOMPRESSED = 200 * 1024 * 1024
MAX_EXPANSION_RATIO = 100
FORMULA_PREFIXES = ("=", "+", "-", "@")
ACTIVE_HTML = re.compile(r"<(script|iframe|object|embed|form)\b|\son[a-z]+\s*=", re.IGNORECASE)
INSTRUCTION_LURES = (
    "ignore previous instructions",
    "ignore all previous",
    "ignore as instrucoes anteriores",
    "system prompt",
    "developer message",
)


class UnsafeContentError(ValueError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def detect_media_type(data: bytes, path: Path | None = None) -> str:
    if data.startswith(b"PK\x03\x04"):
        if path and path.suffix.lower() in {".xlsx", ".xlsm"}:
            return "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return "application/zip"
    if data.startswith(b"\x80"):
        return "application/x-python-pickle"
    if data.startswith(b"%PDF"):
        return "application/pdf"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if data.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    prefix = data[:1024].lstrip().lower()
    if prefix.startswith((b"<!doctype html", b"<html")):
        return "text/html"
    guessed = mimetypes.guess_type(str(path))[0] if path else None
    return guessed or "application/octet-stream"


def inspect_archive(data: bytes) -> list[str]:
    names: list[str] = []
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            infos = archive.infolist()
            if len(infos) > MAX_ARCHIVE_MEMBERS:
                raise UnsafeContentError("Arquivo compactado possui entradas demais")
            compressed = sum(max(info.compress_size, 1) for info in infos)
            uncompressed = sum(info.file_size for info in infos)
            if uncompressed > MAX_ARCHIVE_UNCOMPRESSED:
                raise UnsafeContentError("Arquivo compactado excede o limite descompactado")
            if uncompressed / max(compressed, 1) > MAX_EXPANSION_RATIO:
                raise UnsafeContentError("Taxa de expansao abusiva detectada")
            for info in infos:
                normalized = info.filename.replace("\\", "/").lower()
                if normalized.startswith("/") or "../" in normalized:
                    raise UnsafeContentError("Caminho inseguro dentro do arquivo compactado")
                if normalized.endswith((".zip", ".7z", ".rar", ".tar", ".gz", ".pkl", ".pickle")):
                    raise UnsafeContentError("Arquivo compactado aninhado ou formato executavel rejeitado")
                names.append(normalized)
    except zipfile.BadZipFile as exc:
        raise UnsafeContentError("Assinatura ZIP invalida") from exc
    return names


def inspect_xlsx(data: bytes) -> None:
    names = inspect_archive(data)
    if any(name.endswith("vbaproject.bin") or name.startswith("xl/embeddings/") for name in names):
        raise UnsafeContentError("Macro ou objeto incorporado rejeitado")
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        for name in names:
            if name.startswith("xl/externalLinks/".lower()):
                raise UnsafeContentError("Vinculo externo em XLSX rejeitado")
            if name.startswith("xl/worksheets/") and name.endswith(".xml"):
                content = archive.read(name)
                if b"<f" in content:
                    raise UnsafeContentError("Formula em XLSX rejeitada")


def sanitize_csv(data: bytes, *, max_rows: int = 100_000, max_cells: int = 1_000_000) -> bytes:
    text = data.decode("utf-8-sig")
    source = csv.reader(io.StringIO(text))
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    cell_count = 0
    for row_index, row in enumerate(source, start=1):
        if row_index > max_rows:
            raise UnsafeContentError("CSV excede o limite de linhas")
        safe_row = []
        for value in row:
            cell_count += 1
            if cell_count > max_cells:
                raise UnsafeContentError("CSV excede o limite de celulas")
            stripped = value.lstrip()
            if stripped.startswith(FORMULA_PREFIXES):
                value = "'" + value
            safe_row.append(value)
        writer.writerow(safe_row)
    return output.getvalue().encode("utf-8")


@dataclass
class UntrustedContent:
    content_id: str
    source_kind: str
    locator: str
    media_type: str
    sha256: str
    payload_ref: str
    active_content: str = "not_present"
    formula_policy: str = "not_applicable"
    warnings: list[str] = field(default_factory=list)
    captured_at: str = field(default_factory=utc_now)

    def as_contract(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "content_id": self.content_id,
            "source_kind": self.source_kind,
            "locator": self.locator,
            "captured_at": self.captured_at,
            "media_type": self.media_type,
            "sha256": self.sha256,
            "trust": "untrusted_data_only",
            "handling": {
                "active_content": self.active_content,
                "formula_policy": self.formula_policy,
                "instruction_policy": "never_execute",
                "warnings": self.warnings,
            },
            "payload_ref": self.payload_ref,
        }


def encapsulate_text(content_id: str, text: str, *, source_kind: str, locator: str, payload_ref: str) -> UntrustedContent:
    lowered = text.lower()
    warnings = ["possible_prompt_injection"] if any(lure in lowered for lure in INSTRUCTION_LURES) else []
    active = "rejected" if ACTIVE_HTML.search(text) else "not_present"
    return UntrustedContent(
        content_id=content_id,
        source_kind=source_kind,
        locator=locator,
        media_type="text/html" if "<html" in lowered else "text/plain",
        sha256=sha256_bytes(text.encode("utf-8")),
        payload_ref=payload_ref,
        active_content=active,
        warnings=warnings,
    )


def inspect_file(path: Path | str, *, expected_media_type: str | None = None) -> UntrustedContent:
    file_path = Path(path)
    if file_path.suffix.lower() in {".pkl", ".pickle", ".xlsm"}:
        raise UnsafeContentError(f"Formato rejeitado: {file_path.suffix.lower()}")
    if file_path.stat().st_size > MAX_FILE_BYTES:
        raise UnsafeContentError("Arquivo excede o limite de entrada")
    data = file_path.read_bytes()
    media_type = detect_media_type(data, file_path)
    if media_type == "application/x-python-pickle":
        raise UnsafeContentError("Pickle rejeitado")
    if expected_media_type and media_type != expected_media_type:
        raise UnsafeContentError(f"MIME divergente: esperado {expected_media_type}, detectado {media_type}")

    source_kind = "external_file"
    formula_policy = "not_applicable"
    if file_path.suffix.lower() == ".csv":
        sanitize_csv(data)
        source_kind = "csv"
        formula_policy = "escaped"
    elif file_path.suffix.lower() == ".xlsx":
        inspect_xlsx(data)
        source_kind = "xlsx"
        formula_policy = "rejected"
    elif media_type == "application/zip":
        inspect_archive(data)
        source_kind = "archive"

    return UntrustedContent(
        content_id=f"file-{sha256_bytes(data)[:12]}",
        source_kind=source_kind,
        locator=str(file_path),
        media_type=media_type,
        sha256=sha256_bytes(data),
        payload_ref=str(file_path),
        formula_policy=formula_policy,
    )

