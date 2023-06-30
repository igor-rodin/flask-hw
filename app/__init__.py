from flask import Flask

app = Flask(__name__)

from app import routs
from app import routs_l2
from app import fake_data
from app.lesson_3 import routs
