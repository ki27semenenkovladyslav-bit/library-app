"""Об'єкти передачі даних між Application- та Presentation-шарами."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from library.domain.entities.book import Book


@dataclass(frozen=True)
class AddBookRequest:
    title: str
    author: str
    year: int


@dataclass(frozen=True)
class BookDto:
    id: str
    title: str
    author: str
    year: int
    is_available: bool
    borrower: Optional[str]
    due_date: Optional[date]

    @staticmethod
    def from_entity(book: Book) -> "BookDto":
        return BookDto(
            id=book.id,
            title=book.title,
            author=book.author,
            year=book.year,
            is_available=book.is_available,
            borrower=book.borrower,
            due_date=book.due_date,
        )
