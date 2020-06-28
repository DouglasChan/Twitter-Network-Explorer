import json
import sys
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk import bigrams
import time

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