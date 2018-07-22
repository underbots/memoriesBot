import csv
UDF = 'user_data.csv'
with open(UDF, newline='\n') as cvs_file:
    data = csv.reader(cvs_file, delimiter=',', quotechar='|')

