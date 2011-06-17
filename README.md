# Litch.in PyGtk client

This project is a GTK client written in Python for [Litch.in](http://litch.in) project.

## What is Litch.in ?

Litch.in is a project that allow computer users (PC/MAC) to select partial, window or whole screen and automatically send the screenshot to the Litch.in servers.

A small url is then saved in the clipboard for sharing with who you wants.

The clients are located in the sys tray and can be called any time.

## What is required

 * Python (of course)
 * GTK
 * PyNotify
 * [ImageMagick](http://www.imagemagick.org)

## Tested?

Yup, but so far, only on Fedora 15 with Gnome 3.
A weird bug is present when selecting an area : ImageMagick, sometimes, select the wrong desktop :/

## So, it only works for Gnome now?

This code, yes, but other clients, for other linux desktops, Windows, Mac are or will be written any time soon :)

## Note:

It's my first attempt at using GTK so please excuse me for all the horrible stuff we wrote,
and feel free to report bugs or awfully coded parts ;)
