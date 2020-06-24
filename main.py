import twitter_mention_frequency, twitter_get_user_timeline
import NLP_stats_repackaged, Doc_to_Vec_Refactored
import network_analysis, network_crawler
import NLP_Frequency_stats

from nltk import FreqDist
import sys
from subprocess import call

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
        try:
        #if len(most_mentioned_list) != 0: #Making sure it's not an empty list -- empty users / protected tweets may break the program.
            
            f_name_list.append('user_timeline_' + most_mentioned_list[i][0] + '.jsonl')
            downloading_json(most_mentioned_list[i][0]) #Wait for program to verify that the requisite .jsonl files associated with the user has been downloaded first before proceeding
        except Exception as e:
            print(e)
            continue #Pay attention here, if there's nothing there...hopefully this brings it back up?
               
    return f_name_list
        
def nlp_similarity(json_list): #* May remove -- could come in more useful when combining frequency data of groups?

    for i in range(len(json_list)):

        text_list, text_split_list, word_list = NLP_stats_repackaged.NLP_per_user(json_list[i]) #The main function of the NLP file returns 3 variables.
        
        content_word_list = NLP_stats_repackaged.content_filter(word_list) #Filters out stopwords
        
        fdist = NLP_stats_repackaged.getting_frequency(content_word_list)

if __name__ == '__main__':

    json_filenames = network_crawler.network_crawler(first_handle, levels)
        
    json_filenames = json_filenames[len(json_filenames)-1]

    doc_model = Doc_to_Vec_Refactored.doc_similarity(json_filenames)
     
    cluster_list, cluster_coordinates, graph_figure, ax = network_analysis.network_stuff(json_filenames, doc_model)
    
    NLP_Frequency_stats.frequency_analysis(cluster_list, cluster_coordinates, graph_figure, ax)
    
    nlp_similarity(json_filenames)
    
    