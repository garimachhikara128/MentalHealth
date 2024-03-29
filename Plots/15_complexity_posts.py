import json
import pandas as pd
import numpy as np
import textstat
from scipy.stats import ks_2samp
from nltk.tokenize import sent_tokenize
from gensim.utils import tokenize
import re
from nltk.tokenize import sent_tokenize
import matplotlib.pyplot as plt
from keras.preprocessing.text import text_to_word_sequence

def complexity(text) :

    text = re.sub(r"@\S+", "",text) #Removing @words
    # word_list = list(tokenize(text))
    # # print(word_list)
    # total_length = 0 
    # total_words = 0 
    # for each_word in word_list :

    #     if(each_word != "RT") :
    #         total_length += len(each_word)
    #         total_words += 1

    # if(total_words == 0) :
    #     return 0 
    # else :
    #     return total_length / total_words
    
    # sents_list = sent_tokenize(text)

    # for sent in sents_list :
    c = 0
    t = 0
    word_list = text_to_word_sequence(text)
    for word in word_list :
        c += len(word) 
        t += 1

    if(t == 0) :
        return 0 
    else :
        return c / t 

######
dep_dict = dict()
f_dep_info = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/9_DataUserTimelineClassify/classify_timeline.txt')
dep_info = f_dep_info.read().split("\n")
for each_dep_info in dep_info[0:-1] :
    each_dep_info_split = each_dep_info.split(" ") 
    dep_dict[each_dep_info_split[0]] = each_dep_info_split[2]
######

resdf = pd.DataFrame(columns = ['author_id', 'year', 'category', 'readability'])

f1 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_total.txt')
users_d = f1.read().split("\n")

f2 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_total.txt')
users_a = f2.read().split("\n")

ll = [[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]]]

num_low = 0 
num_moderate = 0
num_high = 0

num = 0
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

    total_tweets = len(tweets) - 1

    sl = [[],[],[],[],[],[]] ## to store complexity for each year for a given user 
    nl = ["","","","","",""]

    for each_tweet in tweets[0:-1]:
        json_each_tweet = json.loads(each_tweet)
        text = json_each_tweet['tweet_text']
        year = (int)(json_each_tweet['tweet_created_at'][0:4])
        id = json_each_tweet['tweet_id']

        # if 1:
        if  dep_dict[id] == '1' :
            # temp = text 
            # temp = p.clean(temp)
            # temp = temp.lower()
            # temp = temp.strip()

            sl[year-2017].append(complexity(text))
            # nl[year-2017] += text + "."


    for y in range(0,6) :

        if(len(sl[y]) > 0) :
            res_user = round(np.mean(sl[y]),2)
            ll[y][idx].append(res_user)
        # if(len(nl[y]) > 0) :
        #     res_user = round(complexity(nl[y]),2)
        #     ll[y][idx].append(res_user)

    num += 1
    print(num)

res = [[],[],[]]

for i in range(0,6) :
    print(2017+i, " :-")
    for j in range(0,3) :
        if (j == 0) :
            print("Low")
        elif(j == 1) : 
            print("Moderate") 
        else :
            print("High")

        res[j].append(np.mean(ll[i][j]))
        print("Mean(Deviation) " , round(np.mean(ll[i][j]),2) , "(" , round(np.std(ll[i][j]),2), ")")

for y in range(0,6) :
    print("year ", (2017+y))
    for i in range(0,3) :
        for j in range(i+1,3) :
            print(i,j)
            statistic, pvalue = ks_2samp(ll[y][i], ll[y][j])
            star = "related"
            if(pvalue <= 0.001) :
                star = "***"
            elif(pvalue <= 0.01) :
                star = "**"
            elif(pvalue <= 0.05) :
                star = "*"

            print("Test statistic: " , round(statistic,2), star)

plt.style.use('seaborn')
plt.figure(figsize=(12,9))
x = [2017, 2018, 2019, 2020, 2021, 2022]

size = 33
plt.plot(x,res[0], color='green', label='Low')
plt.plot(x,res[1], color='blue', label='Moderate')
plt.plot(x,res[2], color='red', label='High')
# plt.plot(high_freq_normalized, marker = "o", color='red')
plt.xlabel("Year", fontsize=size)
plt.ylabel("Complexity", fontsize=size) ### change
plt.xticks(fontsize=size)
plt.yticks(fontsize=size)
plt.legend(loc = "upper left" , fontsize= size)
### change
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plot_complexity_sh_mean.pdf", format="pdf", bbox_inches="tight")
plt.show()