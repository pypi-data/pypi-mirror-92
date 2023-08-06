Prerequisites
---------------

At least one of the following menu launchers need to be installed

- [dmenu](https://tools.suckless.org/dmenu/)
- [bemenu](https://github.com/Cloudef/bemenu)

Else, a *custom* menu may be used by supplying flags as described

pip
------

### Install

Preferred installation method:

```sh
pip install launcher-menus
```

### Update:

```sh
pip install -U launcher-menus
```

### Uninstall:

You may have to do this multiple times until a warning message informs:

<span style="background-color: black; color: yellow;">WARNING: Skipping launcher-menus as it is not installed.</span>

```sh
pip uninstall -y launcher-menus
```

[pspman](https://github.com/pradyparanjpe/pspman)
-------------------------------------------------

### Install:
For automated management: pre-release updates, etc.

**Caution**: PSPMan is unstable and under testing.

```sh
pspman -s -i https://github.com/pradyparanjpe/launcher-menus.git
```

### Update:

```sh
pspman
```

That's it.

### Uninstall:

Remove installation: TODO: Include this in future PSPMan releases

```sh
pip uninstall -y launcher-menus
```

Remove repository clone

```sh
pspman -s -d launcher-menus
```
