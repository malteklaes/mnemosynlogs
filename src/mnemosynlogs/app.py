import tkinter as tk
from .gui.theme.styles import apply_win95_style
from .gui.widgets.titlebar import TitleBar
from .gui.widgets.navbar import NavBar
from .gui.controllers.navigation_controller import NavigationController
from .gui.theme.win95_palette import WIN95

class MnemoSynLogsApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MnemoSynLogs")
        apply_win95_style(self.root)

        TitleBar(self.root, title="MnemoSynLogs")

        # Header-Navigation
        NavBar(self.root, on_nav=self._navigate)

        # Container für Views
        self.container = tk.Frame(self.root, bg=WIN95["bg"])
        self.container.pack(fill="both", expand=True)

        # Footer (App-Status/Version)
        footer = tk.Frame(self.root, bg=WIN95["bg"], relief="sunken", borderwidth=2)
        footer.pack(side="bottom", fill="x")
        tk.Label(footer, text="MnemoSynLogs [v1.4.0]", bg=WIN95["bg"]).pack(side="left", padx=6, pady=2)

        self.nav = NavigationController(self.container)

    def _navigate(self, view_key: str):
        self.nav.show(view_key)

    def run(self):
        self.root.mainloop()
