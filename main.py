import twitter_mention_frequency, twitter_get_user_timeline
import NLP_stats_repackaged, Doc_to_Vec_Refactored
import network_analysis, network_crawler
import Cluster_Analysis_NLP_with_Word_Clouds
import twitter_make_geojson, twitter_make_map

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
            f_name_list.append('user_timeline_' + most_mentioned_list[i][0] + '.jsonl')
            downloading_json(most_mentioned_list[i][0]) #Wait for program to verify that the requisite .jsonl files associated with the user has been downloaded first before proceeding
        except Exception as e: #Adding this exception in case any file does not end up downloading, prevents crashing of the program.
            print(e)
            continue 
               
    return f_name_list

if __name__ == '__main__':

    json_filenames = network_crawler.network_crawler(first_handle, levels)
        
    json_filenames = json_filenames[len(json_filenames)-1]

    doc_model = Doc_to_Vec_Refactored.doc_similarity(json_filenames)
     
    cluster_list, cluster_coordinates, graph_figure, ax = network_analysis.network_building(json_filenames, doc_model)
    
    geo_list = Cluster_Analysis_NLP_with_Word_Clouds.frequency_analysis(cluster_list, cluster_coordinates, graph_figure, ax)

    larger_coordinates_list, larger_text_list, larger_name_list, geo_list = twitter_make_geojson.main_geo_creator(geo_list)
    
    twitter_make_map.make_map(larger_coordinates_list, larger_text_list, larger_name_list, geo_list)

    