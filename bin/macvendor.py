#!/usr/bin/env python

import sys
import os
import csv
import netaddr

if len(sys.argv) != 3:

    print "Usage: python macvendor.py [mac field] [vendor field]"
    sys.exit(1)

else:

    macfield = sys.argv[1]
    vendorfield = sys.argv[2]

    infile = sys.stdin
    outfile = sys.stdout

    r = csv.DictReader(infile)
    header = r.fieldnames

    w = csv.DictWriter(outfile, fieldnames=r.fieldnames)
    w.writeheader()

    for result in r:
        if result[macfield]:
            try:
                lookup = netaddr.EUI(result[macfield])
                result[vendorfield] = ",".join([lookup.oui.registration(reg).org for reg in range(lookup.oui.reg_count)])
            except:
                pass
        w.writerow(result)
