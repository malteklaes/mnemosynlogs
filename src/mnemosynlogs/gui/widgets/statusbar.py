import tkinter as tk
from ..theme.win95_palette import WIN95

class StatusBar(tk.Frame):
    def __init__(self, parent, text_var: tk.StringVar):
        super().__init__(parent, bg=WIN95["bg"])
        # Sunken Feld
        box = tk.Label(self, textvariable=text_var, bg=WIN95["bg"], relief="sunken", anchor="w")
        box.pack(fill="x", padx=6, pady=(0, 6))
