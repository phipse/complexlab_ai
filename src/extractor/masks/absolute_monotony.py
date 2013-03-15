#!/usr/bin/env python

from mask import Mask

class AbsoluteIncreasing(Mask):
    name = "increasing"
    can_overlay = False

    def can_start(self, time, value):
        self.value = value
        return True

    def has_to_end(self, time, value):
        jupp = value < self.value
        if jupp:
            self.value = value - self.value
        return jupp


class AbsoluteDecreasing(AbsoluteIncreasing):
    name = "decreasing"

    def has_to_end(self, time, value):
        jupp = value > self.value
        if jupp:
            self.value = self.value - value
        return jupp
