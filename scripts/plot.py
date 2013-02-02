#!/usr/bin/env python

import sys
import datetime
from itertools import izip, count

with open(sys.argv[1], "r") as f:
    data = eval("".join(f.readlines()))
    
min_val = max_val = None
for date, value in data.values()[0].items():
    if min_val is None:
        min_val = max_val = value
    min_val = min(value, min_val)
    max_val = max(value, max_val)

print min_val, max_val

for i, (date, value) in izip(count(), sorted(data.values()[0].items())):
    dist = "=" if i % 5 == 0 else "-"
    print "% 5i %s " % (i, date) + dist * int(60 * (value - min_val) / (max_val - min_val)) + "#\t%.2f" % value
