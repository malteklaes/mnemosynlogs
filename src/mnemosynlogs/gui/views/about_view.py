import tkinter as tk

class AboutView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        txt = (
            "MnemoSynLogs\n"
            "Version 0.1.0\n\n"
            "CSV-basierte Log-App im 90er-Jahre-Look.\n"
            "Made with Tkinter.\n"
        )
        tk.Label(self, text=txt, justify="left").pack(padx=12, pady=12, anchor="w")