from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy
from flask_migrate import Migrate
import locale
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message

# Tenta definir o locale para Português do Brasil.
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    print("Locale pt_BR.UTF-8 não suportado, usando o padrão do sistema.")

# Inicializa o app
app = Flask(__name__)

load_dotenv()

# Segurança
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')

# # Email
# app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
# app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

# Configurações do Flask-Mail
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

# Banco (SQLite local, arquivo na pasta do pacote)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'cidadania.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

# Apenas imprime status, não recria banco
if not inspector.has_table("usuario"):
    print("Banco ainda não inicializado. Rode 'flask db init/migrate/upgrade'.")
else:
    print("Base de dados já existente")


# Migrações (opcional, mas recomendado)
migrate = Migrate(app, database)

# Importa as rotas no final, após o app estar configurado
from atividadeextensionista2 import routes
