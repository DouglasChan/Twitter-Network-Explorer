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
from wordcloud import WordCloud

import word_cloud_generator

stopwords = nltk.corpus.stopwords.words('english')
stopwords_unigram = ['RT','rt','','-','I\'m','@','—']
stopwords.append(stopwords_unigram)

def content_filter(text):
    '''
    List comprehension for first pass at removing the standard English stopwords
    '''
    content = [w for w in text if w.lower() not in stopwords]
    return content

def frequency_analysis(cluster_setlist): #Take from network_analysis
    
    frequency_unigram_stats = []
    frequency_bigram_stats = []
    cluster_counter = 1
 
    #Do for every json file in the cluster next*
    
    for cluster_list in range(len(cluster_setlist)):#Cluster_setlist is list of networkx set objects.
        cluster_members = list(cluster_setlist[cluster_list]) #Converting from networkx object to list of users within a cluster
        
        cluster_text_list = []
        cluster_text_split_list = []
        cluster_word_list = []

        for j in range(len(cluster_members)):
        
            text_list = [] 
            text_split_list = []
            word_list = []
        
            fname = 'user_timeline_' + cluster_members[j] + '.jsonl' #Converting username back to .jsonl filename
            
            with open(fname) as f: #Taking JSON file and appending just the text information for each tweet.
                for line in f:
                    tweet = json.loads(line)
            
                    text_list.append(tweet['text']) #Adds all tweets to the text list.
        
            for k in range(len(text_list)): #Splits each tweet by word using space as a delimiter. 
                text_split_list.append(text_list[k].split(" "))
        
            for k in range(len(text_split_list)): #Adds all to single list
                for l in range(len(text_split_list[k])):
                    word_list.append(text_split_list[k][l])
                    
            cluster_text_list.append(text_list)
            cluster_text_split_list.append(text_split_list)
            cluster_word_list.append(word_list)
    
        #Making cluster data into a flat list
        
        cluster_text_list = [item for sublist in cluster_text_list for item in sublist]
        cluster_text_split_list = [item for sublist in cluster_text_split_list for item in sublist]
        cluster_word_list = [item for sublist in cluster_word_list for item in sublist]
    
        #print(cluster_text_list)
        #print(len(cluster_text_list))
        
        content_word_list = content_filter(cluster_word_list)

        fdist1 = FreqDist(content_word_list)
        fdist1_most_common = fdist1.most_common(50)
        #print(fdist1_most_common)
        
        custom_words = ['RT','rt','','-','I\'m','@','—','.'] #Second pass at removing other stopwords 
        fdist1_most_common = [i for i in fdist1_most_common if i[0] not in (custom_words or stopwords)]
        
        print(type(fdist1_most_common))
        time.sleep(5)
        
        unigram_distribution_variable = []
        
        for i in range(len(fdist1_most_common)):
            for j in range(fdist1_most_common[i][1]): #The number of times it appears...
                unigram_distribution_variable.append(fdist1_most_common[i][0])
        
        #fdist1_most_common_keys = fdist1_most_common.keys()
        #for i in range(len(fdist1_most_common)):
        
        #print(distribution_variable)
        #print('wut')
        #time.sleep(1000)
        
        
        #print(fdist1_most_common)
        frequency_unigram_stats.append(fdist1_most_common) #Deprecate?
        
        print(unigram_distribution_variable)
        #unigram_distribution_variable = [item for sublist in unigram_distribution_variable for item in sublist]
        
        unigram_distribution_variable = ' '.join(unigram_distribution_variable) #This gives what I'd need -- most frequent unigrams as a long string.
        
        #print(unigram_distribution_variable)
        #print('wut')
        #time.sleep(1000)
        
        bigram_master = []
        
        for bigram in range(len(cluster_text_list)):
            bigram_word_list = []
            bigram_word_list.append(cluster_text_list[bigram].split(" "))
                
            word_output_list = 0
        
            for split_bigram_word in bigram_word_list: #Gets rid of nesting quirk
                word_output_list = split_bigram_word  

            #print(word_output_list)
            #print('wut')
            #time.sleep(1000)
        
            bigrams = list(nltk.bigrams(word_output_list))
        
            filtered = []
            for pairs in bigrams:
                if pairs[0].lower() in stopwords or pairs[1].lower() in stopwords:
                    continue
                elif pairs[0].lower() in custom_words or pairs[1].lower() in custom_words:
                    continue
                else:
                    filtered.append(pairs)
                    
            #print(bigrams)
            #print('wut')
            #time.sleep(1000)
        
            bigram_master.extend(filtered)
            
        #print(bigram_master)
        
        
        
            
        fdistbigram = FreqDist(bigram_master)
        fdistbigram_common = fdistbigram.most_common(50)
        
        
        bigram_distribution_variable = []
        
        for i in range(len(fdistbigram_common)):
            for j in range(fdistbigram_common[i][1]): #The number of times it appears...
                bigram_distribution_variable.append(fdistbigram_common[i][0])
        
        #bigram_distribution_variable = [item for sublist in bigram_distribution_variable for item in sublist]
        
        #print(bigram_distribution_variable)
        #time.sleep(1000)
        
        df = pd.DataFrame(fdist1_most_common, columns =['word', 'frequency'])
        df.plot(kind = 'bar', x = 'word')
        
        dfbigram = pd.DataFrame(fdistbigram_common, columns =['word', 'frequency'])
        dfbigram.plot(kind = 'bar', x = 'word')
        
        #dfbigram2 = pd.DataFrame(fdistbigram_common, columns =['word', 'frequency'])
        #dfbigram2.plot(kind = 'bar', x = 'word')
        
        
        #Wordcloud section?
        
        text = 'Andrew M. Yang[1] (born January 13, 1975) is an American political commentator, entrepreneur, lawyer, and philanthropist. Originally a corporate lawyer, Yang began working in various startups and early stage growth companies as a founder or executive from 2000 to 2009. In 2011, he founded Venture for America (VFA), a nonprofit organization focused on creating jobs in cities struggling to recover from the Great Recession. He then ran as a candidate in the 2020 Democratic presidential primaries.'
        
        
        
        wordcloud = WordCloud().generate(text)
        
        plt.figure()
        plt.imshow(wordcloud)
        
        
        wordcloud2 = WordCloud(collocations=False).generate(unigram_distribution_variable)
        plt.figure()
        plt.imshow(wordcloud2)
        
        #plt.imshow(wordcloud, interpolation='bilinear')
        
        time.sleep(3)
        #word_cloud_generator.generate_cloud()
        
        wordcloud2.to_file('cluster ' + str(cluster_counter) + '.png') 
        cluster_counter += 1
        
        #plt.show()
    
    '''                
    print(cluster_text_list)
    print(cluster_text_split_list)
    print(cluster_word_list)
    print(len(cluster_word_list))
    print(cluster_word_list[0])
    print(len(cluster_word_list[0]))
    print(len(cluster_text_list))
    print(len(cluster_text_list[0]))
    print(len(cluster_text_split_list))
    print(len(cluster_text_split_list[0]))
    print('wut')
    time.sleep(1000)
    '''
        
    '''    
   

          

            df = pd.DataFrame(fdist1_most_common, columns =['word', 'frequency'])
            df.plot(kind = 'bar', x = 'word')
        

            print('----------') # Subdiving data by bigrams

            bigram_master = []

            for bigram in range(len(text_list)):
                word_list = []
                word_list.append(text_list[bigram].split(" "))
        
                word_output_list = 0
            
                for split_bigram_word in word_list: #Gets rid of nesting quirk
                    word_output_list = split_bigram_word                
            
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
            #frequency_

            dfbigram = pd.DataFrame(fdistbigram_common, columns =['word', 'frequency'])
            dfbigram.plot(kind = 'bar', x = 'word')

            #plt.show()       
    '''
if __name__ == '__main__':
    frequency_analysis()
    
#Ref : 
#1. https://stackoverflow.com/questions/43954114/python-wordcloud-repetitve-words