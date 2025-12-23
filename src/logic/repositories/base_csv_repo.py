
import csv
from pathlib import Path
from typing import List, Iterable
from ..models.log_entry import LogEntry

CSV_FIELDS = ["id","ticket id","content","duration","date","time","status","duedate"]

class BaseCsvRepository:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            with self.file_path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
                writer.writeheader()

    def read_all(self) -> List[LogEntry]:
        rows: List[LogEntry] = []
        with self.file_path.open("r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(LogEntry(
                    id=int(r["id"]),
                    ticket_id=self._na_to_none(r["ticket id"]),
                    content=r["content"],
                    duration=self._na_to_int(r["duration"]),
                    date=r["date"],
                    time=r["time"],
                    status=self._na_to_none(r["status"]),
                    duedate=self._na_to_none(r["duedate"])
                ))
        return rows

    def write_all(self, entries: Iterable[LogEntry]) -> None:
        with self.file_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for e in entries:
                writer.writerow({
                    "id": e.id,
                    "ticket id": e.ticket_id or "na",
                    "content": e.content,
                    "duration": e.duration if e.duration is not None else "na",
                    "date": e.date,
                    "time": e.time,
                    "status": e.status or "na",
                    "duedate": e.duedate or "na"
                })

    @staticmethod
    def _na_to_none(val: str):
        return None if val in (None, "", "na") else val

    @staticmethod
    def _na_to_int(val: str):
        if val in (None, "", "na"):
            return None
        return int(val)
