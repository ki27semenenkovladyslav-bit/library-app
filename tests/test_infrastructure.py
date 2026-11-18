import tempfile
import unittest
from datetime import date
from pathlib import Path

from library.domain.entities.book import Book
from library.infrastructure.repositories.in_memory_book_repository import InMemoryBookRepository
from library.infrastructure.repositories.json_book_repository import JsonBookRepository
from library.infrastructure.settings import Settings


class RepositoryContract:
    """Однаковий набір перевірок для будь-якої реалізації IBookRepository."""

    def make_repository(self):
        raise NotImplementedError

    def test_add_get_update(self):
        repo = self.make_repository()
        book = Book(id="b1", title="Лісова пісня", author="Леся Українка", year=1911)
        repo.add(book)
        loaded = repo.get("b1")
        self.assertEqual(loaded.title, "Лісова пісня")
        loaded.borrow("Іван", date(2026, 11, 20), 10)
        repo.update(loaded)
        self.assertEqual(repo.get("b1").borrower, "Іван")
        self.assertEqual(len(repo.list_all()), 1)

    def test_missing_book_returns_none(self):
        self.assertIsNone(self.make_repository().get("nope"))


class InMemoryRepositoryTests(RepositoryContract, unittest.TestCase):
    def make_repository(self):
        return InMemoryBookRepository()


class JsonRepositoryTests(RepositoryContract, unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def make_repository(self):
        return JsonBookRepository(Path(self.tmp.name) / "books.json")


class SettingsTests(unittest.TestCase):
    def test_defaults_when_file_missing(self):
        self.assertEqual(Settings.load("no-such-file.json").storage_type, "memory")


if __name__ == "__main__":
    unittest.main()
