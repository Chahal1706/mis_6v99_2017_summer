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
os.mkdir(staging_dir_name) 

'''Represents a path relative to the current directory on drive'''

zip_file_name = os.path.join(staging_dir_name, "test.zip")

'''It will '''
zf = open(zip_file_name,"wb")

'''write is a function of object zf'''
zf.write(r.content)
zf.close()
