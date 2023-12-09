from pprint import pprint

from flask import Flask, render_template, request
import requests
import smtplib

my_email ="osamaraed53.study@gmail.com"
password = "sxadfhwdmoyknwiv"

endpoint = "https://api.npoint.io/c790b4d5cab58020d391"
response = requests.get(endpoint)
data = response.json()

app = Flask(__name__)


@app.route("/")
def get_all_posts():
    return render_template("index.html", data=data)


@app.route("/about")
def get_about():
    return render_template("about.html")


@app.route("/post/<id>")
def get_post(id):
    print(id)
    return render_template("post.html", data=data[int(id)])


@app.route("/contact", methods=["GET", "POST"])
def get_contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        send_email(name=data["name"],email=data["email"],phone=data["phone"],message=data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(**kwargs):
    email_message = f"Subject:New Message\n\nName: {kwargs.get('name')}\nEmail: {kwargs.get('email')}\nPhone: {kwargs.get('phone')}\nMessage:{kwargs.get('message')}"
    email_message_bytes = email_message.encode('utf-8')
    print(type(email_message_bytes))
    print(type(email_message))
    with smtplib.SMTP("smtp.gmail.com",587) as con:
        con.starttls()
        con.login(user=my_email, password=password)
        con.sendmail(from_addr=my_email, to_addrs="osamaraed53@gmail.com", msg=email_message_bytes)

if __name__ == "__main__":
    app.run(debug=True)