
from dataclasses import dataclass
from typing import Optional

@dataclass
class LogEntry:
    id: int                     # auto
    ticket_id: Optional[str]    # 'ticket id' im CSV, kann 'na' sein
    content: str
    duration: Optional[int]     # Minuten; bei daily/todo/issues oft 'na'
    date: str                   # z.B. "15.06.2025"
    time: str                   # z.B. "12:01:24"
    status: Optional[str]       # z.B. 'todo' / 'done' / 'na'
    duedate: Optional[str]      # z.B. "17.06.2025" / 'na'

