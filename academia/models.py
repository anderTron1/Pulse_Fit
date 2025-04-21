from academia import db 
from datetime import datetime
from flask import flash

class Plano(db.Model):
    __tablename__ = "plano"
    id = db.Column(db.Integer, primary_key=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    dtcadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    plano = db.Column(db.String(50), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Plano {self.nome}>"
    
class Cliente(db.Model):
    __tablename__ = "cliente"
    id = db.Column(db.Integer, primary_key=True)
    ativo = db.Column(db.Boolean, default=True, nullable=False)
    dtcadastro = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    genero = db.Column(db.String(1), nullable=False)
    cpf = db.Column(db.Integer, nullable=False, unique=True)
    rg = db.Column(db.Integer, nullable=False, unique=True)
    dt_nascimento = db.Column(db.DateTime, nullable=False)
    estado_civil = db.Column(db.String(20), nullable=False)

    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.Integer, nullable=False)

    rua = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.Integer)
    complemento = db.Column(db.String(100))
    bairro = db.Column(db.String(50), nullable=False)
    cidade = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), nullable=False)

    plano = db.Column(db.Integer, db.ForeignKey("plano.id",   name="fk_cliente_plano"))

class Checkin(db.Model):
    __tablename__ = "checkin"
    id = db.Column(db.Integer, primary_key=True)
    dt_checkin = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    dt_checkout = db.Column(db.DateTime, nullable=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id",  name="fk_checkin_cliente"))
    
    def verificar_dia(self):
        if self.dt_checkin > self.dt_checkout:
            flash("Data e hora de check-in não pode ser maior que a data e hora de check-out.", "danger")
            return False
        elif self.dt_checkin > datetime.utcnow() or self.dt_checkout > datetime.utcnow():
            flash("Data de check-in e check-out não podem ser maiores que a data atual.", "danger")
            return False
        else:
            return True