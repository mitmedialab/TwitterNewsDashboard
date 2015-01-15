from flask import Flask, g, render_template, request
from pymongo import MongoClient

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

        if not search_params:
            matches = 'Empty'
            matches_count = None
            
        else:
            matches = g.posts.find(search_params)
            matches_count = matches.count()
            
        return render_template('resultsPage.html', matches = matches, count = matches_count)
    
if __name__ == '__main__':
    app.run()
