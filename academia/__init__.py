from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os 
from flask_mail import Mail, Message
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pulsefit.db"
#app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost:5432/pulsefit"
app.config["SECRET_KEY"] = "41eab096907f908050d3345f"

app.config['MAIL_SERVER']='smtp.elasticemail.com'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'pulsefit@pulsefit.com.br'
app.config['MAIL_PASSWORD'] = '10161DBB42C2D50742343FE42169D63119B8'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

url_CloudAMQP = "amqps://kgxhiwjq:oRUI4HrrhxfMYLKYjibDQPNQqe1HHg9S@jaragua.lmq.cloudamqp.com/kgxhiwjq"

#AQUI VAI AS CONFIGURAÇÕES PARA ENVIO DE EMAIL
HORA_ENVIO_RELATORIO = 23
MINUTOS_ENVIO_RELATORIO = 55
EMAIL_PARA_TESTE = 'andreluizpires1507@gmail.com'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from academia import routes

from academia import models

