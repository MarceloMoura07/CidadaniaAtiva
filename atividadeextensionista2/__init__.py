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

# Flask-Mail
# mail = Mail(app)

# --- Banco: usa DATABASE_URL (Render) ou cai para SQLite local ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Pega a variável de ambiente
database_url = os.getenv("DATABASE_URL", "")  # string do Render, ex: postgres://...

# Se não houver DATABASE_URL, usa um SQLite local (arquivo dentro do projeto)
if not database_url:
    sqlite_path = os.path.join(BASE_DIR, "db.sqlite3")
    database_url = f"sqlite:///{sqlite_path}"
    # Opcional: cria a pasta se necessário (não estritamente necessário para o arquivo)
    # os.makedirs(os.path.dirname(sqlite_path), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

from atividadeextensionista2 import models


with app.app_context():
    inspector = sqlalchemy.inspect(database.engine)
    if not inspector.has_table("usuario"):
        print("Banco ainda não inicializado (tabelas não existem).")
    else:
        print("Base de dados já existente")

# Migrações
migrate = Migrate(app, database)

# Rotas no final
from atividadeextensionista2 import routes

