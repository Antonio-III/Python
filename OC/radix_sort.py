"""
Python script that performs a Radix Sort.

Table of Contents: 
    (import) stable_counting_sort(array: list[int], base: int = 10, power_of_base: int = 0)
    radix_sort
    _radix_sort_recursive
    _radix_sort_iterative
"""
from stable_counting_sort import stable_counting_sort

def radix_sort(array: list[int], max_digits: int) -> list[int]:
    """
    Performs the Radix Sort Algorithm, which sorts numbers by their place value.
    """
    return _radix_sort_recursive(array=array, max_digits=max_digits) or _radix_sort_iterative(array=array, max_digits=max_digits)

def _radix_sort_recursive(array: list[int], max_digits: int, base: int = 10, power_of_base: int = 0) -> list[int]:
    """
    Performs the Radix Sort algorithm, and recursively calls itself to sort by the next significant digit.
    """
    # Exit recursion if there are no more digits left to sort.
    if max_digits == power_of_base:
        return array

    out = stable_counting_sort(array, base, power_of_base)

    return _radix_sort_recursive(out, max_digits, power_of_base=power_of_base+1)

def _radix_sort_iterative(array: list[int], max_digits: int, base: int = 10) -> list[int]:
    """
    Performs the Radix Sort algorithm, and iteratively sorts the array by the next significant digit.
    """
    out = array

    for i in range(max_digits):
        power_of_base = i
        out = stable_counting_sort(out, base, power_of_base)

    return out
