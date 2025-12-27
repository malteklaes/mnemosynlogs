
# src/mnemosynlogs/gui/views/edit_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from ...logic.services.log_service import LogService
from ...logic.persistence.activity_persist import ActivityPersist
from ...logic.persistence.daily_persist import DailyPersist
from ...logic.persistence.todo_persist import TodoPersist
from ...logic.persistence.issues_persist import IssuesPersist
from ...util.paths import data_dir_path

COLUMNS = ("id","ticket id","content","duration","date","time","status","duedate")

class EditView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_services()
        self._build_header()
        self._build_table()
        self._build_form()
        self._load()

    def _build_services(self):
        data_dir = data_dir_path()
        self.services = {
            "activity": LogService(ActivityPersist(data_dir)),
            "daily":    LogService(DailyPersist(data_dir)),
            "todo":     LogService(TodoPersist(data_dir)),
            "issues":   LogService(IssuesPersist(data_dir)),
        }
        self.current_log_type = tk.StringVar(value="activity")

    def _build_header(self):
        top = tk.Frame(self)
        top.pack(fill="x", padx=6, pady=6)
        tk.Label(top, text="Log-Typ:").pack(side="left")
        self.cbo_log = ttk.Combobox(top, state="readonly",
                                    values=list(self.services.keys()),
                                    textvariable=self.current_log_type, width=12)
        self.cbo_log.pack(side="left", padx=(4, 12))
        self.cbo_log.bind("<<ComboboxSelected>>", lambda e: self._load())

        tk.Button(top, text="Neu laden", command=self._load).pack(side="left")

    def _build_table(self):
        wrap = tk.Frame(self)
        wrap.pack(fill="both", expand=True, padx=6, pady=(0,6))
        self.tree = ttk.Treeview(wrap, columns=COLUMNS, show="headings", selectmode="browse")
        for c in COLUMNS:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=100 if c != "content" else 420, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", lambda e: self._on_select())

    def _build_form(self):
        frm = tk.LabelFrame(self, text="Bearbeiten")
        frm.pack(fill="x", padx=6, pady=(0,6))

        self.var_id = tk.StringVar()
        self.var_ticket = tk.StringVar()
        self.var_content = tk.StringVar()
        self.var_duration = tk.StringVar()
        self.var_status = tk.StringVar()
        self.var_duedate = tk.StringVar()

        r = 0
        tk.Label(frm, text="ID:").grid(row=r, column=0, sticky="e", padx=4, pady=3)
        tk.Entry(frm, textvariable=self.var_id, state="readonly", width=8).grid(row=r, column=1, sticky="w", padx=4, pady=3)
        r += 1

        tk.Label(frm, text="Ticket-ID:").grid(row=r, column=0, sticky="e", padx=4, pady=3)
        tk.Entry(frm, textvariable=self.var_ticket, width=20).grid(row=r, column=1, sticky="w", padx=4, pady=3)

        tk.Label(frm, text="Content:").grid(row=r, column=2, sticky="e", padx=12, pady=3)
        tk.Entry(frm, textvariable=self.var_content, width=60).grid(row=r, column=3, sticky="we", padx=4, pady=3)
        r += 1

        tk.Label(frm, text="Duration(min):").grid(row=r, column=0, sticky="e", padx=4, pady=3)
        tk.Entry(frm, textvariable=self.var_duration, width=10).grid(row=r, column=1, sticky="w", padx=4, pady=3)

        tk.Label(frm, text="Status:").grid(row=r, column=2, sticky="e", padx=12, pady=3)
        ttk.Combobox(frm, textvariable=self.var_status, values=["na","todo","done",""], width=10, state="readonly").grid(row=r, column=3, sticky="w", padx=4, pady=3)
        r += 1

        tk.Label(frm, text="Due-Date (DD.MM.YYYY):").grid(row=r, column=0, sticky="e", padx=4, pady=3)
        tk.Entry(frm, textvariable=self.var_duedate, width=20).grid(row=r, column=1, sticky="w", padx=4, pady=3)

        btns = tk.Frame(frm)
        btns.grid(row=r, column=3, sticky="e", padx=4, pady=3)
        ttk.Button(btns, text="Speichern", command=self._save).pack(side="left", padx=3)
        ttk.Button(btns, text="Löschen", command=self._delete).pack(side="left", padx=3)

        frm.grid_columnconfigure(3, weight=1)

    def _svc(self) -> LogService:
        return self.services[self.current_log_type.get()]

    def _load(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for e in self._svc().list():
            self.tree.insert("", "end", values=(e.id, e.ticket_id or "na", e.content,
                                                e.duration if e.duration is not None else "na",
                                                e.date, e.time, e.status or "na", e.duedate or "na"))
        # Formular leeren
        self.var_id.set(""); self.var_ticket.set(""); self.var_content.set("")
        self.var_duration.set(""); self.var_status.set(""); self.var_duedate.set("")

    def _on_select(self):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0], "values")
        self.var_id.set(vals[0]); self.var_ticket.set(vals[1] if vals[1] != "na" else "")
        self.var_content.set(vals[2])
        self.var_duration.set("" if vals[3] == "na" else vals[3])
        self.var_status.set("" if vals[6] == "na" else vals[6])
        self.var_duedate.set("" if vals[7] == "na" else vals[7])

    def _save(self):
        if not self.var_id.get():
            messagebox.showwarning("Hinweis", "Bitte zuerst einen Eintrag auswählen.")
            return
        entry_id = int(self.var_id.get())
        # aktuellen Stand laden und gewünschtes Objekt anpassen
        entries = self._svc().list()
        for e in entries:
            if e.id == entry_id:
                e.ticket_id = self.var_ticket.get().strip() or None
                e.content = self.var_content.get().strip()
                e.duration = int(self.var_duration.get()) if self.var_duration.get().strip().isdigit() else None
                e.status = self.var_status.get().strip() or None
                e.duedate = self.var_duedate.get().strip() or None
                self._svc().update(e)
                break
        self._load()
        messagebox.showinfo("Gespeichert", "Eintrag wurde aktualisiert.")

    def _delete(self):
        if not self.var_id.get():
            messagebox.showwarning("Hinweis", "Bitte zuerst einen Eintrag auswählen.")
            return
        if messagebox.askyesno("Löschen", "Diesen Eintrag wirklich löschen?"):
            self._svc().delete(int(self.var_id.get()))
            self._load()
