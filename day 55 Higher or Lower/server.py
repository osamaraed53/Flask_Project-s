from flask import Flask
from random import randint

app = Flask(__name__)

choice = randint(1,9)

@app.route("/")
def home():
    return '<h1>Guess a number between 0 and 9</h1>'\
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" width="480" height="480"/>'


@app.route("/<num>")
def guess(num):
    if int(num) > choice:
        return '<h1 style="color: Yellow">Too high, try again!</h1>' \
                '<img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif"/>'
    if int(num) < choice:
        return '<h1 style="color: Gray">Too low, try again!</h1>' \
                '<img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif"/>'
    else:
        return '<h1 style="color: Green">You Found me!</h1>' \
                '<img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif"/>'


if __name__ == '__main__':
    app.run(debug=True)

