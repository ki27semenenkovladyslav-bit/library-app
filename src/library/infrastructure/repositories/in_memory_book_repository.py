from __future__ import annotations

import copy
from typing import Dict, List, Optional

from library.domain.entities.book import Book
from library.domain.interfaces.book_repository import IBookRepository


class InMemoryBookRepository(IBookRepository):
    """Сховище в оперативній пам'яті (для тестів і демонстрації)."""

    def __init__(self) -> None:
        self._books: Dict[str, Book] = {}

    def add(self, book: Book) -> None:
        self._books[book.id] = copy.deepcopy(book)

    def get(self, book_id: str) -> Optional[Book]:
        book = self._books.get(book_id)
        return copy.deepcopy(book) if book else None

    def list_all(self) -> List[Book]:
        return [copy.deepcopy(b) for b in self._books.values()]

    def update(self, book: Book) -> None:
        self._books[book.id] = copy.deepcopy(book)
