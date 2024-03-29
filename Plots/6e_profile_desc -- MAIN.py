import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

ans = [ [0,0,0,0,0,0,0,0]
, [0,0,0,0,0,0,0,0] 
, [0,0,0,0,0,0,0,0]]
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

    #######################################################
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

    #######################################################

    for each in new_descc :
        ans[idx][dict[each]] += 1

    # print(i, idx, descc, "\n")
    i += 1

final_ans = []
final_ans.append( [ round(elem / num_low , 3) for elem in ans[0]] )
final_ans.append( [ round(elem / num_moderate , 3) for elem in ans[1]] )
final_ans.append( [ round(elem / num_high , 3) for elem in ans[2]] )
print(final_ans)

final_ans = np.array(final_ans).T.tolist()
print(final_ans)

x_axis_labels = ['Low', 'Moderate', 'High'] # labels for x-axis
y_axis_labels = ['Profession', 'Personal', 'Interest', 'Quote', 'Faith', 'Concern',  'Empty' ,  'Other'] # labels for y-axis

sns.set(font_scale=1.8)
g = sns.heatmap(final_ans, annot=True, fmt=".3f", linewidth=.3, xticklabels=x_axis_labels, yticklabels=y_axis_labels, cmap = sns.cm.rocket_r, annot_kws={"size": 16})

# plt.xlabel('User Category', fontsize = 18) 
# plt.ylabel('Vertical Values', fontsize = 15) 

plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/heatmap.pdf", format="pdf", bbox_inches="tight")
plt.show()
