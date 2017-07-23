
# coding: utf-8

# In[2]:

'''We are first importing all the important methods required for the assignment'''

import requests
import os
import zipfile
import openpyxl
import sqlite3
import glob
import getpass
import pandas as pd
from openpyxl import Workbook
import numpy as np

'''This line is initializing the place holder for the url path''' 
url="https://data.medicare.gov/views/bg9k-emty/files/0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip"
#print(url)
'''this line of code will request the above mentioned url and is getting the response back'''
r = requests.get(url)
#print(r)
#print(r.content)


'''Now, we are making a staging directory to store the contensts of the zip folder after unzipping it'''
staging_dir_name = "staging"

if not os.path.exists(staging_dir_name):
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
            df.to_sql(tablename,con=conn,if_exists='replace',dtype = {col:'text' for col in df}, index=False)
           
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




'''
the below block of code is performing the following functions:
1) making connection to the db
2) fetching the data from hospital_general_information
3) putting each row as dictionary to list list_of_rows_from_table
'''
conn = sqlite3.connect("medicare_hospital_compare.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()
rows = c.execute('SELECT * FROM hospital_general_information')

list_of_rows_from_table=list()
for row in rows:
    list_of_rows_from_table.append(dict(row))



conn.close()   
  
'''
the below piece of code performs the following function:
1) reads the hospital_ranking_focus_state file
2) creates a dataframe  : df_hospital_national_ranking which contains data from sheet : Hospital National Ranking
3) crates a dataframe : df_focus_states which contains data from sheet : Focus States'
'''  

df_rows_table = pd.DataFrame(list_of_rows_from_table)

k_url = "http://kevincrook.com/utd/hospital_ranking_focus_states.xlsx"
r = requests.get(k_url)
xf = open("hospital_ranking_focus_states.xlsx","wb")
xf.write(r.content)
xf.close()


xls_file = pd.ExcelFile('hospital_ranking_focus_states.xlsx')
df_hospital_national_ranking=xls_file.parse('Hospital National Ranking')
df_focus_states=xls_file.parse('Focus States')
#print(df_focus_states[:5])
#print(df_hospital_national_ranking[:5])

'''
we filter out the first rows from the ranking dataframe
'''


df_hospital_rank_100=df_hospital_national_ranking[:100].copy()
#print(df_hospital_rank_100)

#df_hospital_rank_100['hospital_name']=df_hospital_rank_100['Provider ID'].map(df_rows_table)
#print(any(df_rows_table.provider_id=='450023'))



#print(df_hospital_rank_100_merged)
#print(any(df_hospital_rank_100['Provider ID']==450023))

#print(df_hospital_rank_100.dtypes)

'''
we convert the data type of provider id to int64 so that we can perform the merge operation below.
'''
df_rows_table['provider_id']=df_rows_table['provider_id'].astype(np.int64)
#df_rows_table.dtypes

'''
the below line is equivalant to a join between the data from :
1) df_hospital_rank_100
2) df_rows_table
we do this because we need the values of Hospital Namne , City, State and county name from second table.
'''

df_hospital_rank_100_merged=pd.merge(left=df_hospital_rank_100,right=df_rows_table,left_on='Provider ID',right_on='provider_id')
#print(df_hospital_rank_100_merged)
'''
we rename the column in the dataframe according to the requirement mentioned below.
'''

df_hospital_rank_100_merged.rename(columns={'hospital_name':'Hospital Name','city':'City','state':'State','county_name':'County'},inplace=True)

#print(df_hospital_rank_100_merged[['Provider ID','Hospital Name','City','State','County']])
'''
we copy the columns required into a staging dataframe.
'''

df_hospital_rank_100_merged_filtered=df_hospital_rank_100_merged[['Provider ID','Hospital Name','City','State','County']].copy()

'''
we remove the automatically created indexed column by setting the Provider ID  as the index
'''


df_hospital_rank_100_merged_filtered.set_index('Provider ID',inplace=True)
#print(df_hospital_rank_100_merged_filtered)





#print("before sorting: ",df_focus_states)
'''
we sort the below dataframe by state name
'''

df_focus_states.sort_values(by='State Name',inplace=True)
#print(df_focus_states)

'''
we create a dictionary from the above data frame.
'''

dict_of_state_abbr_sorted = dict(zip(df_focus_states['State Name'],df_focus_states['State Abbreviation']))

'''
we create an ExcelWriter object - hospital_ranking.xlsx file.
we create a sheet : Nationwide where we store our filtered dataframe.
'''

writer=pd.ExcelWriter('hospital_ranking.xlsx')
df_hospital_rank_100_merged_filtered.to_excel(writer,'Nationwide')

'''
we will now iterate through the key, value pair 
'''
for key,value in dict_of_state_abbr_sorted.items():
    
    '''
    we filter the rows by state name from df_rows_table
    '''
    
    df_rows_table_filter_by_state_name=df_rows_table[(df_rows_table.state==value)].copy()
    '''
    we create an inner join and get eht common data from ranking and the df_rows_table. 
    '''
     
    df_hospital_filtered_by_state_name_merged=pd.merge(left=df_hospital_national_ranking,right=df_rows_table_filter_by_state_name,left_on='Provider ID',right_on='provider_id')
    
    '''
    we rename the columns according to the requirement
    '''
    #df_hospital_filtered_by_state_name_merged.set_index('Provider ID',inplace=True)
    df_hospital_filtered_by_state_name_merged.rename(columns={'hospital_name':'Hospital Name','city':'City','state':'State','county_name':'County'},inplace=True)
    #df_hospital_filtered_by_state_name_merged_columns_filtered=df_hospital_filtered_by_state_name_merged[['Provider ID','Hospital Name','City','State','County']].copy()
    '''
    sort the data obtained per state by Ranking Column.
    '''
    df_hospital_filtered_by_state_name_merged.sort_values(by='Ranking',inplace=True)
    #print(df_hospital_filtered_by_state_name_merged)
    '''
    we then filter out the required column and se the Provider ID as the key
    '''
    df_hospital_filtered_by_state_name_merged_columns_filtered=df_hospital_filtered_by_state_name_merged[['Provider ID','Hospital Name','City','State','County']].copy()
    df_hospital_filtered_by_state_name_merged_columns_filtered.set_index('Provider ID',inplace=True)
    
    '''
    we write the data to a new sheet in the excel file
    '''
    df_hospital_filtered_by_state_name_merged_columns_filtered.to_excel(writer,key)
    #break


    
'''
we save the file. this finishes the file : hospital_ranking.xlsx
'''
writer.save()


'''
we will now prepare the measure_statistics.xlsx
'''

'''
we create a connection to the database and get the data from the timely_and_effective_care__hospital
'''

conn = sqlite3.connect("medicare_hospital_compare.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()
rows = c.execute('SELECT state,measure_id,measure_name,score FROM timely_and_effective_care___hospital')

list_of_rows_from_timely_and_effective_data_table=list()
'''
we are creating a list from the rows of the table with each row as dictionaries.
'''
for row in rows:
    #print(row)
    list_of_rows_from_timely_and_effective_data_table.append(dict(row))

conn.close()
'''
we are creating a dataframe from the above list to perform the aggregations operations.
'''

df_rows_timely_and_effective_care__hospital_table = pd.DataFrame(list_of_rows_from_timely_and_effective_data_table)

#print(df_rows_timely_and_effective_care__hospital_table[:5])

'''
We are getting unique measure id
'''

set_of_measure_id=set(df_rows_timely_and_effective_care__hospital_table['measure_id'])

#print(set_of_measure_id)


list_of_data_frames=list()

'''
we are forming list which are data frames corresponding to each measure id
'''

for measure_id in set_of_measure_id:
    #if measure_id == 'PC_01':
    #print(measure_id)
    df_rows_filtered_measure_id=df_rows_timely_and_effective_care__hospital_table[(df_rows_timely_and_effective_care__hospital_table.measure_id==measure_id)].copy()
    df_rows_filtered_measure_id_only_numerical=df_rows_filtered_measure_id[(df_rows_filtered_measure_id['score'].apply(lambda x : x.isdigit() == True))]
    list_of_data_frames.append(df_rows_filtered_measure_id_only_numerical)
#print(len(list_of_data_frames))

'''
we get a dataframe with all the measureid's
'''
resultant_data_frame=pd.concat(list_of_data_frames)
#print(resultant_data_frame[:500])
'''
we again get the unique measure id's as some of the measureid might be filtered in the previous step
'''
final_set_of_measure_id=set(resultant_data_frame['measure_id'])
#print(final_set_of_measure_id)

'''
we convert the data type of the score column to int64
'''

resultant_data_frame['score']=resultant_data_frame['score'].astype(np.int64)

#measures_statistics.xlsx
list_nationwide=[]

'''
this loop we are performing the following operation
1) Getting the rows from the main data frame filtered by the Measure Id
2) for each measure id , we calculate the minimum, maximum, average and standard deviation 
3) we then add them to the list_nationwide that we created above
'''
for meid in final_set_of_measure_id:
    #print(meid)
    dictionay_of_nationwide_main=dict()
    df_rows_filtered_meid=resultant_data_frame[(resultant_data_frame.measure_id==meid)].copy()
    #print(meid)
    dictionay_of_nationwide_main['Measure ID']=meid
    dictionay_of_nationwide_main['Measure Name']=list(df_rows_filtered_meid['measure_name'])[0]
    #print(list(df_rows_filtered_meid['measure_name'])[0])
    #print(df_rows_filtered_meid['score'].dtype)
    dictionay_of_nationwide_main['Minimum']=(df_rows_filtered_meid['score']).min()
    dictionay_of_nationwide_main['Maximum']=(df_rows_filtered_meid['score']).max()
    dictionay_of_nationwide_main['Average']=(df_rows_filtered_meid['score']).mean()
    dictionay_of_nationwide_main['Standard Deviation']=(df_rows_filtered_meid['score']).std()
    #print((df_rows_filtered_meid['score']).min())
    #print((df_rows_filtered_meid['score']).max())
    #print((df_rows_filtered_meid['score']).mean())
    #print((df_rows_filtered_meid['score']).std())
    #print(dictionay_of_nationwide_main)
    list_nationwide.append(dictionay_of_nationwide_main)
    
    
#print(list_nationwide)
'''
We create a main dataframe from the list that we created above and add appropriate column names.
'''

nationwide_main_dataframe=pd.DataFrame(list_nationwide, columns=['Measure ID', 'Measure Name', 'Minimum','Maximum','Average','Standard Deviation'])
'''
we sort the value by the column Measure ID
'''
nationwide_main_dataframe.sort_values(by='Measure ID',inplace=True)
#print(nationwide_main_dataframe)

'''
we make the column Measure ID as the index ccolumn , this is to prevent the index appearing in the sheet.
'''
nationwide_main_dataframe.set_index('Measure ID',inplace=True)



#print(resultant_data_frame)

'''
we then create the ExcelWriter for the measure_statistics.xlsx.
'''

writer=pd.ExcelWriter('measures_statistics.xlsx')
'''
we then create a sheet "Nationwide" and write the nationwide_main_dataframe in that sheet
we do not close the writer yet
'''
nationwide_main_dataframe.to_excel(writer,'Nationwide')

'''
we then get the key, value from the dict_of_state_abbr_sorted dictionaries and execute the loop as below
'''

for key,value in dict_of_state_abbr_sorted.items():
    #print(key)
    #rint(value)
    ''''''
    list_of_state_wise_aggregated_dictionaries=[]
    dict_of_state_wise_aggregation=dict()
    '''
    we filter the rows by state name from resultant_data_frame
    '''
    resultant_data_frame_filter_by_state_name=resultant_data_frame[(resultant_data_frame.state==value)].copy()
    
    '''
    we then perform the aggregation by score group by measureid , we get the following aggregations
    1) Mean
    2) Minimum
    3) Maximum
    4) Standard Deviation
    '''
    df_resultant_groupby=pd.DataFrame(resultant_data_frame_filter_by_state_name.groupby(['measure_id'])['score'].min())
    df_resultant_groupby['Maximum']=pd.DataFrame(resultant_data_frame_filter_by_state_name.groupby(['measure_id'])['score'].max())
    df_resultant_groupby['Average']=pd.DataFrame(resultant_data_frame_filter_by_state_name.groupby(['measure_id'])['score'].mean())
    df_resultant_groupby['Standard Deviation']=pd.DataFrame(resultant_data_frame_filter_by_state_name.groupby(['measure_id'])['score'].std())
    df_resultant_groupby.reset_index(inplace=True)
    #print(df_resultant_groupby)
    '''
    we then rename the score and measure_id column according to the specification mentioned.    
    '''
    df_resultant_groupby.rename(columns={'score':'Minimum','measure_id':'Measure ID'},inplace=True)
    '''
    we then sort the dataframe by Measure ID
    '''
    df_resultant_groupby.sort_values(by='Measure ID',inplace=True)
    df_resultant_groupby.set_index('Measure ID',inplace=True)
    '''
    We then write the dataframe to a separate sheet and name that sheet by the key.
    '''
    df_resultant_groupby.to_excel(writer,key)
    #print(df_resultant_groupby[:5])
    #print(resultant_data_frame_filter_by_state_name)
    #break


'''
we now close the writer.
'''

writer.save()

#df_rows_timely_and_effective_care__hospital_table['score'].apply(lambda x: x.isdigit)

'''
we now close the connection to the database just in case some connection might be open
'''

conn.close()

