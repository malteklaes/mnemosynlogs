
# src/mnemosynlogs/logic/repositories/base_csv_repo.py
import csv
from pathlib import Path
from typing import List, Iterable
from ..models.log_entry import LogEntry

CSV_FIELDS = ["id","ticket id","content","duration","date","time","status","duedate"]

def _norm(name: str) -> str:
    return (name or "").replace("\ufeff", "").strip().lower().replace("_", " ")

class BaseCsvRepository:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        # Wenn Datei fehlt oder leer ist: Header schreiben
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            self._write_header()

    def _write_header(self):
        with self.file_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()

    def read_all(self) -> List[LogEntry]:
        # BOM-tolerant lesen
        with self.file_path.open("r", newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                # keine Header -> reparieren
                self._write_header()
                return []

            # Header-Normalisierung und Mapping
            mapping = { _norm(orig): orig for orig in reader.fieldnames }
            missing = [k for k in CSV_FIELDS if _norm(k) not in mapping]

            # Wenn Spalten fehlen, versuche zu migrieren (z. B. ticket_id -> ticket id)
            if missing:
                rows = list(reader)
                self._rewrite_with_header(rows, reader.fieldnames)
                # nach Reparatur nochmal lesen
                return self.read_all()

            rows: List[LogEntry] = []
            for r in reader:
                def get(key: str) -> str:
                    return r.get(mapping[_norm(key)], "")
                rows.append(LogEntry(
                    id=int(get("id")) if get("id") else 0,
                    ticket_id=self._na_to_none(get("ticket id")),
                    content=get("content"),
                    duration=self._na_to_int(get("duration")),
                    date=get("date"),
                    time=get("time"),
                    status=self._na_to_none(get("status")),
                    duedate=self._na_to_none(get("duedate"))
                ))
            return rows

    def _rewrite_with_header(self, rows, old_fieldnames):
        """Schreibt Datei mit korrektem Header neu; mappt alte Feldnamen -> neue."""
        old_norm = { _norm(n): n for n in old_fieldnames }
        with self.file_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            for r in rows:
                def val(key):
                    oname = old_norm.get(_norm(key))
                    return (r.get(oname, "") if oname else "")
                writer.writerow({
                    "id": val("id") or "0",
                    "ticket id": val("ticket id") or "na",
                    "content": val("content") or "",
                    "duration": val("duration") or "na",
                    "date": val("date") or "",
                    "time": val("time") or "",
                    "status": val("status") or "na",
                    "duedate": val("duedate") or "na",
                })

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
        return None if val in (None, "", "na", "NA", "Na") else val

    @staticmethod
    def _na_to_int(val: str):
        if val in (None, "", "na", "NA", "Na"):
            return None
        try:
            return int(val)
        except ValueError:
            return None
