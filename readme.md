# Introduction

# Packages
tweepy
twitter_client
json
nltk
gensim
networkx
matplotlib

# Getting Started

1. You will first need to apply for a Twitter developer license at this page (https://developer.twitter.com/en/apply-for-access). 

2. When you have consumer keys and access tokens generated, you can set these environment variables on your machine. Sukhvinder Singh goes through connecting to the Twitter API in this video : (https://www.youtube.com/watch?v=YhfXuS44oH4&list=PLmcBskOCOOFW1SNrz6_yzCEKGvh65wYb9&index=14 ). 

3. Dedicated directory for working *

# Running the Program

# Contents

twitter_client.py : Sets up a connection to the Twitter API using the Python module Tweepy.

twitter_get_user_timeline.py : Input is the Twitter handle of the user of which you wish to collect their tweets. Saves jsonl (json line file) of the user in the directory the main script is run.

twitter_mention_frequency.py : Gets the top users most mentioned by the Twitter account you are looking into. Returns the N most mentioned users as a list of tuples. Part of the basis for the network crawler portion of the program.

NLP_stats_repackaged.py : Various functions to extract and preprocess the text data from a user's collection of tweets. Preprocessing is done to be compatible with the Doc2Vec model, and for word clouds for each cluster.

Doc_to_Vec_Refactored.py : 

# Setting

# References

1. Twitter tutorial -- Sukhvinder Singh -- https://www.youtube.com/watch?v=pVmCI9zIMbc&list=PLmcBskOCOOFW1SNrz6_yzCEKGvh65wYb9

2. 

This is a sample readme file for our Github Example repo. We're learning Markdown.

* This is mean to be an example
* Markdown is really fast
* Pretty cool, right?

* Get license