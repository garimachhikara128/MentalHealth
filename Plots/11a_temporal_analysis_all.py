import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

years =     ['2017',  '2018',  '2019',  '2020',  '2021',  '2022']
tt = timedelta()
activation = [[tt,tt,tt], [tt,tt,tt], [tt,tt,tt], [tt,tt,tt], [tt,tt,tt], [tt,tt,tt]]
info_tweet_freq = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]

low_freq = []
moderate_freq = []
high_freq = []

for i in range(0,24) :
    low_freq.append(0) 
    moderate_freq.append(0)
    high_freq.append(0)

f1 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_total.txt')
users_d = f1.read().split("\n")

f2 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_total.txt')
users_a = f2.read().split("\n")

num_low = 0 
num_moderate = 0
num_high = 0

nou = 0 

ll = []
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
        time = (datetime.strptime(json_each_tweet['tweet_created_at'], '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours = 5,minutes = 30)).hour
        # print(time)

        if idx == 0:
            low_freq[time] += 1
        elif idx == 1 :
            moderate_freq[time] += 1
        else :
            high_freq[time] += 1


print(low_freq)
print(moderate_freq)
print(high_freq)

#### PLOTS
low_freq_normalized = [round(i/sum(low_freq),5) for i in low_freq]
moderate_freq_normalized = [round(i/sum(moderate_freq),5) for i in moderate_freq]
high_freq_normalized = [round(i/sum(high_freq),5) for i in high_freq]

plt.plot(low_freq_normalized, color='green')
plt.plot(moderate_freq_normalized, color='blue')
plt.plot(high_freq_normalized, color='red')
# plt.plot(high_freq_normalized, marker = "o", color='red')

plt.xlabel("Hours")
plt.ylabel("Normalized Number of tweets")
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plot_temporal_all.png", format="png", bbox_inches="tight")
plt.show()
