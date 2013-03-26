#!/usr/bin/env python
"""Module containing conditions for feature discovery

(c) Peter Schwede, Philipp Eppelt, Marius Melzer

"""

import os
import glob

__all__ = [ os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__)+"/*.py") if not os.path.basename(f).startswith('__')] # import all masks, from outside: from extractor.masks import * - TODO make this better! ;-)

import sys
import glob
import inspect
import logging
from os.path import join, basename, realpath, dirname

THISDIR = dirname(realpath(__file__))

def __has_parent(class_, parent):
    if class_ == parent:
        return True
    for c in class_.__bases__:
        if __has_parent(c, parent):
            return True
    return False

def available_mask_packages(directory=THISDIR):
    """returns list of mask package names"""
    result = list()
    for rel_path in glob.glob(join(directory, "*.py")):
        result.append(basename(rel_path)[.-3])
    return result

def get_all_masks(whitelist=["mask"], directory=THISDIR):
    """import all feature masks and return a list"""
    masks = list()

    logging.debug(directory)
    sys.path.append(directory)

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
