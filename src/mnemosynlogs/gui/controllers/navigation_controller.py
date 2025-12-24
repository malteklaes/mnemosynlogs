import tkinter as tk
from ..views.home_view import HomeView
from mnemosynlogs.gui.views.search_view import SearchView
#from ..views.search_view import SearchView
from ..views.edit_view import EditView
from ..views.stats_view import StatsView
from ..views.ai_view import AiView
from ..views.settings_view import SettingsView
from ..views.mail_view import MailView
from ..views.about_view import AboutView

class NavigationController:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        self.views = {}
        self.show("home")

    def show(self, name: str):
        # einfacher View-Switcher
        for child in self.container.winfo_children():
            child.destroy()
        if name == "home":
            HomeView(self.container).pack(fill="both", expand=True)
        elif name == "search":
            SearchView(self.container).pack(fill="both", expand=True)
        elif name == "edit":
            EditView(self.container).pack(fill="both", expand=True)
        elif name == "stats":
            StatsView(self.container).pack(fill="both", expand=True)
        elif name == "ai":
            AiView(self.container).pack(fill="both", expand=True)
        elif name == "settings":
            SettingsView(self.container).pack(fill="both", expand=True)
        elif name == "mail":
            MailView(self.container).pack(fill="both", expand=True)
        elif name == "about":
            AboutView(self.container).pack(fill="both", expand=True)
