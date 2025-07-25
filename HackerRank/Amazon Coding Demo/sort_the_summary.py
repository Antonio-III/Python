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
    
    out = associate_uniques_with_their_count(arr, uniques)
    
    out = sort_2d_arr_by_frequencies_in_descending_order(out)
    
    out = sort_2d_arr_by_uniques_in_ascending_order(out)

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

    S: O(k), k approx. = n, O(2k) at execution.
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

    S: O(n) because if `arr` only contains unique elements, we are equivalently creating another copy of `arr`.
    """

    uniques = []
    
    for i in arr:
        # `not in` operation performs a linear scan of `uniques`. O(k)
        if i not in uniques:
            uniques.append(i)
    return uniques

def associate_uniques_with_their_count(arr: list[int], uniques: list[int]) -> list[list[int]]:
    """
    Returns a 2d array where each inner list contains `a unique element`, and its `count` in the original array. For instance, given an input of:
        arr = [3, 3, 1, 2, 1]
        uniques = [3, 1, 2]
    
    The function will return `[[3, 2], [1, 2], [2, 1]]`. This is because the first element of every inner list are members of `uniques` and the second element of every inner list are the amount of times the respective first element has appeared in the original array `arr`.

    T: O(n^2)

    S: O(n) worst case. Can be O(k) if `arr` contains duplicates
    """
    return [[e, arr.count(e)] for e in uniques]

def sort_2d_arr_by_frequencies_in_descending_order(out: list[list[int]]) -> list[list[int]]:
    """
    T: O(nlogn) 

    S: O(n)
    """
    return sorted(out, key=lambda pair: pair[1], reverse=True)
    
def sort_2d_arr_by_uniques_in_ascending_order(out: list[list[int]]) -> list[list[int]]:
    """
    Takes in a [number, frequency] array like `[[3, 2], [1, 2], [2, 1]]` and sorts the same-frequency lists in ascending order. In the input, `[3, 2] and [1, 2]` have the same frequency (2) and are not in ascending order (3 comes before 1, which is incorrect), so we take this slice and perform a sort operation on them.
    
    Returns `[[1, 2], [3, 2], [2, 1]]`.

    The algorithm works by iterating through the indices of `out` and when a change of frequency has been found, we sort the corresponding indices accordingly. In the case of when we are at the last element, we perform a check if the frequencies match from what we are currently tracking, if they match, we perform a sort including the last element, if we do not, a sort is still performed but excluding the last element.

    Time complexity: O(n log n). The sorting time complexity goes from O(n) — where all elements are unique — to O(n log n) — where all elements have the same frequency.

    Space complexity: O(n), corresponds to the input array. Worst case is O(2n) at the last iteration if the array only had 1 frequency, where we end up slicing the array in its entirety, creating a copy of our input array.

    TODO: I need to find a better solution to accomodate cases where all frequencies are the same.
    """
    # Just a hard-coded value for the first frequency
    prev_freq = out[0][1] if len(out) != 0 else 0

    start_index = 0
    end_index = 0
    
    # T: O(n log n)
    for i in range(1, len(out)):
        curr_freq = out[i][1]
        
    
        if curr_freq != prev_freq:
            end_index = i
            
            out[start_index: end_index] = sorted(out[start_index: end_index])

            prev_freq = curr_freq

            start_index = end_index

        elif (i == len(out) - 1) and prev_freq == curr_freq:
            end_index = i

            out[start_index: end_index+1] = sorted(out[start_index: end_index+1])

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
    arr = [3, 3, 1, 2, 1,2]
    uniques = get_unique_values_v2(arr)
    print(uniques)
    out = associate_uniques_with_their_count(arr, uniques)
    print(out)
    out = sort_2d_arr_by_uniques_in_ascending_order(out)
    print(out)