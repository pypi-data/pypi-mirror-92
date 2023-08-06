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
Menu object and function
'''

import re
import typing
import pathlib
import subprocess
import warnings
import yaml
from . import MENUS
from .errors import FlagNameNotFoundError, CommandError, UsageError


def arg2flag(arg: str) -> typing.List[str]:
    '''
    Convert argument to flag

    Args:
       arg: Convert this argument to possible flag

    Returns:
        A list of possible flags generated from ``arg``

    '''
    flags = []
    # arg is of the type flag_name
    flags.append("--" + arg)  # --flag_name
    flags.append("--" + arg.replace("_", "-"))  # --flag-name
    flags.append("-" + arg[0])  # -f  ``THIS MAY BE AMBIGUOUS``
    return flags


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
    try: proc = subprocess.Popen(
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


class LauncherMenu():
    '''
    Launcher Menu wrapper object with pre-defined menu options.

    Args:
        opts: list: options to be offerred by menu.
        command: command to use {dmenu,bemenu,<custom>}
        flag_names: dict providing action: flags or path to cognate yaml.
        fail: 'warn': warn, 'fail': error, 'guess': try creating, else warn
        **kwargs: default values for ``kwargs`` of ``menu``

    Attributes:
        opts: default options to be offerred
        command: default menu command to run
        flag_names: dictionary of {actions: flag_names}
        fail: default failure behaviour

    Raises:
        TypeError
        FlagNameNotFoundError

    '''
    def __init__(self,
                 opts: typing.List[str] = None,
                 command: str = None,
                 flag_names: typing.Union[pathlib.Path, str, dict] = None,
                 fail: str = 'warn',
                 **kwargs) -> None:
        self.opts = opts
        self.command = command
        self.flag_names = self._read_flag_names(flag_names)
        # ``flag_names`` has two dicts: bool, input
        # bool flags are only 'flagged' in command line
        # input flags demand an accompanying input value
        self.fail = fail
        # Categorise
        self.flag_names = self._categorize_flags(self.flag_names)
        self.kwargs = kwargs

    def __call__(self,
                 opts: typing.List[str] = None, command: str = None,
                 flag_names: typing.Union[pathlib.Path, str, dict] = None,
                 fail: str = 'warn',
                 **kwargs) -> str:
        '''
        Call <command> menu to collect interactive information.

        Args:
            opts: list: options to be offerred by menu.
            command: command to use {dmenu,bemenu,<custom>}
            flag_names: dict providing action: flags or path to cognate yaml.
            fail: 'warn': warn, 'fail': error, 'guess': try creating, else warn
            kwargs: flag to be called at command line:

                - bottom = ``bool``: show bar at bottom
                - grab = ``bool``: show menu before reading stdin (faster)
                - ignorecase = ``bool``: match items ignoring case
                - wrap = ``bool``: wrap cursor selection
                - ifne = ``bool``: display only if opts
                - nooverlap = ``bool``: do not overlap panels
                - lines = ``int``: list opts on vertical 'lines'
                - monitor = ``int``: show menu on (bemenu w/ wayland: -1: all)
                - height = ``int``: height of each menu line
                - index = ``int``: select index automatically
                - prompt = ``str``: prompt string of menu
                - prefix = ``str``: prefix added highlighted item
                - scrollbar = ``str``: display scrollbar {none,always,autohide}
                - font = ``str``: font to be used format: "FONT-NAME [SIZE ]"
                - title_background = ``str``: title background color
                - title_foreground = ``str``: title foreground color
                - normal_background = ``str``: normal background color
                - normal_foreground = ``str``: normal foreground color
                - filter_background = ``str``: filter background color
                - filter_foreground = ``str``: filter foreground color
                - high_background = ``str``: highlight background color
                - high_foreground = ``str``: highlight foreground color
                - scroll_background = ``str``: scrollbar background color
                - scroll_foreground = ``str``: scrollbar foreground color
                - selected_background = ``str``: selected background color
                - selected_foreground = ``str``: selected foreground color
                - windowid = ``str``: embed into windowid

        Raises:
            CommandError
            UsageError
            FlagNameNotFoundError
            ValueError: bad scrollbar options

        Returns:
            User's selected opt from ``opts`` or overridden-entered choice
            else ``None`` [Esc]

        '''
        return self._menu(opts=opts, command=command,
                          flag_names=flag_names, fail=fail, **kwargs)

    def _menu(self,
              opts: typing.List[str] = None, command: str = None,
              flag_names: typing.Union[pathlib.Path, str, dict] = None,
              fail: str = 'warn',
              **kwargs) -> str:
        '''
        Call menu

        '''
        # Command
        command = command or self.command or list(MENUS.keys())[0]

        # Flags
        empty_flags = {'bool': {}, 'input': {}}
        flag_names = self._read_flag_names(flag_names)
        for key, value in flag_names.items():
            flag_names[key] = {**self.flag_names[key],
                               **MENUS.get(command, empty_flags)[key],
                               **value}

        # Similarly, called options:
        kwargs = {**self.kwargs, **kwargs}
        cmd = [command]

        # boolean flags
        for key, value in flag_names['bool'].items():
            if value is not None and key in kwargs and kwargs[key]:
                try:
                    cmd.append(value)
                except KeyError as err:
                    if fail == 'fail':
                        raise FlagNameNotFoundError(
                            command, err.args[0]
                        ) from err
                    else:
                        warnings.warn('''
                        flag name for '{key}' of {command} was not found
                        but not failing
                        ''')
                        if fail == 'guess':
                            cmd.append(arg2flag(key))

        # input flags
        for key, value in flag_names['input'].items():
            if value is not None and key in kwargs:
                if key == 'scrollbar' and value not in ['none',
                                                        'always', 'autohide']:
                    raise ValueError(
                        f"""
                        scrollbar should be in ['none', 'always', 'autohide'],
                        got {value}
                        """
                    )
                try:
                    cmd.extend((value, str(kwargs[key])))
                except KeyError as err:
                    if fail:
                        raise FlagNameNotFoundError(
                            command, err.args[0]
                        ) from err
                    else:
                        warnings.warn('''
                        flag name for '{key}' of {command} was not found
                        but not failing
                        ''')
                        if fail == 'guess':
                            cmd.extend((arg2flag(key), str(value)))
        # unrecognozed flags
        if opts is None:
            opts = []
        opts = [str(choice) for choice in opts]
        return process_comm(cmd, pipe_inputs='\n'.join(opts)) or None

    @staticmethod
    def _read_flag_names(
            flag_names: typing.Union[pathlib.Path, str, dict],
    ) -> typing.Dict[str, dict]:
        '''
        Interpret type of flag_names

        Args:
            flag_names: either a yml file or directly a dict

        Raises:
            FileNotFoundError
        '''
        if isinstance(flag_names, dict):
            return flag_names
        if flag_names is None:
            return {'bool': {}, 'input': {}}
        if isinstance(flag_names, str):
            flag_path = pathlib.Path(flag_names)
        elif isinstance(flag_names, pathlib.Path):
            flag_path = flag_names
        else:
            raise TypeError('''flag_names should be either of
            str, Path, or dict
            ''')
        if flag_path.exists():
            with open(flag_path, 'r') as yml_handle:
                return yaml.safe_load(yml_handle)
        raise FileNotFoundError(f"{str(flag_names)} couldn't be located")

    @staticmethod
    def _categorize_flags(
            flag_names: typing.Dict[str, dict]
    ) -> typing.Dict[str, dict]:
        '''
        Classify flags into bool, input.
        If flag is unrecognized, classify based on its value

        Args:
            flag_names: dictionary to be updated with ``flags``
            a yaml representation of the structure is below
            TODO: create a class structure

              flag_names:

                input:

                  act 1: --flag-one
                  act 2: --flag-two
                  act 3: --flag-three

                bool:

                  act 4: --flag-four
                  act 5: --flag-five

        Returns:
            flag_names:
                with keys 'input', 'bool'
                with values: dictionaries, each containing
                'action' : 'flag' pairs
        '''

        # Don't mess up the referrence
        # deep copy
        altered_flag_names = {}
        altered_flag_names['bool'] = flag_names['bool'].copy()
        altered_flag_names['input'] = flag_names['input'].copy()
        for key, value in flag_names.items():
            if key not in ('bool', 'input'):
                # This flag is unrecognized
                # try to guess its type
                if isinstance(value, bool):
                    altered_flag_names['bool'][key] = value
                else:
                    altered_flag_names['input'][key] = value
        return altered_flag_names
