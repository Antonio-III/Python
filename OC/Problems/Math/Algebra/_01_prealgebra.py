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
    
    terms, signs = get_exps_btween_eqsigns(new)
    
    if not signs:
        res = eval_exp_no_sign(new)
    else:
        res = eval_exp_signs(terms, signs)
    
    print(f"Result: {res}")

    if (type(res) != bool):
        print(f"Rounded to {ROUND_TO} digits: {round(res, ROUND_TO)}")

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

    # Replace variable terms with the found term (if possible).
    new = __plug_in_vars(new, vars, vals)

    # Replace lone equal signs with double equal signs.
    new = __rewrite_eq(new)

    # Rewrite any lone variable like `x` to explicit multiplication like `1*x`.
    new = __rewrite_var(new, vars)

    # Replace caret characters with double-star signs (exponentiation).
    new = __rewrite_expo(new)

    # Rewrite the expression like `2(5)` to explicit multiplication like `2*(5)`. 
    new = __rewrite_par(new)

    return new

def __rewrite_eq(exp: str) -> str:
    """Replaces single equation symbols with double-equal signs. Does not replace the equal symbol if it's part of an inequality or if the equality is already double-signed.

    Args:
        exp: The mathematical expression.

    Returns:
        A new expression where every equality is replaced with a double-equal sign.
    """
    new = ""

    exp_l = len(exp)

    for i in range(exp_l):
        if (exp[i] == "=") and (i > 0) and (i+1 < exp_l):
            if (exp[i+1] != "=") and (exp[i-1] != "=") and (exp[i-1] != "<") and (exp[i-1] != ">"):
                new += "="
        new += exp[i]

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
    """Rewrites parentheses in the expression to represent multiplication (if applicable).

    Example: `2(5)` becomes `2*(5)`. But `1+(2)` remains as `1+(2)`.

    Args:
        exp: The mathematical expression.

    Returns:
        The mathematical expression with all parentheses rewritten as multiplication.
    """
    exp = __pad_par(exp)
    exp_l = len(exp)

    new = ""

    for i in range(exp_l):
        # When encountering an opening parenthesis,
        if (exp[i] == "("):
            # Add a multiplication sign if the last character in the new string is a number.
            if (new[-1].isnumeric()):
                new += "*"

        # Add the current character to the new expression.
        new += exp[i]

        if (i+1 < exp_l): 
            # Add "1" in the expression if we are in an empty parenthesis.
            # This allows evaluation of expressions like (-) = 1*(-1) = -1.
            if ((exp[i] == "(") or (exp[i] == "-")) and (exp[i+1] == ")"):
                new += "1"
            # Add a multiplication sign if we are a closing parenthesis, and the next character is a number or an opening parenthesis.
            #   This also handles parentheses belonging to exponents, making 2**(3)3 = 2**(3)*3.
            elif (exp[i] == ")") and (exp[i+1].isnumeric() or (exp[i+1] == "(")):
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

    # Track the opening and closing parenthesis through a stack, as well as constructing the new expression.
    for i in range(len(exp)):
        if (exp[i] == "("):
            stack.append(exp[i])
            op += 1

        elif (exp[i] == ")"):
            # When encountering a closed parenthesis, we check if we find a match in the parenthesis stack.
            # If a match is found, we pop the corresponding opening parenthesis, and update its count.
            # If no match, add the closed parenthesis to the stack, and update its count.
            if (stack) and (stack[-1] == "("):
                stack.pop()
                op -= 1
            else:
                stack.append(exp[i])
                cp += 1

        new += exp[i]

    # After constructing the new expression, we pad the expression with the complementing parenthesis based on the count of the opposing parenthesis (like pad the expression with opening parentheses for the same amount of times as the remaining closing parenthesis in the stack). Opening parenthesis will always be at the start and closing parenthesis at the end.
    new = f"{'(' * cp}{new}"
    new = f"{new}{')' * op}"

    return new

def get_exps_btween_eqsigns(exp: str) -> tuple[list[str], list[str]]:
    """Returns the expressions between the equality/inequality symbols and the symbols, found in the original expression.

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

        if (i+1) == exp_l:
            terms.append(term)
            term = ""

    return terms, signs

def eval_exp_signs(terms: list[str], signs: list[str]) -> bool:
    """Evaluation process for when the expression has an eq-inequality symbol.

    Args:
        terms: A list of expressions between the signs.
        signs: The sign in the expression.

    Returns:
        A boolean as result of the evaluation.
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

def eval_exp_no_sign(exp: str) -> int | float:
    """Evaluation process for when the expression has no eq/inequality sign.

    Args:
        exp: The mathematical expression.

    Returns:
        A number as result of the evaluation.
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


def __plug_in_vars(exp: str, vars_: list[str], vals_: list[str]) -> str:
    if (not vars_) or (not vals_):
        return exp

    if len(vals_) != len(vars_):
        raise ValueError(f"Expected ({vars_}) values but ({vals_}) plugged.")

    for var, val in zip(vars_, vals_):
        exp = exp.replace(var, f"({val})")

    return exp

if __name__ == "__main__":
    main()