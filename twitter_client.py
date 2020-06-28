import os, sys
from tweepy import API, OAuthHandler 

def get_twitter_auth():
    ''' Setup Twitter authentication.
    
    Return: tweety.OAuthHandler object    
    '''
    
    try:
        consumer_key = os.environ['TWITTER_CONSUMER_KEY'] #These 4 environment variables were set permanently within the User Variables on my Windows machine. 
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
        access_token = os.environ['TWITTER_ACCESS_TOKEN']
        access_secret = os.environ['TWITTER_ACCESS_SECRET']
    except KeyError:
        sys.stderr.write("TWITTER_* environment variables not set\n")
        sys.exit(1)
        
    auth = OAuthHandler(consumer_key, consumer_secret) #Authenticates using the developer user access tokens.
    auth.set_access_token(access_token, access_secret)
    return auth
    
def get_twitter_client():
    """Setup Twitter API client.
    
    Return : tweepy.API object
    """
    auth = get_twitter_auth()
    client = API(auth)
    return client