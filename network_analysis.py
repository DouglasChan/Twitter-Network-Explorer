import networkx as nx
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import time
from networkx.algorithms.community import greedy_modularity_communities

def network_building(files, model):

    cluster_coordinates = []

    network_dict = {} #Per the code in the network lecture, a dictionary is used to keep track of edges.
    
    for tweet_document in files: #The file list is the most expanded json files up to the outermost level of the network.
    
        for tweet_document_compare in files: #Comparing each Twitter user to each other Twiter user
            
            similarity = model.docvecs.similarity(tweet_document,tweet_document_compare)
            print("This is the similarity for %s, and %s. It is %s." %(tweet_document[14:-6], tweet_document_compare[14:-6], similarity)) 
            
            tweet_1_name = tweet_document[14:-6] #For visualization of the users, we take the name of jsonl files and scrub off the prefix and suffix of the users being compared
            tweet_2_name = tweet_document_compare[14:-6]
            
            network_dict.setdefault((tweet_1_name, tweet_2_name), similarity)
        
        print('----------') #Separating similarity scores in raw output    

    G = nx.Graph()
    _ = [G.add_edge(i[0], i[1], weight = sim_score) for i,sim_score in network_dict.items() if sim_score > 0.4]; #Uses similarity scores as the basis for drawing edges in the graph. This parameter sim_score ranges from 0 to 1.
                                                                                              
    '''
    To get the clustering algorithm to work correctly, we must remove isolates in our network. 
    
    The algorithm won't detect isolates automatically, since in our Doc2Vec model we end up comparing similarity of each Twitter user, to each other Twitter user and themselves.
    
    Since a similarity score with themselves will always generate 1, we will need to remove these self-similarity scores from the edge list before proceeding.
    '''
    
    #Removing edges of nodes pointing to themselves.
    edge_list = list(G.edges)
    edge_removal_list = []
    for i in range(len(edge_list)): #Checking if this edge is between a node and itself
        if edge_list[i][0] == edge_list[i][1]:
            edge_removal_list.append(edge_list[i])

    #Using list created above to remove these edges from the graph object.
    for i in range(len(edge_removal_list)):
        G.remove_edge(edge_removal_list[i][0],edge_removal_list[i][1])
        
    '''
    Once the edges have been removed, we can use the inbuilt nx.isolates function to identify which nodes don't have connections to other nodes.
    '''
    G.remove_nodes_from(list(nx.isolates(G)))
    
    #Clustering portion
    
    clusters = greedy_modularity_communities(G)
    
    print(f'The social network has {len(clusters)} clusters.') #Per the network science notebook, we use similar visualizations for our network graphs.
    
    def set_cluster_number(G, cluster_list): #This cluster number function is used to assign a numerical value to the clusters generated through the greedy modularity algorithm for community detection.
        for i, cluster in enumerate(cluster_list):
            for node in cluster:
                G.nodes[node]['cluster'] = i 
                
        return cluster_list
       
    def get_node_color(node):
        color_indices = list(range(0,20))
        color_list = ['red','green','blue','yellow','orange',\
                    'pink','brown','purple','olive','cyan',\
                    'gold','dodgerblue','plum','crimson','silver',\
                    'indianred','peachpuff','honeydew','cornflowerblue','fuchsia'] #Clusters' colors will corresopnd to the values in this color_list. Here we assume that under 20 clusters will be found.
    
        if node['cluster'] in color_indices:
            color = color_list[node['cluster']]
            
        else:
            color = 'grey'
            
        return color
        
    cluster_list = set_cluster_number(G, clusters)
    
    options = {'with_labels': True, 
               'node_color':[get_node_color(G.nodes[n]) for n in G.nodes],
               'edge_color':'grey',
               'font_size': 10}
               
    positions = nx.kamada_kawai_layout(G) #Uses force-directed graph drawing, and the Kawada-Kawai algrotihm.

    graph_figure, ax = plt.subplots(figsize=(300,150)) #Graph created using subplots -- Doing so enables us to draw both word clouds and the network on the same figure.
    ax.set_facecolor('none')
    
    '''
    Experimental Code to display nodes in foreground relative to the word cloud objects.
    '''
    
    #for node in G.nodes():
    #    H = G.subgraph([node])
    #    collection = nx.draw_networkx_nodes(H, positions)
    #    collection.set_zorder(3)
    
    nx.draw(G, positions, **options)
    
    cluster_number = 1
    
    '''
    Cluster locations are important for automatically positioning the word clouds onto the combined network / word cloud figure. 
    
    Since the kamada kawai algorithm centers the figure at 0, 0 with height and width spanning from approximately -1 to 1, 
    we can use this fact to automatically position the word clouds. 
    
    The distance from the center of the network figure, to the center of a given cluster, times a certain ratio is what I decided on. 
    Choosing this distance should make a word cloud appear radially outward on the periphery of a given cluster, 
    but in close proximity enough to give useful information on the frequent words associated with a cluster. 
    '''

    for i in range(len(cluster_list)):
        set_as_list = list(cluster_list[i])
        
        nodes_in_cluster = 0
        
        cluster_x_coords = []
        cluster_y_coords = []
        for j in range(len(set_as_list)): #Name within a cluster
            cluster_x_coords.append(positions[set_as_list[j]][0])
            cluster_y_coords.append(positions[set_as_list[j]][1])

            nodes_in_cluster += 1
            
        average_x = sum(cluster_x_coords) / nodes_in_cluster
        average_y = sum(cluster_y_coords) / nodes_in_cluster
        
        cluster_coordinates.append((average_x,average_y))
        cluster_number += 1
        
    #plt.annotate('origin',(0,0)) This can be uncommented if one wants to verify the center of the figure. 
    
    plt.savefig( "network_graph.png" )
    
    return cluster_list, cluster_coordinates, graph_figure, ax #, cluster_coordinates