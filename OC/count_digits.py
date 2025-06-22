"""
Finds the amount of digits in a given number.

Table of Contents:
    count_digits
    _count_digits_iterative
    _count_digits_recursive
"""

def count_digits(n: int) -> int:
    """
    Returns the amount of digits in `n`.

    O(log10 n)
    """
    return _count_digits_iterative(n)
 
def _count_digits_iterative(n: int) -> int:
    """
    Counts digits using iterative integer division.
    """
    if n == 0: 
        return 1
    
    n = abs(n)

    count = 0

    while n > 0:
        n = n // 10
        count += 1 # This line will increment `count` regardless of the result of the operation, as long as n is not 0.

    return count

def _count_digits_recursive(n: int, count: int = 0) -> int:
    """
    Counts digits recursively integer division.
    """ 
    if n == 0:
        return count or 1
    
    n = abs(n)

    return _count_digits_recursive(n=n//10, count=count+1)

if __name__ == "__main__":
    n = int(input("Enter a number:\n"))
    
    print(count_digits(n))