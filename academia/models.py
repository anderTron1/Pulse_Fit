from academia import db 
from datetime import datetime

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

    plano = db.Column(db.Integer, db.ForeignKey("plano.id",  ondelete="RESTRICT", name="fk_cliente_plano"))
