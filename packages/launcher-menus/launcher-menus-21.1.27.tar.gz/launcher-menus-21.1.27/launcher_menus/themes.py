#!/usr/bin/env python3
# -*- coding: utf-8; mode: python; -*-
#
# Copyright 2021 Pradyumna Paranjape
# This file is part of launcher-menus.
#
# launcher-menus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# launcher-menus is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with launcher-menus.  If not, see <https://www.gnu.org/licenses/>.
#


'''
Launcher Menu Themes

'''


from .functions import LauncherMenu


menu = LauncherMenu()
'''
Plain ``menu`` object.

``command`` defaults to the first one found to be installed.
'''


password_prompt = LauncherMenu(
    filter_background="#000000",
    filter_foreground="#000000",
    prompt="Password: "
)
'''
Password prompt menu.
'''


emergency_prompt = LauncherMenu(
    normal_background="#af1f00",
    filter_background="#af1f00",
    selected_background="#50e0ff",
    normal_foreground="#50e0ff",
    filter_foreground="#50e0ff",
    selected_foreground="#af1f00",
    title_background="#000000",
    title_foreground="#ffffff",
)
'''
Emergy prompt menu
'''
