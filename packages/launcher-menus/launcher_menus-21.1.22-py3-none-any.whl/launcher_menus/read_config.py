#!/usr/bin/env python3
# -*- coding: utf-8; mode: python -*-
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
Load configurations
'''


import os
import typing
import yaml


def flag_names_from_file() -> typing.Dict[str, dict]:
    '''
    Fish out specific flag names from known config files located in menu-cfg.

    Returns:
        flag_name: command- specific dictionary containing- k: action, v: flag.
        flag_name: empty dictionary if that config file was not found.

    '''
    known_menus: typing.Dict[str, dict] = {}
    cfg_dir = os.path.join(os.path.dirname(__file__), 'menu-cfgs')
    for path, _, filenames in os.walk(cfg_dir):
        # walk through all available flag_name files
        for yml_conf in filenames:
            menu, ext = os.path.splitext(yml_conf)
            if ext.lower() in ('.yml', '.yaml'):
                # {command}.yaml file
                with open(os.path.join(path, yml_conf), 'r') as yml_handle:
                    known_menus[menu.rstrip(".")] = yaml.safe_load(yml_handle)
    return known_menus
