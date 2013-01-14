"""Feature condition class

(c) Peter Schwede

"""

class dummy_condition(object):
    """super class for feature conditions. fits everywhere."""

    name = "dummy"
    can_overlay = True

    def __init__(self, name=None):
        if name is not None:
            self.name = name
        self.value = 0.0
        self.t0 = 0
        self.t1 = 0

    def start(self, time, value):
        """returns True, if feature is allowed to start here."""
        self.t0 = time
        return True

    def next(self, time, value):
        """does calculations"""
        self.value = 0.0

    def end(self, time, value):
        """returns True if feature has to end here."""
        self.t1 = time
        return True

    def make_feature(self):
        """constructs a feature description"""
        return (self.name, self.t0, self.t1, self.value)
