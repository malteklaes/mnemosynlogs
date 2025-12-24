import tkinter as tk

class AiView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="AI (in Arbeit) – Analyse/Empfehlungen für Logs.").pack(padx=12, pady=12, anchor="w")
