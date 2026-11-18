"""Сутність «Книга» та бізнес-правила видачі."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

from library.domain.exceptions import (
    BookNotAvailableError,
    BookNotBorrowedError,
    ValidationError,
)

MIN_PUBLICATION_YEAR = 1450   # друкарський верстат Гутенберга
MAX_LOAN_DAYS = 30            # максимальний строк видачі книги


@dataclass
class Book:
    id: str
    title: str
    author: str
    year: int
    borrower: Optional[str] = None
    due_date: Optional[date] = None

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        self.author = self.author.strip()
        if not self.title:
            raise ValidationError("Назва книги не може бути порожньою")
        if not self.author:
            raise ValidationError("Автор книги не може бути порожнім")
        if self.year < MIN_PUBLICATION_YEAR:
            raise ValidationError(
                f"Рік видання має бути не меншим за {MIN_PUBLICATION_YEAR}"
            )

    @property
    def is_available(self) -> bool:
        return self.borrower is None

    def borrow(self, reader: str, today: date, loan_days: int) -> None:
        """Видати книгу читачеві на loan_days днів."""
        reader = reader.strip()
        if not reader:
            raise ValidationError("Ім'я читача не може бути порожнім")
        if not 1 <= loan_days <= MAX_LOAN_DAYS:
            raise ValidationError(
                f"Строк видачі має бути від 1 до {MAX_LOAN_DAYS} днів"
            )
        if not self.is_available:
            raise BookNotAvailableError(
                f"Книга «{self.title}» вже видана читачеві {self.borrower}"
            )
        self.borrower = reader
        self.due_date = today + timedelta(days=loan_days)

    def return_book(self) -> None:
        """Повернути книгу до бібліотеки."""
        if self.is_available:
            raise BookNotBorrowedError(f"Книга «{self.title}» не була видана")
        self.borrower = None
        self.due_date = None

    def is_overdue(self, today: date) -> bool:
        return self.due_date is not None and today > self.due_date
