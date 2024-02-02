import yaml
import os
import sys
import re
import csv

source = os.path.expanduser(sys.argv[1]) #define source of file - need to be specify as atribute of python - python multi.py /Users/USZCZRA/Desktop/INC0264729.csv
#source = 'dmarc_cname_create.csv'
output = {'records': []} #define empty dictionary that would be updated with data yaml structure
index=0 #start counting of generated records based on a number of rows

with open(source, newline='') as file:
    separator = csv.reader(file, delimiter=';', quotechar='"') # read row as a list
    headers = next(separator) # avoid headers
    for line in separator: #read file line by line      
        (type, action, view, record, value, alias, new_record, new_value) = line #define number and names of column from file to script, only number of columns must be equal 
        data = { #structure of yaml dictionary
            "record_type" : type.lower(), #create key "record type" and match value (lower case) from the column type
            "action" : action.lower(), #create key "action" and match value (lower case) from the column action
            "record_name" : record, #create key "record name" and match value (lower case) from the column record
            "view" : view.lower(), #create key "view" and match value (lower case) from the column view
                }
        if type.lower() == "txt":
            data['text'] = value #add key "text" to data dictionary for TXT record
            if action.lower() == "update": 
                data['new_record_name'] = new_record #add key "new record name " to data dictionary for TXT record and update action
                data['new_text'] = new_value #add key "new text" to data dictionary for TXT record and update action
        elif type.lower() == "cname":
            data['canonical'] = value #add key "canonical" to data dictionary for CNAME record
            if action.lower() == "update":
                data['new_record_name'] = new_record #add key "new record name" to data dictionary for CNAME record and update action
                data.pop('canonical') #remove key "canonical" to data dictionary for CNAME record and update action
                data['new_canonical'] = value #but add key "new canonical" to data dictionary for CNAME record and update action
        elif type.lower() == "arecord":
            data['ip_address'] = value #add key "ip address" to data dictionary for A record
            if action.lower() == "update":
                data['new_record_name'] = new_record #add key "new record name" to data dictionary for A record and update action
                data['new_ip_address'] = new_value #add key "new ip address" to data dictionary for A record and update action
        elif type.lower() == "alias":
            data['target_type'] = alias #add key "target type" to data dictionary for Alias record
            data['target_name'] = value #add key "target name" to data dictionary for Alias record
        elif type.lower() == "host":
            data['ip_address'] = value #add key "ip address" to data dictionary for Host record
            if action.lower() == "update":
                data['new_record_name'] = new_record #add key "new record name" to data dictionary for Host record and update action
                data['new_ip_address'] = new_value #add key "new ip address" to data dictionary for Host record and update action
        elif type.lower() == "mx": 
            data['preference'] = alias #add key "preference" to data dictionary for MX record
            data['mail_exchanger'] = value #add key "mail exchanger" to data dictionary for MX record
            if action.lower() == "update":
                data.pop('preference') #remove key "preference" to data dictionary for MX record and update action
                data['new_mail_exchanger'] = new_record #add key "new mail exchanger" to data dictionary for MX record and update action
                data['new_preference'] = new_value #add key "new preference" to data dictionary for MX record and update action
        elif type.lower() == "ptr":
            data['ip_address'] = value #add key "ip address" to data dictionary for PTR record
            if action.lower() == "update":
                data['new_record_name'] = new_record #add key "new record name" to data dictionary for PTR record and update action
                data['new_ip_address'] = new_value #add key "new ip address" to data dictionary for PTR record and update action
# eliminate headers                  
 #       if value.lower() == "value":
 #           data.clear()

        output['records'].append(data) #update output with all data DNS records
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
    
###########################################################

entry = 1    # define start count of DNS records
p = '- action:' # looking for "-action"
with open (convert, 'r', newline='' ) as yamlfile: # open created file
    check = yaml.safe_load_all(yamlfile) # read yaml structure
    for linia in yamlfile.readlines(): # analyze each line
        linia = linia.strip() # read only content without unnecessary characters     
    #    p = re.compile(r'^\-.[a-z]+\:.[a-z]+$') # pattern to find regex for "-action: []"
    #    count = p.findall(linia)   # find all matches of regex
    #print(count) # print all found regex pattern
        if p in str(linia):  # if "- action" in linia
        #    print(str(entry) + " : " + linia) # print linia with "- action"
            entry += 1 # increase count by 1
    print('Created file ' + convert + ' with ' + str(entry-1) + " DNS records") # have to -1 due to after last DNS entry count has been increased by 1


