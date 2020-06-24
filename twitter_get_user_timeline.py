import sys
import json
from tweepy import Cursor
from twitter_client import get_twitter_client

#This file was used in the Mining Twitter with Python Tutorial Series by Sukhvinder Singh (Primarily video no. 15/28).
#This file interacts with *

def getting_timeline(user):
    client = get_twitter_client() #Seems to be the rate limiting step...
    
    fname = "user_timeline_{}.jsonl".format(user)
    
    with open(fname, 'w') as f:
        for page in Cursor(client.user_timeline, screen_name = user, count = 200).pages(16): #Up to 3200 Tweets (Twitter limit?*)
            counter = 0
            for status in page: 
                if counter % 4 == 0: #Tried collecting smaller subsections of Tweets. 
                    f.write(json.dumps(status._json)+"\n")
                    counter += 1
                else:
                    counter += 1

if __name__ == "__main__":
    user = sys.argv[1]
    getting_timeline(user)
    
#Here I tried adding logic with counters so that every nth status in page
#Or every nth page in the Cursor
#Would dump the json data to the file. 
#While this successfully reduced the size of the file,
#It did not decrease the runtime for acquiring the raw data.
#This may have to do with the fact that reinitializing the Twitter client for each user
#May be the rate limiting step.

#In the future,
#Could try customizing it so multiple users' data are collected within one client?
#In other words, Knowing that I could collect 100 people's data within 20 seconds, with 16 tweets each. 
#Would need to figure out the minimum number of tweets that doesn't muck around with the similarity.
#In previous tests, ~ 400 / 3200 isn't terrible. 