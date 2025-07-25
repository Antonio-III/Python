"""
#!/bin/python3
"""

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
    
    uniques = get_unique_values_v2(arr) 
    
    out = map_uniques_to_their_count(arr, uniques)
    
    out = sort_in_descending_order(out)
    
    out = sort_matching_frequencies(out)

    return out

def get_unique_values_v1(arr: list[int]) -> list[int]:
    """
    Returns unique values of `arr`, but order is not preserved.

    T: O(n)

    S: O(k), k approx. = n
    """
    uniques = list(set(arr))

    return uniques

def get_unique_values_v2(arr: list[int]) -> list[int]:
    """
    Returns unique values of `arr`, and order is preserved.

    T: O(n)

    S: O(2k+n), k approx. = n
    """

    uniques = []
    seen = set()
    for i in arr:
        if i not in seen:
            uniques.append(i)
            seen.add(i)
    return uniques

def get_unique_values_v3(arr: list[int]) -> list[int]:
    """
    Returns unique values of `arr`, and order is preserved. Unoptimized.

    T: O(n^2). Can be generalized to O(n*k) where

    k = n-1. The size of `uniques` in the worst case is equal to the current amount of iteration (not n necessarily), so k = n-1, and we will be effectively doing (k) comparisons per nth iteration. The pattern there might look like `0, 1, 2, 3, n-1, ...` and it looks a lot like The sum of first n integers whose formula is n(n+1)/2 to find the sum of the first n terms.

    The formula can be derived from writing the first n integers twice: in ascending and descending order.
        S_asc =  1 + 2 + 3 + ... + (n-1) + n
        S_desc = n + (n-1) + (n-2) + ... + 2 + 1

    We add the terms by adding the nth ascending and descending term together.
        2S = (1+n) + (2+n-1) + (3+n-2) + ... + (n-1+2) + (n+1)

    Each pair then simplifies to:
        2S = (n+1) + (n+1) + (n+1) + ... + (n+1) + (n+1) (n times)

    2S = n+1 * n

    S = n*(n+1)/2

    S: O(n) because if `arr` only contains unique elements, we equivalently creating another copy of `arr`.
    """

    uniques = []
    
    for i in arr:
        # `not in` operation performs a linear scan of `uniques`. O(k)
        if i not in uniques:
            uniques.append(i)
    return uniques

def map_uniques_to_their_count(arr: list[int], uniques: list[int]) -> list[list[int]]:
    """
    Returns a 2d array where each inner list contains `a unique element`, and its `count` in the original array. For instance, given an input of:
        arr = [3, 3, 1, 2, 1]
        uniques = [3, 1, 2]
    
    The function will return `[[3, 2], [1, 2], [2, 1]]`. This is because the first element of every inner list are members of `uniques` and the second element of every inner list are the amount of times the respective first element has appeared in the original array `arr`.

    T: O(n^2)

    S: O(n) worst case. Can be O(k) if `arr` contains duplicates
    """
    return [[e, arr.count(e)] for e in uniques]

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
    # Uncomment these if you want to use in HackerRank's IDE.
    # fptr = open(os.environ['OUTPUT_PATH'], 'w')

    # arr_count = int(input().strip())

    # arr = []

    # for _ in range(arr_count):
    #     arr_item = int(input().strip())
    #     arr.append(arr_item)

    # result = groupSort(arr)

    # fptr.write('\n'.join([' '.join(map(str, x)) for x in result]))
    # fptr.write('\n')

    # fptr.close()
    arr = [3, 3, 1, 2, 1]
    uniques = get_unique_values_v2(arr)
    # uniques = map_uniques_to_their_count(arr, uniques)
    print(map_uniques_to_their_count(arr, uniques))