from flask_bootstrap import Bootstrap5
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, Email




class Loginform(FlaskForm):
    email = EmailField(label="Email", validators=[DataRequired(), Email(message="Invalid email address")])
    password = PasswordField(label="password",
                             validators=[DataRequired(), Length(min=0, max=10)])
    submit = SubmitField(label="log in")


app = Flask(__name__)


bootstap = Bootstrap5(app)

app.secret_key = "Osama112500"


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    login_form = Loginform()
    if login_form.validate_on_submit():
        if login_form.email.data == "admin@email.com" and login_form.password.data == "0":
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=login_form)



if __name__ == '__main__':
    app.run(debug=True)
