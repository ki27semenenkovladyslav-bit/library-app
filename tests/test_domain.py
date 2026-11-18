import unittest
from datetime import date

from library.domain.entities.book import Book
from library.domain.exceptions import (
    BookNotAvailableError,
    BookNotBorrowedError,
    ValidationError,
)

TODAY = date(2026, 11, 20)


def make_book() -> Book:
    return Book(id="b1", title="Кобзар", author="Тарас Шевченко", year=1840)


class BookTests(unittest.TestCase):
    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValidationError):
            Book(id="x", title="  ", author="Автор", year=2000)

    def test_too_old_year_is_rejected(self):
        with self.assertRaises(ValidationError):
            Book(id="x", title="Назва", author="Автор", year=1200)

    def test_borrow_sets_borrower_and_due_date(self):
        book = make_book()
        book.borrow("Іван Петренко", TODAY, 14)
        self.assertFalse(book.is_available)
        self.assertEqual(book.due_date, date(2026, 12, 4))

    def test_cannot_borrow_twice(self):
        book = make_book()
        book.borrow("Іван", TODAY, 14)
        with self.assertRaises(BookNotAvailableError):
            book.borrow("Олена", TODAY, 7)

    def test_loan_days_limit(self):
        with self.assertRaises(ValidationError):
            make_book().borrow("Іван", TODAY, 45)

    def test_return_not_borrowed_book_fails(self):
        with self.assertRaises(BookNotBorrowedError):
            make_book().return_book()

    def test_overdue(self):
        book = make_book()
        book.borrow("Іван", TODAY, 7)
        self.assertFalse(book.is_overdue(date(2026, 11, 27)))
        self.assertTrue(book.is_overdue(date(2026, 11, 28)))


if __name__ == "__main__":
    unittest.main()
