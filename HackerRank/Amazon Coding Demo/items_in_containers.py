#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'numberOfItems' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. STRING s
#  2. INTEGER_ARRAY startIndices
#  3. INTEGER_ARRAY endIndices
#

def numberOfItems(s: str, startIndices: list[int], endIndices: list[int]) -> list[int]:
    """
    Counts the amount of items — represented as * — between complete compartments — 1 pair of | — of a given substring. The count is stored per substring.

    My solution is to slice the original string only containing the starting and ending (inclusive) indices. 
        For some reason, the starting index is 1-indexed. 
    
    We then count the amount of items between the first compartment and the last compartment. We do not consider if there are compartment pieces between the first and last compartments as consideration for these lead to a longer runtime. 

    For each substring, we initialize a total. The total is incremented by counting in each compartment. This total is to be appended by our output array.

    I was not able to submit this problem, and this solution may be really slow.

    Time complexity: O(k * q), where:
        k <= len(s), equivalent to n
        q = len(startIndices), number of queries
        Each query may extract a substring up to length n, requiring n operations.

    Complexity can be generalized to O(n^2).
        
    Space complexity: O(q). Can be generalized to O(n).
    """
    # Write your code here
    out = []
    # At worst, O(n) time 
    for start, end in zip(startIndices, endIndices):
        # At worst, O(n) time, O(k) space but garbage collected
        substring = s[start-1: end]

        total_items = 0

        # O(n) time
        open_compartment = substring.find("|")
        closed_compartment = substring.rfind("|")
        
        # O(n) time, O(k) space but garbage collected
        full_compartment = substring[open_compartment: len(substring)-closed_compartment+1]

        total_items += full_compartment.count("*")
        # 1 value kept per iteration. O(q) space.
        out.append(total_items)

    return out

def numberOfItems_optimized(s: str, startIndices: list[int], endIndices: list[int]) -> list[int]:
    """
    Courtesy of ChatGPT. 
    
    Instead of slicing in each iteration — which takes n time —, we instead make lists that store values, and use these lists instead to deliver results of a query. This method uses a prefix sum.
    """
    return []
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    s = input()

    startIndices_count = int(input().strip())

    startIndices = []

    for _ in range(startIndices_count):
        startIndices_item = int(input().strip())
        startIndices.append(startIndices_item)

    endIndices_count = int(input().strip())

    endIndices = []

    for _ in range(endIndices_count):
        endIndices_item = int(input().strip())
        endIndices.append(endIndices_item)

    result = numberOfItems(s, startIndices, endIndices)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
