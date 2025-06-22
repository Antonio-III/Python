"""
Python script that performs a radix sort.

Table of Contents:
    (import) stable_counting_sort(array: list[int], base: int = 10, power_of_base: int = 0)
    radix_sort(array: list[int], max_digits: int) -> list[int]
    _radix_sort_recursive(array: list[int], max_digits: int, base: int = 10, power_of_base: int = 0) -> list[int]
"""

from stable_counting_sort import stable_counting_sort

def radix_sort(array: list[int], max_digits: int) -> list[int]:
    """
    Performs the Radix Sort Algorithm, which sorts numbers by their place value.
    """
    return _radix_sort_recursive(array=array, max_digits=max_digits)

def _radix_sort_recursive(array: list[int], max_digits: int, base: int = 10, power_of_base: int = 0) -> list[int]:
    """
    Performs the Stable Counting Sort algorithm, and recursively calls itself to sort by the next significant digit.
    """
    # Exit recursion if there are no more digits left to sort.
    if max_digits == power_of_base:
        return array

    out_array = stable_counting_sort(array, base, power_of_base)

    return _radix_sort_recursive(out_array, max_digits, power_of_base=power_of_base+1)