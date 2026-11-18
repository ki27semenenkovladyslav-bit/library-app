"""Читання конфігурації застосунку з appsettings.json."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    storage_type: str = "memory"
    storage_path: str = "books.json"
    storage_indent: int = 2
    default_loan_days: int = 14

    @staticmethod
    def load(path: str | Path) -> "Settings":
        path = Path(path)
        if not path.exists():
            return Settings()
        data = json.loads(path.read_text(encoding="utf-8"))
        storage = data.get("Storage", {})
        loan = data.get("Loan", {})
        return Settings(
            storage_type=storage.get("Type", "memory").lower(),
            storage_path=storage.get("Path", "books.json"),
            storage_indent=int(storage.get("Indent", 2)),
            default_loan_days=int(loan.get("DefaultDays", 14)),
        )
