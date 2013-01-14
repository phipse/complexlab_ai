"""Feature condition class

(c) Peter Schwede

"""

__all__ = ["Condition"]


class Condition(object):
    """super class for feature conditions. fits everywhere."""

    name = "dummy"
    can_overlay = True
    value = 0

    def __init__(self, name=None):
        if name is not None:
            self.name = name
        self.t0 = 0
        self.t1 = 0

    def __start(self, time, value):
        return True

    def __next(self, time, value):
        return True

    def __end(self, time, value):
        return True

    def start(self, time, value):
        """returns True, if feature is allowed to start here."""
        self.t0 = time
        return self.__start(time, value)

    def next(self, time, value):
        """will be called from step to step. please define calculations here"""
        return self.__next(time, value)

    def end(self, time, value):
        """returns True if feature has to end here."""
        self.t1 = time
        return self.__end(time, value)

    def make_feature(self):
        """constructs a feature description"""
        return (self.name, self.t0, self.t1, self.value)
