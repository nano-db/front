from nanodb_driver import Driver
from flask import Flask

app = Flask(__name__)
nano_db = Driver(port=5000)

from app import views
from app import endpoints