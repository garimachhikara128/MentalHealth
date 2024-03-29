from curses.ascii import NUL
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime

sep = "\n\n$$$$$$$$$$\n\n"

years =     ['2017',  '2018',  '2019',  '2020',  '2021',  '2022']
info_reply = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_retweet = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_quote = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_org = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_tweet_freq = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]

new_f_org_low = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/org_low.txt', 'wt')
new_f_org_moderate = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/org_moderate.txt', 'wt')
new_f_org_high = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/org_high.txt', 'wt')

new_f_retweet_low = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/retweet_low.txt', 'wt')
new_f_retweet_moderate = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/retweet_moderate.txt', 'wt')
new_f_retweet_high = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/retweet_high.txt', 'wt')

new_f_reply_low = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/reply_low.txt', 'wt')
new_f_reply_moderate = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/reply_moderate.txt', 'wt')
new_f_reply_high = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/reply_high.txt', 'wt')


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
        if json_each_tweet.get('data') == None :
            continue

        ### check among 4 categories
        author_id = json_each_tweet['data'][0]['author_id']
        year = (int)(json_each_tweet['data'][0]['created_at'][0:4])

        ## check if original post
        if json_each_tweet.get('data')[0].get('referenced_tweets') == None : 

            text = json_each_tweet['data'][0]['text']

            if user_type[author_id] == 0 :
                new_f_org_low.write(text) 
                # new_f_org_low.write(sep) 

            elif user_type[author_id] == 1 :
                new_f_org_moderate.write(text) 
                # new_f_org_moderate.write(sep) 

            elif user_type[author_id] == 2 :
                new_f_org_high.write(text) 
                # new_f_org_high.write(sep)   

            info_org[year-2017][user_type[author_id]] += 1

        ## check if retweet, reply, quoted
        if json_each_tweet.get('data')[0].get('referenced_tweets') != None and json_each_tweet['includes'].get('tweets') != None :

            ref_tweets = json_each_tweet['data'][0]['referenced_tweets']
            text = json_each_tweet['includes']['tweets'][0]['text']

            # if len(ref_tweets) >= 2 :
            #     print(len(ref_tweets), ref_tweets)

            for each_ref_tweet in ref_tweets :
                type = each_ref_tweet['type']

                if type == 'retweeted' :

                    if user_type[author_id] == 0 :
                        new_f_retweet_low.write(text) 
                        # new_f_retweet_low.write(sep) 

                    elif user_type[author_id] == 1 :
                        new_f_retweet_moderate.write(text) 
                        # new_f_retweet_moderate.write(sep) 

                    elif user_type[author_id] == 2 :
                        new_f_retweet_high.write(text) 
                        # new_f_retweet_high.write(sep) 

                    info_retweet[year-2017][user_type[author_id]] += 1

                elif type == 'replied_to' :

                    if user_type[author_id] == 0 :
                        new_f_reply_low.write(text) 
                        # new_f_reply_low.write(sep) 

                    elif user_type[author_id] == 1 :
                        new_f_reply_moderate.write(text) 
                        # new_f_reply_moderate.write(sep) 

                    elif user_type[author_id] == 2 :
                        new_f_reply_high.write(text) 
                        # new_f_reply_high.write(sep) 

                    info_reply[year-2017][user_type[author_id]] += 1

                elif type == 'quoted' :
                    info_quote[year-2017][user_type[author_id]] += 1
            
        info_tweet_freq[year-2017][user_type[author_id]] += 1

    # nou += 1
    # print(nou)


print(num_low) 
print(num_moderate)
print(num_high)

print(info_org)
print(info_retweet)
print(info_reply)
print(info_quote)
print(info_tweet_freq)

bl_org = []
bl_retweet = []
bl_reply = []
bl_quote = []

for io,irt,ir,iq,itf,y in zip(info_org, info_retweet, info_reply, info_quote, info_tweet_freq, years) :
    sl_org = [y]
    sl_retweet = [y]
    sl_reply = [y]
    sl_quote = [y]

    for eio,eirt,eir,eiq,eitf in zip(io,irt,ir,iq,itf) :

        sl_org.append(round(eio/eitf,2))
        sl_retweet.append(round(eirt/eitf,2))
        sl_reply.append(round(eir/eitf,2))
        sl_quote.append(round(eiq/eitf,2))

    bl_org.append(sl_org)
    bl_retweet.append(sl_retweet)
    bl_reply.append(sl_reply)
    bl_quote.append(sl_quote)

print("\n\nReply\n" , bl_org)
print("\n\nLike\n" , bl_retweet)
print("\n\nRetweets\n" , bl_reply)
print("\n\nMentions\n" , bl_quote)


# ############## PLOTS ###############

