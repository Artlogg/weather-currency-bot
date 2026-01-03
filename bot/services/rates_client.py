from __future__ import annotations

from dataclasses import dataclass

import httpx


@dataclass(frozen=True)
class RateResult:
    base: str
    target: str
    rate: float


class RatesClient:
    def __init__(self, http: httpx.AsyncClient) -> None:
        self._http = http

    async def get_rate(self, base: str, target: str) -> RateResult:
        base = base.upper()
        target = target.upper()

        resp = await self._http.get(
            "https://api.frankfurter.app/latest",
            params={"from": base, "to": target},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        rates = data.get("rates") or {}
        if target not in rates:
            raise ValueError("PAIR_NOT_SUPPORTED")

        return RateResult(base=base, target=target, rate=float(rates[target]))
