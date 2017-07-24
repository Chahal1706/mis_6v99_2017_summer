#We are first importing all the important methods required for the assignment

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

#This line is initializing the place holder for the url path and will make a staging directory to store zip folder 
url="https://data.medicare.gov/views/bg9k-emty/files/0a9879e0-3312-4719-a1db-39fd114890f1?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip"
r = requests.get(url)
staging_dir_name = "staging"
if not os.path.exists(staging_dir_name):
    os.mkdir(staging_dir_name) 

#Represents a path relative to the current directory on drive & write a function of object zf to write contents on link r

zip_file_name = os.path.join(staging_dir_name, "test.zip")
zf = open(zip_file_name,"wb")
zf.write(r.content)
zf.close()


z = zipfile.ZipFile(zip_file_name,'r')
#zipfile is a function of object zipfile it will have 
z.extractall(staging_dir_name)
z.close() 
k_url = "http://kevincrook.com/utd/hospital_ranking_focus_states.xlsx"
r = requests.get(k_url)
xf = open("hospital_ranking_focus_states.xlsx","wb")
# Here, we are writing the contents
xf.write(r.content)
xf.close()


wb = openpyxl.load_workbook("hospital_ranking_focus_states.xlsx")
sheet = wb.get_sheet_by_name("Hospital National Ranking") 
sheet2 = wb.get_sheet_by_name("Focus States")



    
    

#for file_name in glob.glob(glob_dir): & Importing csv to sqlite server
glob_dir = os.path.join(staging_dir_name,"*.csv")

    
    
    


  
                      
def create_tables():
    try:
        conn = sqlite3.connect("medicare_hospital_compare.db")
        glob_dir = os.path.join(staging_dir_name, "*.csv")
        #Making condition for file_name
        for file_name in glob.glob(glob_dir):
            absolute_path = os.path.abspath(file_name)
            column_name=[]
            try:
                df= pd.read_csv(absolute_path)
                #creating colum_name list
                column_name = list(df.columns)
                dict_types = {x:'str' for x in column_name}
                df = pd.read_csv(absolute_path,dtype=dict_types)
            except UnicodeDecodeError:
                #creating in_fb to encode cp1252
                in_fp = open(absolute_path, "rt", encoding='cp1252')  
                input_data = in_fp.read()
                in_fp.close()
                n_file_name = absolute_path + ".fix"
                out_fp = open(n_file_name, "wt", encoding='utf-8')
                #now, creating out_fp to encode it to utf-8
                for c in input_data:
                    if c != '\0':
                        out_fp.write(c)
                out_fp.close()
                #creating df to read file_name
                df = pd.read_csv(n_file_name)
                col = list(df.columns)
                dict_types = {x:'str' for x in column_name}
                df = pd.read_csv(n_file_name,dtype=dict_types)
                #creating df to n_file_name
            column_name = list(df.columns)
            
            col_names_new = []
            for item in column_name:
                temp = item.lower().replace(" ", "_").replace("-", "_").replace("%", "pct").replace("/", "_")
                if(not temp[0].isalpha()):
                    #appending in col_names_new
                    col_names_new.append("c_" + temp)
                else:
                    col_names_new.append(temp)
            df.columns = col_names_new
            tablename = os.path.splitext(os.path.basename(file_name))[0].lower().replace(" ","_").replace("-","_").replace("%", "pct").replace("/","_")
            #Here, we creating conditions
            if(not tablename[0].isalpha()):
                tablename = "t_" + tablename
            df.to_sql(tablename,con=conn,if_exists='replace',dtype = {col:'text' for col in df}, index=False)
           
    
    except ConnectionError:
        #Raises exception on unable to establish connection
        print("Unable to get database connection.. Exiting out of program")
        raise SystemExit
    
    finally:
        conn.close()
        #Closes connection upon running the query & Enables garbage collection
    return

create_tables() 







#making connection to the db
conn = sqlite3.connect("medicare_hospital_compare.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()
rows = c.execute('SELECT * FROM hospital_general_information')

list_of_rows_from_table=list()
#fetching the data from hospital_general_information
for row in rows:
    list_of_rows_from_table.append(dict(row))



conn.close()   
  
 
#1) reads the hospital_ranking_focus_state file

df_rows_table = pd.DataFrame(list_of_rows_from_table)

k_url = "http://kevincrook.com/utd/hospital_ranking_focus_states.xlsx"
r = requests.get(k_url)
xf = open("hospital_ranking_focus_states.xlsx","wb")
xf.write(r.content)
#2) creates a dataframe  : df_hospital_national_ranking which contains data from sheet : Hospital National Ranking
xf.close()


xls_file = pd.ExcelFile('hospital_ranking_focus_states.xlsx')
df_hospital_national_ranking=xls_file.parse('Hospital National Ranking')
df_focus_states=xls_file.parse('Focus States')
#3) crates a dataframe : df_focus_states which contains data from sheet : Focus States'



df_hospital_rank_100=df_hospital_national_ranking[:100].copy()



# we filter out the first rows from the ranking dataframe & convert the data type of provider id to int64 so that we can perform the merge operation below.

df_rows_table['provider_id']=df_rows_table['provider_id'].astype(np.int64)


#the below line is equivalant to a join between the data from :1) df_hospital_rank_100 & 2) df_rows_table


df_hospital_rank_100_merged=pd.merge(left=df_hospital_rank_100,right=df_rows_table,left_on='Provider ID',right_on='provider_id')
df_hospital_rank_100_merged.rename(columns={'hospital_name':'Hospital Name','city':'City','state':'State','county_name':'County'},inplace=True)
df_hospital_rank_100_merged_filtered=df_hospital_rank_100_merged[['Provider ID','Hospital Name','City','State','County']].copy()
df_hospital_rank_100_merged_filtered['Provider ID']=df_hospital_rank_100_merged_filtered['Provider ID'].astype(str).str.rjust(6,'0')
df_hospital_rank_100_merged_filtered.set_index('Provider ID',inplace=True)
#we copy the columns required into a staging dataframe & we remove the automatically created indexed column by setting the Provider ID 





df_focus_states.sort_values(by='State Name',inplace=True)
dict_of_state_abbr_sorted = dict(zip(df_focus_states['State Name'],df_focus_states['State Abbreviation']))
writer=pd.ExcelWriter('hospital_ranking.xlsx')
df_hospital_rank_100_merged_filtered.to_excel(writer,'Nationwide')


#we create an ExcelWriter object & we create a sheet where we store our filtered dataframe.we will now iterate through the key, value pair.
 

for key,value in dict_of_state_abbr_sorted.items():
    
    
    
    df_rows_table_filter_by_state_name=df_rows_table[(df_rows_table.state==value)].copy()
    
    #we filter the rows by state name from df_rows_table & inner join and get eht common data from & rename the colums
    
    
     
    df_hospital_filtered_by_state_name_merged=pd.merge(left=df_hospital_national_ranking,right=df_rows_table_filter_by_state_name,left_on='Provider ID',right_on='provider_id')
    
    
    
    df_hospital_filtered_by_state_name_merged.rename(columns={'hospital_name':'Hospital Name','city':'City','state':'State','county_name':'County'},inplace=True)
    
    
    
    df_hospital_filtered_by_state_name_merged.sort_values(by='Ranking',inplace=True)
    
    
    
    
    df_hospital_filtered_by_state_name_merged_columns_filtered=df_hospital_filtered_by_state_name_merged[['Provider ID','Hospital Name','City','State','County']].copy()
    #sort the data obtained per state by Ranking Column. we then filter out the required column and se the Provider ID as the key
    df_hospital_filtered_by_state_name_merged_columns_filtered['Provider ID']=df_hospital_filtered_by_state_name_merged_columns_filtered['Provider ID'].astype(str).str.rjust(6,'0')
    df_hospital_filtered_by_state_name_merged_columns_filtered.set_index('Provider ID',inplace=True)
    df_hospital_filtered_by_state_filtered_100=df_hospital_filtered_by_state_name_merged_columns_filtered[:100].copy()
    
    df_hospital_filtered_by_state_filtered_100.to_excel(writer,key)
    
    #we write the data to a new sheet in the excel file & we will now prepare the measure_statistics.xlsx

    


    

writer.save()


conn = sqlite3.connect("medicare_hospital_compare.db")
conn.row_factory = sqlite3.Row
c = conn.cursor()
rows = c.execute('SELECT state,measure_id,measure_name,score FROM timely_and_effective_care___hospital')

#we are creating a list from the rows of the table with each row as dictionaries.

list_of_rows_from_timely_and_effective_data_table=list()

for row in rows:
    list_of_rows_from_timely_and_effective_data_table.append(dict(row))

conn.close()


df_rows_timely_and_effective_care__hospital_table = pd.DataFrame(list_of_rows_from_timely_and_effective_data_table)

#we are creating a dataframe from the above list to perform the aggregations operations & We are getting unique measure id

set_of_measure_id=set(df_rows_timely_and_effective_care__hospital_table['measure_id'])
list_of_data_frames=list()
for measure_id in set_of_measure_id:
    
    df_rows_filtered_measure_id=df_rows_timely_and_effective_care__hospital_table[(df_rows_timely_and_effective_care__hospital_table.measure_id==measure_id)].copy()
    
    #we are forming list which are data frames corresponding to each measure id
    df_rows_filtered_measure_id_only_numerical=df_rows_filtered_measure_id[(df_rows_filtered_measure_id['score'].apply(lambda x : x.isdigit() == True))]
    list_of_data_frames.append(df_rows_filtered_measure_id_only_numerical)





resultant_data_frame=pd.concat(list_of_data_frames)


final_set_of_measure_id=set(resultant_data_frame['measure_id'])




resultant_data_frame['score']=resultant_data_frame['score'].astype(np.int64)

#we get a dataframe with all the measureid's & we again get the unique measure id's as some of the measureid might be filtered in the previous step


list_nationwide=[]

'''
this loop we are performing the following operation
1) 
2)  
3) we then add them to the list_nationwide that we created above
'''
for meid in final_set_of_measure_id:
    
    dictionay_of_nationwide_main=dict()
    df_rows_filtered_meid=resultant_data_frame[(resultant_data_frame.measure_id==meid)].copy()
    
    dictionay_of_nationwide_main['Measure ID']=meid
    #measures_statistics.xlsx & Getting the rows from the main data frame filtered by the Measure Id
    dictionay_of_nationwide_main['Measure Name']=list(df_rows_filtered_meid['measure_name'])[0]
    
    dictionay_of_nationwide_main['Minimum']=(df_rows_filtered_meid['score']).min()
    dictionay_of_nationwide_main['Maximum']=(df_rows_filtered_meid['score']).max()
    dictionay_of_nationwide_main['Average']=(df_rows_filtered_meid['score']).mean()
    dictionay_of_nationwide_main['Standard Deviation']=(df_rows_filtered_meid['score']).std()
    #for each measure id , we calculate the minimum, maximum, average and standard deviation
    list_nationwide.append(dictionay_of_nationwide_main)
    
    



nationwide_main_dataframe=pd.DataFrame(list_nationwide, columns=['Measure ID', 'Measure Name', 'Minimum','Maximum','Average','Standard Deviation'])

nationwide_main_dataframe.sort_values(by='Measure ID',inplace=True)

nationwide_main_dataframe.set_index('Measure ID',inplace=True)


writer=pd.ExcelWriter('measures_statistics.xlsx')

#We create a main dataframe from the list that we created above and add appropriate column names & we then create a sheet "Nationwide" and write the nationwide_main_dataframe in that sheet

nationwide_main_dataframe.to_excel(writer,'Nationwide')



for key,value in dict_of_state_abbr_sorted.items():
    
   
    list_of_state_wise_aggregated_dictionaries=[]
    dict_of_state_wise_aggregation=dict()
    
    
    
    resultant_data_frame_filter_by_state_name=resultant_data_frame[(resultant_data_frame.state==value)].copy()
    
    
    #we then get the key, value from the dict_of_state_abbr_sorted dictionaries and execute the loop & filter the rows by state name from resultant_data_frame
    
    
    
    
    df_resultant_groupby=pd.DataFrame(resultant_data_frame_filter_by_state_name.groupby(['measure_id','measure_name'])['score'].min())
    df_resultant_groupby['Maximum']=pd.DataFrame(resultant_data_frame_filter_by_state_name.groupby(['measure_id','measure_name'])['score'].max())
    df_resultant_groupby['Average']=pd.DataFrame(resultant_data_frame_filter_by_state_name.groupby(['measure_id','measure_name'])['score'].mean())
    df_resultant_groupby['Standard Deviation']=pd.DataFrame(resultant_data_frame_filter_by_state_name.groupby(['measure_id','measure_name'])['score'].std())
    df_resultant_groupby.reset_index(inplace=True)
    #we then perform the aggregation by score group by measureid , we get the following aggregations
                                                                                                        
    
    
    df_resultant_groupby.rename(columns={'score':'Minimum','measure_id':'Measure ID','measure_name':'Measure Name'},inplace=True)
    
    df_resultant_groupby.sort_values(by='Measure ID',inplace=True)
    df_resultant_groupby.set_index('Measure ID',inplace=True)
    
    df_resultant_groupby.to_excel(writer,key)
    



writer.save()

#we then rename the score and measure_id column according to the specification mentioned & close the connection  
    

conn.close()

