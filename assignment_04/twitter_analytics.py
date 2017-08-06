# Here, we import all the important libraries for the assignment 4


import tweepy
import json
import requests
import numpy as np
import pandas as pd
import os
import requests
import codecs
#Now, we will establish a streaming session and routes messages to StreamListener instance
class MyStreamListener(tweepy.StreamListener):
    def _init_(self, max_responses):
        self.max_responses = max_responses
        self.num_respinses = 0
def on_data(self, data):
    #Here, we will take the maximum responses
    if self.num_responses == self.max_responses:
        return False
    self.num_responses += 1
    
    json_data = json.loads(data)
    
    print(json.dumps()) 
    # Create class MyStreamListener inheriting from StreamListener and overriding on_status
    print("\n\n")
    print("===============================")
    print("===============================")
    
    print(json.dumps(json_data, sort_keys= True, indent=4))
    #Here, we use on_error to catch 420 errors and disconnect our stream
    if 'text' in json_data:
        print("\n\ntweet:",json_data['text'])
        
def on_error(self, error_code):
    print("error:", error_code)
    if eroor_code == 420:
        
        # this line of code will return the false values
        return False

consumer_key =consumer_secret = "MjqClhtU8B3f7wiZI2suLNBfe"
access_token = "794546729584496641-JD1n9KlZEdbi1mpu9HMd9e0RMNBW5s5"
access_token_secret = "3TMebAr3JUGG7NQrs9WBVGDmrZ7zsvArSQ79TevfJYiKm"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# here, we are setting the access token and secret token
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


my_stream_listener = MyStreamListener(100)

my_stream = tweepy.Stream(auth = api.auth, 
                                 listener = my_stream_listener,
                                 # here, we are setting listener setthings
                                 timeout = 60,
                                 wait_on_rate_limit = True
                         ) 


my_stream.filter(track = ['Trump', 'Clinton'])
my_stream.sample()

# Here, we are filtering the stream with language "eng"
my_stream.filter(languages=['en'], async = True)

print(my_stream, (5))


url = 'http://kevincrook.com/utd/tweets.json'
r = requests.get(url)
#print((r.content))
twitter_file = "tweets.json"
# Now, we open a new file twitter file
zf = open(twitter_file,"wb")
zf.write(r.content)
zf.close()
df=pd.read_json('tweets.json')
# now, we write the contents of json tweets file to the twitter file txt
#print(df)

twitter="twitter_analytics.txt"
zf = open(twitter,"wb")
zf.close()


#print(df[:5])

Number_events = len(df.index)
# Here, we calculate the no of events by calculating the rows
print(Number_events)

total_rows = df.count()
print(total_rows)

total_text_count = df['text'].count()
#print (total_text_count)


total_rows3 = df['lang'].count()
#print (total_rows3)





# Now, we count frequencies of tweets in each laguage
counts = df.groupby('lang',).size()
print(type(counts))
df_counts=counts.to_frame().reset_index()

df_counts.rename(columns={0:'counts'},inplace=True)

# Now, we rename columns 


df_counts.sort_values(['counts'],ascending=False,inplace=True)
#print(df_counts.dtypes)
# Now,we will have the count of language in decending order
lang_counts=''

for index,row in df_counts.iterrows():
    lang_counts+='{},{}\n'.format(row[0],row[1])
    #print(row[0],',',row[1])


# Now, we will write all the query output to twitter_analytics text file    
#print(lang_counts)
f=open("twitter_analytics.txt","w" )
f.write('{}\n'.format(Number_events))
f.write('{}\n'.format(total_text_count))
f.write(lang_counts)

# we will close the file
f.close()


#second Sheet work starts here and we create an new file twitter_2

twitter_2="tweets.txt"
zf = open(twitter_2,"wb")
zf.close()

import codecs

tweettexts= df[df.text.notnull()]['text']
# Here, we have tweets_texts file which will have each tweet in each row
tweet_texts=''
for row in tweettexts:
    tweet_texts+='{}\n'.format(row)


with codecs.open('tweets.txt','w','UTF-8') as file:
    file.write(tweet_texts)
    
file.close()
