#We are importing the required libraries for the assignment 

import pandas as pd
import numpy as np
import requests
import os
from mlxtend.frequent_patterns import apriori

#Here, we will import apriori algorithm and association rules
from mlxtend.frequent_patterns import association_rules



#we will download the training set and load it in the dataframe. This line is initializing the place holder for the url path and will make a staging directory to s tore zip folder''' 

url="http://kevincrook.com/utd/market_basket_training.txt"
r = requests.get(url)
#staging_dir_name = "ml_assignment"
#if not os.path.exists(staging_dir_name):
    #os.mkdir(staging_dir_name)
#Here, we will write the contents of market basket training text file to training file and close it

#training_file = os.path.join(staging_dir_name, "market_basket_training.txt")
training_file = "market_basket_training.txt"
zf = open(training_file,"wb")
zf.write(r.content)
zf.close()

if os.path.exists('market_basket_recommendations.txt'):
    os.remove('market_basket_recommendations.txt')
    
#If the files already exists just remove it and create new market_basket_recommendations.txt

training_dataframe=pd.DataFrame([line.strip().split(',') for line in open('market_basket_training.txt', 'r')]).fillna('NULL')

list_of_products=['P01','P02','P04','P05','P06','P07','P08','P09','P10']

training_dataframe.set_index(0,inplace=True)

list_of_combinations_products_training=[]


for index,row in training_dataframe.iterrows():
#Here, we iterate the rows of list_of_combinations_products_training with list of elements
    list_of_elements=[]
    for elem in row:
        if elem!='NULL':
            list_of_elements.append(elem)           
    list_of_combinations_products_training.append(set(list_of_elements))
#This command will print the list of combinations_products_trainings    
print(list_of_combinations_products_training[:5])

list_of_combinations=[]
list_of_frequencies=[]
for elem in list_of_combinations_products_training:
#We check if the elements doesn't exists then we append the file and find out frequency of product
    if elem not in list_of_combinations:
        list_of_combinations.append(elem)
        list_of_frequencies.append(list_of_combinations_products_training.count(elem))
    
print(list_of_combinations[:5])
print(list_of_frequencies[:5])

#Here, we download the test file from the path on the internet
url="http://kevincrook.com/utd/market_basket_test.txt"
r = requests.get(url)
print(r)


#staging_dir_name = "marketbasket_test"
#if not os.path.exists(staging_dir_name):
    #Here, we make a test file test_file and write contents of marketbasket_test in it
    #os.mkdir(staging_dir_name)
#test_file = os.path.join(staging_dir_name, "market_basket_test.txt")
test_file="market_basket_test.txt"
zf = open(test_file,"wb")
zf.write(r.content)
zf.close()

#Now, we create test_dataframe and split the file with comma which can be found on path given below

test_dataframe=pd.DataFrame([line.strip().split(',') for line in open('market_basket_test.txt', 'r')]).fillna('NULL')

print(test_dataframe[:10])
test_dataframe.set_index(0,inplace=True)
test_dataframe[:5]

import itertools
# importing codecs
import codecs


for index,row in test_dataframe.iterrows():
    if 1==1:
        list_of_test_products=[]
        for elem in row:
            #if the element is not null, append with elem
            if elem != 'NULL':
                list_of_test_products.append(elem)
        set_of_test_products=set(list_of_test_products)
        
        
        counter = len(list_of_test_products)
        list_of_possibilities=[]
        #print("number of elements: ",len(list_of_test_products))
        for L in range(1,len(list_of_test_products)+1):
            subset_list=[]
            for subset in itertools.combinations(list_of_test_products, L):
                
                subset_list.append(subset)
            
            list_of_possibilities.append(subset_list)
        #Here, we created a subset, print(subset), print("pssib:",list_of_possibilities)
        number_possibilities=len(list_of_possibilities)
        
        outer_main_list=[]
        
        for n in range(number_possibilities-1,-1,-1):
            main_list=[]
            for elements in list_of_possibilities[n]:
                #Here, we make a list make_list to get the frequencies of list_of_testing_combinations
                
                list_of_testing_combinations_frequencies=[]
                list_of_testing_combinations=[x for x in  list_of_combinations if all(i in x for i in elements)  and len(x) == (len(elements)+1)]
                main_list.extend(list_of_testing_combinations)
                
                
                outer_main_list=main_list[:]
            if len(main_list)>0:
                #If, length in main_list is greater than 0 then we come out of loop
                break
        
        list_of_indexes=[list_of_combinations.index(x) for x in outer_main_list]
        
        list_of_testing_combinations_frequencies=[list_of_frequencies[x] for x in list_of_indexes]
                       
        frequency_dataframe=pd.DataFrame({'combinations':outer_main_list,'frequencies':list_of_testing_combinations_frequencies},columns=['combinations','frequencies'])


        

        frequency_dataframe.sort_values(by='frequencies',inplace=True,ascending=False)
        
        #Now, we creates a dataframe to sort the values by frequences in frequency_dataframe               
        recommendation=frequency_dataframe['combinations'].values[0] - set_of_test_products
        
        recommendation_product=list(recommendation)[0]
        
        
        with codecs.open('market_basket_recommendations.txt','a','UTF-8') as file:
            line='{},{}'.format(index,recommendation_product)
            file.write(line+"\n")
            # Finally, we have recommendations avaiable in the file market_basket_recommendations
        
        
print("done")
