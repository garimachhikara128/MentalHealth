import json
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import re
import os
import pyLDAvis
import pyLDAvis.gensim
import pickle 
import operator as op
import preprocessor as p
import gensim
from gensim.utils import simple_preprocess
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.manifold import TSNE

import numpy as np
from matplotlib import colors as mcolors
from keybert import KeyBERT


STOP_WORDS = set(stopwords.words('english'))
l = []

def fun() :

    doc = ""
    f = open('/Users/garima/Desktop/Self/PhD/Research Work/Mental Health/Phase 2/13_DataTabular/reply_high.txt')
    comments = f.read().split("\n\n")
    for texttt in comments[0:-1] :

        texttt = re.sub(r"\S*https?:\S*", " ", texttt)
        texttt = re.sub(r"\S*http?:\S*", " ", texttt)
        texttt = p.clean(texttt)
        texttt = texttt.replace('\d+', ' ')
        texttt = texttt.lower()

        l.append(texttt)
        doc += texttt + "."

    # df = pd.DataFrame(l, columns =['text'])


    # stop_words = stopwords.words('english')
    # stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'https', 'tco', 'us', "amp", "gt", "ji"])
   
    # def sent_to_words(sentences):
    #     for sentence in sentences:
    #         yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

    # def remove_stopwords(texts):
    #     return [[word for word in simple_preprocess(str(doc)) 
    #             if word not in stop_words] for doc in texts]

    # data = df['text'].values.tolist()
    # data_words = list(sent_to_words(data))

    # # remove stop words
    # data_words = remove_stopwords(data_words)

    # # print(data_words)
        
    # import gensim.corpora as corpora
    # # Create Dictionary
    # id2word = corpora.Dictionary(data_words)
    # # Create Corpus
    # texts = data_words
    # # Term Document Frequency
    # corpus = [id2word.doc2bow(text) for text in texts]
    # # View
    # # print(corpus)

    # from pprint import pprint
    # # number of topics
    # num_topics = 1
    # # Build LDA model
    # lda_model = gensim.models.LdaMulticore(corpus=corpus,
    #                                     id2word=id2word,
    #                                     num_topics=num_topics)
    # # Print the Keyword in the 10 topics
    # pprint(lda_model.print_topics())
    # doc_lda = lda_model[corpus]

    # Get topic weights and dominant topics ------------
    # data_ready = l

    # from collections import Counter
    # topics = lda_model.show_topics(formatted=False)
    # data_flat = [w for w_list in data_ready for w in w_list]
    # counter = Counter(data_flat)

    # out = []
    # for i, topic in topics:
    #     for word, weight in topic:
    #         out.append([word, i , weight, counter[word]])

    # df = pd.DataFrame(out, columns=['word', 'topic_id', 'importance', 'word_count'])        

    # # Plot Word Count and Weights of Topic Keywords
    # fig, axes = plt.subplots(1, 3, figsize=(16,10)) #, sharey=True) #, dpi=160)
    # cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
    # for i, ax in enumerate(axes.flatten()):
    #     ax.bar(x='word', height="word_count", data=df.loc[df.topic_id==i, :], color=cols[i], width=0.5, alpha=0.3, label='Word Count')
    #     ax_twin = ax.twinx()
    #     ax_twin.bar(x='word', height="importance", data=df.loc[df.topic_id==i, :], color=cols[i], width=0.2, label='Weights')
    #     ax.set_ylabel('Word Count', color=cols[i])
    #     ax_twin.set_ylim(0, 0.030); 
    #     ax.set_ylim(0, 2000)
    #     ax.set_title('Topic: ' + str(i), color=cols[i], fontsize=16)
    #     ax.tick_params(axis='y', left=False)
    #     ax.set_xticklabels(df.loc[df.topic_id==i, 'word'], rotation=30, horizontalalignment= 'right')
    #     ax.legend(loc='upper left'); ax_twin.legend(loc='upper right')

    # fig.tight_layout(w_pad=2)    
    # fig.suptitle('Word Count and Importance of Topic Keywords', fontsize=22, y=1.05)    
    # plt.show()
    # print(doc)
    kw_model = KeyBERT()
    s = ""
    keywords = kw_model.extract_keywords(doc, top_n=40, use_maxsum=True , nr_candidates = 40)
    for i in keywords :
         s += i[0] + ", "

    print(s)
if __name__ == '__main__':
    fun()