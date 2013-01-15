import logging
import unittest

import monotony

class TestMonotony(unittest.TestCase):
    def setUp(self):
        self.data = zip(range(10), range(10))

    def test_raising(self):
        cond = monotony.Raising()
        
        cond.start(0,0)
        for idx, val in self.data:
            cond.next(idx, val)
            logging.debug("%i %i", idx, val)
            self.assertFalse(cond.end(idx, val))

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
