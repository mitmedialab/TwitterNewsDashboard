from flask import Flask, g, render_template, request
from twitterSearchEngine import searchTwitter
from pymongo import MongoClient
from time import time

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    client = MongoClient()

    db = client['twitterData']
    posts = db.posts
    
    return client, posts

@app.before_request
def mongo_connect():
    g.client, g.posts = connect_db()
    
@app.teardown_request
def mongo_disconnect(exception):
    client = getattr(g, 'client', None)

    if client is not None:
        client.close()

@app.route('/')
def welcome():
    return render_template('welcomePage.html')

@app.route('/results', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_params = {}
        
        if request.form['username']:
            search_params['Username'] = request.form['username']

        if request.form['ID']:
            search_params['User ID'] = request.form['ID']

        err_message = None
        
        if not search_params:
            match = 'Empty'
            
        else:
            timestamp = time()
            match = g.posts.find(search_params)

            try:
                match = match.next()

            except:
                match = None
                
            if not match or (timestamp - match['Timestamp'] >= 3600):
                screen_name = search_params.get('Username')
                user_id = search_params.get('User ID')

                result = searchTwitter(screen_name, user_id)

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
                             'Timestamp'             : result[8]}
                    
                    g.posts.update({'Username' : result[0],
                                    'User ID'  : result[1]},
                                   match, upsert = True)
                
        return render_template('resultsPage.html', match = match, err_message = err_message)
    
if __name__ == '__main__':
    app.run()
