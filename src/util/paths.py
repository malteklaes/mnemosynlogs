import sys
from pathlib import Path

def resource_path() -> Path:
    # Bei PyInstaller liegt alles unter _MEIPASS; im Dev-Fall normaler Pfad
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent

def data_dir_path() -> Path:
    # Datenordner relativ zum Paket (oder im _MEIPASS)
    base = resource_path() / "data"
    base.mkdir(parents=True, exist_ok=True)
    return base

