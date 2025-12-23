import tkinter as tk
from tkinter import ttk
from ...logic.services.log_service import LogService
from ...logic.repositories.activity_repo import ActivityRepo
from ...logic.repositories.daily_repo import DailyRepo
from ...util.paths import data_dir_path

class HomeView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # Header: Buttons für activity/daily/todo/issues
        btns = tk.Frame(self)
        btns.pack(side="top", fill="x")
        tk.Button(btns, text="activity").pack(side="left", padx=2)
        tk.Button(btns, text="daily").pack(side="left", padx=2)
        tk.Button(btns, text="todo").pack(side="left", padx=2)
        tk.Button(btns, text="issues").pack(side="left", padx=2)

        # Log-Ausgabe (Treeview)
        self.tree = ttk.Treeview(self, columns=("id","ticket","content","duration","date","time","status","duedate"), show="headings")
        for c in self.tree["columns"]:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100)
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        # Eingabeformular (vereinfachtes Beispiel)
        form = tk.Frame(self)
        form.pack(side="bottom", fill="x")
        self.content_var = tk.StringVar()
        tk.Entry(form, textvariable=self.content_var).pack(side="left", fill="x", expand=True)
        tk.Button(form, text="ADD", command=self.add_entry).pack(side="left")

        # Daten laden
        self.activity_service = LogService(ActivityRepo(data_dir_path()))
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for e in self.activity_service.list():
            self.tree.insert("", "end", values=(e.id, e.ticket_id, e.content, e.duration, e.date, e.time, e.status, e.duedate))

    def add_entry(self):
        self.activity_service.add(ticket_id=None, content=self.content_var.get(), duration=None, status=None, duedate=None)
        self.refresh()
