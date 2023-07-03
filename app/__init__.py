from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config[
    "SECRET_KEY"
] = "P7gNZGcZJ$bf560b43e75678ed4976efd8437e80e709b83cf217e94bba95155b247cbcb1bd"
app.config["STUDENTS_FILE"] = "app/lesson_3/data/students.json"

db = SQLAlchemy(app)
csrf = CSRFProtect(app)


from app import routs
from app import routs_l2
from app import fake_data
from app import lesson_3
