from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy()
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False, unique=True)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = Book.query.all()
    return render_template("index.html", books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        book_name = request.form.get("book_name")
        book_author = request.form.get("book_author")
        book_rating = float(request.form.get("book_rating"))

        new_book = Book(title=book_name, author=book_author, rating=book_rating)
        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("add.html")


@app.route("/add/<id>", methods=['POST', 'GET'])
def edit_rating(id):
    if request.method == 'POST':
        book_id = request.form.get("id")
        new_rating = float(request.form.get("rating"))
        with app.app_context():
            book = Book.query.get_or_404(book_id)
            book.rating = new_rating
            db.session.commit()
            return redirect("/")
    with app.app_context():
        book = Book.query.get_or_404(id)

    return render_template("edit_rating.html", book=book)


@app.route('/delete_row')
def delete_row():
    id = request.args.get('id')
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
