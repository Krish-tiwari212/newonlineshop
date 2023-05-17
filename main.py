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
# app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# ckeditor = CKEditor(app)
# login_manager = LoginManager()= "strong"
# Bootstrap(app)
# db = SQLAlchemy()
# db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)