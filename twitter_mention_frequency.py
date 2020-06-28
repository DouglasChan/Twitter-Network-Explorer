import sys
from collections import Counter
import json

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
            users.update(mentions_in_tweet) #For each mention of a user with the "@" symbol, the counter is updated.
        
        common_list = []
        for user, count in users.most_common(150): #This parameter cites the 100 most mentioned users in someone's network. This can be tweaked without running up against the Tweepy limit
            print("{}: {}".format(user, count))
            common_list.append(tuple((user,count)))
            
    return common_list
        
if __name__ == '__main__':
    fname = sys.argv[1]
    
    twitter_mentioning(fname)