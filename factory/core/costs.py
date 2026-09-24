from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from decimal import Decimal, ROUND_UP
from pathlib import Path
from typing import Any, Protocol
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def money(value: Decimal | str | int | float) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.000001"), rounding=ROUND_UP)


@dataclass(frozen=True)
class PricePoint:
    provider: str
    model: str
    operation: str
    unit: str
    currency: str
    unit_price: Decimal
    checked_at: str
    source: str


class PriceSource(Protocol):
    def current_price(self, provider: str, model: str, operation: str) -> PricePoint: ...


@dataclass
class CostQuote:
    quote_id: str
    provider: str
    model: str
    operation: str
    unit: str
    quantity: Decimal
    currency: str
    unit_price: Decimal
    price_checked_at: str
    price_source: str
    expected_cost: Decimal
    maximum_cost: Decimal
    status: str = "quoted"
    observed_cost: Decimal | None = None
    parent_quote_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_contract(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["schema_version"] = "1.0.0"
        for field_name in ("quantity", "unit_price", "expected_cost", "maximum_cost", "observed_cost"):
            value = payload[field_name]
            payload[field_name] = None if value is None else float(value)
        return {"schema_version": payload.pop("schema_version"), **payload}


class CostLedger:
    """Cota antes, reserva o maximo e concilia o debito observado."""

    def __init__(self, path: Path | str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.quotes: dict[str, CostQuote] = {}

    def quote(
        self,
        price_source: PriceSource,
        *,
        provider: str,
        model: str,
        operation: str,
        quantity: Decimal | str | int | float,
        maximum_quantity: Decimal | str | int | float | None = None,
        parent_quote_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> CostQuote:
        point = price_source.current_price(provider, model, operation)
        qty = money(quantity)
        max_qty = money(maximum_quantity if maximum_quantity is not None else quantity)
        if qty <= 0 or max_qty < qty:
            raise ValueError("Quantidade deve ser positiva e o maximo nao pode ser menor que o esperado")
        quote = CostQuote(
            quote_id=f"quote-{uuid4().hex[:12]}",
            parent_quote_id=parent_quote_id,
            provider=provider,
            model=model,
            operation=operation,
            unit=point.unit,
            quantity=qty,
            currency=point.currency,
            unit_price=money(point.unit_price),
            price_checked_at=point.checked_at,
            price_source=point.source,
            expected_cost=money(qty * point.unit_price),
            maximum_cost=money(max_qty * point.unit_price),
            metadata=metadata or {},
        )
        self.quotes[quote.quote_id] = quote
        self._append("quoted", quote)
        return quote

    def reserve(self, quote_id: str) -> CostQuote:
        quote = self._get(quote_id)
        if quote.status != "quoted":
            raise ValueError(f"Cotacao {quote_id} nao pode ser reservada em estado {quote.status}")
        quote.status = "reserved"
        self._append("reserved", quote)
        return quote

    def reconcile(self, quote_id: str, observed_cost: Decimal | str | int | float) -> CostQuote:
        quote = self._get(quote_id)
        if quote.status != "reserved":
            raise ValueError(f"Cotacao {quote_id} nao esta reservada")
        observed = money(observed_cost)
        if observed < 0:
            raise ValueError("Debito observado nao pode ser negativo")
        quote.observed_cost = observed
        quote.status = "reconciled"
        self._append("reconciled", quote)
        return quote

    def fail(self, quote_id: str, reason: str) -> CostQuote:
        quote = self._get(quote_id)
        quote.status = "failed"
        quote.metadata["failure_reason"] = reason
        self._append("failed", quote)
        return quote

    def retry_quote(self, quote_id: str, price_source: PriceSource) -> CostQuote:
        previous = self._get(quote_id)
        return self.quote(
            price_source,
            provider=previous.provider,
            model=previous.model,
            operation=previous.operation,
            quantity=previous.quantity,
            parent_quote_id=previous.quote_id,
            metadata={"retry_of": previous.quote_id},
        )

    def _get(self, quote_id: str) -> CostQuote:
        try:
            return self.quotes[quote_id]
        except KeyError as exc:
            raise KeyError(f"Cotacao desconhecida: {quote_id}") from exc

    def _append(self, event: str, quote: CostQuote) -> None:
        record = {"event": event, "recorded_at": utc_now(), "quote": quote.as_contract()}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

