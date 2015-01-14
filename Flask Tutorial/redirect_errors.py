from flask import abort, Flask, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401) # troll abort - redirects to a 401 page (denied access)
    print "If this prints, the abort function failed!"

if __name__ == '__main__':
    app.run()
