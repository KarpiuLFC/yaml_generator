import os
import sys
import csv
import yaml
import re

dict = {}
output = {'records': []} #define empty dictionary that would be updated with data yaml structure
source = os.path.expanduser(sys.argv[1]) #define source of file - need to be specify as atribute of python - python multi.py /Users/USZCZRA/Desktop/INC0264729.csv
index=0 #start counting of generated records based on a number of rows

txt = re.compile('[tT][xX][tT]')
cname = re.compile('[cC][nN][aA][mM][eE]')
arecord = re.compile('[aA][rR][eE][cC][oO][rR][dD]')
alias = re.compile('[aA][lL][iI][aA][sS]')
host = re.compile('[hH][oO][sS][tT]')
mx = re.compile('[mM][xX]')
ptr = re.compile('[pP][tT][rR]')
update = re.compile('[uU][pP][dD][aA][tT][eE]')

with open(source, newline='', encoding="utf-8-sig") as file:
    csv.reader = csv.DictReader(file, delimiter=';', quotechar='"')
    separator = csv.reader# read row as a list
    template = [row for row in separator]
    for row in template:
        dict.update(row)
        data = { #structure of yaml dictionary
            "record_type" : dict.get("Type"), #create key "record type" and match value (lower case) from the column type
            "action" : dict.get("Action"), #create key "action" and match value (lower case) from the column action
            "record_name" : dict.get("Record_name"), #create key "record name" and match value (lower case) from the column record
            "view" : dict.get("View"), #create key "view" and match value (lower case) from the column view
                }
        
        for value in dict.values():
            if (txt.match(value)):
                #print("txt")
                data['text'] = dict.get("Value") #add key "text" to data dictionary for TXT record
                if "Update" in dict.values(): 
                    data['new_record_name'] = dict.get("New_Record_UPDATE") #add key "new record name " to data dictionary for TXT record and update action
                    data['new_text'] = dict.get("New Value_UPDATE") #add key "new text" to data dictionary for TXT record and update action
            elif (cname.match(value)):
                data['canonical'] = dict.get("Value") #add key "canonical" to data dictionary for CNAME record
                if "Update" in dict.values(): 
                    data['new_record_name'] = dict.get("New_Record_UPDATE") #add key "new record name" to data dictionary for CNAME record and update action
                    data.pop('canonical') #remove key "canonical" to data dictionary for CNAME record and update action
                    data['new_canonical'] = dict.get("New Value_UPDATE") #but add key "new canonical" to data dictionary for CNAME record and update action
            elif (arecord.match(value)):
                data['ip_address'] = dict.get("Value") #add key "ip address" to data dictionary for A record
                if "Update" in dict.values(): 
                    data['new_record_name'] = dict.get("New_Record_UPDATE") #add key "new record name" to data dictionary for A record and update action
                    data['new_ip_address'] = dict.get("New Value_UPDATE") #add key "new ip address" to data dictionary for A record and update action
            elif (alias.match(value)):
                data['target_type'] = dict.get("Alias Target/MX preferance") #add key "target type" to data dictionary for Alias record
                data['target_name'] = dict.get("Value") #add key "target name" to data dictionary for Alias record
            elif (host.match(value)):
                data['ip_address'] = dict.get("Value") #add key "ip address" to data dictionary for Host record
                if "Update" in dict.values(): 
                    data['new_record_name'] = dict.get("New_Record_UPDATE") #add key "new record name" to data dictionary for Host record and update action
                    data['new_ip_address'] = dict.get("New Value_UPDATE") #add key "new ip address" to data dictionary for Host record and update action
            elif (mx.match(value)):
                data['preference'] = dict.get("Alias Target/MX preferance") #add key "preference" to data dictionary for MX record
                data['mail_exchanger'] = dict.get("Value") #add key "mail exchanger" to data dictionary for MX record
                if "Update" in dict.values(): 
                    data.pop('preference') #remove key "preference" to data dictionary for MX record and update action
                    data['new_mail_exchanger'] = dict.get("New Value_UPDATE") #add key "new mail exchanger" to data dictionary for MX record and update action
                    data['new_preference'] = dict.get("New_Record_UPDATE") #add key "new preference" to data dictionary for MX record and update action
            elif (ptr.match(value)):
                data['ip_address'] = dict.get("Value") #add key "ip address" to data dictionary for PTR record
                if "Update" in dict.values(): 
                    data['new_record_name'] = dict.get("New_Record_UPDATE") #add key "new record name" to data dictionary for PTR record and update action
                    data['new_ip_address'] = dict.get("New Value_UPDATE") #add key "new ip address" to data dictionary for PTR record and update action
        output['records'].append(data)
        index += 1  # increase index by 1 with each line

print("Found " + str(index) + " records in request") # Print sum of records 
    
file = input("Please provide name of destination yaml file: ") #+ ".yaml"  # ask for destination file name
if file.endswith('.yaml'): # check if format of file is with .yaml
    convert = file
elif file.endswith('.yml'): # or check if format of file is with .yml
    convert = file
else: # if no extansion 
    convert = str(file) + ".yaml" # add .yaml to name of file
    
with open (convert, 'w+') as final: #open destination file
    yaml.dump(output, final) #write outout in .yaml format       
           
entry = 1    # define start count of DNS records
p = '- action:' # looking for "-action"
with open (convert, 'r', newline='' ) as yamlfile: # open created file
    check = yaml.safe_load_all(yamlfile) # read yaml structure
    for linia in yamlfile.readlines(): # analyze each line
        linia = linia.strip() # read only content without unnecessary characters     
        if p in str(linia):  # if "- action" in linia
            entry += 1 # increase count by 1
    print('Created file ' + convert + ' with ' + str(entry-1) + " DNS records") # have to -1 due to after last DNS entry count has been increased by 1