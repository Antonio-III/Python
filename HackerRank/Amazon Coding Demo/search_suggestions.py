def search_suggestions(repository: list[str], customer_query: str) -> list[list[str]]:
    """
    Amazon Customer Reviews

    Write an algorithm that will output a maximum of 3 keyword suggestions after each character is typed by the customer in the search field.

    - If there are more than 3 acceptable keywords, return the keywords that are first in alphabetical order. 
    - Only return keyword suggestions after the customer has entered at least 2 characters.
    - Keyword suggestions must start with the characters already typed.
    - Both the repository and customer_query should be compared in a case-insensitive way.

    Input
        The input method/function consists of 2 arguments:
        `repository`, a list of unique strings representing the various keywords from the Amazon review comment section;
        `customer_query`, a string representing the full search query of the customer.

    Output
        Return a list of strings in lower case, where each list represents the keyword suggestions made by the system as the customer types each character of the customer_query. Assume the customer types characters in order without deleting or removing any characters. If an output is not possible, return an empty array ([]).

    Example:
        Input: 
            `repository = ["mobile", "mouse", "monitor", "moneypot", "monitor", "mousepad"]`
            `customer_query = "mouse"`

        Output:
            `[
            ['mobile', 'moneypot', 'monitor'],
            ['mouse', 'mousepad'],
            ['mouse', 'mousepad'],
            ['mouse', 'mousepad']
            ]`
    
        Explanation:
            The chain of words the customer typed is "mo", "mou", "mous", "mouse" — hence 4 output elements. 
            For every word, 
            "mo" matches with ['mobile', 'mouse', 'monitor', 'moneypot', 'monitor', 'mousepad'], and so will be sorted alphabetically, with only the top 3 words chosen leading to ['mobile', 'moneypot', 'monitor'].
            "mou" matches with ['mouse', 'mousepad'], and is already sorted with <= 3 elements,
            "mous" matches with ['mouse', 'mousepad'], and is already sorted with <= 3 elements,
            "mouse" matches with ['mouse', 'mousepad'], and is already sorted with <= 3 elements.

    Time complexity: O(nlogn+mn)

    Space complexity: O(4m+w)
    """
    suggestions_past_1st_char = []

    repository.sort()

    
    # T: m = len(customer_query)
    for i in range(1, len(customer_query)):
        
        # S: m * 3
        curr_suggestions = []
        # S: m
        curr_query = customer_query[0:i+1].lower()

        # T: n
        for word in repository:
            # S: w = len(word)
            word = word.lower()
            if word.startswith(curr_query) and len(curr_suggestions) < 3:
                curr_suggestions.append(word)

        suggestions_past_1st_char.append(curr_suggestions)
    
    return suggestions_past_1st_char

if __name__ == "__main__":
    repository = ["abbS", "abc", "Abs", "bcs", "bdsa", "cdde", "rgb", "yjmm", "xxmm", "zeee"]
    customer_query = "123"

    print(search_suggestions(repository, customer_query))