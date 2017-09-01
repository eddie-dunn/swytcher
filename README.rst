===============================
Swytcher
===============================


.. image:: https://img.shields.io/pypi/v/swytcher.svg
        :target: https://pypi.python.org/pypi/swytcher

.. image:: https://img.shields.io/travis/eddie-dunn/swytcher.svg
        :target: https://travis-ci.org/eddie-dunn/swytcher

.. image:: https://readthedocs.org/projects/swytcher/badge/?version=latest
        :target: https://swytcher.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/eddie-dunn/swytcher/shield.svg
        :target: https://pyup.io/repos/github/eddie-dunn/swytcher/
        :alt: Updates


*Automatically switches your keyboard layout based on your active window.*

Are you using multiple keyboard layouts? Have you discovered that the US
keyboard layout is a lot more suitable for programming than the layout you have
to use when writing email or otherwise communicating in your native language?

Does it annoy you that you need to remember to manually switch between layouts
when going from VIM to your chat/email/whatever app?

If so, Swytcher will solve your problems.


* Free software: MIT license
* Documentation: https://swytcher.readthedocs.io.


Features
--------

* Switch keyboard layout based on X window class
* Switch keyboard layout based on X window name

Planned features

* Add explicit command to copy default config instead of doing this
  automatically
* Switch layout based on combination of window class and name
* Remember last keyboard layout for each window

Installation
------------

.. code-block:: bash

    $ pip install --user swytcher


Usage
-----

Run Swytcher once so that the config file is created (or copy the sample config
from the swytcher package).

.. code-block:: bash

    $ swytcher

Then close the application and edit `~/.config/swytcher/config.ini` and add the
window classes/names to the corresponding layout section.

`layout_primary` maps to your first keyboard layout, and `layout_secondary`
will map to your second. If you have more than two layouts you will have to add
more sections to the config file. Each additional layout section must start
with `layout`, and be uniquely named. The order that they have in the config
file should map to the order that you have defined your different layouts in.

Once you are done editing your config file, you can start Swytcher, and your
keyboard layout will be switched whenever you change focus to a window that
corresponds to a window class and/or name in your config file.

Swytcher has been tested with the Gnome Desktop Environmant and the i3 window
manager. Since Swytcher looks at your X keyboard config it should work with
most DEs and WMs.


Credits
---------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

