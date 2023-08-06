# -*- coding: utf-8 -*-

import tkinter as tk


__version__ = "1.0.0"
__author__ = "Adil Gurbuz"
__contact__ = "beucismis@tutamail.com"
__source__ = "https://github.com/beucismis/tkpick"
__description__ = "Get pixel color using the cursor"


class About(tk.Toplevel):
    def __init__(self):
        super().__init__()

    def _init_window(self, icon) -> None:
        self.title(type(self).__name__)
        self.resizable(0, 0)
        self.wm_iconphoto(self._w, icon)

        tk.Label(
            self,
            text=f"\ntkpick {__version__}\n{__description__}",
            compound=tk.TOP,
            image=icon,
        ).pack(padx=5, pady=5)

        content = (
            f"Author: {__author__}\n"
            f"Contact: {__contact__}\n\n"
            f"License: GPL-3.0\n"
            f"Source: {__source__}"
        )
        tk.Label(self, text=content, padx=5, pady=5, relief=tk.RIDGE).pack()

        tk.Button(self, text="Close", command=lambda: self.destroy()).pack(
            padx=5, pady=5, side=tk.RIGHT
        )
