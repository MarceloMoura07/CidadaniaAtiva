from flask import render_template, redirect, url_for, flash, request, abort
from atividadeextensionista2 import app, database, bcrypt
from atividadeextensionista2.forms import FormLogin, FormCriarConta, FormCriarProblema
from atividadeextensionista2.models import Usuario, Problema, Validacao
from flask_login import login_user, logout_user, current_user, login_required
import secrets
from PIL import Image
import os

# ========== Funções auxiliares ==========

def salvar_imagem_problema(imagem):
    nome_aleatorio = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome_aleatorio + extensao
    caminho = os.path.join(app.root_path, 'static/imagens_problemas', nome_arquivo)

    img = Image.open(imagem)
    img.thumbnail((800, 800))
    img.save(caminho)

    return nome_arquivo

# ========== Rotas principais ==========

@app.route('/')
def home():
    problemas = Problema.query.all()

    # Ordena por número de "existe" e depois por data mais recente
    problemas = sorted(
        problemas,
        key=lambda p: (p.contar_validacoes('existe'), p.data_criacao),
        reverse=True
    )

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

# ========== Páginas informativas ==========

@app.route('/contato')
def contato():
    return render_template('contato.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

# ========== Usuários ==========

@app.route('/usuarios')
def usuarios():
    todos_usuarios = Usuario.query.all()

    usuarios_com_post = [u for u in todos_usuarios if u.problemas]

    # Ordena pela última data de postagem (descendente)
    top_usuarios = sorted(
        usuarios_com_post,
        key=lambda u: max(p.data_criacao for p in u.problemas),
        reverse=True
    )[:5]

    total_cadastrados = len(todos_usuarios)

    return render_template("usuarios.html", top_usuarios=top_usuarios, total=total_cadastrados)

# ========== Problemas ==========

@app.route('/problema/criar', methods=['GET', 'POST'])
@login_required
def criar_problema():
    form = FormCriarProblema()

    if form.validate_on_submit():
        nome_imagem = 'sem_imagem.jpg'
        if form.imagem.data:
            nome_imagem = salvar_imagem_problema(form.imagem.data)

        novo_problema = Problema(
            titulo=form.titulo.data,
            descricao=form.descricao.data,
            endereco=form.endereco.data,
            imagem=nome_imagem,
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


@app.route('/problema/<int:id_problema>/validar/<tipo>', methods=['POST'])
@login_required
def validar_problema(id_problema, tipo):
    problema = Problema.query.get_or_404(id_problema)

    # Impede votos repetidos do mesmo tipo
    validacao_existente = Validacao.query.filter_by(
        id_usuario=current_user.id,
        id_problema=problema.id,
        tipo=tipo
    ).first()

    if validacao_existente:
        flash('Você já marcou essa opção.', 'alert-warning')
    else:
        nova_validacao = Validacao(
            id_usuario=current_user.id,
            id_problema=problema.id,
            tipo=tipo
        )
        database.session.add(nova_validacao)
        database.session.commit()

        # Remove problema se houver 3 negações
        if problema.contar_validacoes('nao_existe') >= 3:
            for v in problema.validacoes:
                database.session.delete(v)
            database.session.delete(problema)
            database.session.commit()
            flash('O problema foi removido após múltiplas negações.', 'alert-warning')
            return redirect(url_for('home'))

        flash('Obrigado por sua colaboração!', 'alert-success')

    return redirect(url_for('home'))

@app.route('/problema/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_problema(id):
    # lógica para edição
    pass

@app.route('/problema/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_problema(id):
    # lógica para exclusão com segurança
    pass



# ========== Relatório ==========

@app.route('/relatorio')
@login_required
def relatorio():
    problemas = Problema.query.filter_by(status='ativo').all()

    problemas_ordenados = sorted(
        problemas,
        key=lambda p: p.contar_validacoes('existe'),
        reverse=True
    )

    return render_template('relatorio.html', problemas=problemas_ordenados)
