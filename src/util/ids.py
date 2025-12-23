from typing import Iterable
from ..logic.models.log_entry import LogEntry

def next_id(entries: Iterable[LogEntry]) -> int:
    return (max((e.id for e in entries), default=0) + 1)