#!/bin/python3

import math
import os
import random
import re
import sys



#
# Complete the 'groupSort' function below.
#
# The function is expected to return a 2D_INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY arr as parameter.
#

def groupSort(arr):
    # Write your code here
    # suppose arr = [3, 3, 1, 2, 1]
    
    uniques = get_unique_values(arr) 
    
    out = map_uniques_and_their_count(uniques)
    
    out = sort_in_descending_order(out)
    
    out = sort_matching_frequencies(out)

    return out

def get_unique_values(arr: list[int]) -> set[int]:
    """
    T: O(n)

    S: O(k), k approx. = n
    """
    return set(arr)

def map_uniques_and_their_count(uniques: set[int]) -> list[list[int]]:
    """
    T: O(k^2)

    S: O(2k) in each iteration, but k at exit. The additional k is due to the allocation for `list(uniques)`.

    k variable is used under the assumption that we are sorting `uniques`, a subset of `out`. This subset can be at most of size n.
    """
    return [[e, list(uniques).count(e)] for e in uniques]

def sort_in_descending_order(out: list[list[int]]) -> list[list[int]]:
    """
    T: O(nlogn) 

    S: O(n)
    """
    return sorted(out, key=lambda pair: pair[1], reverse=True)
    
def sort_matching_frequencies(out: list[list[int]]) -> list[list[int]]:
    """
    Takes in a [number, frequency] array like `[[3, 2], [1, 2], [2, 1]]` and sorts the same-frequency lists in ascending order. In the input, `[3, 2] and [1, 2]` have the same frequency (2) and are not in ascending order (3 comes before 1, which is incorrect), so we take this slice and perform a sort operation on them.
    
    Returns `[[1, 2], [3, 2], [2, 1]]`.

    Time complexity: O(n log n). The sorting time complexity goes from O(n) — where all elements are unique — to O(n log n) — where all elements have the same frequency.

    Space complexity: O(n), corresponds to the input array. Worst case is O(2n) at the last iteration if the array only had 1 frequency, where we end up slicing the array in its entirety, creating a copy of our input array.
    """
    prev_freq = 0

    start_index = -1
    end_index = -1
    
    # T: O(n log n)
    for i in range(len(out)):
        curr_freq = out[i][1]

        # Entering and exiting a same-frequency sequence
        if curr_freq != prev_freq:
            
            # We do not sort in the iteration of the first element.
            if prev_freq != 0:
                out[start_index: end_index] = sorted(out[start_index: end_index])

            prev_freq = curr_freq

            start_index = i
            # We have +1 to be inclusive of the ending index. The +1 can be put when we sort.
            end_index = start_index + 1

        else:
            end_index += 1

    return out

    
if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    arr_count = int(input().strip())

    arr = []

    for _ in range(arr_count):
        arr_item = int(input().strip())
        arr.append(arr_item)

    result = groupSort(arr)

    fptr.write('\n'.join([' '.join(map(str, x)) for x in result]))
    fptr.write('\n')

    fptr.close()