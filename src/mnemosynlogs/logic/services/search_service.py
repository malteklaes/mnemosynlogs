from typing import List, Optional
from ..models.log_entry import LogEntry

class SearchService:
    @staticmethod
    def filter(entries: List[LogEntry],
               text: Optional[str] = None,
               status: Optional[str] = None,
               ticket_id: Optional[str] = None) -> List[LogEntry]:
        result = entries
        if text:
            t = text.lower()
            result = [e for e in result if t in e.content.lower()]
        if status:
            result = [e for e in result if (e.status or "").lower() == status.lower()]
        if ticket_id:
            result = [e for e in result if (e.ticket_id or "").lower() == ticket_id.lower()]
        return result
