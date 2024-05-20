import io
import os
import sys
import pandas as pd
import csv
from io import StringIO
from io import BytesIO

#csv_data = """a,b,c
#foo,bar,foo"""

source = os.path.expanduser(sys.argv[1]) #define source of file - need to be specify as atribute of python - python multi.py /Users/USZCZRA/Desktop/INC0264729.csv
read_file = pd.read_excel (source) # Write the dataframe object 

with pd.ExcelFile(source) as xls:  
    df1 = pd.read_excel(xls, header=0)  
    print(df1)
    for row in df1:
        print(row)
# creates and stores your csv data into a file the csv reader can read (bytes)
    print(row)
    
memory_file_in = BytesIO(dupa)

# classic reader
reader = csv.DictReader(memory_file_in)

# writes a csv file
fieldnames = reader.fieldnames  # here we use the data from the above csv file
memory_file_out = BytesIO()     # create a memory file (bytes)

# classic writer (here we copy the first file in the second file)
writer = csv.DictWriter(memory_file_out, fieldnames)
for row in reader:
    print(row)
    writer.writerow(row)