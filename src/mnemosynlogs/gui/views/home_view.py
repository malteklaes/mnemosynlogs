import tkinter as tk
from tkinter import ttk

from ...logic.services.log_service import LogService
from ...logic.persistence.activity_persist import ActivityPersist
from ...logic.persistence.daily_persist import DailyPersist
from ...logic.persistence.todo_persist import TodoPersist
from ...logic.persistence.issues_persist import IssuesPersist
from ...util.paths import data_dir_path
from ..theme.win95_palette import WIN95

# NEU: ActivityDisplay importieren
from ..widgets.activity_display import ActivityDisplay


class HomeView(tk.Frame):
    """
    90er-Look gemäß Bauplan:
    - Sidebar links (activity/daily/todo/issues)
    - Mittlerer Workspace (blau), darin Activity-Anzeige mit Datumsgruppen
    - Unten Eingabeleiste (unverändert)
    """

    def __init__(self, parent):
        super().__init__(parent, bg=WIN95["bg"])

        # Services
        data_dir = data_dir_path()
        self.services = {
            "activity": LogService(ActivityPersist(data_dir)),
            "daily":    LogService(DailyPersist(data_dir)),
            "todo":     LogService(TodoPersist(data_dir)),
            "issues":   LogService(IssuesPersist(data_dir)),
        }
        self.current_log = "activity"

        # --- Haupt-Layout: Sidebar + Workspace ---------------------------------
        main = tk.Frame(self, bg=WIN95["bg"])
        main.pack(fill="both", expand=True, padx=6, pady=6)

        # Sidebar links
        sidebar = tk.Frame(main, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        sidebar.pack(side="left", fill="y", padx=(0, 6))
        for name in ["activity", "daily", "todo", "issues"]:
            tk.Button(
                sidebar,
                text=name,
                relief="raised",
                bg=WIN95["btn_face"],
                width=10,
                command=lambda n=name: self._switch(n)
            ).pack(padx=6, pady=6)

        # Workspace (blau)
        workspace = tk.Frame(main, bg=WIN95["desk_bg"], relief="sunken", borderwidth=2)
        workspace.pack(side="left", fill="both", expand=True)

        # --- ZENTRALE ANZEIGE (ersetzt die alte "Konsole") ----------------------
        console_frame = tk.Frame(workspace, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        console_frame.place(relx=0.05, rely=0.08, relwidth=0.90, relheight=0.70)

        # Placeholder – wird in refresh() ersetzt
        self.activity_display = None

        # --- Eingabe-Leiste unten (UNVERÄNDERT) ---------------------------------
        bottom = tk.Frame(workspace, bg=WIN95["bg"], relief="raised", borderwidth=2)
        bottom.place(relx=0.05, rely=0.80, relwidth=0.90, relheight=0.15)

        # ticket id
        tk.Label(bottom, text="ticket id:", bg=WIN95["bg"]).place(relx=0.01, rely=0.20)
        self.ticket_var = tk.StringVar()
        tik_panel = tk.Frame(bottom, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        tik_panel.place(relx=0.12, rely=0.10, relwidth=0.15, relheight=0.60)
        tk.Entry(tik_panel, textvariable=self.ticket_var, bg=WIN95["entry_bg"]).pack(fill="both", expand=True)

        # content
        tk.Label(bottom, text="content:", bg=WIN95["bg"]).place(relx=0.29, rely=0.20)
        self.content_var = tk.StringVar()
        con_panel = tk.Frame(bottom, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        con_panel.place(relx=0.38, rely=0.10, relwidth=0.35, relheight=0.60)
        tk.Entry(con_panel, textvariable=self.content_var, bg=WIN95["entry_bg"]).pack(fill="both", expand=True)

        # duration
        tk.Label(bottom, text="duration (min):", bg=WIN95["bg"]).place(relx=0.74, rely=0.20)
        self.duration_var = tk.StringVar()
        dur_panel = tk.Frame(bottom, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        dur_panel.place(relx=0.85, rely=0.10, relwidth=0.08, relheight=0.60)
        tk.Entry(dur_panel, textvariable=self.duration_var, bg=WIN95["entry_bg"]).pack(fill="both", expand=True)

        # status
        tk.Label(bottom, text="status:", bg=WIN95["bg"]).place(relx=0.01, rely=0.70)
        self.status_var = tk.StringVar()
        stat_panel = tk.Frame(bottom, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        stat_panel.place(relx=0.12, rely=0.65, relwidth=0.15, relheight=0.25)
        ttk.Combobox(
            stat_panel,
            textvariable=self.status_var,
            values=["na", "todo", "done", ""],
            state="readonly"
        ).pack(fill="both", expand=True)

        # ADD-Button (noch nicht grün – kommt später)
        tk.Button(
            bottom,
            text="add",
            relief="raised",
            bg=WIN95["btn_face"],
            command=self.add_entry
        ).place(relx=0.94, rely=0.10, relwidth=0.05, relheight=0.60)

        # Statuszeile
        self.status = tk.StringVar(value="Bereit.")
        statusbar = tk.Frame(self, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        statusbar.pack(side="bottom", fill="x", padx=6, pady=(0, 6))
        tk.Label(statusbar, textvariable=self.status, bg=WIN95["bg"], anchor="w").pack(fill="x")

        # Initiales Laden
        self.console_frame = console_frame
        self.refresh()

    # --- Service/Logik ----------------------------------------------------------
    def _switch(self, name: str):
        if name in self.services:
            self.current_log = name
            self.refresh()

    def _svc(self) -> LogService:
        return self.services[self.current_log]

    def refresh(self):
        entries = self._svc().list()

        # Alte Anzeige entfernen
        if self.activity_display is not None:
            self.activity_display.destroy()

        # Neue Anzeige mit Datumsgruppen erzeugen
        self.activity_display = ActivityDisplay(self.console_frame, entries)
        self.activity_display.pack(fill="both", expand=True, padx=4, pady=4)

        self.status.set(f"{self.current_log}: {len(entries)} Einträge geladen.")

    def add_entry(self):
        content = (self.content_var.get() or "").strip()
        ticket = (self.ticket_var.get() or "").strip()
        duration = (self.duration_var.get() or "").strip()
        status = (self.status_var.get() or "").strip() or None

        if not content:
            self.status.set("Bitte content eingeben.")
            return

        dur_val = int(duration) if duration.isdigit() else None
        ticket_val = ticket if ticket else None

        self._svc().add(
            ticket_id=ticket_val,
            content=content,
            duration=dur_val,
            status=status,
            duedate=None
        )

        self.content_var.set("")
        self.ticket_var.set("")
        self.duration_var.set("")
        self.status_var.set("")
        self.refresh()
        self.status.set(f"Eintrag zu {self.current_log} hinzugefügt.")
