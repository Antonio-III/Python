"""
Make a function that returns the sum of squares of the first n natural numbers (inclusive).
Example: f(4) = 1^2 + 2^2 + 3^3 + 4^4 = 30
"""
from typing import Callable

from const import MODES

def main() -> None:
    n = 4
    assert(n > 1)

    print(test(sum_square_nums, n))
    print(sum_square_nums(n))

def sum_square_nums(n: int, mode: str = "iter") -> int:
    assert(mode in MODES)

    if mode == MODES[0]:
        out = _sum_square_nums_iter(n)

    elif mode == MODES[1]:
        out = _sum_square_nums_rec(n)
    
    else:
        out = _sum_square_nums_pyt(n)
    
    return out

def _sum_square_nums_iter(n: int) -> int:
    sum = 0

    for i in range(1, n+1):
        sum += i**2

    return sum

def _sum_square_nums_rec(n: int) -> int:
    if n > 1:
        return n**2 + _sum_square_nums_rec(n-1)
    # 1**2 can be used but they are equivalent, so I picked 1 for simplicity.
    return 1

def _sum_square_nums_pyt(n: int) -> int:
    sum = 0

    for i in range(1, n+1):
        sum += i**2

    return sum

def test(func: Callable[[int, str], int], n: int) -> bool:
    return func(n, "iter") == func(n, "rec") == func(n, "pyt") 

if __name__ == "__main__":
    main()