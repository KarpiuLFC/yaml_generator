import os
import pandas as pd
import sys

def open_xlsx():
    global source
    source = os.path.expanduser(sys.argv[1]) #define source of file - need to be specify as atribute of python - python multi.py /Users/USZCZRA/Desktop/INC0264729.csv
    read_file = pd.read_excel (source) # Write the dataframe object 
    global without_extension
    without_extension = os.path.splitext(source)[0]
    read_file.to_csv (f"convert_{without_extension}.csv", index = None, header=True) #into csv file 
open_xlsx()