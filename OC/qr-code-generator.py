import qrcode
import os
"""
Generates a QR code file based on the inputted text.
"""
def main(data:str,file_name:str)->None:
    """
    Generates and downloads the QR code, and outputs the QR code image's path.
    """
    generate_qrcode(data,file_name=file_name)
    print(f"Encoded '{data}' in: {os.getcwd()}\\{file_name}")

def generate_qrcode(data:str,file_name:str)->None:
    """
    Generates a QR code with the inputted data and downloads it in the current directory of the executed file.
    """
    qrcode.make(data).save(file_name)  # type: ignore

if __name__=="__main__":
    FILE_NAME="qrcode.png"
    try:
        data=input("Enter data to encode to the QR code (Right-click to paste an item):\n")
    except KeyboardInterrupt:
        print("Program stopped.")
    else:
        main(data,file_name=FILE_NAME)