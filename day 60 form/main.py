from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/login/<name>", methods=["POST"])
def receive_data(name):
    if name == "form1":
        data = request.form
        username = data['username']
        print(username)
        password = data['password']
        print(password)
        return render_template("new.html", username=username, password=password)


if __name__ == "__main__":
    app.run(debug=True)
