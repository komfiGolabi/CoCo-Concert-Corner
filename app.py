import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_concerts")
def get_concerts():
    concerts = list(mongo.db.concerts.find())
    return render_template("concerts.html", concerts=concerts)


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # invalid password match
                flash("OOPS, your password/username incorrect!")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("OOPS, your password/username incorrect!")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You logged out from your profile!")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/new_concert", methods=["GET", "POST"])
def new_concert():
    if request.method == "POST":
        user = mongo.db.users.find_one({"username": session["user"]})
        new_concert = {
            "artist": request.form.get("artist"),
            "city": request.form.get("city"),
            "country": request.form.get("country"),
            "venue": request.form.get("venue"),
            "genre": request.form.get("genre"),
            "concert_date": request.form.get("concert_date"),
            "description": request.form.get("description"),
            "url_image": request.form.get("url_image"),
            "user_id": ObjectId(user["_id"]),
        }

        mongo.db.concerts.insert_one(new_concert)
        flash("Event succesfully added!")
        return redirect(url_for("new_concert"))

    return render_template("new_concert.html")

    categories = mongo.db.concerts.find().sort("category", 1)
    return render_template("new_concert.html", categories=categories)


@app.route("/edit_concert/<concert_id>", methods=["GET", "POST"])
def edit_concert(concert_id):
    if request.method == "POST":
        user = mongo.db.users.find_one({"username": session["user"]})
        edit_concert = {
            "artist": request.form.get("artist"),
            "city": request.form.get("city"),
            "country": request.form.get("country"),
            "venue": request.form.get("venue"),
            "genre": request.form.getlist("genre"),
            "concert_date": request.form.get("concert_date"),
            "description": request.form.get("description"),
            "url_image": request.form.get("url_image"),
            "user_id": ObjectId(user["_id"]),
        }
        
        mongo.db.concerts.update({"_id": ObjectId(concert_id)}, edit_concert)
        flash("You succesfully edited your event!")

    event = mongo.db.concerts.find_one({"_id": ObjectId(concert_id)})
    categories = mongo.db.concerts.find().sort("category", 1)
    return render_template(
        "edit_concert.html", concert=event, categories=categories)


@app.route("/delete_concert/<concert_id>")
def delete_concert(concert_id):
    mongo.db.concerts.remove({"_id": ObjectId(concert_id)})
    flash("Task Successfully Deleted")
    return redirect(url_for("get_concerts"))


@app.route("/get_categories")
def get_categories():
    categories = list(mongo.db.categories.find().sort("genre", 1))
    return render_template("categories.html", categories=categories)


@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        genre = {
            "genre": request.form.get("genre")
        }
        mongo.db.categories.insert_one(genre)
        flash("New Genre Added")
        return redirect(url_for("get_categories"))

    return render_template("add_category.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
