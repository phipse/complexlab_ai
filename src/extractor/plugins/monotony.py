#!/usr/bin/env python

import condition


class Raising(condition.Condition):
    name = "raising"
    t0 = t1 = None
    value = 0
    can_overlay = False

    def start(self, time, value):
        self.value = value
        self.t0 = time
        return True

    def next(self, time, value):
        self.value = value

    def end(self, time, value):
        self.t1 = time
        return value >= self.value


class Falling(Raising):
    name = "falling"

    def end(self, time, value):
        self.t1 = time
        return value <= self.value
