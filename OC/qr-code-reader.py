from pyzbar.pyzbar import decode
from PIL import Image
"""
Decodes a QR code file and outputs its result onto the terminal.
"""
def main(dir:str)->None:
    """
    Prints out the contents of an inputted QR code.
    """
    output = read_qrcode(dir)
    if output!="":
        print(read_qrcode(dir))

def read_qrcode(dir:str)->str:
    """
    Decodes a QR code image and returns its contents as ASCII characters.
    """
    try:
        data=decode(Image.open(dir))
    except FileNotFoundError:
        print(f"Directory: '{dir}' does not point to an image file.")
        return ""
    else:
        return data[0].data.decode('ascii')
if __name__=="__main__":
    try:
        dir=rf"{input('Enter directory of the image including the image itself:\n')}"
    except KeyboardInterrupt:
        print("Program stopped.")
    else:
        main(dir)