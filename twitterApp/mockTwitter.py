from tweepy import *
from pymongo import MongoClient
from datetime import datetime
from time import time

class MockTwitter:
    def __init__(self):
        self.client = MongoClient()

        twitterAPI = self.client['mockTwitterAPI']
        twitterData = self.client['mockTwitterData']

        self.postsTwitterAPI = twitterAPI.posts
        self.postsTwitterData = twitterData.posts

        self.initPosts()

    def initPosts(self):
        # clear all entries in both databases in case this module
        # has been used before (and therefore both these databases
        # would have already been created and saved)
        self.postsTwitterAPI.remove({})
        self.postsTwitterData.remove({})

        currentTime = time()
        
        dataTwitterAPI = [{'Username'              : 'user1',
                           'User ID'               : '1',
                           'Account Creation Date' : datetime(2014, 1, 1, 13, 31, 36),
                           'Friend Count'          : 5,
                           'Follower Count'        : 2,
                           'Tweet Count'           : 3,
                           'Favorites Count'       : 3,
                           'Organization Count'    : 1,
                           'Image URL'             : 'https://twitterUserImages.com/user1.png',
                           'Timestamp'             : currentTime},
                          {'Username'              : 'user2',
                           'User ID'               : '2',
                           'Account Creation Date' : datetime(2011, 2, 3, 10, 16, 25),
                           'Friend Count'          : 102,
                           'Follower Count'        : 63,
                           'Tweet Count'           : 205,
                           'Favorites Count'       : 12,
                           'Organization Count'    : 5,
                           'Image URL'             : 'https://twitterUserImages.com/user2.png',
                           'Timestamp'             : currentTime + 1},
                          {'Username'              : 'user3',
                           'User ID'               : '6',
                           'Account Creation Date' : datetime(2013, 5, 4, 22, 9, 47),
                           'Friend Count'          : 20,
                           'Follower Count'        : 11,
                           'Tweet Count'           : 48,
                           'Favorites Count'       : 7,
                           'Organization Count'    : 3,
                           'Image URL'             : 'https://twitterUserImages.com/user3.png',
                           'Timestamp'             : currentTime}]

        dataTwitterData = [{'Username'             : 'user2',
                           'User ID'               : '2',
                           'Account Creation Date' : datetime(2011, 2, 3, 10, 16, 25),
                           'Friend Count'          : 102,
                           'Follower Count'        : 63,
                           'Tweet Count'           : 205,
                           'Favorites Count'       : 12,
                           'Organization Count'    : 5,
                           'Image URL'             : 'https://twitterUserImages.com/user2.png',
                           'Timestamp'             : currentTime},
                           {'Username'             : 'user3',
                           'User ID'               : '6',
                           'Account Creation Date' : datetime(2013, 5, 4, 22, 9, 47),
                           'Friend Count'          : 19,
                           'Follower Count'        : 10,
                           'Tweet Count'           : 40,
                           'Favorites Count'       : 5,
                           'Organization Count'    : 2,
                           'Image URL'             : 'https://twitterUserImages.com/user3.png',
                           'Timestamp'             : currentTime - 4000}]

        for dataPoint in dataTwitterAPI:
            self.postsTwitterAPI.update({'Username' : dataPoint['Username'],
                                         'User ID'  : dataPoint['User ID']},
                                        dataPoint, upsert = True)
                                         
        for dataPoint in dataTwitterData:
            self.postsTwitterData.update({'Username' : dataPoint['Username'],
                                          'User ID'  : dataPoint['User ID']},
                                         dataPoint, upsert = True)
    
    def search(self, request):
        if request.method == 'POST':
            search_params = {}

            if request.form.get('username'):
                search_params['Username'] = request.form['username']

            if request.form.get('ID'):
                search_params['User ID'] = request.form['ID']

            err_message = None

            if not search_params:
                match = 'Empty'

            else:
                timestamp = time()
                match = self.postsTwitterData.find(search_params)

                try:
                    match = match.next()

                except:
                    match = None

                if not match or (timestamp - match['Timestamp'] >= 3600):
                    screen_name = search_params.get('Username')
                    user_id = search_params.get('User ID')

                    result = self.searchTwitter(screen_name = screen_name, user_id = user_id)

                    if type(result) == str:
                        match = None
                        err_message = result

                    else:
                        match = {'Username'              : result[0],
                                 'User ID'               : result[1],
                                 'Account Creation Date' : result[2],
                                 'Friend Count'          : result[3],
                                 'Follower Count'        : result[4],
                                 'Tweet Count'           : result[5],
                                 'Favorites Count'       : result[6],
                                 'Organization Count'    : result[7],
                                 'Image URL'             : result[8],
                                 'Timestamp'             : result[9]}

                        self.postsTwitterData.update({'Username' : result[0],
                                                      'User ID'  : result[1]},
                                                      match, upsert = True)

            return match
                
    def searchTwitter(self, screen_name = None, user_id = None):
        search_params = {}

        try:
            if screen_name:
                search_params['Username'] = screen_name

            if user_id:
                search_params['User ID'] = user_id

            if not search_params:
                return "Search fields are empty"

            result = self.postsTwitterAPI.find(search_params)
            match = result.next()

            return match['Username'], match['User ID'], \
                   match['Account Creation Date'], match['Friend Count'], \
                   match['Follower Count'], match['Tweet Count'], \
                   match['Favorites Count'], match['Organization Count'], \
                   match['Image URL'], match['Timestamp']

        except:
            return "Twitter was unable to process your request: [{u'message': u'Sorry, that page does not exist', u'code': 34}]"

class Request:
    def __init__(self, **kwargs):
        self.method = 'POST'
        self.form = {}
        
        self.form['username'] = kwargs.get('username')
        self.form['ID'] = kwargs.get('ID')
