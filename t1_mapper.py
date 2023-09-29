#!/usr/bin/env python3

import sys

#def parse(sd:str):
#    return sd.strip().split()

for source_dest in sys.stdin:
    # ignore comments
    if source_dest[0] != "#":
        #s, d = parse(source_dest)
        s, d = source_dest.strip().split()
        print(s, d)
