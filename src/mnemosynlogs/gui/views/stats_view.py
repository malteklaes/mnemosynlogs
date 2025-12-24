import tkinter as tk

class StatsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Stats (in Arbeit) – hier kommen Summen/Charts je Tag/Status/Duration.").pack(padx=12, pady=12, anchor="w")
