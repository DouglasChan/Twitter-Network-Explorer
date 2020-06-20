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

#Example of code

time_0 = time.time()

fname = sys.argv[1] #Take the first argument entered in as the filename

stopwords = nltk.corpus.stopwords.words('english')

def content_filter(text):
    '''
    List comprehension for first pass at removing the standard English stopwords
    '''
    
    
    
    content = [w for w in text if w.lower() not in stopwords]
    return content

def frequency_analysis():
    
    text_list = [] 
    text_split_list = []
    word_list = []
    
    #Do for every json file in the cluster next*
    
    with open(fname) as f: #Taking JSON file and appending just the text information for each tweet.
        for line in f:
            tweet = json.loads(line)
            
            text_list.append(tweet['text'])
            
    for i in range(len(text_list)): #Splits each tweet by word using space as a delimiter. 
        text_split_list.append(text_list[i].split(" "))
        
    for i in range(len(text_split_list)): #Adds all to single list
        for j in range(len(text_split_list[i])):
            word_list.append(text_split_list[i][j])
    
    content_word_list = content_filter(word_list)
            
    fdist1 = FreqDist(content_word_list)
    fdist1_most_common = fdist1.most_common(50)

    custom_words = ['RT','','-','I\'m','@'] #Second pass at removing other stopwords
    fdist1_most_common = [i for i in fdist1_most_common if i[0] not in custom_words]

    time_2 = time.time()

    #print('Time taken was ' + str(time_1-time_0))
    #print('Then time taken was ' + str(time_2-time_1))
    print('Word list length is ' + str(len(word_list)))
    print('This account has ' + str(len(text_list)) + ' tweets.')

    print('----------') #Visualization of most frequent words by histogram.

    df = pd.DataFrame(fdist1_most_common, columns =['word', 'frequency'])
    df.plot(kind = 'bar', x = 'word')

    print('----------') # Subdiving data by bigrams

    bigram_master = []

    for i in range(len(text_list)):
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
        
    print(fdistbigram_common)

    dfbigram = pd.DataFrame(fdistbigram_common, columns =['word', 'frequency'])
    dfbigram.plot(kind = 'bar', x = 'word')

    print(word_list)

    plt.show()
    
if __name__ == '__main__':
    frequency_analysis()