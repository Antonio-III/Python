"""
Docstring for OC.Problems.Math.Verify_Expression.01_prealgebra

I wrote this script so I can verify my solutions to pre-algebraic equations without having to do it mentally.
"""

# N digits after the decimal point.
ROUND_TO = 3

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

    if (not var) or (not val):
        return exp
    
    new_eq = rewrite_eq(exp)
    new_var = rewrite_var(new_eq, var)
    
    new_exp = new_var.replace(var, f"({val})")

    return new_exp

def rewrite_eq(exp: str) -> str:
    """Replaces an equation symbol with double equal signs. Does not replace the equal symbol if it's part of an inequality.

    Args:
        exp (str): The mathematical expression.

    Returns:
        str: A version of the expression where any `=` is replaced with `==`.
    """
    new = ""

    for i, char in enumerate(exp):
        # For the script to work for equations and inequalities, we only add an extra equal symbol if we are looking at a single equal sign.
        if char == "=":
            if (exp[i-1] != "<") and (exp[i-1] != ">"):
                new += "="
    
        new += char
    return new


def rewrite_var(exp: str, var: str) -> str:
    """
    Rewrites the expression but explicitly adding a `1*` to any lone variable term. Suppports variable terms longer than a single character.

    Args:
        exp (str): The mathematical expression.
        var (str): The letter representing the unknown value.

    Returns:
        str: A copy of the original expression but all the lone variables have an explicit `1*` preceding it.
    """
    prev_var = 0
    next_var = exp.find(var)

    var_count = exp.count(var)

    new = ""

    # To support adding a 1* to multi-length variables, we have to copy CHUNKS of the expression, as opposed to copying every character individually.

    for _ in range(var_count):
        next_var = exp.find(var, prev_var)

        

        # Copy the string until it reaches where the variable is or until the end of the string.
        new += exp[prev_var: next_var]

        if (next_var == 0) or (not exp[next_var-1].isnumeric()):
            new += "1*"
        
        
        prev_var = next_var

    new += exp[prev_var: len(exp)]

    return new

if __name__ == "__main__":
    main()