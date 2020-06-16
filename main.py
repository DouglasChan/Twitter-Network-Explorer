import twitter_mention_frequency
import twitter_get_user_timeline
import NLP_stats_repackaged
import Doc_to_Vec_Refactored
import network_analysis
import network_crawler

#Test
from nltk import FreqDist
import sys
from subprocess import call

import os.path
from os import path
import time

#Assuming you're starting with a profile that actually exists...

#Take the username as a starting point
first_handle = sys.argv[1] #Entering the Twitter handle of person you want to start with.
network_neighbors = int(sys.argv[2]) #Enter this as a parameter?
levels = int(sys.argv[3])

'''
Check if the .jsonl file has been downloaded!
'''
download_start = time.time()

def downloading_json(handle):
    file_name = 'user_timeline_' + handle + '.jsonl' #Converts the handle to the file path of hopefully existing json file.
    for i in range(2):
        if path.exists(file_name) == False:
            time.sleep(6)
            twitter_get_user_timeline.getting_timeline(handle) #Downloads if it doesn't exist
            continue
        else:
            break
    
    return file_name #Gives the full username...
    
def run_network(network_handle):
    f_name = downloading_json(network_handle) 
    return f_name
    
def getting_file_names(most_common_list_input):
    f_name_list = [] #List of json files in the closests neighbors...
    f_handle_list = []
    for i in range(network_neighbors): #Set number of people in network want to check
        if len(most_common_list_input) != 0: #Making sure it's not an empty list...
            f_name_list.append('user_timeline_' + most_common_list[i][0] + '.jsonl')
            f_handle_list.append(most_common_list[i][0])
            downloading_json(most_common_list[i][0]) #Wait for the file to have downloaded all of the right json files...
        else:
            print('Whoops.')
    
    return f_name_list, f_handle_list
    
    
def getting_file_names(most_common_list_input):
    f_name_list = [] #List of json files in the closests neighbors...
    f_handle_list = []
    
    
    print(most_common_list_input)
    print('cough')
    time.sleep(10)
    
    for i in range(network_neighbors): #Set number of people in network want to check
        if len(most_common_list_input) != 0: #Making sure it's not an empty list...
            f_name_list.append('user_timeline_' + most_common_list_input[i][0] + '.jsonl')
            f_handle_list.append(most_common_list_input[i][0])
            downloading_json(most_common_list_input[i][0]) #Wait for the file to have downloaded all of the right json files...
        else:
            print('Whoops2.')
    
    return f_name_list, f_handle_list
    
    
def nlp_similarity(placeholder_input):
    word_filter_all = []
    f_name_remove = []

    for i in range(len(placeholder_input)):
        text_list, text_split_list, word_list = NLP_stats_repackaged.NLP_per_user(placeholder_input[i])
        if len(text_list) == 0:
            f_name_remove.append(placeholder_input[i])

    for i in f_name_remove:
        if i in placeholder_input:
            placeholder_input.remove(i)

    for i in range(len(placeholder_input)):

        text_list, text_split_list, word_list = NLP_stats_repackaged.NLP_per_user(placeholder_input[i]) #The main function of the NLP file returns 3 variables.
        
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

    json_filenames, doc_model = Doc_to_Vec_Refactored.doc_similarity(placeholder_input, word_filter_all)
    return json_filenames, doc_model



if __name__ == '__main__':

    f_name = run_network(first_handle) #Takes the first handle inputted, checks that the appropriate user timeline is there...

    most_common_list = twitter_mention_frequency.twitter_mentioning(f_name) #Raw list, top 40 most connected people?
    
    f_name_list = getting_file_names(most_common_list)
    
    network_crawler.network_crawler(first_handle, levels)
               
    #json_filenames, doc_model = nlp_similarity(f_name_list)        
     
    #network_analysis.network_stuff(json_filenames, doc_model)
    
    