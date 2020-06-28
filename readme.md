# Introduction

# Packages
tweepy (v 3.8.0)

json (v 2.0.9)

nltk (v 3.4.5)

gensim (v 3.8.3)

networkx (v 2.3)

matplotlib (v 3.1.1)

# Getting Started & Running the Program

1. You will first need to apply for a Twitter developer license at this page (https://developer.twitter.com/en/apply-for-access). 

2. When you have consumer keys and access tokens generated, you can set these environment variables on your machine. Sukhvinder Singh goes through connecting to the Twitter API in this video : (https://www.youtube.com/watch?v=YhfXuS44oH4&list=PLmcBskOCOOFW1SNrz6_yzCEKGvh65wYb9&index=14 ). 

3. Ensure you have the third-party packages mentioned above installed.

4. To run the script, first ensure that you know the correct spelling of the Twitter handle you want to start with. In this example, we'll use Khan Academy (khanacademy). 

5. In the directory with all of the scripts, we type: "python main.py khanacademy 5 2" without the quotations. We'll be exploring the network starting at Khan Academy, with 5 neighbors starting from the first node, and then 5 neighbors searched for each of those first level nodes for a depth level of 2.

# Contents

twitter_client.py : Sets up a connection to the Twitter API using the Python module Tweepy.

twitter_get_user_timeline.py : Input is the Twitter handle of the user of which you wish to collect their tweets. Saves jsonl (json line file) of the user in the directory the main script is run.

twitter_mention_frequency.py : Gets the top users most mentioned by the Twitter account you are looking into. Returns the N most mentioned users as a list of tuples. Part of the basis for the network crawler portion of the program.

NLP_stats_repacked.py : Various functions to extract and preprocess the text data from a user's collection of tweets. Preprocessing is done to be compatible with the Doc2Vec model, and for word clouds for each cluster.

Doc_to_Vec_Refactored.py : Takes all the text data from every single user, converts it into the format that the Document2Vector model can work with. Aggregated text from each user is preprocessed and collected, and similarity scores between each pair of users is generated using a Doc2Vec model.

network_crawler.py : Obtains the names of Twitter users in a network. Depending on the number of neighbors specified per node, and the depth of levels to search, the crawler will use top mentioned users (as counted by the file "twitter_mention_frequency.py" as the basis of downloading jsonl files. 

network_analysis.py : This file takes the similarity scores calculated within the "Doc_to_Vec_Refactored.py file and reconfigures each user into a network based on similarity. Nodes that fall below a certain threshold of similarity will not be displayed along with edges that do not represent enough similarity. Clustering in this newly formed network object is also performed here using a greedy algorithm.

Cluster_Analysis_NLP_with_Word_Clouds.py : Takes members within clusters generated by the network analysis script and does NLP frequency analysis for each cluster. Creates wordcloud objects for each cluster and positions them on the matplotlib graph object.

twitter_make_geojson.py : Uses the topleft corner of the bounding box of geodata enabled tweets when available. In Sukhvinder's tutorial the files are individually saves as .geo.json files, but in this case we pass variables to the final script in the pipeline. 

twitter_make_map.py : Creates interactive HTML pages for each user if there are geodata enabled tweets found. 

main.py : Central file linking all subcomponents together. Ensures that .jsonl files are present in the directory before proceding onto modeling and visualization work.

# References

1. Twitter tutorial -- Sukhvinder Singh -- https://www.youtube.com/watch?v=pVmCI9zIMbc&list=PLmcBskOCOOFW1SNrz6_yzCEKGvh65wYb9

2. Sukhvinder Singh's Github page for the course, "Mining Data on Twitter with Python" : https://github.com/karramsos/-Mining-Data-on-Twitter-with-Python

3. David Currie's notebook, "Comparing Books with Word2Vec and Doc2Vec" : https://www.kaggle.com/currie32/comparing-books-with-word2vec-and-doc2vec

4. Generating A Twitter Ego-Network & Detecting Communities : https://towardsdatascience.com/generating-twitter-ego-networks-detecting-ego-communities-93897883d255

5. Text Similarities : Estimate the degree of similarity between two texts : https://medium.com/@adriensieg/text-similarities-da019229c894

6. Mining Twitter data : https://towardsdatascience.com/mining-twitter-data-ba4e44e6aecc

7. Tf-idf for Bigrams & Trigrams : https://www.geeksforgeeks.org/tf-idf-for-bigrams-trigrams/

8. Generating A Twitter Ego-Network & Detecting Communities : https://towardsdatascience.com/generating-twitter-ego-networks-detecting-ego-communities-93897883d255

9. Readme structure was influenced by course TAs' capstone projects : Daria Aza & Patrick Min:
9a. https://github.com/DariaAza/Deep-QLearning-Agent-for-Traffic-Signal-Control 
9b. https://github.com/pwmin/Capstone-Project

* Get license

#Ref : 
#1. https://stackoverflow.com/questions/43954114/python-wordcloud-repetitve-words
#2. https://www.science-emergence.com/Articles/How-to-insert-an-image-a-picture-or-a-photo-in-a-matplotlib-figure/