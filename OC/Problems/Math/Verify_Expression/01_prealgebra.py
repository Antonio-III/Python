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
    print(f"Expression: {new}")

    
    res = eval(new)
    print(f"Result: {res}\nRounded {ROUND_TO} digits: {round(res, ROUND_TO)}")


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

# TODO: Support nested parentheses expressions.
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
    new = ""

    open_par = exp.count("(")
    closed_par = exp.count(")")

    if (open_par != closed_par):
        raise SyntaxError(f"Invalid parenthesis count: {open_par} open: {closed_par} closed")

    i = 0

    open_par_i = exp.find("(")
    close_par_i = exp.find(")")

    # O(n^2). Need to be reduced to O(n) time.
    for _ in range(open_par):
        new += exp[i: open_par_i]

        # Append "1" when encountering open parenthesis.
        if (open_par_i == 0) or not (exp[open_par_i-1].isnumeric()):
            new += "1"

        # Append term between parentheses with multiplication signs on both ends of the term. Parentheses are kept.
        new += f"*({__n_in_par(exp, open_par_i, close_par_i)})*"

        # Append "1" when encountering closed parenthesis.
        if (close_par_i+1 == len(exp)) or not (exp[close_par_i+1].isnumeric()):
            new += "1"
    
        i = close_par_i+1

        open_par_i = exp.find("(", open_par_i+1)
        close_par_i = exp.find(")", close_par_i+1)

    # Append remaining terms after dealing with all the parentheses.
    new += __remaining_terms(exp, i)

    return new

def __n_in_par(exp: str, open_par_i: int, close_par_i: int) -> str:
    """Returns the expression between the opening and closing parenthesis.

    Args:
        exp (str): The mathematical expression.
        open_par_i (int): Index of the opening parenthesis.
        close_par_i (int): Index of the closing parenthesis.

    Returns:
        str: The expression between the opening and closing parenthesis.
    """
    return exp[open_par_i+1 : close_par_i]

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

# TODO: Add support for caret expressions as exponentiation.
# TODO: Add support for variable operations without knowing its value.
# Ex: 1x + 2x = 3x, x^2 * x^3 = x^5.

if __name__ == "__main__":
    main()