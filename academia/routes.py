from academia import app
from flask import render_template, flash, request, redirect, url_for
from academia import db 
from academia.forms import CadastroPlano
from academia.models import Plano


@app.route("/")
def page_home():
    return render_template("home.html")

@app.route("/registrar_plano", methods=['GET', 'POST'])
def page_registrar_plano():
    form_plano = CadastroPlano()

    if request.method == 'POST':
        if form_plano.validate_on_submit():
            plano = form_plano.plano.data
            novo_plano  = Plano(
                plano = plano,
                preco = form_plano.preco.data,
                categoria = form_plano.categoria.data,
                descricao = ";".join(form_plano.descricao.data)
            )    
            db.session.add(novo_plano)
            db.session.commit()
            flash(f"Plano {plano} cadastrado com sucesso!", category="success")
        if form_plano.errors:
            for err in form_plano.errors:
                flash(f"Erro ao cadastrar o plano: {err}", category="danger")
        return redirect(url_for("page_registrar_plano"))
    if request.method == "GET":
        planos = Plano.query.all()
       
        return render_template("registrar_plano.html", form_plano=form_plano, planos=planos)

@app.route("/editar-plano/<int:plano_id>", methods=['GET', 'POST'])
def editar_plano(plano_id):
    plano = Plano.query.get_or_404(plano_id)
    if plano.descricao:
        plano.descricao = plano.descricao.split(";")
    form = CadastroPlano(obj=plano)
    
    if request.method == 'POST':
        if form.validate_on_submit():
            plano.plano = form.plano.data
            plano.preco = form.preco.data
            plano.categoria = form.categoria.data
            plano.descricao = ";".join(form.descricao.data) 
            db.session.commit() 
            flash(f"Plano {plano.plano} atualizado com sucesso!", category="success")
            return redirect(url_for("page_registrar_plano"))

    with db.session.no_autoflush:
        planos = Plano.query.all()
    return render_template("registrar_plano.html", form_plano=form, plano_atual=plano, planos=planos)

@app.route('/deletar-plano', methods=['POST'])
def deletar_plano():
    plano_id = request.form.get('plano_id')
    
    plano = Plano.query.get(plano_id)
    if plano:
        db.session.delete(plano)
        db.session.commit()
        flash(f"Plano {plano.plano} deletado com sucesso!", category="success")
    else:
        flash("Plano não encontrado.", category="danger")
    
    return redirect(url_for('page_registrar_plano'))