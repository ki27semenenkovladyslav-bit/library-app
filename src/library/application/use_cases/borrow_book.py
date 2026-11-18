from library.application.dto import BookDto
from library.application.interfaces.services import IClock
from library.domain.exceptions import BookNotFoundError
from library.domain.interfaces.book_repository import IBookRepository


class BorrowBookUseCase:
    """Видати книгу читачеві."""

    def __init__(self, repository: IBookRepository, clock: IClock,
                 default_loan_days: int = 14) -> None:
        self._repository = repository
        self._clock = clock
        self._default_loan_days = default_loan_days

    def execute(self, book_id: str, reader: str, loan_days: int | None = None) -> BookDto:
        book = self._repository.get(book_id)
        if book is None:
            raise BookNotFoundError(book_id)
        book.borrow(reader, self._clock.today(), loan_days or self._default_loan_days)
        self._repository.update(book)
        return BookDto.from_entity(book)
