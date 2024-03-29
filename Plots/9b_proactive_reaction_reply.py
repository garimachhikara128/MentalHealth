from curses.ascii import NUL
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

years =     ['2017',  '2018',  '2019',  '2020',  '2021',  '2022']
tt = timedelta()
activation = [[tt,tt,tt], [tt,tt,tt], [tt,tt,tt], [tt,tt,tt], [tt,tt,tt], [tt,tt,tt]]
info_tweet_freq = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]

f1 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_total.txt')
users_d = f1.read().split("\n")

f2 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_total.txt')
users_a = f2.read().split("\n")

num_low = 0 
num_moderate = 0
num_high = 0

nou = 0 

user_type = {}

for each_user_d,each_user_a in zip(users_d[0:-1], users_a[0:-1]) :

    idx = 10000
    each_user_split_d = each_user_d.split(" ")
    author_id = each_user_split_d[0] 
    depress_tweet_count = each_user_split_d[1]

    each_user_split_a = each_user_a.split(" ")
    all_tweet_count = each_user_split_a[1]

    # countss = (int)(depress_tweet_count) / (int)(all_tweet_count)

    countss = (int)(depress_tweet_count)
    # print(countss)

    # frequency -> category
    if(countss <= 50) :
        idx = 0
        num_low += 1
    elif(countss <= 150) :
        idx = 1
        num_moderate += 1
    else :
        idx = 2
        num_high += 1

    user_type[author_id] = idx 

f_users = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/11_DataCommentsRetrieve/comments.txt')
    
tweets = f_users.read().split("\n\n$$$$$$$$$$\n\n")

for each_tweet in tweets[0:-1]:

        json_each_tweet = json.loads(each_tweet)

        ### situation of error
        if json_each_tweet.get('data') == None or json_each_tweet['includes'].get('tweets') == None:
            continue

        ### check among 4 categories
        author_id = json_each_tweet['data'][0]['author_id']
        year = (int)(json_each_tweet['data'][0]['created_at'][0:4])

        ## check if original post
        # if json_each_tweet.get('data')[0].get('referenced_tweets') == None : 
            # do nothing

        ## check if retweet, reply, quoted
        if json_each_tweet.get('data')[0].get('referenced_tweets') != None : 

            ref_tweets = json_each_tweet['data'][0]['referenced_tweets']
            user_tweet_time = datetime.strptime(json_each_tweet['data'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')

            org_tweet_time = datetime.strptime(json_each_tweet['includes']['tweets'][0]['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            diff = user_tweet_time - org_tweet_time
            # print(diff)

            for each_ref_tweet in ref_tweets :

                type = each_ref_tweet['type']

                # if type == 'retweeted' :
                #     # activation[year-2017][user_type[author_id]] += diff
                # el
                if type == 'replied_to' :
                    activation[year-2017][user_type[author_id]] += diff
                # elif type == 'quoted' :
                #     activation[year-2017][user_type[author_id]] += diff
            
                info_tweet_freq[year-2017][user_type[author_id]] += 1

    # nou += 1
    # print(nou)


print(num_low) 
print(num_moderate)
print(num_high)

print("tweet_freq")
print(info_tweet_freq)

bl = []
for ey in activation :
    sl = []
    for ee in ey :
        sl.append(ee.days)      
    bl.append(sl)

print("activation")
print(bl)

bl_avg_activation = []
for a,f,y in zip(bl, info_tweet_freq, years) :
    sl_a = [y]
    for ea, ef in zip(a,f) :
        sl_a.append(round((int)(ea)/(int)(ef),2))
    bl_avg_activation.append(sl_a)

print("avg activation")
print(bl_avg_activation)

#### PLOTS

df = pd.DataFrame(bl_avg_activation, columns=["Category", "Low", "Moderate", "High"])
df.plot(x="Category", y=["Low", "Moderate", "High"], kind="bar",figsize=(8,4), rot=0,color = ['palegreen', 'cyan', 'wheat'],grid=True)
plt.xlabel("Years")
plt.ylabel("Number of days")
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plot_proactive_reply.png", format="png", bbox_inches="tight")
plt.show()
