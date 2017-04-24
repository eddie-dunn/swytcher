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
   \  # set US layout as first, Swedish as second, US intl as third:
   "us,se,us(altgr-intl)"
```

## TODO

* Add tests  ☑
* Create setup.py ☑
* Private repo on bitbucket? ☑
* Add config file ☑
    * Use config-file ☑
* Check that package can be installed ☑
    * Figure out how to include config files in the package ☑
* Publish to PyPi ☑

* Publish on Github
* When finished, add my program to
  http://unix.stackexchange.com/questions/12072/how-do-i-get-current-keyboard-layout#
* Debian package?


## More functionality

* Print window class/title that matched
    * Use regex for matching title?
* Executable to toggle layout
* Remember layout for windows
    * Should be easy to implement using the default fallback
      but I need to get unique window id to check against
    * Save keyboard layout every time. If window id is changed, the layout will
      have been saved; this can be used for lookup later

* Add possibility to run user specified command for window events
  * http://unix.stackexchange.com/questions/256713/how-to-execute-a-command-on-window-focus-unfocus

* Install swytcher with git dependencies
  * http://stackoverflow.com/questions/36544700/how-to-pip-install-a-package-that-has-git-dependencies
  * https://www.reddit.com/r/Python/comments/2crput/how_to_install_with_pip_directly_from_github/?st=j1cbteyf&sh=b969f668

* Update questions:
  * http://unix.stackexchange.com/questions/12072/how-do-i-get-current-keyboard-layout#
  * http://unix.stackexchange.com/questions/78980/how-do-i-change-currently-selected-keyboard-layout-from-command-line?rq=1

* Track time spent in different apps:
    > Ah, what I really miss about time tracking software isn't necessarily
    something where I manually type in what I've been working on, as much as
    it's something like a self-hosted RescueTime[0].  Instead of manually
    adding things to it, it allows you to mark certain applications and
    websites as you doing something productive (for example, if you're running
    Atom and visiting StackOverflow and GitHub, you're probably doing something
    productive) and then tracks that via its clients and shows you a nice
    overview of how much of your time is actually spent on doing something
    productive.  Now, of course, the fact that RescueTime is centralized and
    hasn't released the source code of its clients makes me instantly dismiss
    it as a software I would use, but I would love to find a certain
    self-hosted solution that does pretty much exactly what RescueTime does.
    [0] https://www.rescuetime.com/

    https://news.ycombinator.com/item?id=14182563

<!-- vim: set tabstop=8 expandtab shiftwidth=4 softtabstop=4 : -->
