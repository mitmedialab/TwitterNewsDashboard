import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, \
url_for, abort, render_template, flash

# configuration
DATABASE = "tmp/flaskr.db"
DEBUG = True # allow users to execute code on the server
             # DO NOT allow this on a production server!
SECRET_KEY = "development key" # keeps client-side sessions secure
USERNAME = "admin"
PASSWORD = "default"

app = Flask(__name__)
app.config.from_object(__name__) # from_object() looks for the given object (imports if a string)
                                 # and looks for all uppercase variables defined, like the variables
                                 # defined above
                                 #
                                 # the alternative is to load the configuration from a configuration
                                 # file, such as 'FLASKR_SETTINGS' and then write instead:
                                 #
                                 # app.config.from_envvar('FLASKR_SETTINGS', silent = True)
                                 #
                                 # where 'silent' means that Flask should not complain if no such
                                 # environment key, 'FLASKR_SETTINGS,' has been set

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode = 'r') as f:
            db.cursor().executescript(f.read())

        db.commit()

# functions marked with before_request() are called BEFORE a request and are
# passed no arguments; similarly, functions marked with before_request() are
# called AFTER a request and are passed no arguments

@app.before_request
def before_request():
    g.db = connect_db()

# before_request and after_request may not be executed if there is an exception,
# so this is where teardown_request comes in to call functions after a response
# has been constructed; they are not allowed to modify the request and their
# return values are ignored; if an exception occurred, it is passed into each
# function; otherwise, None is passed in
#
# we use the special 'g' object that Flask provides, which stores informaton
# for one request one and is available from within each function; it does not
# store such things on other objects because this would fail when operating in
# threaded environments

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)

    if db is not None:
        db.close()

# the following function shows all the entries stored in the database,
# ordering with the most recent on top; rows returned from the cursor are
# tuples with columns as specified in the select statement; this is good
# enough for small apps but for larger ones, a dict might be preferred

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title = row[0], text = row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries = entries)

# the following function allows the user, if logged in, to add new entries; if
# everything works, flash() will be called to flash an information message for
# the next request and redirect back to the 'show_entries' page

@app.route('/add', methods = ['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    # question marks are used to avoid SQL injection, which is possible
    # when using string formatting to build SQL statements
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'

        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'

        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))

    return render_template('login.html', error = error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
