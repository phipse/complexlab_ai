#!/usr/bin/env python

import os
import sys
import pprint
import logging
import argparse
import datetime
import unittest
from itertools import imap, izip

import condition


class extractor(object):
    """extracts features from datasets"""
    def __init__(self):
        self.__available_conditions = list()
        self.__running_conditions = list()

    def add_feature_condition(self, ft):
        """adds a feature condition to it's collection"""
        self.__available_conditions.append(ft)

    def __max_time_resolution(self, data):
        res = None
        sorted_keys = sorted(data.keys())
        old_t = sorted_keys[-1]
        for t in sorted_keys:
            if res is None:
                res = t - old_t
            else:
                res = min(res, t - old_t)
            old_t = t
        return res

    def __resample(self, data, resolution):
        res = dict()
        return res

    def __may_start(self, this):
        for other in self.__running_conditions:
            if other.name == this.name and not this.can_overlay:
                return False
        return True

    def extract(self, data_dict):
        """extracts features from data dictionary"""
        res = dict()
        for ID, data in data_dict.items():
            #resolution = self.__max_time_resolution(data)
            #resampled = self.__resample(data, resolution)
            logging.debug("ID: %s", ID)
            sorted_times = sorted(data.keys())
            # iterate over all time, value pairs
            for t, v in izip(sorted_times, imap(lambda k: data[k], sorted_times)):
                # check whether started conditions ended and store them as features
                for cond in self.__running_conditions:
                    if cond.end(t, v):
                        self.__running_conditions.remove(cond)

                        feat = cond.make_feature()
                        try:
                            res[ID].append(feat)
                        except KeyError:
                            res[ID] = [feat]
                    else:
                        # cond probably needs a step callback
                        cond.next(t, v)

                # generate new conditions
                for cond_gen in self.__available_conditions:
                    new_cond = cond_gen()
                    if new_cond.start(t, v) and self.__may_start(new_cond):
                        self.__running_conditions.append(new_cond)
        return res

    def __repr__(self):
        return "<Extractor conditions=%s>" % (str(self.__available_conditions),)


class TestExtractor(unittest.TestCase):
    data = list()

    def setUp(self):
        with open(args.datafile, "r") as f:
            self.data = eval("".join(f.readlines()))

    def test_cond(self):
        e = extractor()
        logging.debug(e)
        e.add_feature_condition(condition.dummy_condition)
        res = e.extract(self.data)
        self.assertTrue(len(res[self.data.keys()[0]]) > 0)

    def test_monotony(self):
        import monotony
        e = extractor()
        logging.debug(e)
        e.add_feature_condition(monotony.raising)
        e.add_feature_condition(monotony.falling)
        res = e.extract(self.data)
        logging.debug("res: \n%s", pprint.pformat(res))
        self.assertTrue(len(res[self.data.keys()[0]]) > 0)


if __name__ == "__main__":
    app = argparse.ArgumentParser(description="General testings of Extractor")
    app.add_argument("datafile",
                     help="evaluable python file containing a data dict")
    app.add_argument("unittest_args", nargs="*")
    app.add_argument("--debug", action="store_true")
    args = app.parse_args()

    level = logging.INFO
    if args.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level)
    logging.debug("bla")

    path = os.path.realpath(os.path.dirname(__file__))
    args.datafile = os.path.join(path, args.datafile)

    sys.argv[1:] = args.unittest_args
    unittest.main()
