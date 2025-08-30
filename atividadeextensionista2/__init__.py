from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import locale
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

# Tenta definir o locale para Português do Brasil
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    print("Locale pt_BR.UTF-8 não suportado, usando o padrão do sistema.")

# Inicializa o app
app = Flask(__name__)
load_dotenv(".env")

# Segurança
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')

# --- Banco ---
database_url = os.getenv(
    "DATABASE_URL",
    "sqlite:///banco_local.db"  # fallback local
)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa extensões
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'

# Migrações (para desenvolvimento local)
migrate = Migrate(app, database)

# Importa os models
from atividadeextensionista2 import models

# Cria tabelas se não existirem
with app.app_context():
    database.create_all()
    print("Tabelas criadas ou já existentes!")

# Rotas no final
from atividadeextensionista2 import routes
