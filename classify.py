import os
import numpy as np
import pandas as pd
import time
import datetime
import gc
import random
import re
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler,random_split
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import transformers
from transformers import BertForSequenceClassification, AdamW, BertConfig,BertTokenizer,get_linear_schedule_with_warmup
import json
from sklearn.metrics import classification_report

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(device)

model = BertForSequenceClassification.from_pretrained(
    "bert-base-uncased", # Use the 12-layer BERT model, with an uncased vocab.
    num_labels = 2, # The number of output labels--2 for binary classification.
                    # You can increase this for multi-class tasks.   
    output_attentions = False, # Whether the model returns attentions weights.
    output_hidden_states = False, # Whether the model returns all hidden-states.
)
model = model.to(device)
model.load_state_dict(torch.load('bert_model', map_location=torch.device(device)))
model.eval()

batch_size = 16



# Load the BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

########################
dir = './7_DataUserTimeline/'
all_files = open(dir + 'UniqueUsersOrg.txt')
all_files_list = all_files.read().split("\n") 

file_no = 1 
for file in all_files_list[0:-1]:

    if os.stat(dir + file + '.txt').st_size != 0 :

        print(file_no)
        file_no += 1

        f = open(dir + file + '.txt', 'rt')
        tweets = f.read().split("\n$$$$$$$$$$\n")

        tweet_ids = []
        tweet_created_at = []
        test_input_ids = []
        test_attention_masks = []

        for each_tweet in tweets[0:-1]:

            json_each_tweet = json.loads(each_tweet)
            text = re.sub(r"[^a-zA-Z?.!,¿]+", " ", json_each_tweet['tweet_text']) # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
            text = re.sub(r"http\S+", "",text) #Removing URLs
            text = re.sub(r"https\S+", "",text) #Removing URLs 
            encoded_dict = tokenizer.encode_plus(
                                    # json_each_tweet['text'],  
                                    text,                   
                                    add_special_tokens = True, 
                                    max_length = 512,           
                                    pad_to_max_length = True,
                                    return_attention_mask = True,
                                    return_tensors = 'pt',
                            )
            test_input_ids.append(encoded_dict['input_ids'])
            test_attention_masks.append(encoded_dict['attention_mask'])

            tweet_ids.append(json_each_tweet['tweet_id'])
            tweet_created_at.append(json_each_tweet['tweet_created_at'])

        test_input_ids = torch.cat(test_input_ids, dim=0)
        test_attention_masks = torch.cat(test_attention_masks, dim=0)

        test_dataset = TensorDataset(test_input_ids, test_attention_masks)
        test_dataloader = DataLoader(
                    test_dataset, # The validation samples.
                    sampler = SequentialSampler(test_dataset), # Pull out batches sequentially.
                    batch_size = batch_size # Evaluate with this batch size.
                )

        print("Number of batches : ", len(test_dataloader))
        predictions = []
        for batch in test_dataloader:
            
            b_input_ids = batch[0].to(device)
            b_input_mask = batch[1].to(device)
            with torch.no_grad():        
                output= model(b_input_ids, 
                                        token_type_ids=None, 
                                        attention_mask=b_input_mask)
                logits = output.logits
                logits = logits.detach().cpu().numpy()
                pred_flat = np.argmax(logits, axis=1).flatten()
                    
                predictions.extend(list(pred_flat))

        print(len(tweet_ids), len(tweet_created_at), len(predictions))

        f = open('classify_timeline.txt', 'at')

        for i,j,k in zip(tweet_ids, predictions,tweet_created_at) :
            f.write(str(i) + " " + file + " " + str(j) + " " + str(k))
            f.write("\n")
