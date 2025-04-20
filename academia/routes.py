from academia import app
from flask import render_template, flash
from academia import db 
from academia.forms import CadastroPlano
from academia.models import Plano


@app.route("/")
def page_home():
    return render_template("home.html")

@app.route("/registrar_plano", methods=['GET', 'POST'])
def page_registrar_plano():
    form_plano = CadastroPlano()

    if form_plano.validate_on_submit():
        plano = form_plano.plano.data
        novo_plano  = Plano(
            plano = plano,
            preco = Plano.formatar_preco_para_db(form_plano.preco.data),
            categoria = form_plano.categoria.data,
            descricao = ";".join(form_plano.descricao.data)
        )    
        db.session.add(novo_plano)
        db.session.commit()

        flash(f"Plano {plano} cadastrado com sucesso!", category="success")
    if form_plano.errors:
        for err in form_plano.errors:
            flash(f"Erro ao cadastrar o plano: {err}", category="danger")

    return render_template("registrar_plano.html", form_plano=form_plano)