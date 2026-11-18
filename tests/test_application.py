import unittest
from datetime import date
from typing import Dict, List, Optional

from library.application.dto import AddBookRequest
from library.application.interfaces.services import IClock, IIdGenerator
from library.application.use_cases.add_book import AddBookUseCase
from library.application.use_cases.borrow_book import BorrowBookUseCase
from library.application.use_cases.list_books import ListBooksUseCase
from library.application.use_cases.return_book import ReturnBookUseCase
from library.domain.entities.book import Book
from library.domain.exceptions import BookNotFoundError
from library.domain.interfaces.book_repository import IBookRepository


class FakeRepository(IBookRepository):
    """Тестовий дублер: use cases не знають, яке сховище за інтерфейсом."""

    def __init__(self) -> None:
        self.items: Dict[str, Book] = {}

    def add(self, book: Book) -> None:
        self.items[book.id] = book

    def get(self, book_id: str) -> Optional[Book]:
        return self.items.get(book_id)

    def list_all(self) -> List[Book]:
        return list(self.items.values())

    def update(self, book: Book) -> None:
        self.items[book.id] = book


class FixedClock(IClock):
    def __init__(self, today: date) -> None:
        self.value = today

    def today(self) -> date:
        return self.value


class SequentialIds(IIdGenerator):
    def __init__(self) -> None:
        self.n = 0

    def new_id(self) -> str:
        self.n += 1
        return f"b{self.n}"


class UseCaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repo = FakeRepository()
        self.clock = FixedClock(date(2026, 11, 20))
        self.add = AddBookUseCase(self.repo, SequentialIds())
        self.borrow = BorrowBookUseCase(self.repo, self.clock, default_loan_days=14)
        self.give_back = ReturnBookUseCase(self.repo, self.clock)
        self.list = ListBooksUseCase(self.repo)

    def test_add_and_list_sorted(self):
        self.add.execute(AddBookRequest("Тіні забутих предків", "М. Коцюбинський", 1911))
        self.add.execute(AddBookRequest("Кайдашева сім'я", "І. Нечуй-Левицький", 1879))
        titles = [b.title for b in self.list.execute()]
        self.assertEqual(titles, ["Кайдашева сім'я", "Тіні забутих предків"])

    def test_borrow_uses_default_loan_days(self):
        book = self.add.execute(AddBookRequest("Кобзар", "Т. Шевченко", 1840))
        dto = self.borrow.execute(book.id, "Олена")
        self.assertEqual(dto.due_date, date(2026, 12, 4))
        self.assertFalse(dto.is_available)

    def test_borrow_unknown_book(self):
        with self.assertRaises(BookNotFoundError):
            self.borrow.execute("nope", "Олена")

    def test_return_reports_overdue(self):
        book = self.add.execute(AddBookRequest("Кобзар", "Т. Шевченко", 1840))
        self.borrow.execute(book.id, "Олена", loan_days=3)
        self.clock.value = date(2026, 11, 30)
        dto, overdue = self.give_back.execute(book.id)
        self.assertTrue(dto.is_available)
        self.assertTrue(overdue)


if __name__ == "__main__":
    unittest.main()
