import tkinter as tk
from .gui.theme.styles import apply_win95_style
from .gui.controllers.navigation_controller import NavigationController

class MnemoSynLogsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MnemoSynLogs")
        apply_win95_style(self.root)
        self.nav = NavigationController(self.root)

    def run(self):
        self.root.mainloop()
