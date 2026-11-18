"""Composition Root: єдине місце, де шари «збираються» через DI."""
from __future__ import annotations

from dataclasses import dataclass

from library.application.use_cases.add_book import AddBookUseCase
from library.application.use_cases.borrow_book import BorrowBookUseCase
from library.application.use_cases.list_books import ListBooksUseCase
from library.application.use_cases.return_book import ReturnBookUseCase
from library.domain.interfaces.book_repository import IBookRepository
from library.infrastructure.repositories.in_memory_book_repository import InMemoryBookRepository
from library.infrastructure.repositories.json_book_repository import JsonBookRepository
from library.infrastructure.services import SystemClock, UuidIdGenerator
from library.infrastructure.settings import Settings


@dataclass
class Container:
    add_book: AddBookUseCase
    list_books: ListBooksUseCase
    borrow_book: BorrowBookUseCase
    return_book: ReturnBookUseCase


def create_repository(settings: Settings) -> IBookRepository:
    if settings.storage_type == "json":
        return JsonBookRepository(settings.storage_path, settings.storage_indent)
    if settings.storage_type == "memory":
        return InMemoryBookRepository()
    raise ValueError(f"Невідомий тип сховища: {settings.storage_type}")


def build_container(settings: Settings) -> Container:
    repository: IBookRepository = create_repository(settings)
    clock = SystemClock()
    ids = UuidIdGenerator()
    return Container(
        add_book=AddBookUseCase(repository, ids),
        list_books=ListBooksUseCase(repository),
        borrow_book=BorrowBookUseCase(repository, clock, settings.default_loan_days),
        return_book=ReturnBookUseCase(repository, clock),
    )
