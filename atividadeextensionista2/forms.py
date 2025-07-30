from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf.file import FileField, FileAllowed

# Formulário de login
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_dados = BooleanField('Lembrar login')
    botao_submit_login = SubmitField('Entrar')

# Formulário de cadastro
class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(3, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar conta')

# Formulário para criação de problema urbano (denúncia)
class FormCriarProblema(FlaskForm):
    titulo = StringField('Título do problema', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição detalhada', validators=[DataRequired()])
    endereco = StringField('Endereço do problema', validators=[DataRequired()])
    imagem = FileField('Foto do problema', validators=[FileAllowed(['jpg', 'png'])])
    botao_submit = SubmitField('Registrar problema')

# Formulário de edição de perfil
class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(3, 20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    botao_submit = SubmitField('Salvar alterações')
