# importing package
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import powerlaw

df = pd.read_csv('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 1/NormalData.csv', engine="python")

# print(df.head())

followers_dict = {}
following_dict = {}

for i in df.index:
    author_id = df['author_id'][i]
    followers = df['author_followers_count'][i]
    following = df['author_following_count'][i]

    followers_dict[author_id] = followers
    following_dict[author_id] = following

followers_list = []
following_list = []

for key in followers_dict:
    followers_list.append(followers_dict[key])

for key in following_dict:
    following_list.append(following_dict[key])


fig = plt.figure(figsize=(13,11)) # w, h
gs = fig.add_gridspec(1, 2, hspace=0.4, wspace=0.05)
(ax1, ax2) = gs.subplots(sharex='col', sharey='row')

if 1:
    data = np.array(followers_list) + 1        

    fit = powerlaw.Fit(data, xmin = 1)
    fit.plot_ccdf(ax = ax1, color= 'green', label ='Empirical Data', linewidth = 2.5)
    fit.power_law.plot_ccdf(ax = ax1, color='red',linestyle='dotted', label ='Power Law Fit', linewidth = 2.5)
    fit.lognormal.plot_ccdf(ax = ax1, color='blue',linestyle='--', label ='Log-Normal Fit', linewidth = 2.5)

    print("Power Law Variables : ") 
    print('alpha= ',round(fit.power_law.alpha,3), "\n") #,'  sigma= ',fit.power_law.sigma) # here sigma is error

    print("Log Normal Variables : ")
    print('mu= ',round(fit.lognormal.mu,3),'  sigma= ',round(fit.lognormal.sigma,3), "\n")

    print(fit.distribution_compare('power_law', 'lognormal', normalized_ratio = True), "\n")

    plt.show()