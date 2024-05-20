import io
import os
import sys
import pandas as pd

source = os.path.expanduser(sys.argv[1]) #define source of file - need to be specify as atribute of python - python multi.py /Users/USZCZRA/Desktop/INC0264729.csv
read_file = pd.read_excel (source) # Write the dataframe object 
#without_extension = os.path.splitext(source)[0]
#read_file.to_csv (f"convert_{without_extension}.csv", index = None, header=True) #into csv file
#print(read_file)
f = io.StringIO(read_file.to_csv)
print(f.getvalue)
#file = io.open(read_file, buffering = 5)
 
#print(file.read())
 
# Close the file
#file.close()
