import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView


from config import BaseConfig

csrf = CSRFProtect()

def create_app():
    from app.models import Blog, User, MyModelView, Contact
    from app.extensions import db

    server = Flask(__name__)
    server.config.from_object(BaseConfig)
    csrf.init_app(server)
    csrf._exempt_views.add('dash.dash.dispatch')

    admin = Admin(server)
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Blog, db.session))
    admin.add_view(MyModelView(Contact, db.session))

    register_dashapps(server)
    #register_dashapps_table(server)
    register_extensions(server)
    register_blueprints(server)

    return server

def register_dashapps(app):
    from app.dashapp1.layout import layout
    from app.dashapp1.callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp1 = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/dashboard/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport])

    with app.app_context():
        dashapp1.title = 'Dashapp 1'
        dashapp1.layout = layout
        register_callbacks(dashapp1)

    #_protect_dashviews(dashapp1)

def register_dashapps_table(app):
    from app.dashapp_table.layout import layout
    from app.dashapp_table.callbacks import register_callbacks_table

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp_table = dash.Dash(__name__,
                         server=app,
                         url_base_pathname='/tweettable/',
                         assets_folder=get_root_path(__name__) + '/tweettable/assets/',
                         meta_tags=[meta_viewport])

    with app.app_context():
        dashapp_table.title = 'Dashapp table'
        dashapp_table.layout = layout
        register_callbacks_table(dashapp_table)

    #_protect_dashviews(dashapp_table)

def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import db
    from app.extensions import login_inst
    from app.extensions import migrate
    from app.extensions import mail


    db.init_app(server)
    login_inst.init_app(server)
    login_inst.login_view = 'main.login'
    migrate.init_app(server, db)
    mail.init_app(server)



def register_blueprints(server):
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
