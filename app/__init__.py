from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from app.models import Usuario
    return Usuario.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        from .models import Usuario, Produto, SaidaProduto
        from .routes import bp as routes_bp
        app.register_blueprint(routes_bp)
        db.create_all()
        return app