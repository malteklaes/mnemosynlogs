import tkinter as tk

class MailView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Mail (in Arbeit) – SMTP/Export/Share.").pack(padx=12, pady=12, anchor="w")
