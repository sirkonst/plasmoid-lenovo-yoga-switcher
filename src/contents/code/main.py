# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
from functools import partial
import subprocess

from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

from PyQt4.QtCore import Qt
from PyQt4 import QtGui
# ------------------------------------------------------------------------------
TOUCHPAD = "SynPS/2 Synaptics TouchPad"
TRACKPOINT = "TPPS/2 IBM TrackPoint"
TOUCHSCREEN = "ELAN Touchscreen"
WACOMPEN = "Wacom ISDv4 EC Pen"
# ------------------------------------------------------------------------------


def run(*args):
    return subprocess.call(list(args))

xinput = partial(run, "xinput")
xrandr = partial(run, "xrandr")
# ------------------------------------------------------------------------------


class YogaModesPlasmoid(plasmascript.Applet):

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        self.setHasConfigurationInterface(False)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)

        # -- widgets
        self.icon_laptop = Plasma.IconWidget(
            QtGui.QIcon(
                self.package().path() + "contents/images/mode-laptop.png"),
            "", self.applet
        )
        self.icon_stand = Plasma.IconWidget(
            QtGui.QIcon(
                self.package().path() + "contents/images/mode-stand.png"),
            "", self.applet
        )
        self.icon_tablet = Plasma.IconWidget(
            QtGui.QIcon(
                self.package().path() + "contents/images/mode-tablet.png"),
            "", self.applet
        )
        self.icon_tend = Plasma.IconWidget(
            QtGui.QIcon(
                self.package().path() + "contents/images/mode-tend.png"),
            "", self.applet
        )
        self.target = Plasma.ItemBackground(self.applet)

        # -- some logic
        self.icon_laptop.clicked.connect(self.set_laptop_mode)
        self.icon_stand.clicked.connect(self.set_stand_mode)
        self.icon_tablet.clicked.connect(self.set_tablet_mode)
        self.icon_tend.clicked.connect(self.set_tend_mode)

        # -- layoyt
        layout = QtGui.QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        layout.addItem(self.icon_laptop)
        layout.addItem(self.icon_stand)
        layout.addItem(self.icon_tablet)
        layout.addItem(self.icon_tend)

        self.applet.setLayout(layout)

        self.set_laptop_mode()

    def set_laptop_mode(self):
        self.target.setTargetItem(self.icon_laptop)
        xinput("enable", TOUCHPAD)
        xinput("enable", TRACKPOINT)
        xrandr("--screen", "0", "-o", "normal")
        xinput("set-prop", TOUCHSCREEN, "Evdev Axis Inversion", "0,", "0")
        xinput("set-prop", WACOMPEN, "Wacom Rotation", "0")

    def set_tablet_mode(self):
        self.target.setTargetItem(self.icon_tablet)
        xinput("disable", TOUCHPAD)
        xinput("disable", TRACKPOINT)
        xrandr("--screen", "0", "-o", "normal")
        xinput("set-prop", TOUCHSCREEN, "Evdev Axis Inversion", "0,", "0")
        xinput("set-prop", WACOMPEN, "Wacom Rotation", "0")

    def set_stand_mode(self):
        self.target.setTargetItem(self.icon_stand)
        xinput("disable", TOUCHPAD)
        xinput("disable", TRACKPOINT)
        xrandr("--screen", "0", "-o", "normal")
        xinput("set-prop", TOUCHSCREEN, "Evdev Axis Inversion", "0,", "0")
        xinput("set-prop", WACOMPEN, "Wacom Rotation", "0")

    def set_tend_mode(self):
        self.target.setTargetItem(self.icon_tend)
        xinput("disable", TOUCHPAD)
        xinput("disable", TRACKPOINT)
        xrandr("--screen", "0", "-o", "inverted")
        xinput("set-prop", TOUCHSCREEN, "Evdev Axis Inversion", "1,", "1")
        xinput("set-prop", WACOMPEN, "Wacom Rotation", "3")


def CreateApplet(parent):
    return YogaModesPlasmoid(parent)