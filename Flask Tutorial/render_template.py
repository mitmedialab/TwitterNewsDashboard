from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def greet_visitor():
    return "Hello! Welcome to My Webpage!"

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name = None):
    return render_template('hello.html', name = name) # will search in the
                                                      # templates folder for
                                                      # the appropriate HTML
                                                      # document

if __name__ == '__main__':
    app.run()
