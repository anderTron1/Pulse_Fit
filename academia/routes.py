from academia import app
from flask import render_template, flash, request, redirect, url_for
from academia import db 
from academia.forms import CadastroPlano, CadastroCliente, CadastroCheckin
from academia.models import Plano, Cliente, Checkin


@app.route("/")
def page_home():
    return render_template("home.html")

@app.route("/checkin", methods=['GET', 'POST'])
def page_checkin():
    form_checkin = CadastroCheckin()

    if request.method == 'POST':
        if form_checkin.validate_on_submit():
            id = form_checkin.cliente_id.data
            cliente = Cliente.query.get(id)
            if cliente:
                novo_checkin = Checkin(
                    cliente_id=cliente.id,
                    dt_checkin=form_checkin.dt_checkin.data,
                    dt_checkout=form_checkin.dt_checkout.data
                )
                if novo_checkin.verificar_dia():
                    db.session.add(novo_checkin)
                    db.session.commit()
                    flash(f"Check-in realizado com sucesso para o cliente {cliente.nome}!", category="success")
                    return redirect(url_for("page_home"))
            else:
                flash("Cliente não encontrado.", category="danger")
    else:
        print("é um: ", request.method)
    return render_template("home.html", form_checkin=form_checkin)

@app.route("/registrar_plano", methods=['GET', 'POST'])
def page_registrar_plano():
    form_plano = CadastroPlano()

    if request.method == 'POST':
        if form_plano.validate_on_submit():
            plano = form_plano.plano.data
            novo_plano  = Plano(
                ativo = form_plano.ativo.data,
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
            plano.ativo = form.ativo.data
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

@app.route("/registro", methods=['GET', 'POST'])
def page_registro_cliente():
    form_cliente = CadastroCliente()

    if request.method == 'POST':
        if form_cliente.validate_on_submit():
            cliente = form_cliente.nome.data
            novo_cliente = Cliente(
                ativo = form_cliente.ativo.data,
                nome = form_cliente.nome.data,
                sobrenome = form_cliente.sobrenome.data,
                genero = form_cliente.genero.data,
                cpf = form_cliente.cpf.data,
                rg = form_cliente.rg.data,
                dt_nascimento = form_cliente.dt_nascimento.data,
                estado_civil = form_cliente.estado_civil.data,
                email = form_cliente.email.data,
                telefone = form_cliente.telefone.data,
                rua = form_cliente.rua.data,
                numero = form_cliente.numero.data,
                complemento = form_cliente.complemento.data,
                bairro = form_cliente.bairro.data,
                cidade = form_cliente.cidade.data,
                estado = form_cliente.estado.data,
                plano = form_cliente.plano.data,
            )    
            db.session.add(novo_cliente)
            db.session.commit()
            flash(f"Cliente {cliente} cadastrado com sucesso!", category="success")
        if form_cliente.errors:
            for err in form_cliente.errors:
                flash(f"Erro ao cadastrar o cliente: {err}", category="danger")
        return redirect(url_for("page_registro_cliente"))
        
    if request.method == "GET":
        with db.session.no_autoflush:
            planos = Plano.query.filter_by(ativo=True).all()
            clientes = Cliente.query.all()
        return render_template("cadastro_cliente.html", form_cliente=form_cliente, planos=planos, clientes=clientes)

@app.route("/editar-cliente/<int:cliente_id>", methods=['GET', 'POST'])
def editar_cliente(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    form_cliente = CadastroCliente(obj=cliente)

    if request.method == "POST":
        if "selecionar_plano" in request.form:
            return render_template("cadastro_cliente.html", form_cliente=form_cliente)

        if form_cliente.validate_on_submit() and not "deletar_plano" in request.form:
            cliente.ativo = form_cliente.ativo.data
            cliente.nome = form_cliente.nome.data
            cliente.sobrenome = form_cliente.sobrenome.data
            cliente.genero = form_cliente.genero.data
            cliente.cpf = form_cliente.cpf.data
            cliente.rg = form_cliente.rg.data
            cliente.dt_nascimento = form_cliente.dt_nascimento.data
            cliente.estado_civil = form_cliente.estado_civil.data
            cliente.email = form_cliente.email.data
            cliente.telefone = form_cliente.telefone.data
            cliente.rua = form_cliente.rua.data
            cliente.numero = form_cliente.numero.data
            cliente.complemento = form_cliente.complemento.data
            cliente.bairro = form_cliente.bairro.data
            cliente.cidade = form_cliente.cidade.data
            cliente.estado = form_cliente.estado.data
            cliente.plano = form_cliente.plano.data

            db.session.commit() 
            flash(f"Cliente {cliente.nome} atualizado com sucesso!", category="success")
            return redirect(url_for("page_registro_cliente"))
        elif "deletar_plano" in request.form:
            cliente_id = request.form.get("plano_id")

            print("Valor do id: ", cliente_id)
            cliente = Cliente.query.get(cliente_id)
            if cliente:
                db.session.delete(cliente)
                db.session.commit()
                flash(f"Cliente {cliente.nome} deletado com sucesso!", category="success")
            else:
                flash("Cliente não encontrado.", category="danger")
            return redirect(url_for("page_registro_cliente"))
        else:
            # Caso o formulário não seja válido, renderiza novamente o template com os erros
            flash("Erro ao atualizar o cliente. Verifique os dados e tente novamente.", category="danger")
            #return render_template("cadastro_cliente.html", form_cliente=form_cliente)

    with db.session.no_autoflush:
       planos = Plano.query.filter_by(ativo=True).all()
       clientes = Cliente.query.all()
    return render_template("cadastro_cliente.html", form_cliente=form_cliente, planos=planos, clientes=clientes, cliente_atual=cliente)


@app.route('/status_aluno')
def page_status_aluno():
    clientes = Cliente.query.all()
    return render_template("status_aluno.html", alunos=clientes)