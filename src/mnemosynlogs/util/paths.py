
# src/mnemosynlogs/util/paths.py
import os
import sys
from pathlib import Path

APP_NAME = "MnemoSynLogs"
CSV_HEADER = "id,ticket id,content,duration,date,time,status,duedate\n"

def resource_path() -> Path:
    """
    Pfad zu mitgepackten Ressourcen (Assets, Defaults).
    Bei PyInstaller: _MEIPASS, sonst Paketpfad.
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent

def user_data_dir() -> Path:
    """
    Persistenter, beschreibbarer Datenordner je Benutzer.
    Windows: %APPDATA%/MnemoSynLogs/data
    macOS: ~/Library/Application Support/MnemoSynLogs/data
    Linux: ~/.local/share/MnemoSynLogs/data
    """
    if sys.platform.startswith("win"):
        base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path.home() / ".local" / "share"
    d = base / APP_NAME / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d

def ensure_csv(file_name: str) -> Path:
    """
    Stellt sicher, dass die CSV (im user_data_dir) existiert.
    Falls nicht, wird aus dem mitgepackten 'data' Ordner kopiert
    (wenn vorhanden), sonst mit Header neu angelegt.
    """
    target = user_data_dir() / file_name
    if not target.exists():
        src = resource_path() / "mnemosynlogs" / "data" / file_name
        try:
            if src.exists():
                target.write_bytes(src.read_bytes())
            else:
                target.write_text(CSV_HEADER, encoding="utf-8")
        except Exception:
            # Fallback: Header schreiben
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(CSV_HEADER, encoding="utf-8")
    return target

def data_dir_path() -> Path:
    """
    Für bestehenden Code kompatibel: nutzt den persistente Ordner.
    """
    return user_data_dir()
