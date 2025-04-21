from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectMultipleField, SelectField, BooleanField, DateField
from wtforms.validators import DataRequired 
from wtforms.validators import ValidationError, Email

class CadastroPlano(FlaskForm):
    ativo = BooleanField(label="Ativo", default=True)
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

class CadastroCliente(FlaskForm):
    ativo = BooleanField(label="Ativo", default=True)
    nome = StringField(label="Nome", validators=[DataRequired()])
    sobrenome = StringField(label="Sobrenome", validators=[DataRequired()])
    genero = SelectField(label="Gênero", 
        choices=[
            ("M", "Masculino"),
            ("F", "Feminino"),
            ("O", "Outro"),
        ], validators=[DataRequired()]
    )
    cpf = StringField(label="CPF", validators=[DataRequired()])
    rg = StringField(label="RG", validators=[DataRequired()])
    dt_nascimento = DateField(label="Data de Nascimento", 
                              format="%Y-%m-%d",
                              render_kw={"placeholder": "YYYY-MM-DD"},
                              validators=[DataRequired()])
    estado_civil = SelectField(label="Estado Civil", 
        choices=[
            ("Solteiro", "Solteiro"),
            ("Casado", "Casado"),
            ("Divorciado", "Divorciado"),
            ("Viúvo", "Viúvo"),
        ], validators=[DataRequired()]
    )
    email = StringField(label="Email", validators=[Email(),DataRequired()])
    telefone = StringField(label="Telefone", validators=[DataRequired()])
    rua = StringField(label="Rua", validators=[DataRequired()])
    numero = StringField(label="Número", validators=[DataRequired()])
    complemento = StringField(label="Complemento")
    bairro = StringField(label="Bairro", validators=[DataRequired()])
    cidade = StringField(label="Cidade", validators=[DataRequired()])
    estado = StringField(label="Estado", validators=[DataRequired()])

    id = StringField(label="Código do Cliente")

    plano = StringField(label="Plano", validators=[DataRequired()])
    submit = SubmitField("Salvar Cliente")

    def validate_cpf(self, cpf):
        if not self.cpf.data.isdigit() or len(self.cpf.data) != 11:
            raise ValidationError("CPF deve conter apenas números e ter 11 dígitos.")
        
