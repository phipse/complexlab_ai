"""Feature condition class

(c) Peter Schwede

"""

import logging


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
        self.t_prev = 0

    def can_start(self, time, value):
        """implementors may override this"""
        return True

    def do_next(self, time, value):
        """implementors may override this"""
        return True

    def has_to_end(self, time, value):
        """implementors may override this"""
        return True

    def start(self, time, value):
        """returns True, if feature is allowed to start here."""
        self.t0 = time
        self.t_prev = time
        self.t1 = time
        success = self.can_start(time, value)
        logging.debug("%s: %s (%s to %s) (new=%s old=%s)",
                      self, success, self.t0, time, value, self.value)
        return success

    def next(self, time, value):
        """will be called if not ending."""
        self.t_prev = time
        success = self.do_next(time, value)
        return success

    def end(self, time, value, force=False):
        """returns True if feature has to end here."""
        success = force or self.has_to_end(time, value)
        logging.debug("%s: %s (%s to %s) (new=%s old=%s)",
                      self, success, self.t0, time, value, self.value)
        self.t1 = self.t_prev
        return success

    def make_feature(self):
        """constructs a feature description"""
        res = (self.name, self.t0, self.t1, self.value) 
        logging.debug("%s", res)
        return res

    def is_stub(self, time, value):
        return self.t0 == self.t_prev
