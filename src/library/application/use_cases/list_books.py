from typing import List

from library.application.dto import BookDto
from library.domain.interfaces.book_repository import IBookRepository


class ListBooksUseCase:
    """Отримати каталог книг, упорядкований за назвою."""

    def __init__(self, repository: IBookRepository) -> None:
        self._repository = repository

    def execute(self, only_available: bool = False) -> List[BookDto]:
        books = self._repository.list_all()
        if only_available:
            books = [b for b in books if b.is_available]
        books = sorted(books, key=lambda b: b.title.lower())
        return [BookDto.from_entity(b) for b in books]
