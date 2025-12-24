import tkinter as tk
from ..theme.win95_palette import WIN95

class Toolbar(tk.Frame):
    def __init__(self, parent, buttons):
        """
        buttons: List[Tuple[text, command]]
        """
        super().__init__(parent, bg=WIN95["bg"])
        # 90er: Buttons mit raised Relief und minimalem Spacing
        for text, cmd in buttons:
            b = tk.Button(self, text=text, relief="raised", bg=WIN95["btn_face"], command=cmd)
            b.pack(side="left", padx=3, pady=3)
