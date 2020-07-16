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
from wordcloud import WordCloud

import matplotlib.image as mpimg
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
import os

stopwords = nltk.corpus.stopwords.words('english')
stopwords_unigram = ['RT','rt','','-','I\'m','@','—','.','&','&amp','us','&amp']

for i in range(len(stopwords_unigram)):
    stopwords.append(stopwords_unigram[i])

geo_list = []

def content_filter(text):
    '''
    List comprehension for first pass at removing the standard English stopwords
    '''
    content = [w for w in text if w.lower() not in stopwords]
    return content

def frequency_analysis(cluster_setlist, cluster_coordinates, graph_figure, ax, first_handle): #Take from network_analysis
    
    cluster_counter = 1
    
    for cluster_list in range(len(cluster_setlist)):#Cluster_setlist is a list of networkx set objects.
        cluster_members = list(cluster_setlist[cluster_list]) #Converting from networkx object to list of users within a cluster
        
        cluster_text_list = []
        cluster_text_split_list = []
        cluster_word_list = []

        for j in range(len(cluster_members)):
        
            text_list = [] 
            text_split_list = []
            word_list = []
        
            fname = 'user_timeline_' + cluster_members[j] + '.jsonl' #Converting username back to .jsonl filename
            geo_list.append(fname)
            
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
           
        cluster_text_list = [item for sublist in cluster_text_list for item in sublist] #Making cluster data into a flat list
        cluster_text_split_list = [item for sublist in cluster_text_split_list for item in sublist]
        cluster_word_list = [item for sublist in cluster_word_list for item in sublist]
        
        content_word_list = content_filter(cluster_word_list) #Applying filtering of stopwords to the words in the cluster

        fdist1 = FreqDist(content_word_list)
        fdist1_most_common = fdist1.most_common(50) #The N number of most common words most frequently used in a cluster
        
        df_unigram = pd.DataFrame(fdist1_most_common, columns=['word','frequency'])
        
        df_unigram.plot(kind = 'bar', x = 'word')
        
        print(fdist1_most_common)
        
        unigram_distribution_variable = []
        
        for i in range(len(fdist1_most_common)):
            for j in range(fdist1_most_common[i][1]): #The number of times it appears.
                unigram_distribution_variable.append(fdist1_most_common[i][0])
        
        unigram_distribution_variable = ' '.join(unigram_distribution_variable) #This gives what I'd need -- most frequent unigrams as a long string.
        
        script_dir = os.path.dirname(__file__)
    
        results_dir = os.path.join(script_dir, '{0}/unigram_data/'.format(first_handle))
        sample_file_name = "unigram_{0}.csv".format(cluster_counter) #Check?
    
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
    
        df_unigram.to_csv(results_dir + sample_file_name)
    
        results_dir = os.path.join(script_dir,'{0}/unigram_histograms/'.format(first_handle))
        sample_file_name = "unigram_histogram_{0}.png".format(cluster_counter)
        
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        
        plt.savefig(results_dir + sample_file_name)
        
        ###

        bigrams = [b for l in cluster_text_list for b in zip(l.split(" ")[:-1],l.split(" ")[1:])]

        remove_stopword_bigram = []
        bigrams_pared = []
        
        bigram_filtered = []
        bigram_discard = []
        
        for i in range(len(bigrams)):
            first_condition = bigrams[i][0] in stopwords
            second_condition = bigrams[i][1] in stopwords
            if first_condition or second_condition == True:
                bigram_discard.append(bigrams[i])
            elif ('@' == bigrams[i][0][0]) or ('@' == bigrams[i][1][0]): #Removing mentions from bigrams
                bigram_discard.append(bigrams[i])
            else:
                bigram_filtered.append(bigrams[i])
        
        fdist2 = FreqDist(bigram_filtered)
        fdist2_most_common = fdist2.most_common(50)
        
        fdist2_most_common_split = []
        
        for i in range(len(fdist2_most_common)):
            fdist2_most_common_split.append((fdist2_most_common[i][0][0],fdist2_most_common[i][0][1],fdist2_most_common[i][1]))
        
        bigram_distribution_variable = []
        
        for i in range(len(fdist2_most_common)):
            for j in range(fdist2_most_common[i][1]):
                bigram_distribution_variable.append(fdist2_most_common[i][0])
    
        #Would need to do more work for turning into word cloud, not so important at athe moment.
        
        results_dir = os.path.join(script_dir,'{0}/bigram_data/'.format(first_handle))
        sample_file_name = "bigram_{0}.csv".format(cluster_counter) #Check?
    
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        
        df_bigram_split = pd.DataFrame(fdist2_most_common_split, columns=['word1','word2','frequency'])
        df_bigram_split.to_csv(results_dir+sample_file_name)        
        
        df_bigram = pd.DataFrame(fdist2_most_common, columns=['bigram pair', 'frequency'])
        df_bigram.plot(kind = 'bar', x = 'bigram pair')
        
        results_dir = os.path.join(script_dir,'{0}/bigram_histograms/'.format(first_handle))
        sample_file_name = "bigram_histogram_{0}.png".format(cluster_counter)
        
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        
        plt.savefig(results_dir + sample_file_name)
        
        '''
        This is the section of the program that generates word clouds
        '''
        
        wordcloud = WordCloud(background_color = 'white', collocations=False).generate(unigram_distribution_variable)
        
        results_dir = os.path.join(script_dir,'{0}/unigram_wordclouds/'.format(first_handle))
        sample_file_name = "unigram_wordclouds_{0}.png".format(cluster_counter)
        
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        
        wordcloud.to_file(results_dir + sample_file_name)
        
        cluster_counter += 1
        
        #plt.show()

    for i in range(len(cluster_coordinates)):
        img_orig = mpimg.imread('cluster ' + str(i+1) + '.png')
        imagebox_python = OffsetImage(img_orig, zoom = 0.425) #Zoom magnifies or shrinks the wordcloud object
        
        #imagebox_python.set_zorder(1) #An experimental part of the code for positioning zorder of nodes vs word clouds
        
        annotation_box = AnnotationBbox(imagebox_python,(cluster_coordinates[i-len(cluster_coordinates)][0]*1.45,cluster_coordinates[i-len(cluster_coordinates)][1]*1.40),frameon=False)
        print(annotation_box)
        
        '''
        As explained in the network_analysis.py file, the parameters in the line above control the ratio of positioning the word clouds from the distance between the origin and cluster center.
        '''
        
        ax.add_artist(annotation_box)
        ax.set_facecolor('none') #Syntax related to adding custom .png images to existing matplotlib figures.
    
    results_dir = os.path.join(script_dir,'{0}/network_with_wordclouds/'.format(first_handle))
    sample_file_name = "network_with_wordclouds.png"
        
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)

    graph_figure.savefig(results_dir + sample_file_name)
    
    return geo_list
    
if __name__ == '__main__':
    
    frequency_analysis()
    
#Bigram Link : https://stackoverflow.com/questions/21844546/forming-bigrams-of-words-in-list-of-sentences-with-python