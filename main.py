import twitter_mention_frequency
import twitter_get_user_timeline
import NLP_stats_repackaged
import Doc_to_Vec_Refactored
#Test
from nltk import FreqDist
import sys
from subprocess import call

import os.path
from os import path
import time

import networkx as nx
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

#Assuming you're starting with a profile that actually exists...

#Take the username as a starting point
first_handle = sys.argv[1] #Entering the Twitter handle of person you want to start with.
network_neighbors = int(sys.argv[2]) #Enter this as a parameter?

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
    for i in range(network_neighbors): #Set number of people in network want to check
        if len(most_common_list_input) != 0: #Making sure it's not an empty list...
            f_name_list.append('user_timeline_' + most_common_list[i][0] + '.jsonl')
            mega_list.append(f_name_list)
            downloading_json(most_common_list[i][0]) #Wait for the file to have downloaded all of the right json files...
        else:
            print('Whoops.')
    
    return f_name_list
    
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

    Doc_to_Vec_Refactored.doc_similarity(placeholder_input, word_filter_all)
    
def network_stuff():

    G = nx.Graph()
    _ = [G.add_edge(i[0], i[1], weight = j) for i,j in network_dict.items() if j > 0.44]; #j[0]? ; #0.425 for 50 ; #0.45 for 100
    

    print('Booga')
    time.sleep(10)
    
    print(len(G))
    print(len(G.edges))
    print(G.edges)
    print(type(G.edges))
    
    #Removing self ones?
    edge_list = list(G.edges)
    edge_removal_list = []
    for i in range(len(edge_list)):
        print(edge_list[i])
        
        if edge_list[i][0] == edge_list[i][1]:
            edge_removal_list.append(edge_list[i])
            
    print(edge_removal_list)
    
    
    print('Tooktook')
    time.sleep(12)
    
    
    for i in range(len(edge_removal_list)):
        G.remove_edge(edge_removal_list[i][0],edge_removal_list[i][1])
        
    G.remove_nodes_from(list(nx.isolates(G)))
    isolate_list = list(nx.isolates(G))
    
    
    
    #Clustering portion
    from networkx.algorithms.community import greedy_modularity_communities

    clusters = greedy_modularity_communities(G)
    
    print(f'The social network has {len(clusters)} clusters.')
    
    plt.figure(figsize=(13,7))
    #nx.draw_kamada_kawai(G, with_labels = True)
    
    
    def set_cluster_number(G, cluster_list):
        for i, cluster in enumerate(cluster_list):
            for node in cluster:
                G.nodes[node]['cluster'] = i+1
                
    misc_clusters = [13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50]
            
    def get_node_color(node):

        if node['cluster'] == 1:
            color = 'pink'
        elif node['cluster'] == 2:
            color = 'lightblue'
        elif node['cluster'] == 3:
            color = 'lightgreen'
        elif node['cluster'] == 4:
            color = 'blue'
        elif node['cluster'] == 5:
            color = 'red'
        elif node['cluster'] == 6:
            color = 'orange'
        elif node['cluster'] == 7:
            color = 'purple'
        elif node['cluster'] == 8:
            color = 'brown'
        elif node['cluster'] == 9:
            color = 'darkblue'
        elif node['cluster'] == 10:
            color = 'green'
        elif node['cluster'] == 11 :
            color = 'darkgreen'
        elif node['cluster'] == 12:
            color = 'lightred'
        elif node['cluster'] in misc_clusters:
            color = 'grey'
            
        else:   
            pass
        return color
        
    set_cluster_number(G, clusters)
    
    options = {'with_labels': True, 
               'node_color':[get_node_color(G.nodes[n]) for n in G.nodes],
               'edge_color':'grey',
               'font_size': 10}
    positions = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(20,10))
    nx.draw(G, positions, **options)
    
    
    plt.savefig( "g.png" )


if __name__ == '__main__':

    f_name = run_network(first_handle) #Takes the first handle inputted, checks that the appropriate user timeline is there...

    most_common_list = twitter_mention_frequency.twitter_mentioning(f_name) #Raw list, top 40 most connected people?
    
    mega_list = []
    
    f_name_list = getting_file_names(most_common_list)
               
    nlp_similarity(f_name_list)        
            