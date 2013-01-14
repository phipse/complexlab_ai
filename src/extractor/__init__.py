#!/usr/bin/env python
"""Module with everything you need for feature extraction

(c) Peter Schwede, Philipp Eppelt, Marius Melzer

"""


import glob

__all__ = filter(lambda x: "__" not in x, glob.glob("*.py"))
