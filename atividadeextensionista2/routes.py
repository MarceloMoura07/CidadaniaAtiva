from flask import render_template, redirect, url_for, flash, request, abort
from atividadeextensionista2 import app, database, bcrypt
from atividadeextensionista2.forms import FormLogin, FormCriarConta, FormCriarProblema
from atividadeextensionista2.models import Usuario, Problema
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
def home():
    problemas = Problema.query.order_by(Problema.id.desc()).all()
    return render_template('home.html', problemas=problemas)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash('Login realizado com sucesso!', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('E-mail ou senha incorretos.', 'alert-danger')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        novo_usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha_cript
        )
        database.session.add(novo_usuario)
        database.session.commit()
        flash('Conta criada com sucesso! Faça login.', 'alert-success')
        return redirect(url_for('login'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'alert-success')
    return redirect(url_for('home'))


@app.route('/problema/criar', methods=['GET', 'POST'])
@login_required
def criar_problema():
    form = FormCriarProblema()
    if form.validate_on_submit():
        novo_problema = Problema(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            endereco=form.endereco.data,
            autor=current_user
        )
        database.session.add(novo_problema)
        database.session.commit()
        flash('Problema registrado com sucesso!', 'alert-success')
        return redirect(url_for('home'))

    return render_template('criar_problema.html', form=form)


@app.route('/problema/<int:id>')
def exibir_problema(id):
    problema = Problema.query.get_or_404(id)
    return render_template('problema.html', problema=problema)
