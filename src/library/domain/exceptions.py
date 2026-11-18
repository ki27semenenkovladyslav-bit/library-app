"""Доменні винятки бібліотеки."""


class DomainError(Exception):
    """Базовий виняток доменного шару."""


class ValidationError(DomainError):
    """Дані сутності не відповідають бізнес-правилам."""


class BookNotFoundError(DomainError):
    """Книгу з указаним ідентифікатором не знайдено."""

    def __init__(self, book_id: str) -> None:
        super().__init__(f"Книгу з id '{book_id}' не знайдено")
        self.book_id = book_id


class BookNotAvailableError(DomainError):
    """Книга вже видана іншому читачеві."""


class BookNotBorrowedError(DomainError):
    """Спроба повернути книгу, яку не видавали."""
