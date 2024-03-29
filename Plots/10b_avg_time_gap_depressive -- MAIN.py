from curses.ascii import NUL
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from scipy.stats import ks_2samp

years =     ['2017',  '2018',  '2019',  '2020',  '2021',  '2022']
tt = timedelta()
activation = [[tt,tt,tt], [tt,tt,tt], [tt,tt,tt], [tt,tt,tt], [tt,tt,tt], [tt,tt,tt]]
info_tweet_freq = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]
ll_activation = [[[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]], [[],[],[]]]

dep_dict = dict()
f_dep_info = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/9_DataUserTimelineClassify/classify_timeline.txt')
dep_info = f_dep_info.read().split("\n")
for each_dep_info in dep_info[0:-1] :
    each_dep_info_split = each_dep_info.split(" ") 
    dep_dict[each_dep_info_split[0]] = each_dep_info_split[2]

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

    f_users = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/7_DataUserTimeline/' + author_id + '.txt')

    tweets = f_users.read().split("\n\n$$$$$$$$$$\n\n")

    first_tweet = True
    last_time = timedelta()
    current_time = timedelta()

    for each_tweet in tweets[0:-1]:
        json_each_tweet = json.loads(each_tweet)
        id = json_each_tweet['tweet_id']

        if dep_dict[id] == '1' :
        # if 1:
            year = (int)(json_each_tweet['tweet_created_at'][0:4])

            if first_tweet == True :
                last_time = datetime.strptime(json_each_tweet['tweet_created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                first_tweet = False
            else :
                current_time = datetime.strptime(json_each_tweet['tweet_created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                diff = last_time - current_time 
                ll_activation[year-2017][idx].append(diff.days)
                # print(diff)
                activation[year-2017][idx] += diff
                info_tweet_freq[year-2017][idx] += 1
                last_time = current_time 

print(activation)
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
res = [[],[],[]]
#####
for i in range(0,6) :
    print(2017+i, " :-")
    for j in range(0,3) :
        if (j == 0) :
            print("Low")
        elif(j == 1) : 
            print("Moderate") 
        else :
            print("High")

        res[j].append(np.mean(ll_activation[i][j]))
        print("Mean(Deviation) " , round(np.mean(ll_activation[i][j]),2) , "(" , round(np.std(ll_activation[i][j]),2), ")")

for y in range(0,6) :
    print("year ", (2017+y))
    for i in range(0,3) :
        for j in range(i+1,3) :
            print(i,j)
            statistic, pvalue = ks_2samp(ll_activation[y][i], ll_activation[y][j])
            star = "related"
            if(pvalue <= 0.001) :
                star = "***"
            elif(pvalue <= 0.01) :
                star = "**"
            elif(pvalue <= 0.05) :
                star = "*"

            print("Test statistic: " , round(statistic,2), star)

#### PLOTS

# df = pd.DataFrame(bl_avg_activation, columns=["Category", "Low", "Moderate", "High"])
# df.plot(x="Category", y=["Low", "Moderate", "High"], kind="bar",figsize=(8,4), rot=0,color = ['palegreen', 'cyan', 'wheat'],grid=True, fontsize = 17)
# plt.xlabel("Years", fontsize=17)
# plt.ylabel("Number of days", fontsize=17)
# plt.legend(loc = "upper right", fontsize= 17)
# plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plot_avg_time_gap_depressive.pdf", format="pdf", bbox_inches="tight")
# plt.show()

plt.style.use('seaborn')
# plt.figure(figsize=(12,9))

x = [2017, 2018, 2019, 2020, 2021, 2022]

plt.plot(x, res[0], c='green', label='Low')
plt.plot(x, res[1], c='blue', label='Moderate')
plt.plot(x, res[2], c='red', label='High')

size = 23
plt.xlabel("Year", fontsize=size)
plt.ylabel("Number of days", fontsize=size)
plt.xticks(fontsize=size)
plt.yticks(fontsize=size)
plt.legend(fontsize=size, loc = "upper right")
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plots_avg_gap_depressive.pdf", format="pdf", bbox_inches="tight")
plt.show()
