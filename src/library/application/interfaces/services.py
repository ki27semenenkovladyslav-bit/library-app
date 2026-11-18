"""Інтерфейси сервісів, потрібних use cases (реалізуються в Infrastructure)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date


class IClock(ABC):
    """Джерело поточної дати (дозволяє підміняти час у тестах)."""

    @abstractmethod
    def today(self) -> date: ...


class IIdGenerator(ABC):
    """Генератор унікальних ідентифікаторів сутностей."""

    @abstractmethod
    def new_id(self) -> str: ...
