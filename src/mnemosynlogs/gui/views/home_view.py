
import tkinter as tk
from tkinter import ttk

from ...logic.services.log_service import LogService
from ...logic.persistence.activity_persist import ActivityPersist
from ...logic.persistence.daily_persist import DailyPersist
from ...logic.persistence.todo_persist import TodoPersist
from ...logic.persistence.issues_persist import IssuesPersist
from ...util.paths import data_dir_path
from ..theme.win95_palette import WIN95

class HomeView(tk.Frame):
    """
    90er-Look gemäß Bauplan:
    - Sidebar links (activity/daily/todo/issues)
    - Mittlerer Workspace (blau), darin „Konsole“-Fenster (schwarz, weißer Text)
    - Unten Eingabeleiste (ticket id, content, duration, status, add)
    - Oben wird globaler Header/Titlebar außerhalb dieses Views gerendert
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

        # Sidebar links (vertikale Buttons)
        sidebar = tk.Frame(main, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        sidebar.pack(side="left", fill="y", padx=(0,6))
        for name in ["activity", "daily", "todo", "issues"]:
            tk.Button(sidebar, text=name, relief="raised", bg=WIN95["btn_face"],
                      width=10, command=lambda n=name: self._switch(n)).pack(padx=6, pady=6)

        # Workspace (blau)
        workspace = tk.Frame(main, bg=WIN95["desk_bg"], relief="sunken", borderwidth=2)
        workspace.pack(side="left", fill="both", expand=True)

        # „Konsole“-Fenster (schwarz) im Workspace
        console_frame = tk.Frame(workspace, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        console_frame.place(relx=0.05, rely=0.08, relwidth=0.90, relheight=0.70)  # Position wie im Bauplan (ungefähr)

        self.console = tk.Text(console_frame,
                               bg=WIN95["console_bg"], fg=WIN95["console_fg"],
                               insertbackground=WIN95["console_fg"],
                               font=("Courier New", 10), state="disabled")
        self.console.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        sb = ttk.Scrollbar(console_frame, orient="vertical", command=self.console.yview)
        self.console.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")

        # Eingabe-Leiste unten im Workspace (raised Panel)
        bottom = tk.Frame(workspace, bg=WIN95["bg"], relief="raised", borderwidth=2)
        bottom.place(relx=0.05, rely=0.80, relwidth=0.90, relheight=0.15)

        # ticket id
        tk.Label(bottom, text="ticket id:", bg=WIN95["bg"]).place(relx=0.01, rely=0.20)
        self.ticket_var = tk.StringVar()
        tik_panel = tk.Frame(bottom, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        tik_panel.place(relx=0.12, rely=0.10, relwidth=0.15, relheight=0.60)
        tk.Entry(tik_panel, textvariable=self.ticket_var, bg=WIN95["entry_bg"]).pack(fill="both", expand=True)

        # content (breit)
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
        ttk.Combobox(stat_panel, textvariable=self.status_var,
                     values=["na","todo","done",""], state="readonly").pack(fill="both", expand=True)

        # ADD-Button (rechts außen)
        tk.Button(bottom, text="add", relief="raised", bg=WIN95["btn_face"],
                  command=self.add_entry).place(relx=0.94, rely=0.10, relwidth=0.05, relheight=0.60)

        # Statuszeile (unterhalb des Workspace)
        self.status = tk.StringVar(value="Bereit.")
        statusbar = tk.Frame(self, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        statusbar.pack(side="bottom", fill="x", padx=6, pady=(0,6))
        tk.Label(statusbar, textvariable=self.status, bg=WIN95["bg"], anchor="w").pack(fill="x")

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
        # Konsole neu rendern (einfaches Zeilenformat; später gruppiert nach Datum)
        self.console.configure(state="normal")
        self.console.delete("1.0", "end")
        for e in entries:
            dur = e.duration if e.duration is not None else "na"
            line = f"{e.id}  {e.ticket_id or 'na'}  {e.content}  {dur}min  {e.date}  {e.time}  {e.status or 'na'}\n"
            self.console.insert("end", line)
        self.console.configure(state="disabled")
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

        self._svc().add(ticket_id=ticket_val, content=content,
                         duration=dur_val, status=status, duedate=None)
        self.content_var.set(""); self.ticket_var.set(""); self.duration_var.set(""); self.status_var.set("")
        self.refresh()
        self.status.set(f"Eintrag zu {self.current_log} hinzugefügt.")
