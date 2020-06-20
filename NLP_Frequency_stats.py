import json
import sys
import time
import nltk
from nltk import FreqDist
from nltk.corpus import stopwords
import pandas as pd
import matplotlib.pyplot as plt

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk import bigrams
import time

stopwords = nltk.corpus.stopwords.words('english')

def content_filter(text):
    '''
    List comprehension for first pass at removing the standard English stopwords
    '''
    content = [w for w in text if w.lower() not in stopwords]
    return content

def frequency_analysis(cluster_setlist): #Take from network_analysis
 
    #Do for every json file in the cluster next*
    
    for i in range(len(cluster_setlist)):#Cluster_setlist is list of networkx set objects.
        cluster_members = list(cluster_setlist[i]) #Converting from networkx object to list of users within a cluster
        
        text_list = [] 
        text_split_list = []
        word_list = []
        
        for j in range(len(cluster_members)):
            fname = 'user_timeline_' + cluster_members[j] + '.jsonl' #Converting username back to .jsonl filename
            
            with open(fname) as f: #Taking JSON file and appending just the text information for each tweet.
                for line in f:
                    tweet = json.loads(line)
            
                    text_list.append(tweet['text']) #Adds all tweets to the text list.
        
        for j in range(len(text_list)): #Splits each tweet by word using space as a delimiter. 
            text_split_list.append(text_list[i].split(" "))
        
        for j in range(len(text_split_list)): #Adds all to single list
            for k in range(len(text_split_list[j])):
                word_list.append(text_split_list[j][k])
                
        content_word_list = content_filter(word_list)

        fdist1 = FreqDist(content_word_list)
        fdist1_most_common = fdist1.most_common(50)
        
        print(fdist1)
        print('wut')
        time.sleep(1000)

        custom_words = ['RT','','-','I\'m','@'] #Second pass at removing other stopwords
        fdist1_most_common = [i for i in fdist1_most_common if i[0] not in custom_words]

        print('Word list length is ' + str(len(word_list)))
        print('The cluster has ' + str(len(text_list)) + ' tweets.')
        
        print('----------') #Visualization of most frequent words by histogram.

        df = pd.DataFrame(fdist1_most_common, columns =['word', 'frequency'])
        df.plot(kind = 'bar', x = 'word')
        

        print('----------') # Subdiving data by bigrams

        bigram_master = []

        for j in range(len(text_list)):
            word_list = []
            word_list.append(text_list[i].split(" "))
        
            word_output_list = 0
        
        for j in word_list: #Gets rid of nesting quirk
            word_output_list = j                
        
        bigrams = list(nltk.bigrams(word_output_list))
        
        filtered = []
        for pairs in bigrams:
            if pairs[0].lower() in stopwords or pairs[1].lower() in stopwords:
                continue
            elif pairs[0].lower() in custom_words or pairs[1].lower() in custom_words:
                continue
            filtered.append(pairs)
        
        bigram_master.extend(filtered)
        
        print(len(bigram_master))
        
        fdistbigram = FreqDist(bigram_master)
        fdistbigram_common = fdistbigram.most_common(50)

        dfbigram = pd.DataFrame(fdistbigram_common, columns =['word', 'frequency'])
        dfbigram.plot(kind = 'bar', x = 'word')

        plt.show()

        print('wutend')
        time.sleep(1000)
        
    

    

    

    

    
        
    #print(fdistbigram_common)

    

    #print(word_list)

    #plt.show()
    
if __name__ == '__main__':
    frequency_analysis()