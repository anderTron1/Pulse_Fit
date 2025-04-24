from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os 
from flask_mail import Mail, Message
app = Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pulsefit.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost:5432/pulsefit"
app.config["SECRET_KEY"] = "41eab096907f908050d3345f"

app.config['MAIL_SERVER']='smtp.elasticemail.com'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'pulsefit@pulsefit.com.br'
app.config['MAIL_PASSWORD'] = '10161DBB42C2D50742343FE42169D63119B8'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

from academia import routes

from academia import models

