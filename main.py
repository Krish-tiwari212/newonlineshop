from flask import Flask, render_template, redirect, request, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import json
from statistics import mean

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# ckeditor = CKEditor(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
# Bootstrap(app)
db = SQLAlchemy()
db.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('account'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    db.create_all()
    return render_template("index.html")

@app.route("/product-detail")
def product():
    return render_template('product_details.html')

@app.route("/products")
def all_products():
    return render_template('products.html')

@app.route("/accounts", methods=["GET","POST"])
def account():
    if request.method == "POST" and request.form.get('RegForm'):
        username = request.form["username"]
        email = request.form["email"]
        # if username == "" or email == "" or request.form.get("password") == "":
        #     return render_template('account.html', l=1, p=0)
        # if len(request.form.get("password")) < 8:
        #     return render_template('account.html', l=0, p=1)
        password = (generate_password_hash(request.form.get("password"), method='pbkdf2:sha256:260000',
                                           salt_length=8))[21:]
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect("/")
    if request.method == "POST" and request.form.get('LoginForm'):
        username = request.form["username"]
        password = request.form.get("password")
        meth = 'pbkdf2:sha256:260000$'
        o = User.query.filter_by(username=username).first()
        try:
            if o.username == username and check_password_hash(f"{meth}{o.password}", password):
                login_user(o)
                return redirect("/")
            else:
                return render_template("account.html", l=1)
        except AttributeError:
            return render_template("account.html", l=1)
    return render_template('account.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)