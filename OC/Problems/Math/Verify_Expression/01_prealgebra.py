"""
Docstring for OC.Problems.Math.Verify_Expression.01_prealgebra

I wrote this script so I can verify my solutions to pre-algebra expressions.
"""

# N digits after the decimal point.
ROUND_TO = 3+1

def main():
    exp = input("Enter expression:\n")
    var_c = input("Enter variable character/s:\n").split()
    val = input("Enter found value/s:\n").split()

    new = rewrite(exp, var_c, val)

    # For debugging
    print(f"Expression: {new}")
    
    terms, signs = __get_exps_signs(new)
    
    if not signs:
        res = __eval_exp_no_sign(new)
    else:
        res = __eval_exp_signs(terms, signs)
    
    print(f"Result: {res}")

    if res:
        print(f"Rounded {ROUND_TO} digits: {round(res, ROUND_TO)}")

def rewrite(exp: str, vars: list[str], vals: list[str]) -> str:
    """Rewrites the expression to be appropriate for passing into `eval`.

    Args:
        exp: The mathematical expression.
        var: The letter/s representing the unknown value/s.
        val: The value/s to be plugged into the variable.

    Returns:
        A cleaned expression where the solution has been plugged in. 

        The new expression is passable to the `eval` function for evaluation.
    """

    # Remove whitespaces from expression.
    new = exp.replace(" ", "")

    # Replace lone equal signs with double equal signs.
    new = __rewrite_eq(new)

    # Rewrite any lone variable like `x` to explicit multiplication like `1*x`.
    new = __rewrite_var(new, vars)

    # Replace caret characters with double-star signs (exponentiation).
    new = __rewrite_expo(new)

    # Rewrite the expression like `2(5)` to explicit multiplication like `2*(5)*1`. 
    new = __rewrite_par(new)


    # new = simplify_exp(new)

    # Replace variable terms with the found term (if possible).
    new = __plug_in_vars(new, vars, vals)

    return new

def __rewrite_eq(exp: str) -> str:
    """Replaces an equation symbol with double equal signs. Does not replace the equal symbol if it's part of an inequality.

    Args:
        exp: The mathematical expression.

    Returns:
        A new expression where every equality is replaced with a double-equal sign.
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

    new += exp[i: len(exp)]
    return new

def __rewrite_var(exp: str, vars: list[str]) -> str:
    """
    Rewrites the expression but explicitly adding a `1*` to any lone variable term.

    Suppports variable terms longer than a single character.

    Args:
        exp: The mathematical expression.
        var: The letter representing the unknown value.

    Returns:
        A copy of the original expression but all the lone variables have an explicit `1*` preceding it.
    """

    if not vars:
        return exp

    # To support adding a 1* to multi-length variables, we have to copy CHUNKS of the expression, as opposed to copying every character individually.
    # Loop through the list of variables.
    for v in vars:
        i = 0
        temp = ""
        v_l = len(v)

        # Find the first instance of the current variable.
        next = exp.find(v, i)
        while (next != -1):

            temp += exp[i: next]
            if (next == 0) or (exp[i-1] == "-") or not (exp[i-1].isnumeric()):
                temp += "1"

            temp += f"*{v}"
            i = next + v_l
            next = exp.find(v, i)
        # After exhausting the variable, replace the original expression with the new expression. `new` variable is reserved for the output of this function.
        temp += exp[i: len(exp)]
        exp = temp

    return exp

def __rewrite_par(exp: str) -> str:
    """Rewrites parentheses in the expression to represent multiplication.

    This function should only be ran AFTER converting all variables to include their coefficient.

    Args:
        expThe mathematical expression.

    Raises:
        SyntaxError: There is an uneven count of open and closed parentheses.

    Returns:
        The mathematical expression with all parentheses rewritten as python multiplication.
    """
    exp = __pad_par(exp)

    exp_l = len(exp)
    new = ""

    for i in range(exp_l):
        if (exp[i] == "("):
            # Add "1" before an opening parenthesis if:
            #   1. The opening parenthesis is at the start.
            if (i == 0):
                new += "1"
            
            # This algorithm should not interfere with parentheses meant for exponentiation.
            elif ((i > 1) and exp[i-2: i] == "**") or (exp[i-1] == "^"):
                new += exp[i]
                continue

            # Add "1" before an opening parenthesis if: 
            #   2. The previous character is a negative sign. OR
            #   3. The previous character is neither a number or a closing parenthesis. 
            #       For expressions like 3+(2) = 3+1*(2) = 5 and -(1) = -1*(1) = -1.
            elif exp[i-1] == "-" or (not (exp[i-1].isnumeric()) and exp[i-1] != ")"): 
                new += "1"

            # Add a multiplication sign before the opening parenthesis.
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
        #   1. We are a closing parenthesis in the middle of the expression, and the next character is a number or an opening parenthesis.
        #   1.1 This also handles parentheses belonging to exponents, making 2**(3)3 = 2**(3)*3
        if (i+1 < exp_l) and (exp[i] == ")") and (exp[i+1].isnumeric()):
            new += "*"

    return new

def __pad_par(exp: str) -> str:
    """Pad the expression with the complementing parenthesis on the side of the lesser parenthesis. 

    This allows evaluation support even if the user passes an expression with partial parentheses.

    Args:
        exp: The mathematical expression.

    Returns:
        A tuple containing the rewritten form of the mathematical expression where the parentheses are have been padded to be equal.
    """
    op = 0
    cp = 0
    new = ""
    stack = []

    # Count the opening and closing parenthesis, as well as constructing the new expression, and count its length.
    for i in range(len(exp)):
        if (exp[i] == "("):
            stack.append(exp[i])
            op += 1

        elif (exp[i] == ")"):
            if (stack) and (stack[-1] == "("):
                stack.pop()
                op -= 1
            else:
                stack.append(exp[i])
                cp += 1

        new += exp[i]
        
    new = f"{'(' * cp}{new}"

    new = f"{new}{')' * op}"

    return new

def __remaining_terms(exp: str, start: int) -> str:
    """Returns the remaining expression from the starting index until the end of the expression.

    Used after terminating a loop.

    Args:
        exp: The mathematical expression.
        start: Index representing the start of the remaining terms.

    Returns:
        The remaining expression from the starting index until the end of the expression.
    """
    return exp[start: len(exp)]

def __get_exps_signs(exp: str) -> tuple[list[str], list[str]]:
    """Returns the expressions between the equality/inequality symbols, and the said symbols, found in the original expression.

    Args:
        exp: The mathematical expression.

    Returns:
        A list of expressions and signs found in the original expression.
    """
    signs = []
    terms = []

    sign = ""
    term = ""
    exp_l = len(exp)
    for i in range(exp_l):
        if (exp[i] == "=" or exp[i] == "<" or exp[i] == ">"):
            sign += exp[i]

            if term:
                terms.append(term)

            term = ""

        else:
            term += exp[i]

        if len(sign) == 2:
            signs.append(sign)
            sign = ""


    return terms, signs

def __eval_exp_signs(terms: list[str], signs: list[str]) -> bool:
    """Evaluation process for when the expression has a sign.

    Args:
        terms: A list of expressions between the signs.
        signs: The sign in the expression.

    Returns:
        The result of the evaluation.
    """

    eval_terms = [eval(t) for t in terms]

    for i in range(len(terms)):
        print(f"Term {i+1}: {eval_terms[i]}")

    # Join the lists together to a new expression. Note the amount of terms is always 1 number higher than the amount of signs.
    new = "".join([f"{t}" + s for t, s in zip(eval_terms, signs)])

    # After joining both lists, add the last term.
    new += terms[-1]

    # Evaluate the expression and return the result.
    res = eval(new)

    return res

def __eval_exp_no_sign(exp: str) -> int | float:
    """Evaluation process for when the expression has no sign.

    Args:
        exp: The mathematical expression.

    Returns:
        The result of the evaluation.
    """
    res = eval(exp)
    return res

def __rewrite_expo(exp: str) -> str:
    """Replace caret characters in the expression with a double-star sign.

    Args:
        exp: The mathematical expression.

    Returns:
        New expression where all caret characters are replaced with a double-star sign.
    """
    new = exp.replace("^", "**")
    return new
# TODO: Add support for simplfiying variable terms (and exponents).
# Ex: 1x + 2x = 3x, x^2 * x^3 = x^5.
def __simplify_exp(exp: str) -> str:
    exp_l = len(exp)
    t_e = {}

    for i in range(exp_l):
        pass

def __get_terms_and_expo(exp: str) -> dict[str, int]:
    exp_l = len(exp)
    t_e = {}
    
    var = ""
    const = ""
    for i in range(exp_l):
        if (exp[i].isnumeric()):
            const += exp[1]
        elif (exp[i].isalpha()):
            pass

def __plug_in_vars(exp: str, vars_: list[str], vals_: list[str]) -> str:
    if (not vars_) or (not vals_):
        return exp

    if len(vals_) != len(vars_):
        raise ValueError(f"Variables ({vars_}) values ({vals_}) are not even.")

    for var, val in zip(vars_, vals_):
        exp = exp.replace(var, f"({val})")

    return exp

if __name__ == "__main__":
    main()