from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os 

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pulsefit.db"
app.config["SECRET_KEY"] = "41eab096907f908050d3345f"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from academia import routes

from academia import models

