from pprint import pprint

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
import requests


ENDPOINT = "https://api.themoviedb.org/3/search/movie?include_adult=true&language=en-US&page=1'"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# create database
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top_movies-database.db"
db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Float, nullable=False)
    review = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String(), nullable=False)


# with app.app_context():
# db.create_all() I don't need after run once time
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )

# db.session.add(second_movie)
# db.session.commit()


# my own method to check if rating accept
# def check_rating(field):
#     value = float(field.data)
#     if not (0 <= value <= 10):
#         raise ValidationError("The value must be between 0 and 10.")

# create form to update rating and description
class editForm(FlaskForm):
    rating = StringField(label="Your Rating Out of 10 e.g 7.5", validators=[DataRequired()])
    review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField('Done')


class addForm(FlaskForm):
    new_movie = StringField(label="Movie Title")
    submit = SubmitField(label="Add Movie")


@app.route("/")
def home():
    movies = db.session.query(Movie).order_by(desc(Movie.rating)).all()
    return render_template("index.html", movies=movies)


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    form = editForm()
    movie_id = request.args.get("id")
    movie = db.get_or_404(Movie, movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        movies = db.session.query(Movie).order_by(desc(Movie.rating)).all()
        for i,j in enumerate(movies):
            j.ranking = int(i)+1
            db.session.commit()

        db.session.commit()

        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route('/delete')
def delete():
    movie_id = request.args.get("id")
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect('/')


all_suggested_movie = []


@app.route('/add', methods=["POST", "GET"])
def add():
    form = addForm()
    if form.validate_on_submit():
        global all_suggested_movie
        search_about = str(form.new_movie.data).replace(' ', '+')
        parameters = {
            "query": search_about,
            "include_adult": "true",
            "language": "en-US",
            "page": 1
        }
        headers = {
            "accept": "application / json",
            "API_key": "2c128161b8e56625cc520452b1a3fb8e",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyYzEyODE2MWI4ZTU2NjI1Y2M1MjA0NTJiMWEzZmI4ZSIsInN1YiI6IjY0ZTA0MjBjYTNiNWU2MDFkODc1MjY3ZiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ypVbrHVWcxMQ8ckjxR-epl3K1cMrirOMrNaiSLHiM3U"

        }

        response = requests.get(url=ENDPOINT, headers=headers, params=parameters)
        all_suggested_movie = response.json()["results"]
        pprint(all_suggested_movie)
        return render_template('select.html', suggested_movie=all_suggested_movie)
    return render_template('add.html', form=form)

pprint(all_suggested_movie)
@app.route("/add/0")
def add_after():
    movie_id = request.args.get("id")
    data = {}
    global all_suggested_movie
    print("len(all_suggested_movie)",len(all_suggested_movie))
    for item in all_suggested_movie:
        if int(item["id"]) == int(movie_id):
            data = item
        else:
            print("i am not find any thing")
    pprint(data)
    new_movie = Movie(
        title=data["title"],
        year=data["release_date"].split("-")[0],
        img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
        description=data["overview"],
        review="you need edit",
        ranking=0,
        rating=0.

    )
    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for("edit_rating", id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
