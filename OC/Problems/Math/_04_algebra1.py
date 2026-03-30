from _01_prealgebra import __pad_par, __rewrite_par

# TODO: Add support for simplfiying variable terms (and exponents).
# Ex: 1x + 2x = 3x and x^2 * x^3 = x^5.
def main():
    if (not (exp := input("Enter expression:\n"))):
        raise ValueError("Invalid expression.")

    out = clean_exp(exp)
    out = parse_exp_v2(out)
    print(out)

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

        if (isinstance(self.div, term)):
            denominator = f"{self.div.str_form()}"
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
    
    def __str__(self):
        return self.str_form()
    def __repr__(self):
        return f"term(coeff={self.coeff}, vars={self.vars}, div={self.div})"
        # return self.str_form()

# Feature to turn an expression into a term class (WIP)
# Ex: "5x^2" becomes a term class with ceoff = 5, var = {"x": 2}, div = 1.

# Future update: Polynomial class whose values are on a list of term classes.
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

def parse_exp(exp: str) -> list[term]:
    
    terms_indices = __separate_terms(exp)
    terms_l = []
    for (start, end) in terms_indices:
        curr_term = exp[start: end]

        coeff = __parse_coeff(curr_term)
        vars = __parse_vars(curr_term)
        div = __parse_div(curr_term)
        
        terms_l.append(term(coeff, vars, div))

    return terms_l

def parse_exp_v2(exp: str) -> list[term]:
    
    terms = exp.split("+")
    terms_l = []
    for t in terms:
        t = t.strip("()")
        coeff = __parse_coeff(t)
        vars = __parse_vars(t)
        div = __parse_div(t)
        
        terms_l.append(term(coeff, vars, div))

    return terms_l

def __parse_coeff(exp:str) -> int:
    """Turns the coefficient in the expression to an integer. Expression must be sorted.

    _extended_summary_

    Args:
        exp: The mathematical expression.

    Returns:
        The string of numbers at the front of the expression (coefficient).
    """
    exp_l = len(exp)
    coeff = ""
    for i in range(exp_l):
        if exp[i].isnumeric() or exp[i] == "-" or exp[i] == "+":
            coeff += exp[i]
        else:
            break
    return int(coeff)

def __parse_div(exp: str):
    i = exp.find("/")
    
    if (i == -1):
        return 1

    coeff = __parse_coeff(exp[i+1])
    vars  = __parse_vars(exp[i+1])

    t = term(coeff, vars)
    return t

def __separate_terms(exp: str):
    exp_l = len(exp)

    terms = []
    sub_term = []

    start = 0
    end = 0

    for i in range(exp_l):
        # At start of expression, append the starting term
        if i == 0:
            start = i
            sub_term.append(start)

        # In the middle, append the ending of the initial term,
        # and append the new starting term
        elif (exp[i] == "+") or (exp[i] == "-"):
            start = end = i
            sub_term.append(end)

            if (len(sub_term) == 2):
                terms.append(sub_term)

                sub_term = []

                sub_term.append(start)

        # At the end, append the last term's substring
        if i+1 == exp_l:
            sub_term.append(exp_l)
            terms.append(sub_term)

    return terms


def __separate_terms_v2(exp: str) -> list[str]:
    i = 0
    exp_l = len(exp)
    terms_l = []
    curr_t = ""

    in_par = False

    while (i < exp_l):
        curr_c = exp[i]
        if (curr_c == "+") and not in_par:

            terms_l.append(curr_t)
            curr_t = ""
            i += 1
            continue

        elif curr_c == "(":
            in_par = True

        elif curr_c == ")":
            in_par = False

        curr_t += curr_c

        if (i+1 == exp_l):
            terms_l.append(curr_t)
            curr_t = ""

        i += 1

    return terms_l

def __rewrite_diff_to_neg(exp: str):
    """Replaces all instances of subtraction as an addition of a negative number in the expression.

    Example: `2-6` becomes `2+(-6)`.

    Args:
        exp: The mathematical expression.

    Returns:
        New expression where all subtraction is an addition of a negative number.
    """
    exp_l = len(exp)
    
    new = ""
    open_par = False

    i = 0

    while (i < exp_l):
        curr = exp[i]

        if i > 0:
            if (open_par) and ((curr == "+") or (curr == "-")):
                new += ")"
                open_par = False

            if (curr == "-") and exp[i-1].isalnum():
                new += "+("
                open_par = True
                if exp[i+1] == "(":
                    i += 1

        new += curr

        if (curr == ")"):
            open_par = False

        if (i+1 == exp_l) and open_par:
            new += ")"
            open_par = False

        i += 1
    return new

def __rewrite_neg_to_diff(exp: str) -> str:
    """Rewrites addition of negative numbers as subtraction of positive numbers.

    Example: `2+(-6)` becomes `2-6`.

    Args:
        exp: The mathematical expression.

    Returns:
        The mathematical expression where all addition of negative numbers are rewritten as subtraction of positive numbers.
    """
    exp_l = len(exp)
    
    new = ""

    i = 0
    addend_2 = ""
    while i < exp_l:
        curr = exp[i]

        if (curr == "+" and exp[i+1] == "(" and exp[i-1].isalnum()):
            addend_2 += exp[i+2]
            i += 3
            continue

        if (curr == ")") and (addend_2):
            if ("-" in addend_2):
                new += addend_2
                addend_2 = ""
                i += 1
                continue

        if (not addend_2):
            new += curr
        else:
            addend_2 += curr

        i += 1
    return new

def __rewrite_db_neg_to_pos(exp: str) -> str:
    """Rewrites subtraction of a negative number as an addition of a positive number.

    Args:
        exp: The mathematical expression.

    Returns:
        The mathematical expression but all instances of double negatives are replaced with addition of a positive number.
    """
    exp_l = len(exp)
    
    new = ""

    i = 0

    while i < exp_l:
        curr = exp[i]

        if (i > 0) and (i+3 < exp_l):
            if (curr == "-" and exp[i+1: i+3] == "(-") and exp[i-1].isalnum():

                new += f"+{exp[i+3]}"
                i += 4
                continue
        

        new += curr

        i += 1
    return new

def clean_exp(exp: str) -> str:
    new = exp.replace(" ", "")
    new = __rewrite_par(new)
    new = __rewrite_db_neg_to_pos(new)
    new = __rewrite_diff_to_neg(new)

    return new
def __is_neg(exp: str) -> bool:
    return "-" in exp

# ---

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
    while ((i < n1_flen) and (j < n2_flen)):
        if (n1_factors[i] == n2_factors[j]):
            gcf = n1_factors[i]
            i += 1
            j += 1
            continue

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