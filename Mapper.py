#!/usr/bin/env python3

import sys
from json import loads

"""
TEAM BD1_368_409_413_452
INPUT : 
Input is ADJACENCY LIST through the standard input

Input Format : 
Node\tAdj_List
1\t[1,2,3]

OUTPUT : 
Format : 
IN NODE,CONTRIBUTION
"""

READ_MODE = 'r'
DECIMAL_PLACES_CONT = 2
DECIMAL_PLACES_9 = 9

# read the w file
w_file = open(sys.argv[1] , READ_MODE)

# read the page_embeddings file
page_embeddings_file = open(sys.argv[2] , READ_MODE)

# parse the page_embeddings
parsed_page_embeddings = loads(page_embeddings_file.read().strip())

# parse the rank list
rank_list = {}
for i in w_file.readlines():
    x = i.strip().split(",")
    rank_list[int(x[0])] = float(x[1])

def dot_norm(p, q, p_flag):
    # normal way of calculating
    # dot = p[5] * q[5] + p[1] * q[1] + p[3] * q[3] + p[2] * q[2] + p[4] * q[4] + p[0] * q[0]
    # norm_p = pow(p[5] * p[5] + p[1] * p[1] + p[3] * p[3] + p[2] * p[2] + p[4] * p[4] + p[0] * p[0], 1/2)
    # norm_q = pow(q[5] * q[5] + q[1] * q[1] + q[3] * q[3] + q[2] * q[2] + q[4] * q[4] + q[0] * q[0], 1/2)
    # return dot, norm_p, norm_q
    
    # loop unrolling with kernel size 2
    kernel_size = 2
    i = 0
    dot_product = 0
   
    # only calculate norm for p if the value is not already cached
    if p_flag:
        norm_p = 0
        norm_q = 0
        len_q = len(q)

        while i < len_q:
            dot_product += p[i] * q[i]
            dot_product += p[i+1] * q[i+1]

            norm_p += (p[i] ** 2)
            norm_p += (p[i+1] ** 2)

            norm_q += (q[i] ** 2)
            norm_q += (q[i+1] ** 2)

            i += kernel_size

        return (
            round(dot_product, DECIMAL_PLACES_9), 
            round(norm_p, DECIMAL_PLACES_9), 
            round(norm_q, DECIMAL_PLACES_9)
        ) 
    else:
        norm_q = 0
        len_q = len(q)

        while i < len_q:
            dot_product += p[i] * q[i]
            dot_product += p[i+1] * q[i+1]

            norm_q += (q[i] ** 2)
            norm_q += (q[i+1] ** 2)

            i += kernel_size
            
        return (
            round(dot_product, DECIMAL_PLACES_9), 
            0, 
            round(norm_q, DECIMAL_PLACES_9)
        )

def similarity_of_node(p,q, cache):
    """
    Uses the page embeddings to find the similarity between p and q
    """
    if cache == None:
        dot_p_q, norm_p, norm_q = dot_norm(parsed_page_embeddings[str(p)], parsed_page_embeddings[str(q)], True)
        cache = norm_p
        return round(dot_p_q / (norm_p + norm_q - dot_p_q), DECIMAL_PLACES_9), cache
    else:
        dot_p_q, norm_p, norm_q = dot_norm(parsed_page_embeddings[str(p)], parsed_page_embeddings[str(q)], False)
        return round(dot_p_q / (cache + norm_q - dot_p_q), DECIMAL_PLACES_9), cache

def contribution_of_node(p, adj_list, q, cache):
    """
    Calculates the contribution of p,q
    Contribution(p, q) = Previous_Rank(p) * Similarity(p,q) / No_of_Outlinks(p)
    """
    num_outlinks = len(adj_list)
    similarity, cache = similarity_of_node(p,q,cache)
    
    cont = (rank_list[p] *  similarity / num_outlinks)

    if abs(cont) <= 0.05:
        return cont, cache
    else:
        return cont, cache

cache = None

for adj_item in sys.stdin:
    node, adj_list_str = adj_item.strip().split("\t")
    # adj_list_str => "[1, 2, 3]"
    adj_list = adj_list_str[1:-1].split(", ")

    for i in adj_list:
        cont, cached_norm = contribution_of_node(int(node), adj_list, int(i), cache)
        cache = cached_norm
        print(i, cont)

    # print the node and 0 contribution so as to also get ranks with no incoming links
    print(node, 0)
    cache = None

    
