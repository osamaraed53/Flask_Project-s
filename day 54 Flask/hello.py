from flask import Flask
app = Flask(__name__)

def make_bolds(function):
    def wrapper():
        return "<h1 style='text-align: center'><b>" + function() +"</b></h1>"
    return wrapper

@app.route('/')
@make_bolds
def hello_world():
    return 'Hello, World!'


if __name__ == "__main__":
    app.run(debug=True )