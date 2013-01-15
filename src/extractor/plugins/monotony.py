#!/usr/bin/env python

import condition


class Increasing(condition.Condition):
    name = "increasing"
    can_overlay = False

    def can_start(self, time, value):
        self.value = value
        return True

    def do_next(self, time, value):
        self.value = value

    def has_to_end(self, time, value):
        return value < self.value


class Decreasing(Increasing):
    name = "decreasing"

    def has_to_end(self, time, value):
        return value > self.value
