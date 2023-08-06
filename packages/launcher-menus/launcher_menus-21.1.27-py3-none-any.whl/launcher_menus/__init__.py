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
Python API for Launcher menus

'''


from .checks import MENUS
from .functions import LauncherMenu
from .errors import (FlagNameNotFoundError, MenuError,
                     CommandError, UsageError)
from .themes import menu

__all__ = [
    'LauncherMenu',
    'menu',
    'MenuError',
    'CommandError',
    'UsageError',
    'FlagNameNotFoundError',
    'MENUS'
]

__version__ = '21.1.27'
