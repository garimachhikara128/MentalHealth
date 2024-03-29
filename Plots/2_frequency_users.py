import pandas as pd

#      ['2017',  '2018',  '2019',  '2020',  '2021',  '2022']
info = [[0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0], [0,0,0]]

f = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_year_wise.txt')
users = f.read().split("\n")

for each_user in users[0:-1] :

    each_user_split = each_user.split(" ")
    author_id = each_user_split[0] 

    for i in range(1,7) :
        freq_year = each_user_split[i]

        # frequency -> category
        if(int(freq_year) <= 50) :
            category = 0
        elif(int(freq_year) <= 150) :
            category = 1
        else :
            category = 2

        info[i-1][category] += 1

            
print(info)
