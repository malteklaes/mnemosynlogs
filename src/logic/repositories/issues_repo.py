from pathlib import Path
from .base_csv_repo import BaseCsvRepository

class IssuesRepo(BaseCsvRepository):
    def __init__(self, data_dir: Path):
        super().__init__(data_dir / "issuesLog.csv")
