from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


db = SQLAlchemy()
migrate = Migrate()
login_inst = LoginManager()
mail = Mail()
