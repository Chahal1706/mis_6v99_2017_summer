import pandas as pd
import numpy as np
import requests
import os
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules



'''we will download the training set and load it in the dataframe'''

#This line is initializing the place holder for the url path and will make a staging directory to s tore zip folder 
url="http://kevincrook.com/utd/market_basket_training.txt"
r = requests.get(url)
staging_dir_name = "C:\\Users\\chaha\\Downloads\\ml_assignment"
if not os.path.exists(staging_dir_name):
    os.mkdir(staging_dir_name)
training_file = os.path.join(staging_dir_name, "market_basket_training.txt")
zf = open(training_file,"wb")
zf.write(r.content)
zf.close()


training_dataframe=pd.DataFrame([line.strip().split(',') for line in open('C:\\Users\\chaha\\Downloads\\ml_assignment\\market_basket_training.txt', 'r')]).fillna('NULL')


#training_dataframe=training_dataframe.reset_index()

#print(training_dataframe)

#print(training_dataframe.dtypes)

list_of_products=['P01','P02','P04','P05','P06','P07','P08','P09','P10']

d = {'P01': 1, 'P02': 2, 'P03': 3, 'P04' : 4, 'P05' : 5, 'P06': 6, 'P07' : 7,'P08': 8, 'P09': 9, 'P10': 10}
dataframe_replace_values=pd.DataFrame(list(d.items()),columns=['old_values','new_values'])
    

training_dataframe.replace(d, inplace=True)

print(training_dataframe)
