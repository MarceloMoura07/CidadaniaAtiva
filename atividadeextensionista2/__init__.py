from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy

# Inicializa o app
app = Flask(__name__)

# Chave secreta (usada para cookies e sessões)
app.config['SECRET_KEY'] = '955e2630c4ce08e0b7855eec624f38bc'  # gere com secrets.token_hex(16) se quiser trocar

# Banco de dados: usa PostgreSQL se a variável DATABASE_URL estiver definida, senão usa SQLite local
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividadeextensionista.db'

# Inicializa extensões
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # nome da função de login
login_manager.login_message_category = 'alert-info'  # categoria do flash de mensagem

# Criação automática das tabelas se o banco estiver vazio
from atividadeextensionista2 import models
engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
inspector = sqlalchemy.inspect(engine)

# Cria o banco se não existir a tabela principal
if not inspector.has_table("usuario"):
    with app.app_context():
        database.drop_all()
        database.create_all()
        print("Base de dados criada")
else:
    print("Base de dados já existente")

# Importa as rotas no final, após o app estar configurado
from atividadeextensionista2 import routes
