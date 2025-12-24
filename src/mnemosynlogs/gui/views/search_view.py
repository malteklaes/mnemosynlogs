import tkinter as tk
from tkinter import ttk
from ...logic.services.log_service import LogService
from ...logic.services.search_service import SearchService
from ...logic.repositories.activity_repo import ActivityRepo
from ...logic.repositories.daily_repo import DailyRepo
from ...logic.repositories.todo_repo import TodoRepo
from ...logic.repositories.issues_repo import IssuesRepo
from ...util.paths import data_dir_path

COLUMNS = ("id","ticket id","content","duration","date","time","status","duedate")

class SearchView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self._build_services()
        self._build_header()
        self._build_filters()
        self._build_results()
        self._bind_events()
        self._load_default()

    # --- Services & Datenquellen -------------------------------------------------
    def _build_services(self):
        data_dir = data_dir_path()
        self.services = {
            "activity": LogService(ActivityRepo(data_dir)),
            "daily":    LogService(DailyRepo(data_dir)),
            "todo":     LogService(TodoRepo(data_dir)),
            "issues":   LogService(IssuesRepo(data_dir)),
        }
        self.current_log_type = tk.StringVar(value="activity")
        self.search_service = SearchService()

    # --- UI: Header --------------------------------------------------------------
    def _build_header(self):
        header = tk.Frame(self)
        header.pack(side="top", fill="x", padx=6, pady=6)

        tk.Label(header, text="Log-Typ:").pack(side="left")
        self.cbo_log = ttk.Combobox(header, state="readonly",
                                    values=["activity","daily","todo","issues"],
                                    textvariable=self.current_log_type, width=12)
        self.cbo_log.pack(side="left", padx=(4, 12))

        self.btn_refresh = ttk.Button(header, text="Alle laden", command=self._load_default)
        self.btn_refresh.pack(side="left")

    # --- UI: Filterleiste --------------------------------------------------------
    def _build_filters(self):
        frm = tk.LabelFrame(self, text="Filter")
        frm.pack(side="top", fill="x", padx=6, pady=(0,6), ipady=3)

        # Textfilter
        tk.Label(frm, text="Text:").grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.var_text = tk.StringVar()
        tk.Entry(frm, textvariable=self.var_text, width=40).grid(row=0, column=1, sticky="we", padx=4, pady=3)

        # Status
        tk.Label(frm, text="Status:").grid(row=0, column=2, sticky="w", padx=12, pady=3)
        self.var_status = tk.StringVar()
        self.cbo_status = ttk.Combobox(frm, textvariable=self.var_status,
                                       values=["", "todo", "done", "na"], width=10, state="readonly")
        self.cbo_status.grid(row=0, column=3, sticky="w", padx=4, pady=3)
        self.cbo_status.set("")

        # Ticket-ID
        tk.Label(frm, text="Ticket-ID:").grid(row=0, column=4, sticky="w", padx=12, pady=3)
        self.var_ticket = tk.StringVar()
        tk.Entry(frm, textvariable=self.var_ticket, width=16).grid(row=0, column=5, sticky="w", padx=4, pady=3)

        # Buttons
        self.btn_search = ttk.Button(frm, text="Suchen", command=self._do_search)
        self.btn_search.grid(row=0, column=6, padx=(12,4), pady=3, sticky="w")

        self.btn_clear = ttk.Button(frm, text="Zurücksetzen", command=self._clear_filters)
        self.btn_clear.grid(row=0, column=7, padx=4, pady=3, sticky="w")

        frm.grid_columnconfigure(1, weight=1)  # Textfeld dehnbar

    # --- UI: Ergebnisliste -------------------------------------------------------
    def _build_results(self):
        wrap = tk.Frame(self)
        wrap.pack(side="top", fill="both", expand=True, padx=6, pady=(0,6))

        self.tree = ttk.Treeview(wrap, columns=COLUMNS, show="headings", selectmode="browse")
        for c in COLUMNS:
            self.tree.heading(c, text=c)
            width = 90
            if c == "content":
                width = 420
            elif c in ("id", "duration"):
                width = 70
            self.tree.column(c, width=width, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(wrap, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Statusbar
        self.status = tk.StringVar(value="Bereit.")
        tk.Label(self, textvariable=self.status, anchor="w").pack(side="bottom", fill="x", padx=6, pady=(0,6))

    # --- Events ------------------------------------------------------------------
    def _bind_events(self):
        self.cbo_log.bind("<<ComboboxSelected>>", lambda e: self._load_default())
        # Enter im Text-, Ticket- oder Statusfeld startet Suche
        for widget in (self.cbo_status, ):
            widget.bind("<<ComboboxSelected>>", lambda e: self._do_search())
        # Return-Taste in Eingabefeldern
        def bind_return(w):
            w.bind("<Return>", lambda e: self._do_search())
        bind_return(self.children_lookup(self, tk.Entry, index=0))  # Text
        bind_return(self.children_lookup(self, tk.Entry, index=1))  # Ticket

    def children_lookup(self, root, cls, index=0):
        # kleine Hilfe, um das n-te Entry zu finden (nur fürs Return-Binding)
        matches = []
        def walk(w):
            for c in w.winfo_children():
                if isinstance(c, cls):
                    matches.append(c)
                walk(c)
        walk(root)
        return matches[index] if index < len(matches) else None

    # --- Datenladen & Suche ------------------------------------------------------
    def _get_current_service(self) -> LogService:
        return self.services[self.current_log_type.get()]

    def _load_default(self):
        self._populate_tree(self._get_current_service().list())
        self.status.set(f"{self.current_log_type.get()} – {len(self.tree.get_children())} Einträge geladen.")

    def _do_search(self):
        svc = self._get_current_service()
        entries = svc.list()
        filtered = self.search_service.filter(
            entries,
            text=self.var_text.get().strip() or None,
            status=(self.var_status.get().strip() or None),
            ticket_id=(self.var_ticket.get().strip() or None)
        )
        self._populate_tree(filtered)
        self.status.set(f"Suche in {self.current_log_type.get()}: {len(filtered)} Treffer.")

    def _clear_filters(self):
        self.var_text.set("")
        self.cbo_status.set("")
        self.var_ticket.set("")
        self._load_default()

    
    def _populate_tree(self, entries):
            # Tree leeren
            for i in self.tree.get_children():
                self.tree.delete(i)
            # Einträge füllen
            for e in entries:
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        e.id,
                        e.ticket_id or "na",
                        e.content,
                        e.duration if e.duration is not None else "na",
                        e.date,
                        e.time,
                        e.status or "na",
                        e.duedate or "na",
                    ),
                )

