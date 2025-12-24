from tkinter import ttk
import tkinter as tk
from .win95_palette import WIN95

def apply_win95_style(root: tk.Tk):
    # Grundfarbe
    root.configure(bg=WIN95["bg"])
    root.option_add("*Background", WIN95["bg"])
    root.option_add("*foreground", WIN95["text"])
    root.option_add("*Font", "TkDefaultFont 9")

    style = ttk.Style(root)
    style.theme_use("default")

    # Treeview
    style.configure("Treeview",
                    background=WIN95["bg"],
                    fieldbackground=WIN95["bg"],
                    foreground=WIN95["text"],
                    borderwidth=1)
    style.map("Treeview",
              background=[("selected", "#000080")],
              foreground=[("selected", "#ffffff")])

    # Buttons (ttk) – für „Win95“ nutzen wir lieber tk.Button (siehe Widgets)
    style.configure("TButton",
                    background=WIN95["btn_face"],
                    foreground=WIN95["text"],
                    borderwidth=1,
                    padding=4)
    style.map("TButton",
              relief=[("pressed", "sunken"), ("!pressed", "raised")])

    # LabelFrame (Groupbox)
    style.configure("TLabelframe", background=WIN95["bg"], borderwidth=2, relief="groove")
    style.configure("TLabelframe.Label", background=WIN95["bg"], foreground=WIN95["group_text"])

    # Entry
    style.configure("TEntry",
                    fieldbackground=WIN95["entry_bg"],
                    foreground=WIN95["text"])

    # Scrollbar
    style.configure("TScrollbar", background=WIN95["btn_face"])
