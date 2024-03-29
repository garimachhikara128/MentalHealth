import json
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ks_2samp
import numpy as np

# plt.style.use('seaborn')

years =     ['2017',  '2018',  '2019',  '2020',  '2021',  '2022']
info_reply = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_retweet = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_quote = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_org = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
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
        if json_each_tweet.get('data') == None :
            continue

        ### check among 4 categories
        author_id = json_each_tweet['data'][0]['author_id']
        year = (int)(json_each_tweet['data'][0]['created_at'][0:4])

        ## check if original post
        if json_each_tweet.get('data')[0].get('referenced_tweets') == None : 
            info_org[year-2017][user_type[author_id]] += 1

        ## check if retweet, reply, quoted
        if json_each_tweet.get('data')[0].get('referenced_tweets') != None : 

            ref_tweets = json_each_tweet['data'][0]['referenced_tweets']

            if len(ref_tweets) >= 2 :
                print(len(ref_tweets), ref_tweets)
            for each_ref_tweet in ref_tweets :
                type = each_ref_tweet['type']

                if type == 'retweeted' :
                    info_retweet[year-2017][user_type[author_id]] += 1
                elif type == 'replied_to' :
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

print("\n\nOriginal\n" , bl_org)
print("\n\nRetweet\n" , bl_retweet)
print("\n\nReply\n" , bl_reply)
print("\n\nQuote\n" , bl_quote)

# ############## PLOTS ###############

size = 17

# create data
df_org = pd.DataFrame(bl_org,
                   columns=['Org', 'Low', 'Moderate', 'High'])

df_retweet = pd.DataFrame(bl_retweet,
                   columns=['Retweet', 'Low', 'Moderate', 'High'])

df_reply = pd.DataFrame(bl_reply,
                   columns=['Reply', 'Low', 'Moderate', 'High'])

df_quote = pd.DataFrame(bl_quote,
                   columns=['Quote', 'Low', 'Moderate', 'High'])

# view data
# print(df)

hatch = [ "/","/","/","/","/","/", "o","o","o","o","o","o", '.','.','.','.','.','.']

# fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 4.77))

# plot grouped bar chart
bars1 = df_org.plot(x='Org',
        kind='bar',
        stacked=False,
        grid=True,
        # ylim = (0,0.5),
        rot=0,
        color = ['mediumseagreen', 'lightskyblue', 'lightcoral'],
        width = 0.75,
        # ax=axes[0][0],
        legend = False,
        fontsize = size
        )
bars1.set_ylabel('Avg. number of original posts', fontdict={'fontsize':size})
bars1.set_xlabel('Year', fontdict={'fontsize':size})

# i = 0
# for patch in bars1.patches:
#    patch.set_hatch(hatch[i])
#    i = i + 1

# plot grouped bar chart
# bars2 = df_retweet.plot(x='Retweet',
#         kind='bar',
#         stacked=False,
#         grid=True,
#         # ylim = (0,12),
#         rot=0,
#         color =  ['mediumseagreen', 'lightskyblue', 'lightcoral'],
#         width = 0.75,
#         # ax=axes[0][1],
#         fontsize = size,
#         legend = False,
#         )
# bars2.set_ylabel('Avg. number of retweeted posts', fontdict={'fontsize':size})
# bars2.set_xlabel('Year', fontdict={'fontsize':size})

# i = 0
# for patch in bars2.patches:
#    patch.set_hatch(hatch[i])
#    i = i + 1

# bars3 = df_reply.plot(x='Reply',
#         kind='bar',
#         stacked=False,
#         grid=True,
#         # ylim = (0,0.5),
#         rot=0,
#         color = ['mediumseagreen', 'lightskyblue', 'lightcoral'],
#         width = 0.75,
#         # ax=axes[1][0],
#         fontsize = size,
#         legend = False,
#        # figsize = (12,9)
#         )
# bars3.set_ylabel('Avg. number of replied posts', fontdict={'fontsize':size})
# bars3.set_xlabel('Year', fontdict={'fontsize':size})

# bars4 = df_quote.plot(x='Quote',
#         kind='bar',
#         stacked=False,
#         grid=True,
#         # ylim = (0,3),
#         rot=0,
#         color = ['palegreen', 'cyan', 'wheat'],
#         width = 0.75,
#         ax=axes[1][1],
#         fontsize = 12,
#         legend = False,
#         )
# bars4.set_ylabel('Avg Quotes', fontdict={'fontsize':10})
# bars4.set_xlabel('Year', fontdict={'fontsize':10})

# plt.legend(loc = "upper right", fontsize = size)
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plot_comment_org.pdf", format="pdf", bbox_inches="tight")
plt.show()