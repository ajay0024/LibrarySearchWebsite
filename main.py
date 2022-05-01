import json
from flask import Flask, render_template, redirect, url_for, flash, request, abort
from libgen_api import LibgenSearch
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
# from flask_gravatar import Gravatar
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mySecretIsOpen'
# app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

##CONNECT TO DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
uri = os.environ.get("DATABASE_URL", "sqlite:///library.db")  # or other relevant config var
print("MYDATABASE", uri)
if uri.startswith("postgres://"):
    print(uri)
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
# Following has been added as special case for Pythonanywhere
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://ajay24:v6bLKAqzEyjyHRx@ajay24.mysql.pythonanywhere-services.com/ajay24$library"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.context_processor
def inject_now():
    return {'year': date.today().year}


# gravatar = Gravatar(app,
#                     size=100,
#                     rating='g',
#                     default='retro',
#                     force_default=False,
#                     force_lower=False,
#                     use_ssl=False,
#                     base_url=None)


##CONFIGURE TABLES

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    username = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    country = db.Column(db.String(250), nullable=False)


db.create_all()


def admin_only(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.id != 1:
            return abort(403)
        return func(*args, **kwargs)

    return decorated_function


@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    print(current_user)
    return render_template("index.html", user=current_user)


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        print(request.values)
        if request.values.get("type") == "register":
            if User.query.filter_by(email=request.values.get("email")).first():
                flash("Email already registered. Please login instead")
                return redirect(url_for("login"))
            if User.query.filter_by(username=request.values.get("username")).first():
                flash("Username already registered. Please use a different username.")
                return redirect(url_for("login"))
            else:
                generated_password = generate_password_hash(request.values.get("password"), method="pbkdf2:sha256",
                                                            salt_length=8)
                new_user = User(
                    email=request.values.get("email"),
                    password=generated_password,
                    name=request.values.get("name"),
                    username=request.values.get("username"),
                    country=request.values.get("country")
                )
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
        elif request.values.get("type") == "login":
            print("trying login")
            username = request.values.get("username")
            password = request.values.get("password")
            print(username, password)
            user = User.query.filter_by(username=username).first()
            if not user:
                flash("That username does not exist in our database, please try again or register.")
                return redirect(url_for("login"))
            elif not check_password_hash(user.password, password):
                flash('Password incorrect, please try again.')
                return redirect(url_for("login"))
            else:
                login_user(user)
        return redirect(url_for("home"))
    return render_template("login.html")


@app.route('/search_book', methods=["GET"])
def search_book():
    if request.method == 'GET':
        s = LibgenSearch()
        filters = {}
        if request.args.get('year') != "":
            filters["Year"] = request.args.get('year')
        # if request.args.get('language') != "":
        #     filters["Language"] = request.args.get('language')
        if len(request.args.get('search-keyword')) > 3:
            keyword = request.args.get('search-keyword')
            # Search Title if title selected
            if request.args.get('search-option') == 'title':
                results = s.search_title_filtered(keyword, filters, exact_match=True)
            # Search Author if author selected
            elif request.args.get('search-option') == 'author':
                results = s.search_author_filtered(keyword, filters, exact_match=True)
            for result in results:
                result["links"] = s.resolve_download_links(result)
            js_str = json.dumps(results)
            return js_str
        else:
            return None
    return render_template("login.html")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.route("/about")
# def about():
#     return render_template("about.html")
#
#
# @app.route("/contact")
# def contact():
#     return render_template("contact.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
