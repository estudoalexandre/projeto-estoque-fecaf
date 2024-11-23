# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user
from werkzeug.security import check_password_hash
from app.models import Usuario
from app import db
import time

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('dashboard.html')

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')    
        password = request.form.get('password')
        user = Usuario.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('routes.index'))
        else:
            flash('Usuário ou senha inválidos!')
    return render_template('login.html')

@bp.route('/registrar/', methods=['GET', 'POST'])
def registrar_usuario_comum():
    if current_user.nivel_funcao != 'administrador':
        flash('Acesso negado. Apenas administradores podem registrar novos usuários!', 'danger')
        return redirect(url_for('routes.index'))

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # Verifica se o username já existe
        user = Usuario.query.filter_by(username=username).first()
        if user:
            flash('Usuário já existe!', 'danger')
            return redirect(url_for('routes.registrar_usuario_comum'))

        # Cria o novo usuário dentro de um bloco try-except
        try:
            novo_usuario = Usuario(username=username, password=password, email=email, nivel_funcao='comum')
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário registrado com sucesso!', 'success')
            return redirect(url_for('routes.index'))
        except IntegrityError:
            db.session.rollback()  # Reverte qualquer alteração pendente
            flash('Erro: O nome de usuário ou email já existe!', 'danger')
            return redirect(url_for('routes.registrar_usuario_comum'))

    return render_template('registrar.html')


