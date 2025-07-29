from atividadeextensionista2 import database, login_manager
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')

    problemas = database.relationship('Problema', backref='autor', lazy=True)
    validacoes = database.relationship('Validacao', backref='usuario', lazy=True)

class Problema(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.Text, nullable=False)
    endereco = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, default=datetime.datetime.utcnow)
    status = database.Column(database.String, default='ativo')  # ativo ou resolvido
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    validacoes = database.relationship('Validacao', backref='problema', lazy=True)

class Validacao(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    tipo = database.Column(database.String, nullable=False)  # "existe" ou "nao_existe"
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_problema = database.Column(database.Integer, database.ForeignKey('problema.id'), nullable=False)
