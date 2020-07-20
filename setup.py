#!/usr/bin/env python

from setuptools import setup

setup(name             = "pystdlib",
      version          = "unstable",
      author           = "Alex Ermolov",
      url              = "https://github.com/wiedzmin/pystdlib",
      description      = "Standard library for workplace python scripts",
      packages         = ["pystdlib", "pystdlib.passutils", "pystdlib.uishim", "pystdlib.xlib"],
      license          = "GPL",
      install_requires = ["python-xlib", "dmenu", "pyfzf", "notify2"]
)
