from atividadeextensionista2 import app, database
from atividadeextensionista2.models import Usuario, Problema, Validacao

with app.app_context():
    # Remove todas as tabelas (se já existir algum banco corrompido)
    database.drop_all()
    # Cria todas as tabelas de acordo com os models
    database.create_all()

print("Banco recriado com sucesso!")
