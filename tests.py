#!/usr/bin/env python
import os
import sys
import logging

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orca.settings")
    sys.path.append(r'../../madlee')

    logging.basicConfig(filename="debug.log", level=logging.DEBUG)

    from orca.ocean import ocean_man
    s30 = ocean_man['S30']

    # d = s30.frame(1030, 'close', date1=20100101, date2=20110101)
    # print d

    print s30.min_date(), s30.max_date()

