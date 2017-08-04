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


if os.path.exists('market_basket_recommendations.txt'):
    os.remove('market_basket_recommendations.txt')


training_dataframe=pd.DataFrame([line.strip().split(',') for line in open('C:\\Users\\chaha\\Downloads\\ml_assignment\\market_basket_training.txt', 'r')]).fillna('NULL')


#training_dataframe=training_dataframe.reset_index()

#print(training_dataframe)

#print(training_dataframe.dtypes)

list_of_products=['P01','P02','P04','P05','P06','P07','P08','P09','P10']

print(training_dataframe[:5])

training_dataframe.set_index(0,inplace=True)

list_of_combinations_products_training=[]
for index,row in training_dataframe.iterrows():
    list_of_elements=[]
    for elem in row:
        if elem!='NULL':
            list_of_elements.append(elem)
    list_of_combinations_products_training.append(set(list_of_elements))
    
print(list_of_combinations_products_training[:5])



list_of_combinations=[]
list_of_frequencies=[]
for elem in list_of_combinations_products_training:
    if elem not in list_of_combinations:
        list_of_combinations.append(elem)
        list_of_frequencies.append(list_of_combinations_products_training.count(elem))
    
print(list_of_combinations[:5])
print(list_of_frequencies[:5])


url="http://kevincrook.com/utd/market_basket_test.txt"
r = requests.get(url)
print(r)


staging_dir_name = "C:\\Users\\chaha\\Downloads\\marketbasket_test"
if not os.path.exists(staging_dir_name):
    os.mkdir(staging_dir_name)
test_file = os.path.join(staging_dir_name, "market_basket_test.txt")

zf = open(test_file,"wb")
zf.write(r.content)
zf.close()


test_dataframe=pd.DataFrame([line.strip().split(',') for line in open('C:\\Users\\chaha\\Downloads\\marketbasket_test\\market_basket_test.txt', 'r')]).fillna('NULL')

print(test_dataframe[:10])
test_dataframe.set_index(0,inplace=True)
test_dataframe[:5]

import itertools
import codecs


for index,row in test_dataframe.iterrows():
    if 1==1:
        list_of_test_products=[]
        for elem in row:
            if elem != 'NULL':
                list_of_test_products.append(elem)
        set_of_test_products=set(list_of_test_products)
        #print("1at" ,set_of_test_products)
        #print("number of elements: ",len(list_of_test_products))
        counter = len(list_of_test_products)
        list_of_possibilities=[]
        for L in range(1,len(list_of_test_products)+1):
            subset_list=[]
            for subset in itertools.combinations(list_of_test_products, L):
                subset_list.append(subset)
        #print(subset)
            list_of_possibilities.append(subset_list)
        #print("pssib:",list_of_possibilities)
        number_possibilities=len(list_of_possibilities)
        #print("printint")
        outer_main_list=[]
        
        for n in range(number_possibilities-1,-1,-1):
            main_list=[]
            for elements in list_of_possibilities[n]:
                #print("elemtns",set(elements))
                #print("lenth ",len(elements))
                list_of_testing_combinations_frequencies=[]
                list_of_testing_combinations=[x for x in  list_of_combinations if all(i in x for i in elements)  and len(x) == (len(elements)+1)]
                main_list.extend(list_of_testing_combinations)
                #print("printing")
                #print("main_list",main_list)
                outer_main_list=main_list[:]
            if len(main_list)>0:
                break
        #print(len(outer_main_list))
        list_of_indexes=[list_of_combinations.index(x) for x in outer_main_list]
        #print("list_of_indexes",len(list_of_indexes))
        list_of_testing_combinations_frequencies=[list_of_frequencies[x] for x in list_of_indexes]
        #print("testing_combination_frequencides",len(list_of_testing_combinations_frequencies))

        #print("indexes",list_of_indexes)
        #print("list_of_testing_combinations_frequencies",list_of_testing_combinations_frequencies)
        
        frequency_dataframe=pd.DataFrame({'combinations':outer_main_list,'frequencies':list_of_testing_combinations_frequencies},columns=['combinations','frequencies'])


        #print(frequency_dataframe)

        frequency_dataframe.sort_values(by='frequencies',inplace=True,ascending=False)
        #print(frequency_dataframe)
        #print("tesing set:",set_of_test_products)
        #print(frequency_dataframe['combinations'].values[0])
        #print(index)
        recommendation=frequency_dataframe['combinations'].values[0] - set_of_test_products
        #print(list(recommendation)[0])
        recommendation_product=list(recommendation)[0]
        #print("finidhssfdsfdsfsf")
        #print(set_of_test_products)
        with codecs.open('market_basket_recommendations.txt','a','UTF-8') as file:
            line='{},{}'.format(index,recommendation_product)
            file.write(line+"\n")
        
        #a = [1,2,3]
        #b = [1,2]
        #[i for i in a if i not in b]

#print(list_of_possibilities)
