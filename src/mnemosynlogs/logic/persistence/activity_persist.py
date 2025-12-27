from pathlib import Path
from .base_csv_persist import BaseCsvPersistence
from ...util.paths import ensure_csv

class ActivityPersist(BaseCsvPersistence):
    def __init__(self, _data_dir: Path = None):
        super().__init__(ensure_csv("activityLog.csv"))
