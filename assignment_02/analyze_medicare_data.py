'''We are first importing all the important methods required for the assignment'''

import requests
import os
import zipfile
import openpyxl
import sqlite3
import glob
import getpass
import pandas as pd

'''This line is initializing the place holder for the url path''' 
url="https://data.medicare.gov/views/bg9k-emty/files/0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip"
#print(url)
'''this line of code will request the above mentioned url and is getting the response back'''
r = requests.get(url)
#print(r)
#print(r.content)


'''Now, we are making a staging directory to store the contensts of the zip folder after unzipping it'''
staging_dir_name = "staging"


os.mkdir(staging_dir_name) 

'''Represents a path relative to the current directory on drive'''

zip_file_name = os.path.join(staging_dir_name, "test.zip")

'''It will '''
zf = open(zip_file_name,"wb")

'''write is a function of object zf, it will write all contents on link r to zf file'''
zf.write(r.content)
zf.close()

'''zipfile is a function of object zipfile it will have '''
z = zipfile.ZipFile(zip_file_name,'r')
z.extractall(staging_dir_name)
z.close() 


k_url = "http://kevincrook.com/utd/hospital_ranking_focus_states.xlsx"
r = requests.get(k_url)
xf = open("hospital_ranking_focus_states.xlsx","wb")
xf.write(r.content)
xf.close()


wb = openpyxl.load_workbook("hospital_ranking_focus_states.xlsx")
   
sheet = wb.get_sheet_by_name("Hospital National Ranking") 


sheet2 = wb.get_sheet_by_name("Focus States")



    
    


glob_dir = os.path.join(staging_dir_name,"*.csv")
#for file_name in glob.glob(glob_dir):
    
    
    
#Importing csv to sqlite server

  
                      
def create_tables():
    try:
        conn = sqlite3.connect("medicare_hospital_compare.db")
        glob_dir = os.path.join(staging_dir_name, "*.csv")
        for file_name in glob.glob(glob_dir):
            absolute_path = os.path.abspath(file_name)
            column_name=[]
            try:
                df= pd.read_csv(absolute_path)
                column_name = list(df.columns)
                dict_types = {x:'str' for x in column_name}
                df = pd.read_csv(absolute_path,dtype=dict_types)
            except UnicodeDecodeError:
                in_fp = open(absolute_path, "rt", encoding='cp1252')  
                input_data = in_fp.read()
                in_fp.close()
                n_file_name = absolute_path + ".fix"
                out_fp = open(n_file_name, "wt", encoding='utf-8')
                for c in input_data:
                    if c != '\0':
                        out_fp.write(c)
                out_fp.close()
                df = pd.read_csv(n_file_name)
                col = list(df.columns)
                dict_types = {x:'str' for x in column_name}
                df = pd.read_csv(n_file_name,dtype=dict_types)
            column_name = list(df.columns)
            col_names_new = []
            for item in column_name:
                temp = item.lower().replace(" ", "_").replace("-", "_").replace("%", "pct").replace("/", "_")
                if(not temp[0].isalpha()):
                    col_names_new.append("c_" + temp)
                else:
                    col_names_new.append(temp)
            df.columns = col_names_new
            tablename = os.path.splitext(os.path.basename(file_name))[0].lower().replace(" ","_").replace("-","_").replace("%", "pct").replace("/","_")
            if(not tablename[0].isalpha()):
                tablename = "t_" + tablename
            df.to_sql(tablename,con=conn,if_exists='fail',dtype = {col:'text' for col in df}, index=False)
           
    ## Raises exception on unable to establish connection
    except ConnectionError:
        print("Unable to get database connection.. Exiting out of program")
        raise SystemExit
    ## Closes connection upon running the query
    finally:
        conn.close()
    ##Enables garbage collection
    #gc.collect()
    return

create_tables() 