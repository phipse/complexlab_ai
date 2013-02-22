#!/usr/bin/env python
"""Module containing conditions for feature discovery

(c) Peter Schwede, Philipp Eppelt, Marius Melzer

"""

import sys
import glob
import inspect
import logging
from os.path import join, basename


def __has_parent(class_, parent):
    if class_ == parent:
        return True
    for c in class_.__bases__:
        if __has_parent(c, parent):
            return True
    return False

def get_all(directory, whitelist=["mask"]):
    # TODO make this work somehow
    masks = list()

    sys.path.append(directory)
    logging.debug(directory)

    mask = __import__("mask")
    mask_classes = inspect.getmembers(mask, inspect.isclass)
    Mask = dict(mask_classes)["Mask"]

    for rel_path in glob.glob(join(directory, "*.py")):
        logging.debug(rel_path)
        name = basename(rel_path)[:-3]
        logging.debug("%s %s", name, whitelist)
        if "__" in name or name not in whitelist:
            logging.debug("ignored %s", name)
            pass
        else:
            logging.debug("importing %s", name)
            m = __import__(name)
            for name, class_ in inspect.getmembers(m, inspect.isclass):
                logging.debug("%s: %s(%s)", name, class_.__bases__, class_)
                # search for Mask in parent classes
                if __has_parent(class_, Mask) and class_ != Mask:
                    masks.append(class_)

    sys.path.remove(directory)
    logging.debug(masks)
    return masks
