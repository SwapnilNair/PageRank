#!/usr/bin/env python3

import sys
import time

cur = None
prev_data = []

start = time.time()
f = open(sys.argv[1], 'w')

for i in sys.stdin:
    # get data from line read
    d = i.strip().split()

    # check for key change
    if d[0] != cur:
        # print nth node in adjustancy list for prev node 
        if prev_data != None and len(prev_data) >= 2:
            print(f"{prev_data[1]}]")
        # setup new node
        cur = d[0]
        # print node and bracket
        print(f"{d[0]}  [", end="")
        
        prev_data = d
        
        f.write(f"{cur},1\n")
    else:
        # print previous
        print(f"{prev_data[1]}", end=", ")
        # set previous
        prev_data = d

# print nth node in adjustancy list for last node
print(f"{d[1]}]")
f.close()

 end = time.time()

print(end-start)
