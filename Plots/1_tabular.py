import pandas as pd

f = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/9_DataUserTimelineClassify/classify_timeline.txt')

years = ['2017', '2018', '2019', '2020', '2021', '2022']
all_dict = {}
depressive_dict = {}
tweets = f.read().split("\n")

for each_tweet in tweets[0:-1] :

    each_tweet_split = each_tweet.split(" ")

    tweet_id = each_tweet_split[0] 
    author_id = each_tweet_split[1] 
    model_label = each_tweet_split[2] 
    created_at = each_tweet_split[3][0:4]

    if author_id not in all_dict :
        all_dict.update({author_id : [0, 0, 0, 0, 0, 0]})
        depressive_dict.update({author_id : [0, 0, 0, 0, 0, 0]})

    all_dict[author_id][int(created_at)-2017] += 1

    if (int)(model_label) == 1 :
        depressive_dict[author_id][int(created_at)-2017] += 1

### total
f_total = open("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_year_wise.txt", 'wt')

for each_entry in all_dict :
    f_total.write(str(each_entry) + " " +
                    str(all_dict[each_entry][0]) + " " + str(all_dict[each_entry][1]) + " " +
                    str(all_dict[each_entry][2]) + " " + str(all_dict[each_entry][3]) + " " +
                    str(all_dict[each_entry][4]) + " " + str(all_dict[each_entry][5]))
    f_total.write("\n")

### dep
dep_total = open("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_year_wise.txt", 'wt') 

for each_entry in depressive_dict :
    dep_total.write(str(each_entry) + " " + 
                        str(depressive_dict[each_entry][0]) + " " + str(depressive_dict[each_entry][1]) + " " +
                        str(depressive_dict[each_entry][2]) + " " + str(depressive_dict[each_entry][3]) + " " +
                        str(depressive_dict[each_entry][4]) + " " + str(depressive_dict[each_entry][5]))
    dep_total.write("\n")

# columns=['author_id', '2017', '2018', '2019', '2020', '2021', '2022'])

