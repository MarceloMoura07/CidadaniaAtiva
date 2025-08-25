from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField,
    BooleanField, TextAreaField
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.file import FileField, FileAllowed

from atividadeextensionista2.models import Usuario


# ========== Formulário de Login ==========

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_dados = BooleanField('Lembrar login')
    botao_submit_login = SubmitField('Entrar')


# ========== Formulário de Criação de Conta ==========

class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20)])
    confirmacao_senha = PasswordField('Confirme a senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar conta')

# ========== Formulário de Recuperação de Senha ==========

# Solicitar reset de senha
# class FormSolicitarReset(FlaskForm):
#     email = StringField('E-mail', validators=[DataRequired(), Email()])
#     botao_submit = SubmitField('Enviar link de recuperação')
#
#     # def validate_email(self, email):
#     #     usuario = Usuario.query.filter_by(email=email.data).first()
#     #     if usuario is None:
#     #         raise ValidationError('Não existe conta com esse e-mail. Cadastre-se primeiro.')
#
#
# # Redefinir senha
# class FormResetarSenha(FlaskForm):
#     senha = PasswordField('Nova Senha', validators=[DataRequired(), Length(6, 20)])
#     confirmacao_senha = PasswordField('Confirme a Senha', validators=[DataRequired(), EqualTo('senha')])
#     botao_submit = SubmitField('Redefinir senha')
#
#

# ========== Formulário de Criação de Problema Urbano ==========

class FormCriarProblema(FlaskForm):
    titulo = StringField('Título do problema', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição detalhada', validators=[DataRequired()])
    endereco = StringField('Endereço do problema', validators=[DataRequired()])
    imagem = FileField('Foto do problema', validators=[FileAllowed(['jpg', 'png'], 'Apenas imagens .jpg ou .png')])
    botao_submit = SubmitField('Registrar problema')


# ========== Formulário de Edição de Perfil ==========

# class FormEditarPerfil(FlaskForm):
#     username = StringField('Nome de usuário', validators=[DataRequired(), Length(min=3, max=20)])
#     email = StringField('E-mail', validators=[DataRequired(), Email()])
#     foto_perfil = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'], 'Apenas imagens .jpg ou .png')])
#     botao_submit = SubmitField('Salvar alterações')

