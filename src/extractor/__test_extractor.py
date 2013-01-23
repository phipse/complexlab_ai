#!/usr/bin/env python

import os
import sys
import pprint
import logging
import argparse
import datetime  # eval() will use it
import unittest

from extractor import Extractor


class TestExtractor(unittest.TestCase):
    data = list()

    def setUp(self):
        with open(args.datafile, "r") as f:
            self.data = eval("".join(f.readlines()))
            logging.debug(self.data)

    def test_cond(self):
        from classifiers import Classifier
        e = Extractor()
        logging.debug(e)
        e.add_feature_condition(Classifier)
        res = e.extract(self.data)
        self.assertTrue(len(res[self.data.keys()[0]]) > 0)

    def test_monotony(self):
        from classifiers import monotony
        e = Extractor()
        logging.debug(e)
        e.add_feature_condition(monotony.Raising)
        e.add_feature_condition(monotony.Falling)
        res = e.extract(self.data)
        logging.debug("res: \n%s", pprint.pformat(res))
        self.assertTrue(len(res[self.data.keys()[0]]) > 0)


if __name__ == "__main__":
    app = argparse.ArgumentParser(description="General testings of Extractor")
    app.add_argument("datafile",
                     help="evaluable python file containing a data dict")
    app.add_argument("-d", "--debug", action="store_true")
    app.add_argument("unittest_args", nargs="*")
    args = app.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    path = os.path.realpath(os.path.dirname(__file__))
    logging.debug(path)
    args.datafile = os.path.join(path, args.datafile)

    sys.argv[1:] = args.unittest_args
    unittest.main()
