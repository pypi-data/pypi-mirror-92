# -*- coding: utf-8 -*-
#!/usr/bin/python3

"""
Copyright (C) 2020- beucismis

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from .workbench import Tool
from threading import Thread


def main():
    bench = Tool()
    Thread(target=bench.listener_mouse).start()
    Thread(target=bench.listener_keyboard).start()

    try:
        bench.mainloop()
    except SystemExit:
        bench.destroy()
    return 0


if __name__ == "__main__":
    main()
