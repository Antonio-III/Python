"""
Docstring for OC.Problems.Math.Verify_Expression.01_prealgebra

I wrote this script so I can verify my solutions to pre-algebraic equations without having to do it mentally.
"""

def main():
    exp = input("Enter expression:\n")
    var_c = input("Enter variable character:\n")
    val = input("Enter found value:\n")

    new = rewrite(exp, var_c, val)

    print(new)
    print(eval(new))

def rewrite(exp: str, var_c: str, val: str) -> str:
    """
    Rewrites a mathematical expression where the value of the variable is plugged in. 
    
    :param exp: The mathematical expression.
    :type exp: str
    :param var_c: The letter representing the unknown value.
    :type var_c: str
    :param val: The value found after solving the equation.
    :type val: str
    :return: A reformatted expression of the mathematical expression where the solution has been plugged in, to be passed to `eval()` function.
    :rtype: str
    """
    # Make an empty string.
    new = ""
    
    # Loop through original string.
    for i, char in enumerate(exp):
        
        # When encountering variable term with no coeff, add a 1 before copying the term.
        if char == var_c:
            
            # There are 2 places where a coeff-less variable might appear: in the beginning or in the middle of the expression:
            # If it's in the beginning, we add a 1 to variable because if it had a coeff, it would be in the middle of the expression.
            # If it's in the middle, we check for the previous char to see if the variable is indeed coeff-less.
            if i == 0 or not (exp[i-1].isnumeric()):
                new += "1"  
        
        # Copy the characer to new string.
        new += char
    
    # In python, equality symbol is "==" as opposed to "=".
    new = new.replace("=", "==")
    
    # Replace any instances of the variable with the found value.
    new = new.replace(var_c, f"*({val})")    

    return new

if __name__ == "__main__":
    main()