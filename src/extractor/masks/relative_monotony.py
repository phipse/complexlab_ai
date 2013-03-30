#!/usr/bin/env python

from mask import Mask

class RelativeIncreasing(Mask):
    can_overlay = False

    def can_start(self, time, value):
        self.value = value
        self.t_prev = time
        self.t0 = time
        return True

    def do_next(self, time, value):
        self.value = value
        self.t_prev = time

    def has_to_end(self, time, value):
        res = value < self.value
        if res:
            dt = (self.t_prev - self.t0).total_seconds()
            if dt == 0:
                return True
            self.value = (value - self.value) / dt
        return res


class RelativeDecreasing(RelativeIncreasing):
    def has_to_end(self, time, value):
        res = value > self.value
        if res:
            dt = (self.t_prev - self.t0).total_seconds()
            if dt == 0:
                return True
            self.value = (self.value - value) / dt
        return res
