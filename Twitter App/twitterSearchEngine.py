from tweepy import *
from time import time

consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth)

def searchTwitter(screen_name, user_id):
    try:
        user = api.get_user(screen_name = screen_name, user_id = user_id)

        screen_name = user.screen_name
        user_id = user.id_str
        creation_date = user.created_at
        friend_count = user.friends_count
        follower_count = user.followers_count
        org_count = user.listed_count
        tweet_count = user.statuses_count
        favorites_count = user.favourites_count
        timestamp = time()
        
        return screen_name, user_id, creation_date, friend_count, follower_count, \
               org_count, tweet_count, favorites_count, timestamp
    
    except TweepError, TweepErrorMessage:
        return "Twitter was unable to process your request: " + str(TweepErrorMessage)
