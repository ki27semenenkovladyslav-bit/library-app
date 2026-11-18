from typing import List

from library.application.dto import BookDto
from library.domain.interfaces.book_repository import IBookRepository


class ListBooksUseCase:
    """Отримати каталог книг, упорядкований за назвою."""

    def __init__(self, repository: IBookRepository) -> None:
        self._repository = repository

    def execute(self) -> List[BookDto]:
        books = sorted(self._repository.list_all(), key=lambda b: b.title.lower())
        return [BookDto.from_entity(b) for b in books]
