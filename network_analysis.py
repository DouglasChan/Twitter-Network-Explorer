import networkx as nx
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import time

def network_stuff(files, model):

    network_dict = {} #Per the code in the network lecture, a dictionary is used to keep track of edges *
    
    for tweet_document in files: #The file list is the most expanded json files up to the outermost level of the network.
        #most_similar = model.docvecs.most_similar(tweet_document)[0][0]
    
        for tweet_document_compare in files: #Comparing each Twitter user to each other Twiter user
            similarity = model.docvecs.similarity(tweet_document,tweet_document_compare)
            print("This is the similarity for %s, and %s. It is %s." %(tweet_document[14:-6], tweet_document_compare[14:-6], similarity))
            
            tweet_1_name = tweet_document[14:] #For visualization of the users, we take the name of jsonl files and scrub off the prefix and suffix of the users being compared
            tweet_1_name = tweet_1_name[:-6]
            tweet_2_name = tweet_document_compare[14:]
            tweet_2_name = tweet_2_name[:-6]
            
            #print("This is the similarity for %s, and %s. It is %s." %(tweet_1_name, tweet, similarity))
            
            network_dict.setdefault((tweet_1_name, tweet_2_name), similarity)
        
        print('----------')    

    G = nx.Graph()
    _ = [G.add_edge(i[0], i[1], weight = j) for i,j in network_dict.items() if j > 0.5]; #j[0]? ; #0.425 for 50 ; #0.45 for 100

    print('Booga')
    time.sleep(5)
    
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
    time.sleep(5)
    
    
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