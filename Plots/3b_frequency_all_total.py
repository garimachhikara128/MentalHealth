import pandas as pd
import json 

#      ['2017',  '2018',  '2019',  '2020',  '2021',  '2022']
info = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]

new_f = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_total.txt', 'wt')

f = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_year_wise.txt')
users = f.read().split("\n")

for each_user in users[0:-1] :

    each_user_split = each_user.split(" ")
    author_id = each_user_split[0] 

    total = 0 
    for i in range(1,7) :
        freq_year = each_user_split[i]
        total += (int)(freq_year)
        # frequency -> category

    new_f.write(author_id + " " + str(total))
    new_f.write("\n")
