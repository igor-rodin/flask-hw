from flask import Flask

app = Flask(__name__)

from app import routs
from app import fake_data
