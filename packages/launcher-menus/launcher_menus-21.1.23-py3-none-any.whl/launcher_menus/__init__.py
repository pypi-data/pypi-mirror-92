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


import os
import typing
import subprocess
from .read_config import flag_names_from_file


def check_installations() -> typing.Dict[str, dict]:
    '''
    check available installations:
    fetch <menu>.yml configurations [bemenu, dmenu],
    look for system-executable <menu>

    Returns:
        {<menu>: configuration} for menus available in system & yaml.

    Raises:
        FileNotFoundError: no launcher menus could be located

    '''
    known_menus = flag_names_from_file()
    avail_menus: typing.Dict[str, dict] = {}
    for menu_cmd, flags in known_menus.items():
        if os.environ.get("READTHEDOCS"):
            # RTD virutal environment
            return avail_menus
        if not subprocess.call(['command', '-v', menu_cmd],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL):
            # call didn't return an exit-code
            avail_menus[menu_cmd] = flags

    if not avail_menus:
        print('Please install at least one of:')
        for menu_cmd in known_menus.keys():
            print(menu_cmd)
        raise FileNotFoundError('no usable menu launchers were found')
    return avail_menus


MENUS: typing.Dict[str, dict] = check_installations()
'''
Configuration for menus known and found to be installed
'''


from .errors import FlagNameNotFoundError, MenuError, CommandError, UsageError
from .functions import LauncherMenu

menu = LauncherMenu()
'''
Plain ``menu`` object.

``command`` defaults to the first one found to be installed.
'''

__all__ = [
    'LauncherMenu',
    'menu',
    'MenuError',
    'CommandError',
    'UsageError',
    'FlagNameNotFoundError',
    'MENUS'
]

__version__ = '21.1.23'
