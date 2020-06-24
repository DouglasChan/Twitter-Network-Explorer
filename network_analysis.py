import networkx as nx
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt
import time
from networkx.algorithms.community import greedy_modularity_communities
#Test

def network_stuff(files, model):

    cluster_coordinates = []

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
    _ = [G.add_edge(i[0], i[1], weight = j) for i,j in network_dict.items() if j > 0.425]; #Uses similarity scores as the basis for drawing edges in the graph. 
                                                                                         #This parameter will vary depending on the size of the network. 42.5, 57.5    
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
                G.nodes[node]['cluster'] = i #Was i + 1
                
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

    #graph_figure = plt.figure(figsize=(40,20))
    graph_figure, ax = plt.subplots(figsize=(300,150))
    ax.set_facecolor('none')
    #ax.set_xlim([-2, 2]) #Remove?
    #ax.set_ylim([-2, 2]) #Remove?
    
    #Checking if I can annotate:
    #plt.annotate('x',(0.45, -0.1)) I can 
    
    #Calculating the center
    
    #print(G.nodes)
    #print(G.edges)
    
    #G.nodes.set_zorder(2)
    
    '''
    IF I WANT TO TRY ZORDER
    '''
    
    #for node in G.nodes():
    #    H = G.subgraph([node])
    #    collection = nx.draw_networkx_nodes(H, positions)
    #    collection.set_zorder(3)
    
    #print('wut')
    #time.sleep(1000)
    
    nx.draw(G, positions, **options)
    
    #print(G.nodes)
    #print('wut')
    #time.sleep(1000)
    
    
    #print(type(positions))
    
    cluster_number = 1
    #x_coords = []
    #y_coords = []
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
        
        plt.annotate(str(cluster_number),(average_x,average_y))
        
        #Location of the Word cloudsd
        
        plt.annotate('cloud ' + str(cluster_number), (average_x*1.4,average_y*1.4))
        
        cluster_coordinates.append((average_x,average_y))
        
        cluster_number += 1
        
    
    print(average_x)
    print(average_y)
    plt.annotate('origin',(0,0))
    
    plt.savefig( "g.png" )
    #graph_figure = plt
    
    #or i in range(len(positions.keys())):
    #    pass
    
    
    #Calculating positions
    
    #Calculating absolute center
    
    #for i in range(len(cluster_list)):
    #    set_as_list = list(cluster_list[i])
    #    for j in range(len(set_as_list)):
    #        print(set_as_list[j])
    
    #print(positions)
    #print('wut')
    #time.sleep(1000)
    
    #print(cluster_coordinates)
    #print('wut')
    #time.sleep(1000)
    
    return cluster_list, cluster_coordinates, graph_figure, ax #, cluster_coordinates