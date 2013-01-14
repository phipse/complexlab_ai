#!/usr/bin/env python
"""Module containing conditions for feature discovery

(c) Peter Schwede, Philipp Eppelt, Marius Melzer

"""

import imp
import glob
import inspect
from os.path import join, dirname, realpath


def get_all_plugins(without=["condition"]):
    # TODO make this work somehow
    plugins = list()
    for rel_path in glob.glob(join(dirname(__file__), "*.py")):
        name = ".".join(rel_path[len("plugins/"):-3].split("/"))
        path = dirname(realpath(rel_path))
        if "__" in name or name in without:
            print "ignored", name
        else:
            print name, path
            desc = imp.find_module(name, [path])
            plugins += inspect.getmembers(imp.load_module(name, *desc),
                                          inspect.isclass)
    return plugins
