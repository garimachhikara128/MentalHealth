import json
import pandas  as pd

f = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/9_DataUserTimelineClassify/classify_timeline.txt', 'rt')

years = ['2017', '2018', '2019', '2020', '2021', '2022']
all_dict = {}
depressive_dict = {}
tweets = f.read().split("\n")

i = 1 
for each_tweet in tweets[0:-1] :

    each_tweet_split = each_tweet.split(" ")

    tweet_id = each_tweet_split[0] 
    author_id = each_tweet_split[1] 
    model_label = each_tweet_split[2] 
    created_at = each_tweet_split[3][0:4]

    if author_id not in all_dict :

        file_user_desc = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/7_DataUserTimeline/' + author_id + '.txt', 'rt')
        each_tweet = file_user_desc.read().split("\n\n$$$$$$$$$$\n\n")[0]
        desc = json.loads(each_tweet)['author_description']

        all_dict.update({author_id : [0, 0, 0, 0, 0, 0, desc]})
        depressive_dict.update({author_id : [0, 0, 0, 0, 0, 0, desc]})

    all_dict[author_id][int(created_at)-2017] += 1

    if (int)(model_label) == 1 :
        depressive_dict[author_id][int(created_at)-2017] += 1
    
    print(i)
    i += 1


### total
al = []
for each_entry in all_dict :
    al.append([      each_entry ,
                     all_dict[each_entry][0] ,  all_dict[each_entry][1] ,
                     all_dict[each_entry][2] ,  all_dict[each_entry][3] ,
                     all_dict[each_entry][4] ,  all_dict[each_entry][5] ,  all_dict[each_entry][6] ])
    

al_df = pd.DataFrame(al, columns=['author_id', '2017', '2018', '2019', '2020', '2021', '2022', 'desc'])
al_df.to_csv("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/all_desc.csv", index = False)

### dep
dl = []
for each_entry in depressive_dict :
    dl.append([         each_entry ,
                         depressive_dict[each_entry][0] ,  depressive_dict[each_entry][1] ,
                         depressive_dict[each_entry][2] ,  depressive_dict[each_entry][3] ,
                         depressive_dict[each_entry][4] , depressive_dict[each_entry][5] ,  depressive_dict[each_entry][6] ])

dl_df = pd.DataFrame(dl, columns=['author_id', '2017', '2018', '2019', '2020', '2021', '2022', 'desc'])
dl_df.to_csv("/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/depressive_desc.csv", index = False)

# columns=['author_id', '2017', '2018', '2019', '2020', '2021', '2022'])

