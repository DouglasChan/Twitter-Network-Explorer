import sys
from collections import Counter
import json

#This file was used in the Mining Twitter with Python Tutorial Series by Sukhvinder Singh (Primarily video no. *).
#Specifically, this client helps us connect to the Twitter API using Tweepy.
#This file interacts with *

def get_mentions(tweet):
    entities = tweet.get('entities', {})
    hashtags = entities.get('user_mentions', [])
    return [tag['screen_name'] for tag in hashtags]
        
def twitter_mentioning(fname):
    with open(fname, 'r') as f:
        users = Counter()
        for line in f:
            tweet = json.loads(line)
            mentions_in_tweet = get_mentions(tweet)
            users.update(mentions_in_tweet)
        
        common_list = []
        for user, count in users.most_common(100):
            print("{}: {}".format(user, count))
            common_list.append(tuple((user,count)))
            
    return common_list
        
if __name__ == '__main__':
    fname = sys.argv[1]
    
    twitter_mentioning(fname)