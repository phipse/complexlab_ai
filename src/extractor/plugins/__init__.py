#!/usr/bin/env python
"""Module containing conditions for feature discovery

(c) Peter Schwede, Philipp Eppelt, Marius Melzer

"""

import sys
import glob
import inspect
import logging
from os.path import join, dirname, basename


def get_all(whitelist=["condition"]):
    # TODO make this work somehow
    plugins = list()
    directory = dirname(__file__)
    sys.path.append(directory)
    logging.debug(directory)
    for rel_path in glob.glob(join(directory, "*.py")):
        name = basename(rel_path)[:-3]
        logging.debug("%s %s", name, whitelist)
        if "__" in name or name not in whitelist:
            logging.debug("ignored %s", name)
            pass
        else:
            logging.debug("importing %s", name)
            for name, class_ in inspect.getmembers(__import__(name),
                                                   inspect.isclass):
                plugins.append(class_)
    sys.path.remove(directory)
    logging.debug(plugins)
    return plugins
