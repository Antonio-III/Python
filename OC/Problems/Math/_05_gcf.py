def main():
    num_list = sorted([int(num) for num in input("Enter numbers:\n").split()])
    print(__find_GCF(num_list))

def __find_GCF(num_list: list[int]) -> int:
    factors_list = []
    for num in num_list:
        factors_list.append(__find_factors(num))

    limit = len(factors_list[0])
    factors_l = len(factors_list)
    factors_ptr = [1] * factors_l
    
    gcf = 1

    while (factors_ptr[0] < limit):
        s = 0
        biggest_factor = factors_list[0][factors_ptr[0]]
        for i in range(factors_l):
            s += factors_list[i][factors_ptr[i]]

        if (div:=__is_divisible(s, biggest_factor)):
            gcf = biggest_factor

        for i in range((0) if div else (1), factors_l):
                factors_ptr[i] += 1

    return gcf

def __find_factors(n: int, unique: bool = True) -> list[int]:
    i = 1

    factors = []
    while (i**2 <= n):
        q1 = n/i
        q2 = n//i
        if (q1 == q2):
            factors.append(i)
            if (q2 != i) or not unique:
                factors.append(q2)

        i += 1
    return sorted(factors)

def __is_divisible(dividend: int, divisor: int) -> bool:
    q1 = dividend/divisor
    q2 = dividend//divisor

    return q1 == q2

if __name__ == "__main__":
    main()