from tweepy import *
from time import time

consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = API(auth)

doesNotExistMessage = "[{u'message': u'Sorry, that page does not exist', u'code': 34}]"

def searchTwitter(screen_name, user_id):
    try:
        user = api.get_user(screen_name = screen_name, user_id = user_id)

        # The Twitter API gives precedence to screen_name over user_id.
        # However, we do not want that to happen to avoid erroneous
        # searches, so we need to check that the returned screen_name
        # and the returned user_id are the same as the ones inputted,
        # provided they were not None.

        if (screen_name and screen_name != user.screen_name) or \
           (user_id and user_id != user.id_str):
            raise TweepError(doesNotExistMessage)

        screen_name = user.screen_name
        user_id = user.id_str
        creation_date = user.created_at
        friend_count = user.friends_count
        follower_count = user.followers_count
        org_count = user.listed_count
        tweet_count = user.statuses_count
        favorites_count = user.favourites_count
        image_url = user.profile_image_url_https
        timestamp = time()
        
        return screen_name, user_id, creation_date, friend_count, follower_count, \
               org_count, tweet_count, favorites_count, image_url, timestamp
    
    except TweepError, TweepErrorMessage:
        return "Twitter was unable to process your request: " + str(TweepErrorMessage)
