#!/usr/bin/env python3


import sys

curr_key = None
rank_of_node = 0
DECIMAL_PLACES = 2

"""
TEAM BD1_368_409_413_452
INPUT : 

Input Format : 
NODE,CONTRIBUTION

OUTPUT : 
Format : 
NODE,RANK
"""

"""
1, cont(1,2)
1, cont(1,3)
1, cont(1,4)
"""

for line_that_has_to_be_stripped_and_split in sys.stdin:
    # key contribution
    key, cont = line_that_has_to_be_stripped_and_split.strip().split()

    cont = float(cont)

    if key != curr_key:
        # key change
        if curr_key != None:
            print(f'{curr_key},{round(rank_of_node,2)}')

        curr_key = key
        rank_of_node = round(0.34 + 0.57 * cont, DECIMAL_PLACES)
    else:
        rank_of_node += round(0.57 * cont, DECIMAL_PLACES)


print(f'{curr_key},{round(rank_of_node,2)}')
