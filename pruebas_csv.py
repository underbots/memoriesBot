import csv
import os
def new_user( user_id , first_name , user_name , UDF):
    """
@param user_id , first_name , user_name: are self explained  
@param UDF user data file, data user register
--@param DIR path to save the file 
"""

    # Add in csv data information
    with open(UDF, 'a', newline='') as csvfile: # cambio w por a
    fieldnames = ['id', 'first name' , 'username' ]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
    writer.writerow({'id': user_id, 'first name': first_name , 'username': user_name})

    writer.close()



    
