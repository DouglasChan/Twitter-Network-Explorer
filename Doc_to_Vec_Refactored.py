import json
import gensim
import time
import nltk
import networkx as nx
from nltk.tokenize import word_tokenize
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

#This doc2vec model used on Twitter text corpora was guided by the Kaggle project, "Comparing Books with Word2Vec and Doc2Vec". 

def doc_similarity(json_filenames, word_filters):
    stopwords = nltk.corpus.stopwords.words('english')
    custom_words = ['RT','rt','','-','I\m','@','--','|','I\'m','&amp;'] #May be redundant?
    stopwords.append(custom_words)

    tweet_corpus = [] #What is this?
    
    for i in range(len(json_filenames)): #For each user
        local_tweet_corpus = []
        
        for line in open(json_filenames[i], 'r'): #Tweets are in sentence format
            word_list = word_tokenize(json.loads(line)['text'])
            
            for word in word_list:
                if (word in word_filters[i]) and (word not in stopwords):
                    local_tweet_corpus.append(json.loads(line)['text']) #Adds to the variable specific to 
                    break
        
        local_tweet_as_one = ' '.join(map(str, local_tweet_corpus)) #Combines each tweet string with all other tweet strings from the same user collected.
        #Each individual tweet is separated by a space character, and the whole corpus is stored as a large string, per the requirements of the model shown below.
        
        tweet_corpus.append( #The tweet corpus before training the model looks like a large list. If we looked for 20 neighbors, it would be a list of 20 items, each item containing a list of all 
                            #the words (single words, no spaces allowed) for a user's tweet corpus. The model will be comparing these 20 items with each other for similarity scores.
            gensim.models.doc2vec.TaggedDocument( #Uses the doc2vec model
                gensim.utils.simple_preprocess(
                    local_tweet_as_one), #local_tweet_as_one needs to be a long string, not a list.
                    ["{}".format(json_filenames[i])]))

       
    #Building the model.
    model = gensim.models.Doc2Vec(size = 300, #Number of features of the Doc2Vec model
                              min_count = 3, #As with other vectorizers, ignores words with a total frequency lower than this.
                              iter = 100)
                              
    model.build_vocab(tweet_corpus)
    
    model.train(tweet_corpus, total_examples=model.corpus_count, epochs=model.epochs)
    
    model.docvecs.most_similar(1) #Uses cosine similarity between the 20 lists within the larger tweet_corpus list. 

    #NETWORK
    
    network_dict = {} #Network stuff
    
    for tweet_document in json_filenames:
        most_similar = model.docvecs.most_similar(tweet_document)[0][0]
    
        for tweet_document_compare in json_filenames:
            similarity = model.docvecs.similarity(tweet_document,tweet_document_compare)
            print("This is the similarity for %s, and %s. It is %s." %(tweet_document, tweet_document_compare, similarity))
            
            #network_dict.setdefault((tweet_document, tweet_document_compare), []).append(similarity) #Network
            tweet_1_name = tweet_document[14:]
            tweet_1_name = tweet_1_name[:-6]
            tweet_2_name = tweet_document_compare[14:]
            tweet_2_name = tweet_2_name[:-6]
            network_dict.setdefault((tweet_1_name, tweet_2_name), similarity)
        
        print('----------')
    
    '''
    #NETWORK COMPONENT
    
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
    
    # Make a graph
    #G = nx.Graph()
    # Add the edges if weight is greater than 20 - ie 20 transactions
    #_ = [G.add_edge(i[0], i[1], weight = len(j)) for i,j in mydict.items() if len(j) > 20]; 
    '''
    
    

if __name__ == '__main__':
    doc_similarity()