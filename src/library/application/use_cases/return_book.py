from library.application.dto import BookDto
from library.application.interfaces.services import IClock
from library.domain.exceptions import BookNotFoundError
from library.domain.interfaces.book_repository import IBookRepository


class ReturnBookUseCase:
    """Прийняти книгу від читача. Повертає (книга, чи було прострочення)."""

    def __init__(self, repository: IBookRepository, clock: IClock) -> None:
        self._repository = repository
        self._clock = clock

    def execute(self, book_id: str) -> tuple[BookDto, bool]:
        book = self._repository.get(book_id)
        if book is None:
            raise BookNotFoundError(book_id)
        was_overdue = book.is_overdue(self._clock.today())
        book.return_book()
        self._repository.update(book)
        return BookDto.from_entity(book), was_overdue
