import json
import matplotlib.pyplot as plt
import powerlaw
import numpy 
from scipy.stats import ks_2samp
from scipy import stats
import random

info_followers = [0,0,0]
info_following = [0,0,0]
info_users = [0,0,0]
# info_tweet_freq = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]

f1 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_total.txt')
users_d = f1.read().split("\n")

f2 = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_total.txt')
users_a = f2.read().split("\n")

num_low = 0 
num_moderate = 0
num_high = 0

followers_list = [[],[],[]]
following_list = [[],[],[]]

nou = 0 

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

    f_users = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/7_DataUserTimeline/' + author_id + '.txt')
    
    tweets = f_users.read().split("\n\n$$$$$$$$$$\n\n")

    json_each_tweet = json.loads(tweets[0])
    followers_count = json_each_tweet['author_followers_count']
    following_count = json_each_tweet['author_following_count']

    # if(followers_count >= 50000) :
    #     continue 

    info_followers[idx] += followers_count
    info_following[idx] += following_count
    info_users[idx] += 1

    followers_list[idx].append(followers_count) 
    following_list[idx].append(following_count) 

    nou += 1

print(info_followers)
print(info_following)
print(info_users)

frac_followers = []
frac_following = []
for i,j,k in zip(info_followers, info_following, info_users) :
    frac_followers.append(round(i/k,2)) 
    frac_following.append(round(j/k,2)) 

print("avg followers", frac_followers)
print("avg following", frac_following)

fig = plt.figure(figsize=(13,11)) # w, h
gs = fig.add_gridspec(2, 3, hspace=0.4, wspace=0.05)
(ax1, ax2, ax3), (ax4, ax5, ax6) = gs.subplots(sharex='col', sharey='row')

# ############## PLOTS ###############
size = 18 
## FOLLOWERS ##
ll = [ax1, ax2, ax3]
for i in range(0,3) :

    data = numpy.array(followers_list[i]) + 1        

    fit = powerlaw.Fit(data, xmin = 1)
    fit.plot_ccdf(ax = ll[i], color= 'green', label ='Empirical Data', linewidth = 2.5)
    fit.power_law.plot_ccdf(ax=ll[i], color='red',linestyle='dotted', label ='Power Law Fit', linewidth = 2.5)
    fit.lognormal.plot_ccdf(ax=ll[i], color='blue',linestyle='--', label ='Log-Normal Fit', linewidth = 2.5)

    print("Power Law Variables : ") 
    print('alpha= ',round(fit.power_law.alpha,3), "\n") #,'  sigma= ',fit.power_law.sigma) # here sigma is error

    print("Log Normal Variables : ")
    print('mu= ',round(fit.lognormal.mu,3),'  sigma= ',round(fit.lognormal.sigma,3), "\n")

    print(fit.distribution_compare('power_law', 'lognormal', normalized_ratio = True), "\n")

ax1.set_xlabel("Number of followers", fontsize=size)         
ax2.set_xlabel("Number of followers", fontsize=size)         
ax3.set_xlabel("Number of followers", fontsize=size)   

## FOLLOWING ##
ll = [ax4, ax5, ax6]
for i in range(0,3) :

    data = numpy.array(following_list[i]) + 1        
    
    fit = powerlaw.Fit(data, xmin = 1)
    fit.plot_ccdf(ax = ll[i], color= 'green', label ='Empirical Data', linewidth = 2.5)
    fit.power_law.plot_ccdf(ax=ll[i], color='red',linestyle='dotted', label ='Power Law Fit', linewidth = 2.5)
    fit.lognormal.plot_ccdf(ax=ll[i], color='blue',linestyle='--', label ='Log-Normal Fit', linewidth = 2.5)


    print("Power Law Variables : ") 
    print('alpha= ',round(fit.power_law.alpha,3), "\n") #,'  sigma= ',fit.power_law.sigma) # here sigma is error

    print("Log Normal Variables : ")
    print('mu= ',round(fit.lognormal.mu,3),'  sigma= ',round(fit.lognormal.sigma,3), "\n")

    print(fit.distribution_compare('power_law', 'lognormal', normalized_ratio = True), "\n")

ax4.set_xlabel("Number of following", fontsize=size)         
ax5.set_xlabel("Number of following", fontsize=size)         
ax6.set_xlabel("Number of following", fontsize=size)  

ax1.set_ylabel("P (Followers)", fontsize=size)         
ax4.set_ylabel("P (Following)", fontsize=size)        

ax1.title.set_text('a). low SHFU')
ax2.title.set_text('b). moderate SHFU')
ax3.title.set_text('c). high SHFU')
ax4.title.set_text('d). low SHFU')
ax5.title.set_text('e). moderate SHFU')
ax6.title.set_text('f). high SHFU')

ax1.title.set_size(size)
ax2.title.set_size(size)
ax3.title.set_size(size)
ax4.title.set_size(size)
ax5.title.set_size(size)
ax6.title.set_size(size)

for ax in fig.get_axes():
    ax.tick_params(labelsize=size)

fig.subplots_adjust(bottom=0.3)

ax1.legend(loc = "upper left", fontsize=size, ncol=3, bbox_to_anchor=(0, -1.67)) #"lower left" upper right

for ax in fig.get_axes():
    ax.grid()

# ax1.text(2, -2, "a", fontsize=15, bbox = dict(facecolor = 'red', alpha = 0.5))

# plt.savefig("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/followers_following.pdf", format="pdf", bbox_inches="tight")
# plt.show()

#### TESTS

for i in range(0,3) :
    for j in range(i+1,3) :
        statistic, pvalue = ks_2samp(following_list[i], following_list[j])

        print(i,j)
        print("Test statistic: " , statistic, "P-value: " , pvalue)

        print(stats.ttest_ind(following_list[i], following_list[j], equal_var=False))
