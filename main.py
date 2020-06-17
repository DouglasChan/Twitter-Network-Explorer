import twitter_mention_frequency
import twitter_get_user_timeline
import NLP_stats_repackaged
import Doc_to_Vec_Refactored
import network_analysis
import network_crawler

from nltk import FreqDist
import sys
from subprocess import call

import os.path
from os import path
import time

#Assuming you're starting with a profile that actually exists...

first_handle = sys.argv[1] #Entering the Twitter handle of person you want to start with.
network_neighbors = int(sys.argv[2]) #The number of people to compare with per node at each level
levels = int(sys.argv[3]) #The degrees of separation of how far one would want to get

def downloading_json(handle): #This function checks if the .jsonl file has been downloaded to the directory.
    file_name = 'user_timeline_' + handle + '.jsonl' #Converts the handle to the filename of the existing json file.
    for i in range(2):
        if path.exists(file_name) == False:
            time.sleep(6) #Sleep statements are necessary insertions here. If the program isn't given enough time to download a given json file, downloads will keep restarting until the end of the loop taking much longer.
            twitter_get_user_timeline.getting_timeline(handle) #Downloads the json file if it doesn't exist in the directory
            continue
        else:
            break
    
    return file_name #Gives the full username...
        
def getting_file_names(most_mentioned_list):
    f_name_list = [] #List of json files in the closests neighbors...
    
    for i in range(network_neighbors): #The function checks for the most mentioned neighbors specified by network_neighbors parameter.
        if len(most_mentioned_list) != 0: #Making sure it's not an empty list -- empty users / protected tweets may break the program.
            f_name_list.append('user_timeline_' + most_mentioned_list[i][0] + '.jsonl')
            downloading_json(most_mentioned_list[i][0]) #Wait for program to verify that the requisite .jsonl files associated with the user has been downloaded first before proceeding
        else:
            raise Exception("We weren't able to get all the raw data.")
    
    return f_name_list
        
def nlp_similarity(json_list):

    word_filter_all = [] #This is the list of words that will be removed

    for i in range(len(json_list)):

        text_list, text_split_list, word_list = NLP_stats_repackaged.NLP_per_user(json_list[i]) #The main function of the NLP file returns 3 variables.
        
        content_word_list = NLP_stats_repackaged.content_filter(word_list) #Filters out
        
        fdist = NLP_stats_repackaged.getting_frequency(content_word_list)
        
        word_filter_list = []
        f_name_remove = []
        
        if len(fdist) == 0: #Creates local list of words to create subsection of tweets
            pass
        else:
            for i in range(5):
                word_filter_list.append(fdist[i][0])
                
        if len(word_filter_list) != 0: #Removes jsonl file name from list of jsonl files if the Twitter user isn't found...
            word_filter_all.append(word_filter_list)
            
    #print(json_list)
    #print('wut')
    #time.sleep(1000)

    doc_model = Doc_to_Vec_Refactored.doc_similarity(json_list)
    return doc_model



if __name__ == '__main__':

    f_name = downloading_json(first_handle)

    most_common_list = twitter_mention_frequency.twitter_mentioning(f_name) #Raw list, top 40 most connected people?
    
    f_name_list = getting_file_names(most_common_list)
    
    json_filenames = network_crawler.network_crawler(first_handle, levels)
        
    json_filenames = json_filenames[len(json_filenames)-1]
    print(json_filenames)
    
    time.sleep(10)
               
    doc_model = nlp_similarity(json_filenames)        
     
    network_analysis.network_stuff(json_filenames, doc_model)
    
    