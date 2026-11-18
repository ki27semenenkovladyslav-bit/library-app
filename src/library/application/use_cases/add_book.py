from library.application.dto import AddBookRequest, BookDto
from library.application.interfaces.services import IIdGenerator
from library.domain.entities.book import Book
from library.domain.interfaces.book_repository import IBookRepository


class AddBookUseCase:
    """Додати нову книгу до каталогу."""

    def __init__(self, repository: IBookRepository, ids: IIdGenerator) -> None:
        self._repository = repository
        self._ids = ids

    def execute(self, request: AddBookRequest) -> BookDto:
        book = Book(
            id=self._ids.new_id(),
            title=request.title,
            author=request.author,
            year=request.year,
        )
        self._repository.add(book)
        return BookDto.from_entity(book)
