# importing package
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# create data

f = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_total.txt')
users = f.read().split("\n")

author_id_list = []
tweet_count_list = []

for each_user in users[0:-1] :

        each_user_split = each_user.split(" ")
        author_id = each_user_split[0] 
        tweet_count = each_user_split[1]

        author_id_list.append(author_id)
        tweet_count_list.append((int)(tweet_count))

# x = np.array(author_id_list)
# y = np.array(tweet_count_list)
# plt.xticks([])
# plt.scatter(x, tweet_count_list, c=tweet_count_list, cmap='Spectral_r')
# plt.colorbar()
# plt.show()
# x = np.array(author_id_list)
# y = pd.DataFrame(tweet_count_list).value_counts().plot()
# plt.show()
# # print(y)

plt.style.use('seaborn')
plt.figure(figsize=(8,4))
plt.grid(True)
plt.axvline(x=50, color ="black", linestyle = "dotted")
plt.axvline(x=150, color ="black", linestyle ="dotted")
plt.hist(tweet_count_list, bins=300,color = 'steelblue')
plt.xlabel("Self-harm post count from 2017 - 2022", fontsize=18)
plt.ylabel("Number of users", fontsize=18)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/plots_absolute.pdf", format="pdf", bbox_inches="tight")
plt.show()