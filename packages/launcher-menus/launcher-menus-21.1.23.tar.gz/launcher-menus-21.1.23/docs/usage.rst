Call ``<menu>``
---------------

A replacement for input popups.

Call menu launchers [``dmenu``, ``bemenu``, ``<others>``] from python

Import in your script:

.. code:: python


   # import
   from launcher_menus import menu

   user_letter = menu(command='bemenu', opts=['a', 'b', 'c', 'd'])
   if user_letter is not None:
       # user did not hit <Esc>
       print(user_letter)
   else:
       print("Aborted...")

Results:

::

   a


Personalized usage: pre-defined styles

.. code:: python

   # import
   from launcher_menus import LauncherMenu

   mask_color = "#000000"
   password_menu = LauncherMenu(command='bemenu', filter_background=mask_color,
                                filter_foreground=mask_color)
   password = password_menu()
   if password is None:
       # user hit <Esc>
       print("Can't go ahead without password")
   else:
       print(password)  # A bad idea


Results:

::

   Can't go ahead without password
