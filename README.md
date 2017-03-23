# Swytcher

> A small program that listens to X events and changes your keyboard layout.

Use setxkbmap to configure your different keyboard layouts.

E.g.,

```bash
setxkbmap -option ''  # clear previous options
setxkbmap \
	-option grp:shifts_toggle \  # toggle layout by lshift+rshift
	-option grp_led:caps \  # caps led indicates secondary layout
	-option caps:escape \  # map caps to escape
	se,us  # set US layout as primary, Swedish as secondary
```

## TODO

* Add tests

* Create setup.py

* Private repo on bitbucket? ☑

* Use config-file

* Finish README.md

* Publish on Github

* Publish to PyPi

* When finished, add my program to
  http://unix.stackexchange.com/questions/12072/how-do-i-get-current-keyboard-layout#

* Debian package?

More functionality:

* Executable to toggle layout
* Remember layout for windows
    * Should be easy to implement using the default fallback
