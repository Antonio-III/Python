"""
Finds a duplicate within a single list object.

Table of Contents:
    (import) radix_sort
    (import) count_digits
    contains_duplicates
    find_duplicate
"""
from radix_sort import radix_sort
from count_digits import count_digits

def contains_duplicates(array: list[int]) -> bool:
    """
    Finds duplicates in an array using Radix Sort. Return True if found, else False.
    """
    pos_array = [n for n in array if n >= 0] 
    neg_array = [n for n in array if n < 0]

    max_digits_pos = count_digits(max(pos_array)) if pos_array else -1
    min_digits_neg = count_digits(min(neg_array)) if neg_array else -1

    
    sorted_pos_array = radix_sort(pos_array, max_digits_pos) if max_digits_pos != -1 else []
    sorted_neg_array = radix_sort(neg_array, min_digits_neg) if min_digits_neg != -1 else []

    return find_duplicate(sorted_pos_array) or find_duplicate(sorted_neg_array)

def find_duplicate(array: list[int]) -> bool:
    """
    Linear search to find duplicate elements. Returns True if duplicates in `array` found. False otherwise.

    O(n)
    """
    for i in range(len(array) - 1):
        if array[i] == array[i + 1]:
            return True
    return False

if __name__ == "__main__": 
    array = list(map(int, input("Enter numbers separated with whitespace:\n").split()))

    print(contains_duplicates(array=array))