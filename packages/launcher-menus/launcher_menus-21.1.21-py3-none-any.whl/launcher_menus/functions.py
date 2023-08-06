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
menu function
'''

import re
import typing
import pathlib
import subprocess
import warnings
import yaml
from . import MENUS
from .errors import FlagNameNotFoundError, CommandError, UsageError


def process_comm(cmd: list, pipe_inputs: str = '',
                 timeout: float = None, **kwargs) -> str:
    '''
    Args:
        cmd: list form of commands to be passed to Popen as args
        pipe_inputs: inputs to be passed as stdin
        timeout: timeout of communication in seconds
        **kwargs: passed to Popen

    Raises:
        UsageError: Command usage error
        CommandError: can't open process/ stderr from process

    Return
        stdout: str: returned by process

    '''
    try:
        proc = subprocess.Popen(
            cmd,
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            **kwargs
            )
    except OSError as err:
        raise CommandError(cmd, err) from err

    stdout, stderr = proc.communicate(input=pipe_inputs, timeout=timeout)
    if stderr:
        if re.match('usage', stderr, re.I):
            raise UsageError(cmd, stderr)
        raise CommandError(cmd, stderr)
    return stdout.rstrip('\n')


def menu(opts: typing.List[str] = None, command: str = None,
         config_yml: str = None, **flags) -> str:
    '''
    Call <command> menu to collect interactive information.

    Args:
        opts: list: options to be offerred by menu.
        command: command to use {dmenu,bemenu,<custom>}
        bottom: bool: show bar at bottom
        grab: bool: show menu before reading stdin (faster)
        ignorecase: bool: match items ignoring case
        wrap: bool: wrap cursor selection (only for bemenu)
        ifne: bool: display only if opts (bemenu)
        nooverlap: bool: do not overlap panels (bemenu w/ wayland)
        lines: int: list opts on vertical 'lines'
        monitor: int: show menu on (bemenu w/ wayland: -1: all)
        height: int: height of each menu line (bemenu)
        index: int: select index automatically (bemenu)
        prompt: str: prompt string of menu
        prefix: str: prefix added highlighted item (bemenu)
        scrollbar: str: display scrollbar [none, always, autohide] (bemenu)
        font: str: font to be used format: "FONT-NAME [SIZE (bemenu)]"
        title_background: str: #RRGGBB title background color (bemenu)
        title_foreground: str:  #RRGGBB title foreground color (bemenu)
        normal_background: str: #RRGGBB normal background color
        normal_foreground: str: #RRGGBB normal foreground color
        filter_background: str: #RRGGBB filter background color (bemenu)
        filter_foreground: str: #RRGGBB filter foreground color (bemenu)
        high_background: str: #RRGGBB highlight background color (bemenu)
        high_foreground: str: #RRGGBB highlight foreground color (bemenu)
        scroll_background: str: #RRGGBB scrollbar background color (bemenu)
        scroll_foreground: str: #RRGGBB scrollbar foreground color (bemenu)
        selected_background: str: #RRGGBB selected background color
        selected_foreground: str: #RRGGBB selected foreground color
        windowid: str: embed into windowid (dmenu)
        config_yml: path of yaml config file. Extends and overrides default.
        **flags: action='--flag' for ``command``. Extends and overrides config.

    Raises:
        CommandError
        UsageError
        FlagNameNotFoundError
        ValueError: bad scrollbar options

    Returns:
        User's selected or overridden-entered opt from ``opts`` else None [Esc]

    '''
    bool_kwargs: typing.Dict[str, bool] = {
        'bottom': None,
        'grab': None,
        'ignorecase': None,
        'wrap': None,
        'ifne': None,
        'nooverlap': None,
    }

    input_kwargs: typing.Dict[str, str] = {
        'lines': None,
        'monitor': None,  # may be str, doesn't harm
        'height': None,
        'index': None,
        'prompt': None,
        'prefix': None,
        'scrollbar': None,
        'font': None,
        'title_background': None,
        'title_foreground': None,
        'normal_background': None,
        'normal_foreground': None,
        'filter_background': None,
        'filter_foreground': None,
        'high_background': None,
        'high_foreground': None,
        'scroll_background': None,
        'scroll_foreground': None,
        'selected_background': None,
        'selected_foreground': None,
        'windowid': None,
    }

    # parse bool_kwargs
    for key in bool_kwargs:
        if key in flags:
            bool_kwargs[key] = flags[key]
            del flags[key]

    # parse input_kwargs
    for key in input_kwargs:
        if key in flags:
            input_kwargs[key] = flags[key]
            del flags[key]

    # Default command
    if command is None:
        command = list(MENUS.keys())[0]

    flag_name = MENUS.get(command) or {}

    # Override default config by supplied config
    if config_yml is not None and pathlib.Path(config_yml).exists():
        with open(config_yml, 'r') as yml_handle:
            flag_name.update(yaml.safe_load(yml_handle))
            # NEXT: in python3.9, the following
            # flag_name |= yaml.safe_load(yml_handle)

    # Override config by supplied flags
    flag_name.update(flags)
    # NEXT: in python3.9, the following
    # flag_name |= flags

    # still empty?
    if not flag_name:
        warnings.warn('No flags found in config nor supplied')

    cmd = [command]

    try:

        # boolean flags
        for key, value in bool_kwargs.items():
            if value is not None:
                cmd.append(flag_name[key])

        # input flags
        for key, value in input_kwargs.items():
            if value is not None:
                if key == 'scrollbar' and value not in ['none',
                                                        'always', 'autohide']:
                    raise ValueError(
                        f"""
                        scrollbar should be in ['none', 'always', 'autohide'],
                        got {value}
                        """
                    )
                cmd.extend((flag_name[key], str(value)))

    except KeyError as err:
        raise FlagNameNotFoundError(command, err.args[0]) from err

    if opts is None:
        opts = []
    return process_comm(cmd, pipe_inputs='\n'.join(opts)) or None
