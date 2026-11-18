from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional

from library.domain.entities.book import Book
from library.domain.interfaces.book_repository import IBookRepository


class JsonBookRepository(IBookRepository):
    """Сховище книг у JSON-файлі."""

    def __init__(self, path: str | Path, indent: int = 2) -> None:
        self._path = Path(path)
        self._indent = indent

    # --- серіалізація -------------------------------------------------
    @staticmethod
    def _to_dict(book: Book) -> dict:
        return {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "year": book.year,
            "borrower": book.borrower,
            "due_date": book.due_date.isoformat() if book.due_date else None,
        }

    @staticmethod
    def _from_dict(data: dict) -> Book:
        due = data.get("due_date")
        return Book(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=int(data["year"]),
            borrower=data.get("borrower"),
            due_date=date.fromisoformat(due) if due else None,
        )

    def _load(self) -> Dict[str, Book]:
        if not self._path.exists():
            return {}
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        return {item["id"]: self._from_dict(item) for item in raw}

    def _save(self, books: Dict[str, Book]) -> None:
        payload = [self._to_dict(b) for b in books.values()]
        self._path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=self._indent),
            encoding="utf-8",
        )

    # --- IBookRepository ----------------------------------------------
    def add(self, book: Book) -> None:
        books = self._load()
        books[book.id] = book
        self._save(books)

    def get(self, book_id: str) -> Optional[Book]:
        return self._load().get(book_id)

    def list_all(self) -> List[Book]:
        return list(self._load().values())

    def update(self, book: Book) -> None:
        self.add(book)
