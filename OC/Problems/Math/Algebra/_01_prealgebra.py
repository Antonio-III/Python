"""
I wrote this script so I can verify my solutions to pre-algebra expressions.
"""

from math import sqrt

# N digits after the decimal point.
ROUND_TO = 3+1
SPEC_CHAR = "?"

SPEC_CMDS = ["\\sqrt", "\\frac"]
SPEC_CMDS_FUNC = ["sqrt"]

def main():
    exp, var_c, val = get_inputs()

    new = rewrite(exp, var_c, val)

    # For debugging
    print(f"Expression: {new}")
    
    terms, signs = get_exps_btween_eqsigns(new)
    
    if not signs:
        res = eval(new)
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
    exp = __rewrite_eq(exp)

    terms, signs = get_exps_btween_eqsigns(exp)

    terms_new = []
    for term in terms:
        term = __pad_par(term)
        terms_new.append(term)

    new = "".join([f"{t}" + s for t, s in zip(terms_new, signs)])
    new += terms_new[-1]

    new = __plug_in_vars(new, vars, vals)

    new = clean_exp(new)

    new = replace_spec_cmds(new)

    # This is the only way to represent multiplication because I want this script to 
    # support multi-character variables.
    new = __rewrite_par(new)

    __check_unplugged_vars(new)

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
    **DEPRECATED**

    Rewrites the expression but explicitly adding a multiplication sign to any lone variable term.

    For instance, `x` becomes `1*x` and `3y` becomes `3*y`.
    Suppports variable terms longer than a single character.

    Args:
        exp: The mathematical expression.
        var: The letter representing the unknown value.

    Returns:
        A copy of the original expression but all the lone variables have an explicit `1*` preceding it.
    """

    if not vars:
        return exp

    new = exp

    # To support adding a 1* to multi-length variables, we have to copy CHUNKS of the expression, as opposed to copying every character individually.
    # Loop through the list of variables.
    for v in vars:
        i = 0
        temp = ""
        v_l = len(v)

        # Find the first instance of the current variable.
        next = new.find(v, i)
        while (next != -1):

            temp += new[i: next]
            if (next == 0) or (new[i-1] == "-") or not (new[i-1].isnumeric()):
                temp += "1"

            temp += f"*{v}"
            i = next + v_l
            next = new.find(v, i)

        temp += exp[i: len(exp)]
        new = temp

    return new

def __rewrite_par(exp: str) -> str:
    """Rewrites parentheses in the expression to represent multiplication (if applicable).

    Example: `2(5)` becomes `2*(5)`. But `1+(2)` remains as `1+(2)`.

    **Assumes the variables have been plugged in and has correct parentheses.**

    Args:
        exp: The mathematical expression.

    Returns:
        The mathematical expression with all parentheses rewritten as multiplication.
    """
    exp_l = len(exp)

    new = ""

    for i in range(exp_l):
        # When encountering an opening parenthesis,
        if (exp[i] == "("):
            # Add a multiplication sign if the last character in the new string is a number.
            if (i > 0) and ((new[-1].isnumeric())):
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

    **The input assumes that all brackets are converted to parentheses.**

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

    # Join the lists together to a new expression. The amount of terms is always 1 number higher than the amount of signs.
    new = "".join([f"{t}" + s for t, s in zip(eval_terms, signs)])

    # After joining both lists, add the last term.
    new += terms[-1]

    # Evaluate the expression and return the result.
    return eval(new)

def eval_exp_no_sign(exp: str) -> int | float:
    """**DEPRECATED**

    Evaluation process for when the expression has no eq/inequality sign.

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
    """Plugs in the values for the inputted variables.

    Args:
        exp: The mathematical expression.
        vars_: A list of variables.
        vals_: A list of the variable's value.

    Raises:
        ValueError: Inputted variables and their values are uneven.

    Returns:
        The expression where all variables are plugged in.
    """
    if (not vars_) or (not vals_):
        return exp

    if (len_vals:=len(vals_)) != (len_vars:=len(vars_)):
        raise ValueError(f"Expected {len_vals} variables values but {len_vars} plugged.")

    # Associate the variables with their values.
    # This allows variables like `a` and and `aa` to be distinct.
    mapped = {}
    for var, val in zip(vars_, vals_):
        mapped[var] = val
    
    masked = mask_spec_cmds(exp)
    for val in sorted(mapped, reverse=True):
        masked = masked.replace(val, f"({mapped[val]})")

    exp = merge_mask(exp, masked)
    return exp

def __replace_sqrt(exp: str) -> str:
    """Replaces all square root commands to a function call to `math.sqrt`. 

    `sqrt`, when empty, roots the number 1.

    Args:
        exp: The mathematical expression.

    Returns:
        The mathematical expression with all instances of square root commands replaced function calls to `sqrt`.
    """
    exp = mask_spec_cmds(exp, "sqrt")

    new = ""
    i = 0
    while ((sign := exp.find(SPEC_CHAR, i)) != -1):
        new += exp[i:sign]

        num = __get_sub_exp(exp, sign+1)

        new += f"(sqrt({num}))"
        i = sign + 1 + len(num)

    if (i < (exp_l:=len(exp)) ):
        new += exp[i: exp_l]

    return new

def __get_sub_exp(exp: str, i: int) -> str:
    """Returns the sub-expression starting at the index `i`. The sub expression can be a number (whole or decimal) or an expression that starts and stops with a parenthesis.

    Args:
        exp: The mathematical expression.
        i: Starting point of the sub-expression.
    """
    if exp[i] != "(":
        return __get_num(exp, i)

    sub_exp = "("
    op = 1
    for c in exp[i+1::]:
        if (c == "("):
            op += 1
        elif (c == ")"):
            op -= 1

        sub_exp += c

        if op == 0:
                break

    return sub_exp

def __get_num(exp: str, i: int) -> str:
    """Returns the number starting at index `i`.

    Args:
        exp: The mathematical expression.
        i: Starting position (0-indexed).
    """
    num = ""
    for c in exp[i::]:
        if (c.isnumeric()) or (c == "."):
            num += c
        else:
            break
    return num

def __replace_brackets(exp: str) -> str:
    """Replaces curly- and L-brackets with parentheses.

    Args:
        exp: The mathematical expression.

    Returns:
        The mathemematical expression but all its brackets are now parentheses.
    """
    OP = "("
    ED = ")"

    new = exp

    new = new.replace("{", OP).replace("}", ED)
    new = new.replace("[", OP).replace("]", ED)

    return new

def replace_spec_cmds(exp: str) -> str:
    """Changes commands (the ones starting with a back-slash) to a value that can be evaluated on. For instance, \\sqrt becomes a function call instead.

    Args:
        exp: The mathematical expression.

    Returns:
        The mathematical expression with all back-slash commands replaced with its proper notation.
    """
    # TODO: Update this to a more generalized function, so I don't have to update this function by putting more and more function calls. Below is a template.
    # new = exp
    # for spec in SPEC_CMDS:
    #     new = replace_cmd(new, spec)
    # return new
    new = __replace_sqrt(exp)
    new = __replace_frac(new)
    return new

def get_inputs() -> tuple[str, list[str], list[str]]:
    exp = input("Enter expression:\n")
    var_c = input("Enter variable character/s:\n").split()
    val = input("Enter found value/s:\n").split()

    # Input cleaning
    val = clean_val(val)
    notify_updated_val(val)
    # ---

    return exp, var_c, val

def clean_val(val: list[str]) -> list[str]:
    """Cleans the inputted values so it's ready for evaluation.

    This function is separated because 
    Args:
        val: A list of inputted values.

    Returns:
        A list of inputted values, but cleaner.
    """
    new_val = []

    for val_ in val:
        new = clean_exp(val_)
        new_val.append(new)

    return new_val

def notify_updated_val(val: list[str]) -> None:
    """Prints the updated values in `val`.

    Args:
        val: A list of potential value/s for the variable/s.
    """
    print("Variable values updated to:")
    for exp in val:
        print(f"{exp}")

def __replace_frac(exp: str) -> str:
    """Represents the `\\frac` special command as a division operation between dividend and divisor.

    Args:
        exp: The mathematical expression with a `\\frac` command.

    Returns:
        The expression but its `\\frac` commands represented properly.
    """
    exp = mask_spec_cmds(exp, "frac")

    new = ""
    i = 0
    while ((sign := exp.find(SPEC_CHAR, i)) != -1):
        new += exp[i:sign]
        
        num = __get_sub_exp(exp, sign+1)
        i = sign + 1 + len(num)

        den = __get_sub_exp(exp, i)
        i += len(den)

        new += f"{num}/{den}"

    if (i < (exp_l:=len(exp)) ):
        new += exp[i: exp_l]

    return new

def __check_unplugged_vars(exp: str) -> None:
    """Checks the expression for unplugged variables. Raises error if found.

    Args:
        exp: The mathematical expression.

    Raises:
        ValueError: An unplugged variable was found.
    """
    # Replace all function calls to a special character.
    temp = exp
    temp = mask_func_calls(temp, eq_len=True)

    for i in range(len(temp)):
        try:
            assert not (temp[i].isalpha())
        except AssertionError as e:
            _msg = f"Variable with unknown value: {temp}"
            msg = err_msg("ValueError", _msg, exp, i, True)
            raise ValueError(msg) from e

def err_msg(err: str, msg: str, exp: str, i: int=0, char: bool=False) -> str:
    """Error message formatter.

    The error message shows where in the expression did the error occur.

    Args:
        err: String literal for the name of the error (Per Python).
        msg: The error message (Per Python).
        exp: The mathematical expression.
        i: The index for where the error occurred. Defaults to 0.
        char: Flag for whether the error is a character or a sub-expression. Defaults to False.

    Returns:
        The formatted error message.
    """
    padding = len(err) + 2 + len(msg) - (len(exp) - i - 1) - 1
    caret = '^' * (1 if char else len(exp[i::]))

    return f"{msg}\n{'~' * padding}{caret}"

def correct_exp_in_spec_commands(exp: str) -> str:
    """Correct the parentheses count of the expression inside the curly brackets of special commands.

    **The input is assumed to contain curly brackets for special commands.**

    Args:
        exp: The mathematical expression that contains special commands.
    """
    start = stop = i = 0
    new = ""

    while ( ((start:= exp.find("{", start)) != -1) and ((stop:= exp.find("}", stop)) != -1) ):
        new += exp[i: start]
        new += __pad_par(exp[start: stop+1])
        i = stop + 1
        
        start += 1
        stop += 1

    if i < (exp_l:= len(exp)):
        new += exp[i: exp_l]

    return new


def mask_spec_cmds(exp: str, cmd: str = "", eq_len: bool = False) -> str:
    """Replaces special commands with a question mark character (`?`).

    **The input is assumed to have the correct amount of parentheses.**

    Args:
        exp: The mathematical expression that contains a special command.
        cmd: The command that will be masked. If cmd is not given, then all commands will be masked.
        eq_len: Flag for whether the mask will be as long as the length of the special command (excluding its brackets). The mask is 1 character by default.

    Returns:
        The new expression with all special commands replaced with `?`.
    """
    if not cmd:
        for cmd_ in SPEC_CMDS:
            len_ = len(cmd) if eq_len else 1
            exp = exp.replace(cmd_, SPEC_CHAR*len_)
        return exp

    len_ = (len(cmd)+2) if eq_len else 1
    return exp.replace(f"\\{cmd}", SPEC_CHAR)

def mask_func_calls(exp: str, eq_len: bool = False) -> str:
    """Replace function calls (only its characters) with a question mark (`?`).

    **The input is assumed to have the correct amount of parentheses.**

    This allows having variables that use the same characters as the special commands. For instance, `t` can be a variable even when `sqrt` is in the expression.

    Args:
        exp: The mathematical expression containing function calls.
        eq_len: Flag for whether the mask will be as long as the length of the special command (excluding its brackets). The mask is 1 character long by default.

    Returns:
        The mathematical expression but all its function calls are hidden.
    """
    for f in SPEC_CMDS_FUNC:
        len_ = len(f) if eq_len else 1
        exp = exp.replace(f, SPEC_CHAR*len_)
    return exp

def merge_mask(exp: str, exp_masked: str) -> str:
    """Updates the mathematical expression with the plugged values.

    This function was created so that inputs like `\\sqrt4+t`, `t=1` does not become `\\sqr(1)+(1)`.
    Args:
        exp: The mathematical expression.
        exp_masked: The masked mathematical expression (special commands are hidden).

    Returns:
        An updated expression where all plugged values and special commands are in a single expression.
    """
    new = ""
    for i in range(len(exp_masked)):
        if (exp_masked[i] == SPEC_CHAR):
            cmd = __get_nearest_cmd(exp, i)
            new += cmd
            continue
        new += exp_masked[i]

    return new

def clean_exp(exp: str) -> str:
    """Processes the mathematical expression so that its notation is clear for Python evaluation.

    Args:
        exp: The mathematical expression.

    Returns:
        The mathematical expression but it's notation is standardized.
    """
    # Remove whitespaces from expression.
    new = exp.replace(" ", "")

    new = correct_exp_in_spec_commands(new)

    # Standardize brackets.
    new = __replace_brackets(new)

    # Replace caret characters with double-star signs (exponentiation).
    new = __rewrite_expo(new)

    return new

def __get_nearest_cmd(exp: str, i: int) -> str:
    """Obtains the nearest command starting at index `i`.

    _extended_summary_

    Args:
        exp: The mathematical expression with a special command.
        i: The starting point of the search.

    Returns:
        The special command nearest to `i`.
    """
    j = 0
    cmd = ""
    for cmd_ in SPEC_CMDS:
        if (k := exp.find(cmd_, i)) != -1:
            if (j == 0):
                j = k
                cmd = cmd_
            elif (k < j):
                j = k
                cmd = cmd_
    return cmd

if __name__ == "__main__":
    main()