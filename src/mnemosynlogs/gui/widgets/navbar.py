
import tkinter as tk
from ..theme.win95_palette import WIN95

class NavBar(tk.Frame):
    def __init__(self, parent, on_nav):
        super().__init__(parent, bg=WIN95["bg"], relief="raised", borderwidth=2)
        self.pack(fill="x")

        items = [
            ("home", "home"),
            ("search", "search"),
            ("edit/del", "edit"),
            ("stats", "stats"),
            ("AI", "ai"),
            ("settings", "settings"),
            ("mail", "mail"),
            ("about", "about")
        ]
        for label, key in items:
            tk.Button(self, text=label, relief="raised", bg=WIN95["btn_face"],
                      command=lambda k=key: on_nav(k)).pack(side="left", padx=4, pady=4)
