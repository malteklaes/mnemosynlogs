import tkinter as tk
from collections import defaultdict
from datetime import datetime
from textwrap import wrap

ORANGE = "#ff9900"

COL_ID      = 5
COL_TIME    = 10
COL_TICKET  = 14
COL_DUR     = 10
COL_CONTENT = 50


class ActivityDisplay(tk.Frame):
    def __init__(self, parent, entries):
        super().__init__(parent, bg="black")

        # Scrollbar erstellen
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")

        self.text = tk.Text(
            self,
            bg="black",
            fg="white",
            insertbackground="white",
            relief="sunken",
            borderwidth=2,
            wrap="none",              # Wrapping selbst
            font=("Courier New", 10),
            yscrollcommand=self.scrollbar.set,
            state="normal"
        )
        self.text.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.text.yview)

        # Tag-Konfigurationen
        self.text.tag_configure(
            "date",
            foreground=ORANGE,
            font=("Courier New", 10, "bold")
        )
        self.text.tag_configure("entry", foreground="white")

        self.render(entries)
        self.text.config(state="disabled")

    def render(self, entries):
        self.text.config(state="normal")
        self.text.delete("1.0", "end")

        # Gruppieren nach Datum
        grouped = defaultdict(list)
        for e in entries:
            grouped[e.date or "ohne Datum"].append(e)

        # ---- Header ---------------------------------------------------------
        header = (
            " "
            + "ID".ljust(COL_ID)
            + "Uhrzeit".ljust(COL_TIME)
            + "Ticket Id".ljust(COL_TICKET)
            + "Dauer".ljust(COL_DUR)
            + "Content".ljust(COL_CONTENT)
            + "\n"
        )
        sep_len = COL_ID + COL_TIME + COL_TICKET + COL_DUR + COL_CONTENT + 1
        separator = "-" * sep_len + "\n"

        self.text.insert("end", header, "entry")
        self.text.insert("end", separator, "entry")

        # ---- Inhalt ---------------------------------------------------------
        for date in sorted(grouped.keys(), reverse=True):
            # Datum mit Wochentag, robust für verschiedene Formate
            date_str = date
            for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
                try:
                    dt = datetime.strptime(date, fmt)
                    date_str = dt.strftime("%d.%m.%Y (%A)")
                    break
                except Exception:
                    continue

            self.text.insert("end", f"\n{date_str}\n", "date")


            # Einträge nach Uhrzeit sortieren (neueste oben)
            for e in sorted(grouped[date], key=lambda x: (x.time or ""), reverse=True):
                eid     = str(e.id).ljust(COL_ID)
                time    = (e.time or "--:--").ljust(COL_TIME)
                ticket  = (e.ticket_id or "").ljust(COL_TICKET)
                dur     = (f"{e.duration} min" if e.duration else "na").ljust(COL_DUR)

                # Content sauber umbrechen
                content_lines = wrap(e.content or "", COL_CONTENT) or [""]

                # erste Zeile (mit Metadaten)
                line = (
                    " "
                    + eid
                    + time
                    + ticket
                    + dur
                    + content_lines[0].ljust(COL_CONTENT)
                    + "\n"
                )
                self.text.insert("end", line, "entry")

                # Folgezeilen: nur Content, sauber eingerückt
                indent = " " + " " * (COL_ID + COL_TIME + COL_TICKET + COL_DUR)
                for cont in content_lines[1:]:
                    self.text.insert(
                        "end",
                        indent + cont.ljust(COL_CONTENT) + "\n",
                        "entry"
                    )

        self.text.config(state="disabled")
