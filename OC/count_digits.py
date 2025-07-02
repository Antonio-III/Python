"""
Finds the amount of digits in a given number. Only works for base 10

Table of Contents
    count_digits
    _count_digits_iterative
    _count_digits_recursive
    _count_digits_log2
    _count_digits_log10
    _count_digits_log
"""
from math import log, log2, log10 

def count_digits(n: int, base: int = 10) -> int:
    """
    Returns the amount of digits in `n`.

    O(log₁₀ n)
    """
    return _count_digits_iterative(n, base)
 
def _count_digits_iterative(n: int, base: int) -> int:
    """
    Counts digits using iterative integer division.

    O(log₁₀ n)
    """
    if n == 0: 
        return 1
    
    n = abs(n)
    
    count = 0

    while n > 0:
        n = n // base
        count += 1 # This line will increment `count` regardless of the result of the operation, as long as n is not 0.

    return count

def _count_digits_recursive(n: int, count: int = 0, base: int = 10) -> int:
    """
    Counts digits recursively integer division.

    O(log₁₀ n)
    """ 
    if n == 0:
        return count or 1
    
    n = abs(n)

    return _count_digits_recursive(n // base, count + 1, base)

def _count_digits_log2(n: int) -> int:
    return int(log2(n))

def _count_digits_log10(n: int) -> int:
    return int(log10(n))

def _count_digits_log(n: int, base: int = 10) -> int:
    return int(log(n, base))

if __name__ == "__main__":
    n = int(input("Enter a number:\n"))
    
    print(count_digits(n))