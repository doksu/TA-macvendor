#!/usr/bin/env python

import sys
import os
import csv
import netaddr

if len(sys.argv) != 3:

    print("Usage: python macvendor.py [macfield] [vendorfield]")
    sys.exit(1)

else:

    # initialise a bunch of stuff

    macfield = sys.argv[1]
    vendorfield = sys.argv[2]

    infile = sys.stdin
    outfile = sys.stdout

    r = csv.DictReader(infile)
    header = r.fieldnames

    w = csv.DictWriter(outfile, fieldnames=r.fieldnames)
    w.writeheader()

    cache = {}

    # for each event
    for result in r:

        # if the event's mac address field has a value
        if result[macfield]:

            # check if we're already resolved it
            if result[macfield] in cache:

                # if so, provide the cached resolution
                result[vendorfield] = cache[result[macfield]]

            # if we haven't already resolved it
            else:

                # attempt to resolve the mac address
                try:
                    lookup = netaddr.EUI(result[macfield])
                    result[vendorfield] = ",".join([lookup.oui.registration(reg).org for reg in range(lookup.oui.reg_count)])

                    # update the cache
                    cache[result[macfield]] = result[vendorfield]

                # if resolution failed
                except:

                    # update the cache accordingly
                    cache[result[macfield]] = None

        # output to Splunk
        w.writerow(result)
