import dash
from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from dateutil import parser
import pytz
from pytz import timezone


from config import BaseConfig

csrf = CSRFProtect()

def create_app():
    from app.models import Blog, User, MyModelView, Contact
    from app.extensions import db
    from app.dashapp1.layout import layout as layout_1
    from app.dashapp1.callbacks import register_callbacks as register_callbacks_1
    #from app.dashapp2.layout import layout as layout_2
    #from app.dashapp2.callbacks import register_callbacks as register_callbacks_2
    from app.dashapp3.layout import layout as layout_3
    from app.dashapp3.callbacks import register_callbacks as register_callbacks_3

    server = Flask(__name__)
    server.config.from_object(BaseConfig)
    csrf.init_app(server)
    csrf._exempt_views.add('dash.dash.dispatch')

    admin = Admin(server)
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Blog, db.session))
    admin.add_view(MyModelView(Contact, db.session))

    register_dashapp(server, 'dashapp1', 'dashboard1', layout_1, register_callbacks_1)
    #register_dashapp(server, 'dashapp2', 'dashboard2', layout_2, register_callbacks_2)
    register_dashapp(server, 'dashapp3', 'dashboard3', layout_3, register_callbacks_3)
    register_extensions(server)
    register_blueprints(server)
    server.jinja_env.filters['formatdatetime'] = format_datetime

    return server

def format_datetime(date,fmt=None):
    western = timezone("America/Los_Angeles")
    native=pytz.utc.localize(date, is_dst=None).astimezone(western)
    #date = parser.parse(str(date))
    #native = date.astimezone(western)
    format='%m-%d-%Y %I:%M %p'
    return native.strftime(format)

def register_dashapp(app, title, base_pathname, layout, register_callbacks_fun):
    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    my_dashapp = dash.Dash(__name__,
                           server=app,
                           url_base_pathname=f'/{base_pathname}/',
                           assets_folder=get_root_path(__name__) + f'/{base_pathname}/assets/',
                           meta_tags=[meta_viewport])

    with app.app_context():
        my_dashapp.title = title
        my_dashapp.layout = layout
        register_callbacks_fun(my_dashapp)
    #_protect_dashviews(my_dashapp)

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
