import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import ks_2samp

years =     ['2017',  '2018',  '2019',  '2020',  '2021',  '2022']
info_reply = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_like = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_retweet = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_mentions = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
info_tweet_freq = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]

ll_info_reply = [[[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]]
ll_info_like = [[[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]]
ll_info_retweet = [[[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]]
ll_info_mention = [[[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]]
# ll_info_tweet_freq = [[[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]]

f1 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_total.txt')
users_d = f1.read().split("\n")

f2 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_total.txt')
users_a = f2.read().split("\n")

num_low = 0 
num_moderate = 0
num_high = 0

count_low = 0
count_moderate = 0
count_high = 0 

nou = 0 

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

    f_users = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/7_DataUserTimeline/' + author_id + '.txt')
    
    tweets = f_users.read().split("\n\n$$$$$$$$$$\n\n")

    for each_tweet in tweets[0:-1]:
        json_each_tweet = json.loads(each_tweet)
        text = json_each_tweet['tweet_text']
        
        year = (int)(json_each_tweet['tweet_created_at'][0:4])
       
        reply_count = json_each_tweet['tweet_reply_count']
        like_count = json_each_tweet['tweet_like_count']
        retweet_count = json_each_tweet['tweet_retweet_count']

        mentions_count = 0
        for i in range(0,len(text)) :
            if text[i] == '@' :
                mentions_count += 1

        info_reply[year-2017][idx] += reply_count
        info_like[year-2017][idx] += like_count
        info_retweet[year-2017][idx] += retweet_count
        info_mentions[year-2017][idx] += mentions_count
        info_tweet_freq[year-2017][idx] += 1

        ll_info_reply[year-2017][idx].append(reply_count)
        ll_info_like[year-2017][idx].append(like_count)
        ll_info_retweet[year-2017][idx].append(retweet_count)
        ll_info_mention[year-2017][idx].append(mentions_count)

        if idx == 0 : 
            count_low += 1
        elif idx == 1 :
            count_moderate += 1
        else :
            count_high += 1
        
    nou += 1
    # print(nou)

print(count_low) 
print(count_moderate)
print(count_high)

print(num_low) 
print(num_moderate)
print(num_high)

print(info_reply)
print(info_like)
print(info_retweet)
print(info_mentions)
print(info_tweet_freq)

bl_reply = []
bl_like = []
bl_retweet = []
bl_mentions = []

for ir,il,irt, im, itf,y in zip(info_reply, info_like, info_retweet, info_mentions, info_tweet_freq, years) :
    sl_reply = [y]
    sl_like = [y]
    sl_retweet = [y]
    sl_mentions = [y]
    for eir, eil, eirt, eim, eitf in zip(ir, il, irt, im, itf) :

        if eitf == 0 :
            eitf = 1

        sl_reply.append(round(eir/eitf,2))
        sl_like.append(round(eil/eitf,2))
        sl_retweet.append(round(eirt/eitf,2))
        sl_mentions.append(round(eim/eitf,2))

    bl_reply.append(sl_reply)
    bl_like.append(sl_like)
    bl_retweet.append(sl_retweet)
    bl_mentions.append(sl_mentions)

print("\n\nReply\n" , bl_reply)
print("\n\nLike\n" , bl_like)
print("\n\nRetweets\n" , bl_retweet)
print("\n\nMentions\n" , bl_mentions)

print("\n\nReply:-", )
for i in range(0,6) :
    print(2017+i, " :-")
    for j in range(0,3) :
        if (j == 0) :
            print("Low")
        elif(j == 1) : 
            print("Moderate") 
        else :
            print("High")

        print("Mean(Deviation) " , round(np.mean(ll_info_reply[i][j]),2) , "(" , round(np.std(ll_info_reply[i][j]),2), ")")

for y in range(0,6) :
    print("year ", (2017+y))
    for i in range(0,3) :
        for j in range(i+1,3) :
            print(i,j)
            statistic, pvalue = ks_2samp(ll_info_reply[y][i], ll_info_reply[y][j])
            star = "related"
            if(pvalue <= 0.001) :
                star = "***"
            elif(pvalue <= 0.01) :
                star = "**"
            elif(pvalue <= 0.05) :
                star = "*"

            print("Test statistic: " , round(statistic,2), star)

print("------------------")

print("\n\nLike:-", )
for i in range(0,6) :
    print(2017+i, " :-")
    for j in range(0,3) :
        if (j == 0) :
            print("Low")
        elif(j == 1) : 
            print("Moderate") 
        else :
            print("High")

        print("Mean(Deviation) " , round(np.mean(ll_info_reply[i][j]),2) , "(" , round(np.std(ll_info_reply[i][j]),2), ")")

for y in range(0,6) :
    print("year ", (2017+y))
    for i in range(0,3) :
        for j in range(i+1,3) :
            print(i,j)
            statistic, pvalue = ks_2samp(ll_info_like[y][i], ll_info_like[y][j])
            star = "related"
            if(pvalue <= 0.001) :
                star = "***"
            elif(pvalue <= 0.01) :
                star = "**"
            elif(pvalue <= 0.05) :
                star = "*"

            print("Test statistic: " , round(statistic,2), star)

print("------------------")

print("\n\nMention:-", )
for i in range(0,6) :
    print(2017+i, " :-")
    for j in range(0,3) :
        if (j == 0) :
            print("Low")
        elif(j == 1) : 
            print("Moderate") 
        else :
            print("High")

        print("Mean(Deviation) " , round(np.mean(ll_info_reply[i][j]),2) , "(" , round(np.std(ll_info_reply[i][j]),2), ")")

for y in range(0,6) :
    print("year ", (2017+y))
    for i in range(0,3) :
        for j in range(i+1,3) :
            print(i,j)
            statistic, pvalue = ks_2samp(ll_info_mention[y][i], ll_info_mention[y][j])
            star = "related"
            if(pvalue <= 0.001) :
                star = "***"
            elif(pvalue <= 0.01) :
                star = "**"
            elif(pvalue <= 0.05) :
                star = "*"

            print("Test statistic: " , round(statistic,2), star)

print("------------------")

                     
############## PLOTS ###############

# create data
df_reply = pd.DataFrame(bl_reply,
                   columns=['Reply', 'Low', 'Moderate', 'High'])

df_like = pd.DataFrame(bl_like,
                   columns=['Like', 'Low', 'Moderate', 'High'])

df_retweet = pd.DataFrame(bl_retweet,
                   columns=['Retweet', 'Low', 'Moderate', 'High'])

df_mentions = pd.DataFrame(bl_mentions,
                   columns=['Mentions', 'Low', 'Moderate', 'High'])

# view data
# print(df)

hatch = [ "/","/","/","/","/","/", "o","o","o","o","o","o", '.','.','.','.','.','.']

fig, axes = plt.subplots(nrows=1, ncols=3) #, figsize=(10, 4.77))
fig.tight_layout()
# plot grouped bar chart
bars1 = df_reply.plot(x='Reply',
        kind='bar',
        stacked=False,
        grid=True,
        # ylim = (0,0.5),
        # rot=0,
        color = ['palegreen', 'cyan', 'wheat'],
        width = 0.75,
        ax=axes[0],
        legend = False,
        fontsize = 12
        )
bars1.set_ylabel('Avg. number of replies per tweet', fontdict={'fontsize':12})
bars1.set_xlabel('Reply', fontdict={'fontsize':12})

# i = 0
# for patch in bars1.patches:
#    patch.set_hatch(hatch[i])
#    i = i + 1

# plot grouped bar chart
bars2 = df_like.plot(x='Like',
        kind='bar',
        stacked=False,
        grid=True,
        # ylim = (0,12),
        # rot=0,
        color = ['palegreen', 'cyan', 'wheat'],
        width = 0.75,
        ax=axes[1],
        fontsize = 12,
        legend = False,
        )
bars2.set_ylabel('Avg. number of likes per tweet', fontdict={'fontsize':12})
bars2.set_xlabel('Like', fontdict={'fontsize':12})

# i = 0
# for patch in bars2.patches:
#    patch.set_hatch(hatch[i])
#    i = i + 1

# bars3 = df_retweet.plot(x='Retweet',
#         kind='bar',
#         stacked=False,
#         grid=True,
#         # ylim = (0,0.5),
#         rot=0,
#         color = ['palegreen', 'cyan', 'wheat'],
#         width = 0.75,
#         ax=axes[1][0],
#         fontsize = 12,
#         legend = False,
#         )
# bars3.set_ylabel('Number of retweets per tweet', fontdict={'fontsize':10})
# bars3.set_xlabel('Retweet', fontdict={'fontsize':10})

bars4 = df_mentions.plot(x='Mentions',
        kind='bar',
        stacked=False,
        grid=True,
        # ylim = (0,3),
        # rot=0,
        color = ['palegreen', 'cyan', 'wheat'],
        width = 0.75,
        ax=axes[2],
        fontsize = 12,
        legend = False,
        )
bars4.set_ylabel('Avg. number of mentions per tweet', fontdict={'fontsize':12})
bars4.set_xlabel('Mentions', fontdict={'fontsize':12})

plt.legend(loc = "upper left")
# plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plot_measures_full.png", format="png", bbox_inches="tight")
# plt.show()