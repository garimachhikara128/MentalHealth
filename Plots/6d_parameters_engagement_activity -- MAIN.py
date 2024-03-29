import json
import math
from datetime import datetime, timedelta
from statistics import pvariance
import numpy as np
from scipy.stats import ks_2samp,kstest
from scipy import stats
import random
import scikit_posthocs as sp

info_followers = [0,0,0]
info_following = [0,0,0]
info_users = [0,0,0]
# info_tweet_freq = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]


followers_list = [[],[],[]]
following_list = [[],[],[]]
tweet_list = [[],[],[]]

a_followers_list = [[],[],[]]
a_following_list = [[],[],[]]
a_tweet_list = [[],[],[]]

eng_followers = [[],[],[]]
eng_following = [[],[],[]]
eng_tweets = [[],[],[]]

act_followers = [[],[],[]]
act_following = [[],[],[]]
act_tweets = [[],[],[]]

f1 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_total.txt')
users_d = f1.read().split("\n")

f2 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_total.txt')
users_a = f2.read().split("\n")

num_low = 0 
num_moderate = 0
num_high = 0

nou = 0 

for each_user_d,each_user_a in zip(users_d[0:-1], users_a[0:-1]) :

    idx = 10000
    each_user_split_d = each_user_d.split(" ")
    author_id = each_user_split_d[0] 
    depress_tweet_count = each_user_split_d[1]

    each_user_split_a = each_user_a.split(" ")
    all_tweet_count = each_user_split_a[1]

    # countss = (int)(depress_tweet_count) / (int)(all_tweet_count)
    # print(countss)

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

    f_users = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/7_DataUserTimeline/' + author_id + '.txt')
    
    tweets = f_users.read().split("\n\n$$$$$$$$$$\n\n")

    tweet_count = 0
    for each_tweet in tweets[0:-1]:
        tweet_count += 1

    json_each_tweet = json.loads(tweets[0])
    followers_count = json_each_tweet['author_followers_count']
    following_count = json_each_tweet['author_following_count']
    tweet_created_at = datetime.strptime(json_each_tweet['tweet_created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    author_created_at = datetime.strptime(json_each_tweet['author_created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
    
    gap = (tweet_created_at - author_created_at).days
    if(gap == 0) :
        gap = 1 

    eng_followers[idx].append(math.log(1+followers_count))
    eng_following[idx].append(math.log(1+following_count))
    eng_tweets[idx].append(math.log(1+tweet_count))

    act_followers[idx].append(math.log(1+(followers_count/gap)))
    act_following[idx].append(math.log(1+(following_count/gap)))
    act_tweets[idx].append(math.log(1+(tweet_count/gap)))

    followers_list[idx].append(followers_count) 
    following_list[idx].append(following_count) 
    tweet_list[idx].append(tweet_count) 

    a_followers_list[idx].append(followers_count/gap) 
    a_following_list[idx].append(following_count/gap) 
    a_tweet_list[idx].append(tweet_count/gap) 

    nou += 1

print("EXACT VALUES :--")
for i in range(0,3) :
    print(i)
    print("Mean: " , round(np.mean(followers_list[i]),2))
    # print("Deviation: " , round(np.std(followers_list[i]),2))

    print("Mean: " , round(np.mean(following_list[i]),2))
    # print("Deviation: " , round(np.std(following_list[i]),2))

    print("Mean: " , round(np.mean(tweet_list[i]),2))
    # print("Deviation: " , round(np.std(tweet_list[i]),2))

print("ACTIVITY")
for i in range(0,3) :
    print(i)
    print("Mean: " , round(np.mean(a_followers_list[i]),2))
    # print("Deviation: " , round(np.std(a_followers_list[i]),2))

    print("Mean: " , round(np.mean(a_following_list[i]),2))
    # print("Deviation: " , round(np.std(a_following_list[i]),2))

    print("Mean: " , round(np.mean(a_tweet_list[i]),2))
    # print("Deviation: " , round(np.std(a_tweet_list[i]),2))

print("\nEngagement Followers :")

for i in range(0,3) :
    # print("Mean: " , round(np.mean(eng_followers[i])),3)
    print("Median: " , round(np.median(eng_followers[i]),2))
    print("Deviation: " , round(np.std(eng_followers[i]),2))

print("\nEngagement Following :")

for i in range(0,3) :
    # print("Mean: " , round(np.mean(eng_following[i])),3)
    print("Median: " ,  round(np.median(eng_following[i]),2))
    print("Deviation: " , round(np.std(eng_following[i]),2))

print("\nEngagement Tweets :")

for i in range(0,3) :
    print("Median: " , round(np.median(eng_tweets[i]),2))
    print("Deviation: " , round(np.std(eng_tweets[i]),2))

print("######")

print("\nActivity Followers :")

for i in range(0,3) :
    print("Median: " , round(np.median(act_followers[i]),2))
    print("Deviation: " , round(np.std(act_followers[i]),2))

print("\nActivity Following :")

for i in range(0,3) :
    print("Median: " , round(np.median(act_following[i]),2))
    print("Deviation: " , round(np.std(act_following[i]),2))

print("\nActivity Tweets :")

for i in range(0,3) :
    print("Median: " , round(np.median(act_tweets[i]),2))
    print("Deviation: " , round(np.std(act_tweets[i]),2))

#### TESTS

for i in range(0,3) :
    for j in range(i+1,3) :
        statistic, pvalue = ks_2samp(tweet_list[i], tweet_list[j])
        # statistic, pvalue = stats.ttest_ind(act_following[i], act_following[j], equal_var=False)
        # statistic, pvalue = stats.kruskal(eng_tweets[0], eng_tweets[1],eng_tweets[2])
        print(i,j)
        print("Test statistic: " , round(statistic,2), "P-value: " , round(pvalue,5))
        if(pvalue <= 0.001) :
            print("***")
        elif(pvalue <= 0.01) :
            print("**")
        elif(pvalue <= 0.05) :
            print("*")
        else :
            print("related")
        print("\n")
