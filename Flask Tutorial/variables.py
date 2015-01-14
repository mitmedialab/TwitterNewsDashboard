from flask import Flask
app = Flask(__name__)

@app.route('/')
def greet_visitor():
    return "Hello! Welcome to My Webpage!"

# can add variable parts to the URL by marking these
# special sections as <variable_name> so that they
# serve as keywords to the function
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return "User %s" % username

# can also add a converter to specify a rule for the
# type of variable being passed into the function
@app.route('/hello/<int:post_id>')
def show_post(post_id):
    # show the user profile for that user
    return "Post %d" % post_id

if __name__ == '__main__':
    app.run()
