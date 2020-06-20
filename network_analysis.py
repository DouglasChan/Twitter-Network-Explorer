import networkx as nx
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import time
from networkx.algorithms.community import greedy_modularity_communities

def network_stuff(files, model):

    network_dict = {} #Per the code in the network lecture, a dictionary is used to keep track of edges *
    
    for tweet_document in files: #The file list is the most expanded json files up to the outermost level of the network.
    
        for tweet_document_compare in files: #Comparing each Twitter user to each other Twiter user
            
            similarity = model.docvecs.similarity(tweet_document,tweet_document_compare)
            print("This is the similarity for %s, and %s. It is %s." %(tweet_document[14:-6], tweet_document_compare[14:-6], similarity))
            
            tweet_1_name = tweet_document[14:-6] #For visualization of the users, we take the name of jsonl files and scrub off the prefix and suffix of the users being compared
            tweet_2_name = tweet_document_compare[14:-6]
            
            network_dict.setdefault((tweet_1_name, tweet_2_name), similarity)
        
        print('----------') #Separating similarity scores in raw output    

    G = nx.Graph()
    _ = [G.add_edge(i[0], i[1], weight = j) for i,j in network_dict.items() if j > 0.50]; #Uses similarity scores as the basis for drawing edges in the graph. 
                                                                                         #This parameter will vary depending on the size of the network.    
    print('There are ' + str(len(G)) + ' nodes being compared.')
    print('There are ' + str(len(G.edges)) + ' edges in the network.')
    
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
                G.nodes[node]['cluster'] = i+1
                
        #cluster_list = cluster_list
        '''
        print(cluster_list)
        print(type(cluster_list))
        print('wut')
        print(type(cluster_list[0]))
        print(type(list(cluster_list[0])))
        print(list(cluster_list[0]))
        print('wut2')
        time.sleep(1000)
        '''
        return cluster_list
       
    def get_node_color(node):
        color_indices = list(range(0,20))
        color_list = ['red','green','blue','yellow','orange',\
                    'pink','brown','purple','olive','cyan',\
                    'gold','dodgerblue','plum','crimson','silver',\
                    'indianred','peachpuff','honeydew','cornflowerblue','fuchsia']
    
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
    positions = nx.kamada_kawai_layout(G)

    plt.figure(figsize=(30,15))
    
    #Checking if I can annotate:
    #plt.annotate('x',(0.45, -0.1)) I can 
    
    #Calculating the center
    
    nx.draw(G, positions, **options)
    
    plt.savefig( "g.png" )
    
    print(type(positions))
    
    node_number = 0
    x_coords = []
    y_coords = []
    for i in range(len(cluster_list)):
        set_as_list = list(cluster_list[i])
        for j in range(len(set_as_list)): #Name within a cluster
            x_coords.append(positions[set_as_list[j]][0])
            y_coords.append(positions[set_as_list[j]][1])

            node_number += 1
            
    average_x = sum(x_coords) / node_number
    average_y = sum(y_coords) / node_number
    
    print(average_x)
    print(average_y)
    plt.annotate('xxx',(0.45,-0.1))
    
    #or i in range(len(positions.keys())):
    #    pass
    
    
    #Calculating positions
    
    #Calculating absolute center
    
    #for i in range(len(cluster_list)):
    #    set_as_list = list(cluster_list[i])
    #    for j in range(len(set_as_list)):
    #        print(set_as_list[j])
    
    print(positions)
    print('wut')
    time.sleep(1000)
    
    return cluster_list