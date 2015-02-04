from flask import Flask, url_for
app = Flask(__name__)

@app.route('/')
def greet_visitor():
    return "Hello! Welcome to My Webpage!"

@app.route('/index')
def index():
    return "This is nothing yet, but we're working on it!"

@app.route('/login')
def login():
    return "Just kidding! No need to login! :P"

@app.route('/user/<username>')
def profile(username):
    return "Hello, %s" % username

if __name__ == '__main__':
    with app.test_request_context(): # tells Flask to behave as though it
                                     # is handling a request, even though
                                     # we are interacting with it
                                     
        # url_for accepts the name of a function as the first argument,
        # with remaining arguments serving as keyword arguments; unknown
        # variables are appended to the URL as query parameters
        print url_for('index')
        print url_for('login')
        print url_for('login', next = '/')
        print url_for('profile', username = 'John Doe')
        
    app.run()
