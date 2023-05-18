from functools import wraps

import flask_login
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

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.TEXT)
    price = db.Column(db.String(100))
    image1 = db.Column(db.String(100))
    image2 = db.Column(db.String(100))
    image3 = db.Column(db.String(100))
    image4 = db.Column(db.String(100))
    image5 = db.Column(db.String(100))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('account'))

def admin_only(func):
    @wraps(func)
    def wrapper(*args, ** kwargs):
        if current_user.id == 1 or current_user.username == "useroperator1":
            return func(*args, ** kwargs)
        else:
            return redirect(url_for('unauthorized'))
    return wrapper

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    db.create_all()
    c = Product.query.all()
    return render_template("index.html",l=c,len=len(c))

@app.route("/product-detail/<num>")
def product(num):
    num = int(num)
    c = Product.query.filter_by(id=num).first()
    d = Product.query.all()
    return render_template('product_details.html',lis=c,l=d)

@app.route("/products")
def all_products():
    c = Product.query.all()
    return render_template('products.html',l=c,len=len(c))

@app.route("/accounts", methods=["GET","POST"])
def account():
    if request.method == "POST" and request.form.get('RegForm'):
        username = request.form["username"]
        email = request.form["email"]
        if username == "" or email == "" or request.form.get("password") == "":
            return render_template('account.html', l=1, p=0)
        if len(request.form.get("password")) < 8:
            return render_template('account.html', l=0, p=1)
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

@app.route('/add_product', methods=["GET","POST"])
@login_required
@admin_only
def add_product():
    if request.method=="POST":
        name = request.form.get("name")
        desc = request.form.get("description")
        price = request.form.get("price")
        img1 = request.form.get("image1")
        img2 = request.form.get("image2")
        img3 = request.form.get("image3")
        img4 = request.form.get("image4")
        img5 = request.form.get("image5")
        new_product = Product(name=name, description=desc,price=price,image1=img1,image2=img2,image3=img3,image4=img4,image5=img5)
        db.session.add(new_product)
        db.session.commit()
    return render_template('addproduct.html')

@app.route("/delete/<num>")
@login_required
@admin_only
def dele(num):
    c = db.session.query(Product).filter_by(id=int(num)).first()
    db.session.delete(c)
    db.session.commit()
    return redirect("/")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)