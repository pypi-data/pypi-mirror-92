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
   title_background:
   title_foreground:
   normal_background:
   normal_foreground:
   filter_background:
   filter_foreground:
   high_background:
   high_foreground:
   scroll_background:
   scroll_foreground:
   selected_background:
   selected_foreground:
   windowid:
