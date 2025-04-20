from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired 

class CadastroPlano(FlaskForm):
    plano = StringField(label="Nome do Plano", validators=[DataRequired()])
    preco = DecimalField(label="Preço do Plano", validators=[DataRequired()])
    
    categoria = SelectField(label="Categoria do Plano", 
        choices=[
            ("Mensal", "Mensal"),
            ("Trimestral", "Trimestral"),
            ("Semestral", "Semestral"),
            ("Anual", "Anual"),
        ], validators=[DataRequired()]
    )
    descricao = SelectMultipleField(label="Descrição do Plano",
        choices=[
            ("Acesso total à academia (segunda a sábado)", "Acesso total à academia (segunda a sábado)"),
            ("Aulas coletivas", "Aulas coletivas"),
            ("Personal trainer", "Personal trainer"),
            ("Avaliação física", "Avaliação física"),
            ("Camiseta Pulse Fit", "Camiseta Pulse Fit"),
        ], validators=[DataRequired()]
    )
    submit = SubmitField("Salvar Plano")
