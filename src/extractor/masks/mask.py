"""Feature condition class

(c) Peter Schwede

"""

import logging

from features import FeatureGroup


class Mask(object):
    """super class for feature conditions. fits everywhere."""

    name = "dummy"
    can_overlay = True
    value = 0

    def __init__(self, name, default_attr_ranges):
        self.name = name
        self.__t0 = 0
        self.__t1 = 0
        self.__t_prev = 0
        self.feature_group = FeatureGroup(self.name, default_attr_ranges)

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
        self.__t0 = time
        self.__t_prev = time
        self.__t1 = time
        success = self.can_start(time, value)
        logging.debug("%s: %s %s", self, success, value,)
        return success

    def next(self, time, value):
        """will be called if not ending."""
        self.__t_prev = time
        success = self.do_next(time, value)
        return success

    def end(self, time, value, force=False):
        """returns True if feature has to end here."""
        self.__t1 = self.__t_prev
        success = force or self.has_to_end(time, value)
        logging.debug("%s: %s (o,n=%s,%s)",
                      self, success, self.value, value)
        return success

    def make_feature(self):
        """constructs a feature description"""
        return self.feature_group.create_feature([self.__t0, self.__t1, self.value])

    def is_stub(self, time, value):
        return self.__t0 == self.__t_prev

    def __len__(self):
        return self.__t1 - self.__t0

    def __repr__(self):
        return "<%s t0=%s, t1=%s, val=%f>" % (self.name, self.__t0,
                                              self.__t1, self.value,)
