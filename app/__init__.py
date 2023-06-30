from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
db = SQLAlchemy(app)

from app import routs
from app import routs_l2
from app import fake_data
from app import lesson_3
