# Python script to convert a given hex #FFFFFF and converts it to rgb(255, 255, 255)

HEX_MIN_LEN = 6
HEX_MAX_LEN = 7

RGB_MAX_LEN = 3

START = 0
INTERVAL = 2

HEX_ORDER = "0123456789abcdef"


# X_SIGNIFICANT_DIGIT
MOST_SIG_DIG = 16**1
LEAST_SIG_DIG = 16**0

MAX_COLOR = 255
INCLUSIVE = 1

def main():
    while True:
        
        try:
            user_command = input("Choose function:\n1. HEX #000000 to RGB(0,0,0)\n2. RGB(0,0,0) to HEX #000000.\nPress `ctrl + c` to exit.\n")
            match user_command:
                case "1":
                    color_in_hex = input("Enter color's hexadecimal. Accepted inputs: #FFFFFF, ffffff.\n")
          
                case "2":
                    color_in_rgb = input("Enter color's rgb(0,0,0) form. Accepted inputs: rgb(0,0,0), (0,0,0), 0,0,0.\n")
                    
                case _:
                    print(f"Invalid input: {user_command}")

        except ( KeyboardInterrupt ):
            print("Exit successful")
            break
        
        else:
            match user_command:
                case "1":
                    print( convert_hex_to_rgb( color_in_hex ) )

                case "2":
                    print( convert_rgb_to_hex( color_in_rgb ) )

        
        
# Function 1. From #ffffff to rgb(255,255,255)
def convert_hex_to_rgb(hex_form: str):
    hex_form_clean = hex_form.replace("#","").lower()
    pairs = []

    if value_is_valid(hex_form_clean, "length"):

        for index in range(START , len(hex_form_clean), INTERVAL ):

            first_char, second_char = hex_form_clean[ index : index + INTERVAL ]
            
            
            color_strength = ( HEX_ORDER.find(first_char)  * ( MOST_SIG_DIG ) ) + ( HEX_ORDER.find( second_char ) * ( LEAST_SIG_DIG ) )
    
            
            if value_is_valid( color_strength, "color" ):
                pairs.append( color_strength )

            else:
                return f"Value cannot be evaluated: {first_char}{second_char}"
            
        return f"rgb{tuple( pairs )}"    
    
    else:
        return f"Hex code must be 6 or 7 in length. Input's length: {len( hex_form )}"

# Function 2. From rgb(255,255,255) to #ffffff
def convert_rgb_to_hex(rgb_form: str):
    hex_count = len(HEX_ORDER)
    hex_form = "#"

    try:
        rgb_tuple_form = tuple( [ int( x ) for x in rgb_form.lower().strip( "rgb" ).strip( "()" ).split( "," ) ] )

    except (ValueError):
        return f"Non-integer found in {rgb_form}. Try again."
    
    if len( rgb_tuple_form ) > RGB_MAX_LEN:
        return "RGB values can only contain 3 values."
     

    for value in rgb_tuple_form:
        try:
            curr_val_in_hex = f"{HEX_ORDER[ int(value / hex_count) ]}{HEX_ORDER[ value % hex_count ]}"
        except (IndexError):
            return f"Entered value cannot exceed {MAX_COLOR}: {value}."
        else:
            hex_form += curr_val_in_hex

    return hex_form.upper()
  
def value_is_valid(value: int, test_mode: str):
    match test_mode:
        case "length": # Input cannot be like #9999999123
            return True if len(value) in [HEX_MIN_LEN, HEX_MAX_LEN] else False
        case "color": # Input cannot be over 255
            return True if value in range(MAX_COLOR + INCLUSIVE) else False
        

if __name__ == "__main__": 
    main()
