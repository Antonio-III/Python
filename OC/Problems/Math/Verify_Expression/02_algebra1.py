# TODO: Add support for simplfiying variable terms (and exponents).
# Ex: 1x + 2x = 3x and x^2 * x^3 = x^5.
def main():
    # if (not (coeff := input("Enter coefficient:\n"))) or (not coeff.isnumeric()):
    #     raise ValueError("Coefficient is not numeric.")

    # if (not (vars := input("Enter variables (including exponents):\n"))):

    #     raise ValueError("Invalid input.")
    t1 = term("12", "z^7")
    t2 = term("-6", "z^5")
    t1.divide(t2)

    print(t1.str_form())

    t1.add(t2)

class term():
    """Data type to represent a product/quotient of fininite coefficients and variables.
    """
    def __init__(self, coeff: int = 1, vars: dict[str, int] = {}, div: "term | int" = 1):
        self.coeff = coeff
        self.vars = vars
        self.div = div

    def str_form(self) -> str:
        """Returns the term in its string form.
        """
        numerator = f"{self.coeff}{self.__convert_vars_to_str()}"
        denominator = 1

        if (isinstance(self.div, "term")):
            denominator = f"{self.div.str_form()}"

        if denominator != 1:
            return f"({numerator})/{denominator}"

        return f"{numerator}"

    def __convert_vars_to_str(self) -> str:
        """Returns the variables in string form.
        """
        vars_str = ""
        for v in self.vars.keys():
            # Show variables AND their exponents 
            if self.vars[v] > 1:
                vars_str += f"{v}^{self.vars[v]}"
            else:
                vars_str += f"{v}"

        return vars_str

    # Only perform on like terms
    def add(self, addend: "term"):
        if self.vars == addend.vars:
            self.coeff += addend.coeff
        
    def subtract(self, subtrahend: "term"):
        if self.vars == subtrahend.vars:
            self.coeff -= subtrahend.coeff
    # ---

    def multiply(self, factor: "term"):
        self.coeff *= factor.coeff

        for v in factor.vars:
            if (self.vars.get(v)):
                self.vars[v] += factor.vars[v]
            else:
                self.vars[v] = factor.vars[v]

    def divide(self, divisor: "term"):
            # Simplify expressions to lowest terms.
            self.coeff, divisor.coeff = __simplify_fraction(self.coeff, divisor.coeff)
            q1 = self.coeff/divisor.coeff
            q2 = self.coeff//divisor.coeff
            
            # Division only occurs between divisible numbers.
            if (q1 == q2):
                self.coeff = q2

            # Divide the exponents.
            for v in divisor.vars:
                if (self_expo := self.vars.get(v)):
                    if (self_expo < divisor.vars[v]):
                        divisor.vars[v] -= self.vars[v]
                        del self.vars[v]

                    elif (self_expo > divisor.vars[v]):
                        self.vars[v] -= divisor.vars[v]
                        del divisor.vars[v]

                    elif (self_expo == divisor.vars[v]):
                        del self.vars[v]
                        del divisor.vars[v]

def __record_vars(exp: str) -> tuple[list[str], list[int]]:
    """Parse the variables from a string expression. Records variables and exponents into separate lists.

    Args:
        exp: The mathematical expression.

    Returns:
        A list of variables and a list of their corresponding exponents.
    """

    variables_l = []
    exponents_l = []

    vars_len = len(exp)

    exponent_counter = ""
    
    for i in range(vars_len):
        curr = exp[i]

        if curr.isalpha():
            variables_l.append(curr)

            if exponent_counter:
                exponents_l.append(int(exponent_counter))
                exponent_counter = ""

            if (i+1 == vars_len) or (exp[i+1] != "^"):
                exponents_l.append(1)


        elif curr.isnumeric() and ((i > 0) and ((exp[i-1] == "^") or exponent_counter)):
            exponent_counter += curr

            if (i+1 == vars_len):
                exponents_l.append(int(exponent_counter))

    return variables_l, exponents_l

def __parse_vars(exp: str) -> dict[str, int]:
    """Parse the variables from a string expression. Creates a dict to store the variables and their respective exponents. The dict is sorted.

    Args:
        exp: The Mathematical expression.

    Returns:
        The dictionary contaning the variables (Keys) and their exponents (Value).
    """
    vars_d = {}
    variables_l, exponents_l = __record_vars(exp)

    for v, e in zip(variables_l, exponents_l):
        vars_d[v] = e

    return dict(sorted(vars_d.items()))

def parse_exp(exp: str):
    coeff = __parse_coeff(exp)
    vars = __parse_vars(exp)
    div = __parse_div(exp)

def __parse_div(exp: str):
    i = exp.find("/")
    
    if (i == -1):
        return 1

    coeff = __parse_coeff(exp[i])
    vars  = __parse_vars(exp[i])

    term = term(coeff, vars)
    return term

def __parse_div(self, div: str):
    int_d = int(div)
    float_d = float(div)
    return (int_d if (int_d == float_d) else float_d)


# Extras

def __is_divisible(dividend: int, divisor: int) -> bool:
    q1 = dividend/divisor
    q2 = dividend//divisor

    return q1 == q2

def __simplify_fraction(numerator: int, denominator: int):
    gcf = __find_GCF(numerator, denominator)

    return numerator//gcf, denominator//gcf

def __find_GCF(n1: int, n2: int):
    n1_factors = __find_factors(n1)
    n2_factors = __find_factors(n2)

    n1_flen = len(n1_factors)
    n2_flen = len(n2_factors)

    i = j = 1

    gcf = 1
    while ((i+1 < n1_flen) or (j+1 < n2_flen)):
        if (n1_factors[i] == n2_factors[j]):
            gcf = n1_factors[i]
            i += 1
            j += 1

        if n1_factors[i] < n2_factors[j]:
            i += 1
        elif n1_factors[i] > n2_factors[j]:
            j += 1

    return gcf

def __find_factors(n: int) -> list[int]:
    i = 1

    factors = []
    while (i**2 <= n):
        q1 = n/i
        q2 = n//i
        if (q1 == q2):
            factors.append(i)
            factors.append(q2)

        i += 1
    return sorted(factors)
if __name__ == "__main__":
    main()