import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import preprocessor as p
import string
from scipy.stats import ks_2samp

# years =     ['2017',  '2018',  '2019',  '2020',  '2021',  '2022']
similarity = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]

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

model = SentenceTransformer('distilbert-base-nli-mean-tokens')

num_low = 0 
num_moderate = 0
num_high = 0

ans = [[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]]]
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

    sl = [[],[],[],[],[],[]] ## to store embeddings for each year for a given user 
    for each_tweet in tweets[0:-1]:
        json_each_tweet = json.loads(each_tweet)
        text = json_each_tweet['tweet_text']
        year = (int)(json_each_tweet['tweet_created_at'][0:4])
        id = json_each_tweet['tweet_id']

        if 1:
        # if dep_dict[id] == '1' : 
            temp = text 
            temp = p.clean(temp)
            temp = temp.lower()
            translating = str.maketrans('', '', string.punctuation)
            temp = temp.translate(translating)
            temp = temp.strip()

            temp_e = model.encode(temp)
            sl[year-2017].append(temp_e)

    for y in range(0,6) :

        if(len(sl[y]) > 0) :
            centroid_embedding = np.average(sl[y], axis = 0) 
            # print(len(centroid_embedding))

            avg_cosine_sim = 0.0

            for each_embedding in sl[y] :
                avg_cosine_sim += cosine_similarity(each_embedding.reshape(1,-1), centroid_embedding.reshape(1,-1))[0][0]

            res_user =  avg_cosine_sim / len(sl[y])
            ans[y][idx].append(res_user)

    num += 1
    print(num)

file = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/similarity2.txt','wt')

file.write(str(ans))
file.close() 

print("MEAN RESULTS :--")

for i in range(0,6) :
    print(2017+i, " :-")
    for j in range(0,3) :
        if (j == 0) :
            print("Low")
        elif(j == 1) : 
            print("Moderate") 
        else :
            print("High")

        print("Mean(Deviation) " , round(np.mean(ans[i][j]),2) , "(" , round(np.std(ans[i][j]),2), ")")

print("MEDIAN RESULTS :--")

for i in range(0,6) :
    print(2017+i, " :-")
    for j in range(0,3) :
        if (j == 0) :
            print("Low")
        elif(j == 1) : 
            print("Moderate") 
        else :
            print("High")

        print("Median(Deviation) " , round(np.median(ans[i][j]),2) , "(" , round(np.std(ans[i][j]),2), ")")

for y in range(0,6) :
    print("year ", (2017+y))
    for i in range(0,3) :
        for j in range(i+1,3) :
            print(i,j)
            statistic, pvalue = ks_2samp(ans[y][i], ans[y][j])
            star = "related"
            if(pvalue <= 0.001) :
                star = "***"
            elif(pvalue <= 0.01) :
                star = "**"
            elif(pvalue <= 0.05) :
                star = "*"

            print("Test statistic: " , round(statistic,2), star)

print("------------------")
