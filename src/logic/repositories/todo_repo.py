from pathlib import Path
from .base_csv_repo import BaseCsvRepository

class TodoRepo(BaseCsvRepository):
    def __init__(self, data_dir: Path):
        super().__init__(data_dir / "todoLog.csv")
