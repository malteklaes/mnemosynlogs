from pathlib import Path
from .base_csv_repo import BaseCsvRepository
from ...util.paths import ensure_csv

class ActivityRepo(BaseCsvRepository):
    def __init__(self, _data_dir: Path = None):
        super().__init__(ensure_csv("activityLog.csv"))
