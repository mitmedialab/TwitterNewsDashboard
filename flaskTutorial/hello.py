from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == '__main__':
    # app.run(host = None, port = None, debug = None, **options)
    #
    # host = '0.0.0.0' --> server becomes publically available
    # debug is a boolean saying whether or not the page should
    # reload itself after every change (debug = True); note this
    # can dangerous on production machines because it still allows
    # the execution of arbitrary code
    
    app.run()
    
