import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ans = [[ [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]], 
       [ [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]],
       [ [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0] , [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]]

# info_tweet_freq = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]

# dict = {'Profession' : 0  , 'Personal' : 1, 'Interest' : 2, 'Quote' : 3, 'Philosophical' : 4 ,'Faith' : 5, 'Nation' : 6, 'Concern' : 7, 'Empty' : 8, 'Other' : 9}
dict = {'Profession' : 0  , 'Personal' : 1, 'Interest' : 2, 'Quote' : 3, 'Philosophical' : 3 ,'Faith' : 4, 'Nation' : 1, 'Concern' : 5, 'Empty' : 6, 'Other' : 7}

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

df = pd.read_csv('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_desc copy.csv')

# print(df)
# print("\n\n")

num_low = 0 
num_moderate = 0
num_high = 0

nou = 0 
i = 0
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


    each_user_desc = df.iloc[i]['type']

    descc = each_user_desc.strip().split(" ") 

    new_descc = []
    ## Nation -> Personal Philosophical -> Quote
    for val in descc :

        if(val == 'Nation') :
            flag = 0
            for val1 in descc :
                if(val1 == 'Personal') :
                    flag = 1
                    break
            
            if flag == 0 :
                new_descc.append('Personal')

        elif(val == 'Philosophical') :
            flag = 0
            for val1 in descc :
                if(val1 == 'Quote') :
                    flag = 1
                    break
            
            if flag == 0 :
                new_descc.append('Quote')

        else :
            new_descc.append(val)

    for x in range(0,len(new_descc)) :

        for y in range(x, len(new_descc)) :

            ans[idx][dict[new_descc[x]]][dict[new_descc[y]]] += 1

            if x != y :
                ans[idx][dict[new_descc[y]]][dict[new_descc[x]]] += 1

    # print(i, idx, descc, "\n")
    i += 1

## PLOTS
sns.set(font_scale=2)
labels = ['Profession', 'Personal', 'Interest', 'Quote', 'Faith', 'Concern',  'Empty' ,  'Other'] # labels for y-axis
plt.figure(figsize=(10, 6))

## FIRST
res = np.array(ans[2])/num_high ## 2 changes here 
print(res.shape)
mask = np.triu(np.ones_like(res, dtype=bool))
np.fill_diagonal(mask, False)
g = sns.heatmap(res, annot=True, linewidth=.3, fmt=".2f", xticklabels=labels, yticklabels=labels, cmap = sns.cm.rocket_r, mask=mask , annot_kws={"size": 20}) #, "weight":"bold"}) #, vmin = 0.0, vmax = 0.46, cbar = False)

plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/heatmap_cross_high.pdf", format="pdf", bbox_inches="tight")
plt.show()
