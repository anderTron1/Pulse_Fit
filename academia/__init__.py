from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate




app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pulsefit.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from academia import routes

from academia import models

