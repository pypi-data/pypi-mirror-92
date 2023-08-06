# -*- coding: utf-8 -*-

import tkinter as tk
from .about import About
from threading import Thread
from pynput import mouse, keyboard
from os import path, name as os_name


if os_name == "posix":
    import gi

    gi.require_version("Gdk", "3.0")
    from gi.repository import Gdk
else:
    raise OSError(f"Unsported OS: {os_name}")

this_dir, this_filename = path.split(__file__)


class Tool(tk.Tk):
    def __init__(self):
        super().__init__()
        self._init_window()

    def _init_window(self) -> None:
        self.overrideredirect(True)

        self.icon = tk.PhotoImage(
            file=f"{this_dir}/assets/tkpick.gif"
        ).subsample(5, 5)

        # window width / window height
        self.ww, self.wh = 60, 20
        # window x / window y
        self.wx, self.wy = 10, 20

        self.sw = self.winfo_screenwidth()
        self.sh = self.winfo_screenheight()

        self.label = tk.Label()
        self.label.config(relief=tk.SUNKEN, border=2)
        self.label.pack(fill=tk.BOTH, expand=1)

    def on_move(self, x, y):
        if x + self.wx + self.ww > self.sw:
            self.geometry(f"{self.ww}x{self.wh}+{x-self.ww}+{y+self.wy}")
        elif y + self.wy + self.wh > self.sh:
            self.geometry(f"{self.ww}x{self.wh}+{x+self.wx}+{y-self.wy}")
        else:
            self.geometry(f"{self.ww}x{self.wh}+{x+self.wx}+{y+self.wy}")

        self.color = self.pixel_at(x, y)
        self.label.config(text=self.color, bg=self.color)

    def _set_label_fg_color(self, r, g, b) -> None:
        if max(r, g, b) > 127:
            self.label.config(fg="#000000")
        else:
            self.label.config(fg="#FFFFFF")

    def pixel_at(self, x, y):
        # https://stackoverflow.com/a/27406714/12418109
        w = Gdk.get_default_root_window()
        pb = Gdk.pixbuf_get_from_window(w, x, y, 1, 1)

        r, g, b = pb.get_pixels()
        self._set_label_fg_color(r, g, b)

        # RGB to HEX
        return "#{:02x}{:02x}{:02x}".format(r, g, b)

    def listener_mouse(self):
        with mouse.Listener(on_move=self.on_move) as l:
            l.join()

        listener = mouse.Listener(on_move=self.on_move)
        listener.start()

    def listener_keyboard(self):
        with keyboard.GlobalHotKeys(
            {
                "<shift>+c": self.copy,
                "<shift>+a": self.about,
                "<shift>+q": self.quit,
            }
        ) as h:
            h.join()

    def copy(self):
        self.clipboard_clear()
        self.clipboard_append(self.color)

    def about(self):
        About()._init_window(self.icon)

    def quit(self):
        self.after(0, self.destroy)  # fix the main thread problem
