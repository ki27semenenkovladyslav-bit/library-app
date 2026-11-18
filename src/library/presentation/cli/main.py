"""Консольний інтерфейс LibraryApp."""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from library.application.dto import AddBookRequest, BookDto
from library.infrastructure.settings import Settings
from library.presentation.composition import build_container


def _format(book: BookDto) -> str:
    status = "доступна" if book.is_available else (
        f"видана: {book.borrower} до {book.due_date:%d.%m.%Y}")
    return f"[{book.id}] {book.title} — {book.author}, {book.year} ({status})"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="library", description="Облік книг бібліотеки")
    parser.add_argument("--config", default="config/appsettings.json",
                        help="шлях до файлу конфігурації")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add", help="додати книгу")
    add.add_argument("title")
    add.add_argument("author")
    add.add_argument("year", type=int)

    lst = sub.add_parser("list", help="показати каталог")
    lst.add_argument("--available", action="store_true", help="лише доступні книги")

    borrow = sub.add_parser("borrow", help="видати книгу читачеві")
    borrow.add_argument("book_id")
    borrow.add_argument("reader")
    borrow.add_argument("--days", type=int, default=None)

    ret = sub.add_parser("return", help="повернути книгу")
    ret.add_argument("book_id")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    app = build_container(Settings.load(args.config))

    if args.command == "add":
        book = app.add_book.execute(AddBookRequest(args.title, args.author, args.year))
        print(f"Додано: {_format(book)}")
    elif args.command == "list":
        books = app.list_books.execute(only_available=args.available)
        if not books:
            print("Каталог порожній")
        for book in books:
            print(_format(book))
    elif args.command == "borrow":
        book = app.borrow_book.execute(args.book_id, args.reader, args.days)
        print(f"Видано: {_format(book)}")
    elif args.command == "return":
        book, overdue = app.return_book.execute(args.book_id)
        print(f"Повернено: {_format(book)}")
        if overdue:
            print("Увага: книгу повернено із запізненням!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
