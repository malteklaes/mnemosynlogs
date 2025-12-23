from tkinter import ttk
from .win95_palette import WIN95

def apply_win95_style(root):
    root.configure(bg=WIN95["bg"])
    style = ttk.Style(root)
    style.theme_use("default")

    # Buttons: flach mit „3D“-Kanten-Effekt über Reliefs
    style.configure("TButton",
                    background=WIN95["btn_face"],
                    foreground=WIN95["text"],
                    borderwidth=1,
                    padding=4)
    style.map("TButton",
              background=[("active", WIN95["btn_highlight"])],
              relief=[("pressed", "sunken"), ("!pressed", "raised")])

    style.configure("Treeview",
                    background=WIN95["bg"],
                    fieldbackground=WIN95["bg"],
                    foreground=WIN95["text"])
    style.configure("TEntry",
                    fieldbackground="#ffffff",
                    foreground=WIN95["text"])
