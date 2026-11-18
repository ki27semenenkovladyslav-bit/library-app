"""Інтерфейс репозиторію книг (порт доменного шару)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from library.domain.entities.book import Book


class IBookRepository(ABC):
    """Абстракція сховища книг.

    Описана в Domain-шарі, а реалізується в Infrastructure-шарі.
    Use cases залежать лише від цього інтерфейсу (принцип DIP).
    """

    @abstractmethod
    def add(self, book: Book) -> None: ...

    @abstractmethod
    def get(self, book_id: str) -> Optional[Book]: ...

    @abstractmethod
    def list_all(self) -> List[Book]: ...

    @abstractmethod
    def update(self, book: Book) -> None: ...
