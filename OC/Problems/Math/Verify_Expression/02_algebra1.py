# TODO: Add support for simplfiying variable terms (and exponents).
# Ex: 1x + 2x = 3x and x^2 * x^3 = x^5.

class Term():
    def __init__(self, coeff: float = 0.0, vars: dict[str, int] = {}):
        self.coeff = coeff
        # Dict of letters (str) in descending power
        self.vars = vars

    def str_form(self):
        pass
    def __get_coeff(self):
        int_coeff = int(self.coeff)
        
        return (int_coeff if int_coeff == self.coeff else self.coeff)

    def __get_variables(self):
        vars = ""
        for v in self.vars:
            vars += f"{v}^{self.vars[v]}"
        return vars

    # Only perform on like terms
    def add(self, addend: "Term"):
        if self.vars == addend.vars:
            self.coeff += addend.coeff

    def sub(self, subtrahend: "Term"):
        if self.vars == subtrahend.vars:
            self.coeff -= subtrahend.coeff
    # ---
    
    def mul(self, factor: "Term"):
        self.coeff *= factor.coeff

        for v in factor.vars:
            if (self.vars.get(v)):
                self.vars[v] += factor.vars[v]
            else:
                self.vars[v] = factor.vars[v]

    def div(self, divisor: "Term"):
            self.coeff /= divisor.coeff

            for v in divisor.vars:
                if (self.vars.get(v)):
                    self.vars[v] -= divisor.vars[v]
                else:
                    self.vars[v] = divisor.vars[v]


def __simplify_var_exp(exp: str) -> dict:
    """Simplifies the expression if it contains variables.

    This function is to be ran after some data cleaning process (proper parentheses, explicit coeffs).
    Args:
        exp: _description_

    Returns:
        _description_
    """
    exp = exp.replace("**", "^")
    exp_l = len(exp)
    # Plan to track a term: A list with indices:
    #   0: Sign (str)
    #   1: Coefficient (float)
    #   2: Variables (dict) letters (ascending) powers (int)

    # ALT 
    # A dict with the FULL variables concatenated (str) as the KEY and its values are a list with indices:
    # 0: Sign (Str)
    # 1: Coefficient (float)

    # ALT 2
    # A dict with keys:
    # "Sign": str
    # "Coeff": float
    # "Variables": list[str]
    # "Exponents": list[int]
    
    # Adding or subtracting variable "like terms" is to perform +- operations on their coefficients.
    # Multiplying or div. variable "like terms" is to perform */ on their coefficients AND their integer powers.
    
    return {}

def get_terms_and_signs(exp: str) -> tuple[list[str], list[str]]:


    if not exp:
        return ([""], [""])
    new = ""
    
    if exp[0] != "+" or exp[0] != "-":
        new += "+"
    terms = []
    signs = []
    pass