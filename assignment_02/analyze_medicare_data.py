'''We are first importing all the important methods required for the assignment'''

import requests
import os
import zipfile
import openpyxl
import sqlite3
import glob
import getpass

'''This line is initializing the place holder for the url path''' 
url="https://data.medicare.gov/views/bg9k-emty/files/0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip"
print(url)
'''this line of code will request the above mentioned url and is getting the response back'''
r = requests.get(url)
print(r)
print(r.content)


'''Now, we are making a staging directory to store the contensts of the zip folder after unzipping it'''
staging_dir_name = "staging"

"""
os.mkdir(staging_dir_name) 

'''Represents a path relative to the current directory on drive'''

zip_file_name = os.path.join(staging_dir_name, "test.zip")

'''It will '''
zf = open(zip_file_name,"wb")

'''write is a function of object zf, it will write all contents on link r to zf file'''
zf.write(r.content)
zf.close()

'''zipfile is a function of object zipfile it will have '''
#z = zipfile.ZipFile(zip_file_name,'r')
z.extractall(staging_dir_name)
z.close() 

"""

k_url = "http://kevincrook.com/utd/hospital_ranking_focus_states.xlsx"
r = requests.get(k_url)
xf = open("C:\\Users\\chaha\\Downloads\\hospital_ranking_focus_states.xlsx","wb")
xf.write(r.content)
xf.close()


wb = openpyxl.load_workbook("hospital_ranking_focus_states.xlsx")
for sheet_name in wb.get_sheet_names():
    print(sheet_name)
    
sheet = wb.get_sheet_by_name("Hospital National Ranking") 
i = 1
while sheet.cell(row=i, column=1).value != None:
    print(sheet.cell(row=i, column=1).value, "|" , sheet.cell(row=i, column=2).value)
    i+=1
    

sheet2 = wb.get_sheet_by_name("Focus States")
i = 1
while sheet.cell(row=i, column=1).value != None:
    print(sheet2.cell(row=i, column=1).value, "|" , sheet2.cell(row=i, column=2).value)
    i+=1
    
wb2 = openpyxl.Workbook()
sheet_1 = wb2.create_sheet("utd")
sheet_1.cell(row=1,column=1,value="buan")
for i in range(2,11):
    sheet_1.cell(row=i,column=1,value=i-1)
    
    
sheet_2 = wb2.create_sheet("test")
sheet_2.cell(row=1,column=2,value="valued")
wb2.remove_sheet(wb2.get_sheet_by_name('Sheet'))
wb2.save("test.xlsx")
wb2.close()

conn = sqlite3.connect("test.db")
c1 = conn.cursor()
sql_str = "drop table if exists my_table"
c1.execute(sql_str)

sql_str = """
create table if not exists my_table (
column_1 text,
column_2 text,
column_3 text
)
"""

c1.execute(sql_str)
sql_str = "insert into my_table (column_1,column_2,column_3) values (?,?,?)"
sql_tuple=('a','b','c')
c1.execute(sql_str,sql_tuple)
conn.commit()


sql_str = "select * from my_table"
rows = c1.execute(sql_str)
for row in rows :
    print(row)
    
sql_str = "select * from sqlite_master"
rows = c1.execute(sql_str)
for row in rows :
    print(row)
    
sql_str = "PRAGMA table_info('my_table')"
rows = c1.execute(sql_str)
for row in rows :
    print(row)
    


sql_str = "select * from sqlite_master where tbl_name = ?"
sql_tuple = ('my_table',)
c1.execute(sql_str,sql_tuple)
for row in rows :
    print(row)

sql_str = "select count(*) from my_table"
rows = c1.execute(sql_str)
for row in rows :
    print(row)

fn =  os.path.join(staging_dir_name, "Timely and Effective Care - Hospital.csv")
in_fp = open(fn,"rt",encoding='cp1252')#rt = read text
input_data = in_fp.read()
in_fp.close()

ofn =  os.path.join(staging_dir_name, "Timely and Effective Care - Hospital.csv.fix")
out_fp = open(ofn,"wt",encoding='utf-8')# switching from codepage 1252 to utf-8 and removing nulls
for c in input_data:
    if c != '\0':
        out_fp.write(c)
out_fp.close()


# get the zip file unzip and loop through the files,create tables from csv files with the replacements and insert the data into table
#check through db browser
#code to convert from cp1253 to utf-8 
#use numpi for sd(population),median,mode
#create the output excel files as shown above
glob_dir = os.path.join(staging_dir_name,"*.csv")
for file_name in glob.glob(glob_dir):
    print (file_name)
    print("    basename:",os.path.basename(file_name))#basename is filename without the path
    print("    split extension:",os.path.splitext(os.path.basename(file_name)))
    print("    dirname:",os.path.dirname(file_name))
    print("    absolute path:",os.path.abspath(file_name))
    
c1.close() 
