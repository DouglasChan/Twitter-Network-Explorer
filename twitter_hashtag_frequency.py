import sys
from collections import Counter
import json

#This file was used in the Mining Twitter with Python Tutorial Series by Sukhvinder Singh (Primarily video no. 14/28).
#Specifically, this client helps us connect to the Twitter API using Tweepy.
#This file interacts with *

def get_hashtags(tweet):
    entities = tweet.get('entities', {}) #* Talk about how this works
    hashtags = entities.get('hashtags', [])
    return [tag['text'].lower() for tag in hashtags]
    
if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as f:
        hashtags = Counter()
        for line in f:
            tweet = json.loads(line)
            hashtags_in_tweet = get_hashtags(tweet)
            hashtags.update(hashtags_in_tweet)
        for tag, count in hashtags.most_common(20): #Takes the most 20 frequent hashtags for a given user...
            print("{}: {}".format(tag,count))