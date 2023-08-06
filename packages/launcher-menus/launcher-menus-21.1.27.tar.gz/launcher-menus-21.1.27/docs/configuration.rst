Files
-----

|menu|.yml files bear flags corresponding to actions for |menu|,
where |menu| may be dmenu, bemenu, etc

Location:
^^^^^^^^^

``<installation path>/site-packages/launcher_menus/``\ `menu-cfgs <launcher_menus/menu-cfgs>`__


Configuration format
--------------------

Copy `template <launcher_menus/menu-cfgs/template.yml>`__ to
`menu-cfgs <launcher_menus/menu-cfgs>`__/|menu|.yml

.. |menu| replace:: <menu>


Edit fields to provide flags:

-  Example:

   .. code:: yaml

      bottom: -b
      prompt: --prompt

template.yml
^^^^^^^^^^^^

.. code:: yaml

  bool:
    bottom: null
    grab: null
    wrap: null
    ifne: null
    ignorecase: null
    nooverlap: null

  input:
    version: null
    lines: null
    monitor: null
    height: null
    prompt: null
    prefix: null
    index: null
    scrollbar: null
    font: null
    title_background: null
    title_foreground: null
    normal_background: null
    normal_foreground: null
    filter_background: null
    filter_foreground: null
    high_background: null
    high_foreground: null
    scroll_background: null
    scroll_foreground: null
    selected_background: null
    selected_foreground: null
    windowid: null
