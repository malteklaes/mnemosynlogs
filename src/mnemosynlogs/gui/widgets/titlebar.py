import tkinter as tk
from ..theme.win95_palette import WIN95

class TitleBar(tk.Frame):
    def __init__(self, parent, title="MnemoSynLogs", on_close=None, on_minimize=None):
        super().__init__(parent, bg=WIN95["title_bar"])
        self.pack(fill="x")
        self.label = tk.Label(self, text=title, bg=WIN95["title_bar"], fg=WIN95["title_text"])
        self.label.pack(side="left", padx=6, pady=2)

        btn_frame = tk.Frame(self, bg=WIN95["title_bar"])
        btn_frame.pack(side="right")

        # Fake 90er: kleine graue Buttons im Titel
        self.btn_min = tk.Button(btn_frame, text="_", width=3, relief="raised",
                                 bg=WIN95["btn_face"], command=(on_minimize or (lambda: None)))
        self.btn_min.pack(side="left", padx=1, pady=1)

        self.btn_close = tk.Button(btn_frame, text="X", width=3, relief="raised",
                                   bg=WIN95["btn_face"], command=(on_close or (lambda: None)))
        self.btn_close.pack(side="left", padx=1, pady=1)
