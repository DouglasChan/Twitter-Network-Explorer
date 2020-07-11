import json
import gensim
import time
import nltk
import networkx as nx
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#This doc2vec model used on Twitter text corpora was guided by the Kaggle project, "Comparing Books with Word2Vec and Doc2Vec". 

def doc_similarity(json_filenames):
    stopwords = nltk.corpus.stopwords.words('english')
    custom_words = ['RT','rt','','-','I\m','@','--','|','I\'m','&amp;','#','.','``','...',':','https','\'','’','“','\'s','‘','!','\'re',',','(','[','\'m','n\'t','\'ve','\'d','&']
 
    for i in range(len(custom_words)):
        stopwords.append(custom_words[i])

    tweet_corpus = [] 
    
    for i in range(len(json_filenames)): #For each user
        local_tweet_corpus = []
        
        for line in open(json_filenames[i], 'r'): #Tweets are in sentence format
            word_list = word_tokenize(json.loads(line)['text'])
           
            for word in word_list:
                if word.lower() not in stopwords:
                    local_tweet_corpus.append(word) #Adds to the list of text for a specific user (local). This is in contrast to the list of all specified users' text corpora.
                    break
        
        local_tweet_as_one = ' '.join(map(str, local_tweet_corpus)) #Combines each tweet string with all other tweet strings from the same user collected.
        #Each individual tweet is separated by a space character, and the whole corpus is stored as a large string, per the requirements of the model shown below.
        
        tweet_corpus.append( #The tweet corpus before training the model looks like a large list. If we looked for 20 neighbors, it would be a list of 20 items, each item containing a list of all 
                            #the words (single words, no spaces allowed) for a user's tweet corpus. The model will be comparing these 20 items with each other for similarity scores.
            gensim.models.doc2vec.TaggedDocument( #Uses the doc2vec model
                gensim.utils.simple_preprocess(
                    local_tweet_as_one), #local_tweet_as_one needs to be a long string, not a list.
                    ["{}".format(json_filenames[i])]))
                    
    #Building the model.
    model = gensim.models.Doc2Vec(size = 300, #Number of features of the Doc2Vec model
                              min_count = 3, #As with other vectorizers, ignores words with a total frequency lower than this.
                              iter = 100) # The number of iterations
                              
    model.build_vocab(tweet_corpus)
    
    model.train(tweet_corpus, total_examples=model.corpus_count, epochs=model.epochs)

    doc2vec_scores = []
    
    ### Printing out the similarity scores to the terminal ###
    
    #for tweet_document in json_filenames:
    #    for tweet_document_compare in json_filenames:
    #        similarity = model.docvecs.similarity(tweet_document,tweet_document_compare)
            
    #        print("This is the similarity for %s, and %s. It is %s." %(tweet_document, tweet_document_compare, similarity))
        
    #    print('----------') #Separating by user.
    
    doc_model = model
    
    return doc_model

if __name__ == '__main__':
    doc_similarity()