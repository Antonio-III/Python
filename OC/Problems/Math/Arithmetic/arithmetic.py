"""
Library for basic math operations.

Functions are sorted by return type: int -> float -> bool -> list
"""

# int/float

# bool
def is_divisible(dividend: int, divisor: int) -> bool:
    """Return True if the dividend can be completely divided by the divisor, else False.
    """
    return (dividend/divisor) == (dividend//divisor)

# list
def find_factors(n: int, unique: bool = True) -> list[int]:
    """Find the factors of `|n|`.

    Args:
        n: An integer.
        unique: Flag for removing duplicate factors. Defaults to True.

    Returns:
        Sorted list containing the factors of `n`.
    """
    n = abs(n)
    i = 1

    factors = []

    while (i**2 <= n):
        q1 = n/i
        q2 = n//i
        if (q1 == q2):
            factors.append(i)
            # When dividing a perfect square by its root, we can choose to ignore the "duplicate" number.
            if (q2 != i) or not unique:
                factors.append(q2)

        i += 1

    return sorted(factors)

