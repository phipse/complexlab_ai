#!/usr/bin/env python

import condition


class Raising(condition.Condition):
    name = "raising"
    can_overlay = False

    def can_start(self, time, value):
        self.value = value
        return True

    def do_next(self, time, value):
        self.value = value

    def has_to_end(self, time, value):
        return value < self.value


class Falling(Raising):
    name = "falling"

    def has_to_end(self, time, value):
        return value > self.value
