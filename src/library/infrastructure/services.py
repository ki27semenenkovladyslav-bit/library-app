import uuid
from datetime import date

from library.application.interfaces.services import IClock, IIdGenerator


class SystemClock(IClock):
    def today(self) -> date:
        return date.today()


class UuidIdGenerator(IIdGenerator):
    def new_id(self) -> str:
        return uuid.uuid4().hex[:8]
