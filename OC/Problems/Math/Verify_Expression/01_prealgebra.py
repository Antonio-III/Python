"""
Docstring for OC.Problems.Math.Verify_Expression.01_prealgebra

I wrote this script so I can verify my solutions to pre-algebra expressions.
"""

# N digits after the decimal point.
ROUND_TO = 3+1

def main():
    exp = input("Enter expression:\n")
    var_c = input("Enter variable character:\n")
    val = input("Enter found value:\n")

    new = rewrite(exp, var_c, val)

    # For debugging
    print(f"Expression: {new}")
    
    terms, sign = __get_terms_sign(new)
    
    if not sign:
        res = __eval_no_sign(terms)
    else:
        res = __eval_sign(terms, sign)
    
    print(f"Result: {res}")

    if res:
        print(f"Rounded {ROUND_TO} digits: {round(res, ROUND_TO)}")

def rewrite(exp: str, var: str, val: str) -> str:
    """Rewrites a mathematical expression where the value of the variable is plugged in.

    Args:
        exp (str): The mathematical expression.
        var (str): The letter representing the unknown value.
        val (str): The value found after solving the equation.

    Returns:
        str: A reformatted expression of the mathematical expression where the solution has been plugged in. It's up to you to put this into the eval function.
    """

    # Remove whitespaces from expression.
    exp = exp.replace(" ", "")

    # Replace lone equal signs with double equal signs.
    new = __rewrite_eq(exp)

    # Rewrite any lone variable (like x) to explicit multiplication (like 1*x).
    new = __rewrite_var(new, var)

    # If multiplication is represented with parentheses, rewrite the expression [like 2(5)] to explicit multiplication [like 2*(5)*1]. 
    new = __rewrite_par(new)

    # Replace variable terms with the found term (if possible).
    if val:
        new = new.replace(var, f"({val})")

    return new

def __rewrite_eq(exp: str) -> str:
    """Replaces an equation symbol with double equal signs. Does not replace the equal symbol if it's part of an inequality.

    Args:
        exp (str): The mathematical expression.

    Returns:
        str: A version of the expression where any `=` is replaced with `==`.
    """
    eq_count = exp.count("=")

    if not eq_count:
        return exp
    
    new = ""
    
    # TODO: Add a step to verify if equality/inequality symbols are valid.

    i = 0

    for _ in range(eq_count):
        
        eq_i = exp.find("=", i)

        new += exp[i: eq_i]

        # For the script to work for equations and inequalities, we only add an extra equal symbol if we are looking at a single equal sign.
        new += "==" if (exp[eq_i-1] != "<") and (exp[eq_i-1] != ">") else "="

        i = eq_i+1

    new += __remaining_terms(exp, i)
    return new


def __rewrite_var(exp: str, var: str) -> str:
    """
    Rewrites the expression but explicitly adding a `1*` to any lone variable term.

    Suppports variable terms longer than a single character.

    Args:
        exp (str): The mathematical expression.
        var (str): The letter representing the unknown value.

    Returns:
        str: A copy of the original expression but all the lone variables have an explicit `1*` preceding it.
    """

    if not var:
        return exp
    
    new = ""

    i = 0

    var_count = exp.count(var)

    # To support adding a 1* to multi-length variables, we have to copy CHUNKS of the expression, as opposed to copying every character individually.

    for _ in range(var_count):
        var_i = exp.find(var, i)

        # Copy the string until it reaches where the variable is or until the end of the string.
        new += exp[i: var_i]

        if (var_i == 0) or (not exp[var_i-1].isnumeric()):
            new += "1"
        
        new += f"*{var}"  

        i = var_i+1

    new += __remaining_terms(exp, i)

    return new

def __rewrite_par(exp: str) -> str:
    """Rewrites parentheses in the expression to represent multiplication.

    This function should only be ran AFTER converting all variables to numeric terms.

    Args:
        exp (str): The mathematical expression.

    Raises:
        SyntaxError: There is an uneven count of open and closed parentheses.

    Returns:
        str: The mathematical expression with all parentheses rewritten as python multiplication.
    """
    exp, exp_l = __pad_par(exp)

    new = ""

    for i in range(exp_l):
        if (exp[i] == "("):
            # Add "1" before an opening parenthesis if:
            #   1. The opening parenthesis is at the start.
            #   2. The previous character is a negative sign.
            #   3. The previous character is NOT a number. 
            #       For expressions like 3+(2) = 3+1*(2) = 5 and -(1) = -1*(1) = -1.
            if (i == 0) or exp[i-1] == "-" or not (exp[i-1].isnumeric()): 
                new += "1"

            # Add a multiplication sign before every opening parenthesis.
            new += "*"

        # Add the current character to the new expression.
        new += exp[i]

        # Add "1" in the expression if:
        #   1. We are in the middle of the expression, and the current character is an opening parenthesis or a negative sign, and the next character is a closing parenthesis. 
        #   1.1 This allows evaluation of expressions like (-) = 1*(-1) = -1.
        # This code block cannot exist alongside the above condition because this block requires the current character to be added to the new expression.
        if (i+1 < exp_l) and ((exp[i] == "(") or (exp[i] == "-")) and (exp[i+1] == ")"):
                new += "1"

        # Add a multiplication sign if:
        #   1. We are in the middle of the expression, and the next character is a number.
        if (i+1 < exp_l) and (exp[i] == ")") and (exp[i+1].isnumeric()):
            new += "*"

    return new

# This returns an int for optimization.
def __pad_par(exp: str) -> tuple[str, int]:
    """Pad the expression with the complementing parenthesis on the side of the lesser parenthesis. This allows evaluation support even if the user passes an expression with partial parentheses.

    Args:
        exp (str): The mathematical expression.

    Returns:
        str: A tuple containing the rewritten form of the mathematical expression where the parentheses are have been padded to be equal, and the length of the new expression. The length value is for optimization for the current use of this function.
    """
    op = 0
    cp = 0
    l = 0
    new = ""

    # Count the opening and closing parenthesis, as well as constructing the new expression, and count its length.
    for c in exp:
        if (c == "("):
            op += 1
        elif (c == ")"):
            cp += 1
        new += c
        l += 1

    # Pad the complementing parenthesis to the new expression.
    if (op < cp):
        diff = cp - op
        new = f"{'(' * diff}{new}"
    elif (op > cp):
        diff = cp - op
        new = f"{new}{')' * diff}"
    
    return new, l


def __remaining_terms(exp: str, start: int) -> str:
    """Returns the remaining expression from the starting index until the end of the expression.

    Used after terminating a loop.

    Args:
        exp (str): The mathematical expression.
        start (int): Index representing the start of the remaining terms.

    Returns:
        str: The remaining expression from the starting index until the end of the expression.
    """
    return exp[start: len(exp)]

# Change this function to get EVERY term between signs.
def __get_terms_sign(exp: str) -> tuple:
    """Returns the terms between the signs, and the signs. If there are no signs, the expression is returned.

    Args:
        exp (str): _description_

    Returns:
        tuple: _description_
    """
    sign = ""
    for c in exp:
        if (c == "=" or c == "<" or c == ">"):
            sign += c
        
    if not sign:
        return exp, ""
    
    return exp.split(sign), sign

def __eval_sign(terms: list, sign: str) -> int | float | bool:
    """Evaluation process for when the expression has a sign.

    Args:
        terms (list): A list of expressions between the signs.
        sign (str): The sign in the expression.
    """
    res = eval(sign.join(terms))

    eval_terms = (eval(t) for t in terms)
    for t in eval_terms:
        print(t)

    return res
def __eval_no_sign(exp: str) -> int | float | bool:
    """Evaluation process for when the expression has no sign.

    Args:
        exp (str): The mathematical expression.
    """
    res = eval(exp)
    return res

# TODO: Add support for caret expressions as exponentiation.
# TODO: Add support for variable operations without knowing its value.
# Ex: 1x + 2x = 3x, x^2 * x^3 = x^5.

if __name__ == "__main__":
    main()