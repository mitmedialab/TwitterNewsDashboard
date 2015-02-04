from flask import Flask
app = Flask(__name__)

@app.route('/')
def greet_visitor():
    return "Hello! Welcome to My Webpage!"

# by placing a trailing slash at the end,
# it allows people to redirect to this page
# if the trailing slash is omitted; this is
# similar to a file system
@app.route('/projects/')
def projects():
    return "The Project Page"

# by placing no trailing slash at the end,
# including a slash at the end will produce
# a 404 ("Not Found") error
@app.route('/about')
def about():
    return "The About Page"

if __name__ == '__main__':
    app.run()
