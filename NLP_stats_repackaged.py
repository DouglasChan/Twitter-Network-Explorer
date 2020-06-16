import json
import sys
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk import bigrams
import time
#Test
#This file takes in the filename as the first argument.

def NLP_per_user(fname):
    text_list = [] #Each item in text_list is the text from a single tweet
    text_split_list = [] #Text split list is a nested list with each smallest item being a given word separated by spaces.
    word_list = [] #Word list is a flat list of all the words from all the tweets. 
    
    print(fname)
    time.sleep(10)
    
    with open(fname) as f: #Taking the JSON file and appending just the text information for each tweet.
        for line in f:
            tweet = json.loads(line)
            text_list.append(tweet['text'])
        
    for i in range(len(text_list)): #Splits each tweet by word using space as a delimiter. 
        text_split_list.append(text_list[i].split(" "))    
    
    for i in range(len(text_split_list)): #Adds all to single list
        for j in range(len(text_split_list[i])):
            word_list.append(text_split_list[i][j])
     
    return text_list, text_split_list, word_list
    
stopwords = stopwords.words('english')
    
def content_filter(text): #This function and the one below are called by the main function.
    custom_words = ['RT','','-','I\m','@','--','|','I\'m','&amp;']
    stopwords.append(custom_words) #Adding custom stopwords associated with Twitter (ex : RT standing for Retweet, @ is the at symbol)
    content = [w for w in text if w.lower() not in stopwords]
    return content
    
def getting_frequency(list):
    fdist = FreqDist(list)
    fdist_most_common = fdist.most_common(50) #For NLP analysis, this function returns the 50 most common n-grams associated with a given user's profile.
    
    custom_words = ['RT','','-','I\m','@','--','|','I\'m','&amp;'] #Added some custom stopwords that were often used in Twitter.
    fdist_most_common = [i for i in fdist_most_common if i[0] not in custom_words]
    return fdist_most_common
    
if __name__ == "__main__":
    fname = sys.argv[1]
    
    NLP_per_user(fname)