from math import sqrt

# Index values, and integers.
THOUSANDTH = 3
H_THOUSANDTH = 5

NDIGITS = THOUSANDTH


STR_ROUNDING = [
    "Tenths",
    "Hundredths",
    "Thousandths",
    "Ten Thousandths"
    "Hundred Thousandths"
]


def main() -> None:
    x = float(input("Enter number:\n"))
    out = round(sqrt(x), NDIGITS)
    print(f"√{x} (Nearest {STR_ROUNDING[NDIGITS-1]}) ≈ {out}")
if __name__ == "__main__":
    main()