# TODO: Add support for simplfiying variable terms (and exponents).
# Ex: 1x + 2x = 3x and x^2 * x^3 = x^5.
def main():
    # if (not (coeff := input("Enter coefficient:\n"))) or (not coeff.isnumeric()):
    #     raise ValueError("Coefficient is not numeric.")

    # if (not (vars := input("Enter variables (including exponents):\n"))):

    #     raise ValueError("Invalid input.")
    t1 = Term("2", "x^3y^9z^2")
    t2 = Term("-7", "x^7y^4z^3")
    t3 = Term("2", "x^6y^3z^7")
    t1.multiply(t2)
    t1.multiply(t3)
    print(t1.str_form())

class Term():
    def __init__(self, coeff_str: str = "", vars_str: str = ""):
        self.coeff = self.__parse_coeff(coeff_str)
        self.vars = self.__parse_vars(vars_str)

    def str_form(self) -> str:
        return f"{self.__get_coeff()}{self.__get_variables()}"

    def __get_coeff(self) -> int | float:
        int_coeff = int(self.coeff)

        return (int_coeff if (self.coeff == int_coeff) else self.coeff)

    def __get_variables(self) -> str:
        vars_str = ""
        for v in self.vars.keys():
            # Show variables AND their exponents 
            if self.vars[v] > 1:
                vars_str += f"{v}^{self.vars[v]}"
            else:
                vars_str += f"{v}"

        return vars_str
    
    def __record_vars(self, vars_str: str) -> tuple[list[str], list[int]]:
        """Step 1 of parsing the variables from a string. Records variables and exponents into separate lists.

        Args:
            vars_str: The Term's variables in string form.

        Returns:
            A list of variables and a list of their corresponding exponents.
        """

        variables_l = []
        exponents_l = []

        vars_len = len(vars_str)

        exponent_counter = ""
        
        for i in range(vars_len):
            curr = vars_str[i]

            if curr.isalpha():
                variables_l.append(curr)

                if exponent_counter:
                    exponents_l.append(int(exponent_counter))
                    exponent_counter = ""

                if (i+1 == vars_len) or (vars_str[i+1] != "^"):
                    exponents_l.append(1)


            elif curr.isnumeric():
                exponent_counter += curr

                if (i+1 == vars_len):
                    exponents_l.append(int(exponent_counter))

        return variables_l, exponents_l

    def __parse_vars(self, vars_str: str) -> dict[str, int]:
        """Step 2 (last) of parsing the variables from a string. Creates a dict to store the variables and their respective exponents. The dict is sorted.

        Args:
            vars_str: The Term's variables in string form.

        Returns:
            The dictionary contaning the variables (Keys) and their exponents (Value).
        """
        vars_d = {}
        variables_l, exponents_l = self.__record_vars(vars_str)

        for v, e in zip(variables_l, exponents_l):
            vars_d[v] = e

        return dict(sorted(vars_d.items()))

    def __parse_coeff(self, coeff_str: str) -> int | float:
        """Step 1 (Last) of parsing the coefficient.

        Args:
            coeff_str: The Term's coefficient in string form.

        Returns:
            The coefficient in int or float form.
        """
        int_coeff = int(coeff_str)
        float_coeff = float(coeff_str)

        return (int_coeff if (int_coeff == float_coeff) else float_coeff)
    
    # Only perform on like terms
    def add(self, addend: "Term"):
        if self.vars == addend.vars:
            self.coeff += addend.coeff
        
    def subtract(self, subtrahend: "Term"):
        if self.vars == subtrahend.vars:
            self.coeff -= subtrahend.coeff
    # ---

    def multiply(self, factor: "Term"):
        self.coeff *= factor.coeff

        for v in factor.vars:
            if (self.vars.get(v)):
                self.vars[v] += factor.vars[v]
            else:
                self.vars[v] = factor.vars[v]

    def divide(self, divisor: "Term"):
            self.coeff /= divisor.coeff

            for v in divisor.vars:
                if (self.vars.get(v)):
                    self.vars[v] -= divisor.vars[v]
                else:
                    self.vars[v] = divisor.vars[v]


if __name__ == "__main__":
    main()