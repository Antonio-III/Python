"""
This script modifies a csv file's column. Right now, the file only supports replacing the column with new data.

Table of Contents
    
"""
import typing

def main(dir: str, col_num: int) -> None:
    table = get_csv_data(dir)
    scores = extract_col(table, col_num, False)
    new_scores = modify_column(scores, col_num)
    table = replace_col(table, col_num, new_scores, False)

    replace_csv_data(dir,table)
    print("Process completed.")

def get_csv_data(dir: str) -> list[str]:
    """
    1. Collects file data from the given directory.
    2. It is otherwise considered a generic "get all data from file" function, but slightly modified to fit the formatting of csv files.
    """
    csv_data = []
    with open(dir,"r") as file_reader:
        # csv files have a "\n" at the end so we strip it.
        csv_data+=[row.strip().split(",") for row in file_reader]
    return csv_data

def replace_csv_data(dir:str,new_content:list[str])->None:
    """
    1. Writes data into a truncated file in the given directory.
    2. Function name uses the name csv for the purposes of this script. It is otherwise considered a generic "write to file" function.
    """
    write_to_file(dir,new_content)
    return None

def modify_column(column:list, col_num:int)->list[str]:
    """
    1. Replace the target column's inputted text with another inputted text.
    """
    input(f"You have selected to replace/strip column number {col_num}'s (1-indexed) values. Press Enter to continue, or Ctrl+C to stop.")
    target_text=input("Target text to be replaced:\n")
    replace_text=input("Replace it with (Press Enter to replace it with nothing):\n")
    return [score.replace(target_text,replace_text) for score in column]

# imported functions
def replace_col(table:list,pos:int,new_value:list,ignore_header:bool)->list[typing.Any]:
    """
    1. Replaces `pos-1`th column in table with `value` (list). 
        1. `pos` is 1-indexed as an argument.
    2. Has an option to ignore header.
        Ignoring header means to slice table as table[1:] instead of table[:].
    """
    pos-=1
    for row,new_val in zip(table[1:] if ignore_header else table[:],new_value):
        row[pos]=new_val
    return table
def extract_col(table:list,pos:int,ignore_header:bool)->list[typing.Any]:
    """
    1. Return a list of elements in the `n-1`th position of every row.
        1. `pos` is 1-indexed as an argument.
    2. Has an option to ignore the first row (ignore_header:bool).
    3. Example: extract_col(table=table,n=1,ignore_header=True):
        1. if table =  [[1,2,3],
                       [4,5,6],
                       [7,8,9]]
        2. return: [4,7].
    """
    pos-=1
    return [ row[pos] for row in (table[1:] if ignore_header else table[:]) ]
def write_to_file(dir:str,new_content:list)->None:
    """
    This is a modified version of the original function.
    1. Truncates (clears) the file in the given directory.
    2. Writes contents into the file, with a "\n" at the end.
    """

    with open(dir,"w") as file_handler:
        for row in new_content:
            row_contents=",".join(row)
            file_handler.write(row_contents+"\n")
    return None

if __name__=="__main__":
    input("You have to write the code yourself on how the selected column is to be modified. Press Enter to continue.")
    DIR=input("Enter directory of the csv file you want to modify. This directory must point to a .csv file:\n").strip(""" "'""")
    COL_NUM=int(input("Enter column number (1-indexed) that you want to modify:\n"))
   
    main(fr"{DIR}",COL_NUM)