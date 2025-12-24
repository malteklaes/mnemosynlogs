import tkinter as tk

class SettingsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Settings – Farbschema, Standard-Log, Speicherpfad (in Arbeit).").pack(padx=12, pady=12, anchor="w")
