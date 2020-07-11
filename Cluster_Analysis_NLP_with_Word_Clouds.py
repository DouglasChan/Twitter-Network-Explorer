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

stopwords = nltk.corpus.stopwords.words('english')
stopwords_unigram = ['RT','rt','','-','I\'m','@','—','.','&','&amp','us','&amp']

for i in range(len(stopwords_unigram)):
    stopwords.append(stopwords_unigram[i])

#print(stopwords)
#time.sleep(1000)

geo_list = []

def content_filter(text):
    '''
    List comprehension for first pass at removing the standard English stopwords
    '''
    content = [w for w in text if w.lower() not in stopwords]
    return content

def frequency_analysis(cluster_setlist, cluster_coordinates, graph_figure, ax): #Take from network_analysis
    
    #frequency_unigram_stats = []
    frequency_bigram_stats = []
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
                
                #Where I would put new bigram?
        
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
        
        
        #custom_words = ['RT','rt','','-','I\'m','@','—','.'] #Second pass at removing other stopwords 
        #fdist1_most_common = [i for i in fdist1_most_common if i[0] not in (custom_words or stopwords)]
        
        df_unigram = pd.DataFrame(fdist1_most_common, columns=['word','frequency'])
        
        df_unigram.plot(kind = 'bar', x = 'word')
        
        print(fdist1_most_common)
        
        unigram_distribution_variable = []
        
        for i in range(len(fdist1_most_common)):
            for j in range(fdist1_most_common[i][1]): #The number of times it appears.
                unigram_distribution_variable.append(fdist1_most_common[i][0])
        
        #frequency_unigram_stats.append(fdist1_most_common)
        
        unigram_distribution_variable = ' '.join(unigram_distribution_variable) #This gives what I'd need -- most frequent unigrams as a long string.
        ###

        #print(cluster_text_list)
        #print(len(cluster_text_list))

        bigrams = [b for l in cluster_text_list for b in zip(l.split(" ")[:-1],l.split(" ")[1:])]

        yes_counter = 0
        no_counter = 0
        remove_stopword_bigram = []
        bigrams_pared = []

        '''
        for i in range(len(bigrams)):
            if (bigrams[i][0] or bigrams[i][1] or bigrams[i][0].lower() or bigrams[i][1].lower()) in stopwords:
                print('yes')
                print('\n')
                print(bigrams[i][0])
                print(bigrams[i][1])
                print(bigrams[i][0].lower())
                print(bigrams[i][1].lower())
                print('\n')
                time.sleep(4)
                yes_counter += 1
                remove_stopword_bigram.append(i)
                print(remove_stopword_bigram)
                
            else:
                print('no')
                no_counter += 1
            #print('\n')'
        '''
            
        #print(remove_stopword_bigram)
        #time.sleep(1000)
        
        bigram_filtered = []
        bigram_discard = []
        
        for i in range(len(bigrams)):
            if (bigrams[i][0] or bigrams[i][1] or bigrams[i][0].lower()) in stopwords:
                print(bigrams[i][0])
                print(bigrams[i][1])
                bigram_discard.append(bigrams[i])
                print('discard')
                print('\n')
            else:
                bigram_filtered.append(bigrams[i])
                print('filtered')
                print('\n')

            print(bigrams[i])
            print('This is filtered.')
            print(bigram_filtered)
            print('This is discarded')
            print(bigram_discard)
            time.sleep(10)
        
        time.sleep(1000)
                
        for i in range(len(bigrams)):
            if i not in remove_stopword_bigram:
                bigrams_pared.append(bigrams[i])
                
        #for i in range(len(bigrams_without)):
        #    bigrams_pared_2.append(bigrams[i])
            
        #print(bigrams_pared_2)
        
        #print(remove_stopword_bigram)
        #print(bigrams_pared)
        #print(yes_counter)
        #print(no_counter)
        #print(stopwords)
        #print(len(bigrams))
        #print(len(bigrams_pared))
        #time.sleep(1000)

        #print(stopwords)
        
        fdist2 = FreqDist(bigrams_pared_2)
        fdist2_most_common = fdist2.most_common(50)
        print(fdist2_most_common)

        time.sleep(1000)
        
        #Bigram Link : https://stackoverflow.com/questions/21844546/forming-bigrams-of-words-in-list-of-sentences-with-python
        
        '''
        bigram_master = []
        
        for bigram in range(len(cluster_text_list)):
            bigram_word_list = []
            bigram_word_list.append(cluster_text_list[bigram].split(" "))
                
            word_output_list = 0
        
            for split_bigram_word in bigram_word_list: #Gets rid of nesting quirk
                word_output_list = split_bigram_word  

            bigrams = list(nltk.bigrams(word_output_list))
        
            filtered = []
            for pairs in bigrams: #Similar process as to the unigrams
                if pairs[0].lower() in stopwords or pairs[1].lower() in stopwords:
                    continue
                elif pairs[0].lower() in custom_words or pairs[1].lower() in custom_words:
                    continue
                else:
                    filtered.append(pairs)
        
            bigram_master.extend(filtered)
            
        fdistbigram = FreqDist(bigram_master)
        fdistbigram_common = fdistbigram.most_common(50)
        
        bigram_distribution_variable = []
        
        for i in range(len(fdistbigram_common)): #Again, this code is similar to that of the unigrams, and the explanation is the same.
            for j in range(fdistbigram_common[i][1]): 
                bigram_distribution_variable.append(fdistbigram_common[i][0])
        
        df = pd.DataFrame(fdist1_most_common, columns =['word', 'frequency'])
        
        dfbigram = pd.DataFrame(fdistbigram_common, columns =['word', 'frequency'])
        '''
        
        '''
        This is the section of the program that generates word clouds
        '''
        
        wordcloud = WordCloud(background_color = 'white', collocations=False).generate(unigram_distribution_variable)
        
        wordcloud.to_file('cluster ' + str(cluster_counter) + '.png') 
        cluster_counter += 1
        
        plt.show()

    for i in range(len(cluster_coordinates)):
        img_orig = mpimg.imread('cluster ' + str(i+1) + '.png')
        imagebox_python = OffsetImage(img_orig, zoom = 0.425) #Zoom magnifies or shrinks the wordcloud object
        
        #imagebox_python.set_zorder(1) #An experimental part of the code for positioning zorder of nodes vs word clouds
        
        annotation_box = AnnotationBbox(imagebox_python,(cluster_coordinates[i-len(cluster_coordinates)][0]*1.45,cluster_coordinates[i-len(cluster_coordinates)][1]*1.45),frameon=False) 
        
        '''
        As explained in the network_analysis.py file, the parameters in the line above control the ratio of positioning the word clouds from the distance between the origin and cluster center.
        '''
        
        ax.add_artist(annotation_box)
        ax.set_facecolor('none') #Syntax related to adding custom .png images to existing matplotlib figures.
        
    plt.show()
    
    return geo_list
    
if __name__ == '__main__':
    
    frequency_analysis()