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
    
    def formatar_preco_para_db(valor_str):
        valor_str = valor_str.replace('R$', '').strip()

        valor_str = valor_str.replace('.', '')

        valor_str = valor_str.replace(',', '.')

        try:
            return float(valor_str)
        except ValueError:
            return None