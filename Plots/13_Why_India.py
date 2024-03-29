from curses.ascii import NUL
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime

sep = "\n\n$$$$$$$$$$\n\n"

f_users = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/11_DataCommentsRetrieve/comments.txt')
    
tweets = f_users.read().split("\n\n$$$$$$$$$$\n\n")

keywords = ['covid', 'labour', 'oxygen', 'farmer', 'muslim', 'religion', 'dalit', 'cbse']
freq = [0 for _ in keywords]
# for i in keywords :
#     freq.append(0)

count = 0 

for each_tweet in tweets[0:-1]:

        json_each_tweet = json.loads(each_tweet)

        ### situation of error
        if json_each_tweet.get('data') == None :
            continue

        ## check if original post
        text = json_each_tweet['data'][0]['text']
            
        for i,item in enumerate(keywords) :
            if text.find(item) != -1 :
                freq[i] += 1 

        ## check if retweet, reply, quoted
        if json_each_tweet.get('data')[0].get('referenced_tweets') != None and json_each_tweet['includes'].get('tweets') != None :
            ref_text = json_each_tweet['includes']['tweets'][0]['text']

            for i,item in enumerate(keywords) :
                if ref_text.find(item) != -1 :
                    freq[i] += 1 

print(keywords)
print(freq)      
print(sum(freq))