#!/usr/bin/env python

import pdb
from datetime import datetime

from classifier import Classifier

class Increasing(Classifier):
    name = "increasing"
    can_overlay = False

    def can_start(self, time, value):
        self.value = value
        return True

    def do_next(self, time, value):
        self.value = value

    def has_to_end(self, time, value):
        if time == datetime(2008,1,8):
            pdb.set_trace()
        return value < self.value


class Decreasing(Increasing):
    name = "decreasing"

    def has_to_end(self, time, value):
        return value > self.value
