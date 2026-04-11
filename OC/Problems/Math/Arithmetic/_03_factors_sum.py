from _04_gcf import find_factors

def main() -> None:
    x = input("Enter quadratic coefficient and constant:\n").split()
    y = int(input("Target sum:\n"))

    prod = 1
    for i in x:
        prod *= int(i)
    
    factors = find_factors(abs(prod), unique=False)
    print(factors_sum(factors, y))

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

    return (-1, -1)

if __name__ == "__main__":
    main()