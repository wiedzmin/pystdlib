#!/usr/bin/env python

from setuptools import setup

setup(name             = "pystdlib",
      version          = "0.9", # neither unstable, nor 1.0-compliant
      author           = "Alex Ermolov",
      url              = "https://github.com/wiedzmin/pystdlib",
      description      = "Standard library for workplace python scripts",
      packages         = [
          "pystdlib",
          "pystdlib.browser",
          "pystdlib.git",
          "pystdlib.passutils",
          "pystdlib.shell",
          "pystdlib.systemd",
          "pystdlib.uishim",
          "pystdlib.xlib"
      ],
      license          = "GPL",
      install_requires = ["papis-python-rofi", "python-xlib", "pygit2", "dmenu", "pyfzf", "notify2"]
)
