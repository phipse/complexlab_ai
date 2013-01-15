#!/usr/bin/env python

import logging
import unittest
from itertools import izip, count

import monotony


class TestMonotony(unittest.TestCase):
    def setUp(self):
        self.foo = [3., 1., 2., 3., 4., 5., 5., 4., 2., 0., 5., 9.]
        self.data = izip(count(), self.foo)

    def test_raising(self):
        stat = list()
        cond = monotony.Raising()
        cond.start(-1, 0)
        old_val = -1
        for idx, val in self.data:
            if cond.end(idx, val):
                self.assertFalse(old_val <= val)
                if not cond.is_stub(idx, val):
                    feat = cond.make_feature()
                    stat.append(feat)
                cond = monotony.Raising()
                cond.start(idx, val)
            else:
                self.assertTrue(old_val <= val)
                cond.next(idx, val)
            old_val = val
        cond.end(idx, val, force=True)
        stat.append(cond.make_feature())
        logging.debug(self.foo)
        logging.debug(stat)
        self.assertTrue(len(stat) == 3)

if __name__ == "__main__":
    FORMAT = "%(levelname)-8s %(module)-8s %(funcName)-8s %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    unittest.main()
