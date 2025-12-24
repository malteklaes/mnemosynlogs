from datetime import datetime
from typing import List, Optional
from ..models.log_entry import LogEntry
from ..repositories.base_csv_repo import BaseCsvRepository
from ...util.ids import next_id

class LogService:
    def __init__(self, repo: BaseCsvRepository):
        self.repo = repo

    def list(self) -> List[LogEntry]:
        return self.repo.read_all()

    def add(self, *, ticket_id: Optional[str], content: str,
            duration: Optional[int], status: Optional[str],
            duedate: Optional[str]) -> LogEntry:
        entries = self.repo.read_all()
        new_id = next_id(entries)                         # max(id)+1
        now = datetime.now()
        e = LogEntry(
            id=new_id,
            ticket_id=ticket_id,
            content=content,
            duration=duration,
            date=now.strftime("%d.%m.%Y"),
            time=now.strftime("%H:%M:%S"),
            status=status,
            duedate=duedate
        )
        entries.append(e)
        self.repo.write_all(entries)
        return e

    def update(self, entry: LogEntry) -> None:
        entries = self.repo.read_all()
        for i, e in enumerate(entries):
            if e.id == entry.id:
                entries[i] = entry
                break
        self.repo.write_all(entries)

    def delete(self, entry_id: int) -> None:
        entries = [e for e in self.repo.read_all() if e.id != entry_id]
        self.repo.write_all(entries)
