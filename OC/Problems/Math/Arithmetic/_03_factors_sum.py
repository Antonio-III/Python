from arithmetic import find_factors

def main() -> None:
    factors = input("Enter quadratic coefficient and constant:\n").split()
    assert(len(factors) == 2)

    x, y = (int(n) for n in factors)

    z = int(input("Target sum:\n"))

    print(factors_sum(x*y, z))


def factors_sum(x: int, y: int) -> tuple[int, int]:
    """Return the pair of factors of `x` that sum to `y`.
    """
    # This function is made to quickly find factors of the middle coefficient in a quadratic expression, to see if it is factorable.

    if not y:
        return (0, y)

    limit = int((abs(x)) ** 0.5)

    for f1 in range(limit+1):
        if (y % f1) == 0:
            f2 = y//f1
            if (f1 + f2 == y):
                return (f1, f2)
            if (-f1 + f2 == y):
                return (-f1, f2)
            if (f1 - f2 == y):
                return (f1, -f2)
            if (-f1 - f2 == y):
                return (-f1, -f2)

    return (0, 0)

if __name__ == "__main__":
    main()