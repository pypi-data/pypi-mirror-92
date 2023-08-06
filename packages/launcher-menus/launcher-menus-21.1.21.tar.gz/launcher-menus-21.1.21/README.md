Description
==============

Launcher menu wrapper.

Provides an API for launcher menus such as:
  - [dmenu](https://tools.suckless.org/dmenu/)
  - [bemenu](https://github.com/Cloudef/bemenu)

Can be extended to other menus:
  - Create its \<menu\>.yml config file from template.yml OR
  - Supply flags through ``**flags`` to ``menu`` function.

Documentation
=============

[![Documentation Status](https://readthedocs.org/projects/launcher-menus/badge/?version=latest)](https://launcher-menus.readthedocs.io/?badge=latest)

Installation
============

pip
---

Preferred method `pip install launcher-menus`

[pspman](https://github.com/pradyparanjpe/pspman)
-------------------------------------------------

For automated management: pre-release updates, etc
`pspman -s -i https://github.com/pradyparanjpe/launcher-menus.git`

Uninstallation
==============

pip
---

`pip uninstall -y launcher-menus`

pspman
------

Remove installation `pip uninstall -y launcher-menus`

Remove repository clone `pspman -s -d launcher-menus`

Usage
=====

Call menu
---------

-   Call menu launchers \[dmenu, bemenu, \<others\>\] from python
-   Import in your script

``` {.python tangle="no"}
from launcher_menus import menu as bemenu
user_letter = bemenu(command='bemenu', opts=['a', 'b', 'c', 'd'])
if user_letter is not None:
    # user did not hit <Esc>
    print(user_letter)
```

Results:

``` {.example}
a
```

What does it do
---------------

-   Runs a subprocess for the selected menu and returns its standard
    output or ``None``

Configuration
=============

-   \<menu\>.yml files bear flags corresponding to actions for \<menu\>
-   \<menu\>.yml files are located in
    `<installation path>/site-packages/launcher_menus/`[menu-cfgs](launcher_menus/menu-cfgs)

Configuration format
--------------------

-   Copy [template](launcher_menus/menu-cfgs/template.yml) to [menu-cfgs](launcher_menus/menu-cfgs)``/<menu>.yml``
-   Edit fields to provide flags:
   - Example:
   ``` {.example}
   bottom: -b
   prompt: --prompt
   ```

### template.yml

``` {.yml}
version:
bottom:
grab:
ignorecase:
wrap:
ifne:
nooverlap:
lines:
monitor:
height:
prompt:
prefix:
index:
scrollbar:
font:
title background:
title foreground:
normal background:
normal foreground:
filter background:
filter foreground:
high background:
high foreground:
scroll background:
scroll foreground:
selected background:
selected foreground:
windowid:

```


TODO
====

-   Configure rofi
-   Configure wofi (dead project?)
-   Configure others as issues arise
