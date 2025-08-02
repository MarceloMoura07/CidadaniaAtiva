from atividadeextensionista2 import database, login_manager
from flask_login import UserMixin
from datetime import datetime

# ========== Função de carregamento do usuário (para o Flask-Login) ==========

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


# ========== Modelo: Usuário ==========

class Usuario(database.Model, UserMixin):
    __tablename__ = 'usuario'

    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')

    # Relacionamentos
    problemas = database.relationship('Problema', backref='autor', lazy=True)
    validacoes = database.relationship('Validacao', backref='usuario', lazy=True)


# ========== Modelo: Problema ==========

class Problema(database.Model):
    __tablename__ = 'problema'

    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    descricao = database.Column(database.Text, nullable=False)
    endereco = database.Column(database.String, nullable=False)
    imagem = database.Column(database.String, default='sem_imagem.jpg')
    data_criacao = database.Column(database.DateTime, default=datetime.utcnow)
    status = database.Column(database.String, default='ativo')

    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    # Relacionamento com validações
    validacoes = database.relationship(
        'Validacao',
        backref='problema',
        lazy=True,
        cascade='all, delete-orphan'  # Remove as validações quando o problema é excluído
    )

    def contar_validacoes(self, tipo):
        """
        Conta quantas validações de um tipo específico ('existe' ou 'nao_existe') esse problema recebeu.
        """
        return len([v for v in self.validacoes if v.tipo == tipo])


# ========== Modelo: Validação ==========

class Validacao(database.Model):
    __tablename__ = 'validacao'

    id = database.Column(database.Integer, primary_key=True)
    tipo = database.Column(database.String, nullable=False)  # "existe" ou "nao_existe"

    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_problema = database.Column(database.Integer, database.ForeignKey('problema.id'), nullable=False)
