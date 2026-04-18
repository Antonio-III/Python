from _04_gcf import find_factors

def main() -> None:
    factors = input("Enter quadratic coefficient and constant:\n").split()
    assert(len(factors) == 2)

    x, y = (int(n) for n in factors)

    z = int(input("Target sum:\n"))

    print(factors_sum_quadra(x, y, z))

def factors_sum(factors: list[int], x: int) -> tuple[int, int]:
    
    for i in range(len(factors)//2):
        f1, f2 = factors[i], factors[-(i + 1)]
        if x >= 0:
            if (f1 + f2 == x):
                return (f1, f2)
            if (-f1 + f2 == x):
                return (-f1, f2)
        elif x < 0:
            if (f1 - f2 == x):
                return (f1, -f2)
            if (-f1 - f2 == x):
                return (-f1, -f2)

    return (0, 0)

def factors_sum_quadra(x: int, y: int, z: int) -> tuple[int, int]:
    prod = x*y
    factors = find_factors(prod, unique=False)

    for i in range(len(factors)//2):
        f1, f2 = factors[i], factors[-(i + 1)]
        if prod >= 0:
            if (f1 + f2 == z):
                return (f1, f2)
            if (-f1 - f2 == z):
                return (-f1, -f2)
        elif prod < 0:
            if (f1 - f2 == z):
                return (f1, -f2)
            if (-f1 + f2 == z):
                return (-f1, f2)

    return (0, 0)


if __name__ == "__main__":
    main()