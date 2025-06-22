def count_digits_iterative(n: int) -> int:
    """
    Counts digits using iterative integer division.
    """
    if n == 0: 
        return 1
    
    n = abs(n)
    count = 0

    while n > 0:
        n = n // 10
        count += 1 # This line will increment `count` regardless of the result of the operation, as long as n != 0.

    return count