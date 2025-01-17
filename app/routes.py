# app/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Usuario, Produto, SaidaProduto
from app import db
from sqlalchemy.exc import IntegrityError

bp = Blueprint('routes', __name__)


@bp.route('/')
@login_required
def index():
    todos_produtos = Produto.query.order_by(Produto.id).all()
    return render_template('dashboard.html', todos_produtos=todos_produtos)

@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')    
        password = request.form.get('password')
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('routes.index'))
        else:
            flash('Usuário ou senha inválidos!')
    return render_template('login.html')

@bp.route('/registrar/', methods=['GET', 'POST'])
@login_required
def registrar_usuario_comum():
    if current_user.nivel_funcao != 'administrador':
        abort(403)

    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if len(password) < 8:
            flash('A senha deve ter no mínimo 8 caracteres!', 'danger')
            return redirect(url_for('routes.registrar_usuario_comum'))
        
        if password != confirm_password:
            flash('As senhas não coincidem!', 'danger')
            return redirect(url_for('routes.registrar_usuario_comum'))

        # Verifica se o username já existe
        user = Usuario.query.filter_by(username=username).first()
        if user:
            flash('Usuário já existe!', 'danger')
            return redirect(url_for('routes.registrar_usuario_comum'))

        # Cria o novo usuário dentro de um bloco try-except
        try:
            password_hash = generate_password_hash(password)
            
            novo_usuario = Usuario(username=username, password=password_hash, email=email, confirm_password=password_hash)
            db.session.add(novo_usuario)
            db.session.commit()
            flash('Usuário registrado com sucesso!', 'success')
            return redirect(url_for('routes.index'))
        except IntegrityError:
            db.session.rollback()  # Reverte qualquer alteração pendente
            flash('Erro: O nome de usuário ou email já existe!', 'danger')
            return redirect(url_for('routes.registrar_usuario_comum'))

    return render_template('registrar.html')

@bp.route('/listar_usuarios/', methods=['GET', 'POST'])
@login_required
def listar_usuarios():
    if current_user.nivel_funcao != 'administrador':
        abort(403)
    try:
        todos_usuarios = Usuario.query.all()
    except:
        return "<h1> Não existem usuarios cadastrados  </h1>"
        
    return render_template('listar_usuarios.html', todos_usuarios=todos_usuarios)

@bp.route('/editar_usuario_comum/<int:usuario_id>/', methods=['GET', 'POST'])
@login_required
def editar_usuario_comum(usuario_id):
    if current_user.nivel_funcao != 'administrador':
        abort(403)
    
    usuario = Usuario.query.get(usuario_id)
    if request.method == 'POST':
        usuario.username = request.form.get('username')
        usuario.email = request.form.get('email')
        usuario.nivel_funcao = request.form.get('nivel_funcao')
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('routes.listar_usuarios'))
    return render_template('editar_usuario.html', usuario=usuario)

@bp.route('/deletar_usuario_comum/<int:usuario_id>/', methods=['POST'])
@login_required
def deletar_usuario_comum(usuario_id):
    if current_user.nivel_funcao != 'administrador':
        abort(403)
    
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuário deletado com sucesso!', 'success')
    return redirect(url_for('routes.index'))
    

@bp.route('/logout/', methods=['GET', 'POST'])
@login_required
def logout():
    if request.method == 'POST':
        logout_user()
        flash('Você foi desconectado com sucesso!', 'success')
        return redirect(url_for('routes.login'))
    

@bp.route('/cadastrar_produto/', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    if current_user.nivel_funcao != 'administrador':
        abort(403)
    
    if request.method == 'POST':
        nome = request.form.get('nome')    
        quantidade = request.form.get('quantidade')
        minimo_estoque = request.form.get('minimo_estoque')
        preco_unitario = request.form.get('preco_unitario')
        
        novo_produto = Produto(nome=nome, quantidade=quantidade, minimo_estoque=minimo_estoque, preco_unitario=preco_unitario)
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso!', 'success')
        return redirect(url_for('routes.cadastrar_produto'))
    return render_template('cadastrar_produtos.html')

@bp.route('/editar_produto/<int:produto_id>/', methods=['GET', 'POST'])
@login_required
def editar_produto(produto_id):
    if current_user.nivel_funcao != 'administrador':
        abort(403)

    produto = Produto.query.get(produto_id)
    if request.method == 'POST':
        produto.nome = request.form.get('nome')
        produto.quantidade = request.form.get('quantidade')
        produto.minimo_estoque = request.form.get('minimo_estoque')
        produto.preco_unitario = request.form.get('preco_unitario')
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
    return render_template('editar_produto.html', produto=produto)


@bp.route('/deletar_produto/<int:produto_id>/', methods=['POST'])
@login_required
def deletar_produto(produto_id):
    if current_user.nivel_funcao != 'administrador':
        abort(403)
    
    produto = Produto.query.get_or_404(produto_id) 
    db.session.delete(produto)
    db.session.commit()
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('routes.index'))


@bp.route('/saida_produto/<int:produto_id>/', methods=['GET', 'POST'])
@login_required
def saida_produto(produto_id):
    if current_user.nivel_funcao != 'administrador':
        abort(403)
    
    produto = Produto.query.get(produto_id)
    if request.method == 'POST':
        quantidade = int(request.form.get('quantidade'))
        motivo = request.form.get('motivo')
        if produto.quantidade < quantidade:
            flash('Quantidade indisponível no estoque!', 'danger')
            return redirect(url_for('routes.saida_produto', produto_id=produto_id))
        
        produto.quantidade -= quantidade
        produto_saida = SaidaProduto(produto_id=produto_id, quantidade=quantidade, motivo=motivo)
        db.session.add(produto_saida)
        db.session.commit()
        flash('Saída de produto registrada com sucesso!', 'success')
        return redirect(url_for('routes.index'))
    return render_template('saida_produto.html', produto=produto)

@bp.errorhandler(403)
def forbidden_error(error):
    return render_template('403.html', message="Acesso negado. Apenas administradores podem acessar essa página "), 403

@bp.errorhandler(401)
def unauthorized_error(error):
    return render_template('401.html', message="Acesso negado. Faça login para acessar esta página!"), 401

@bp.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', message="Página não encontrada!"), 404