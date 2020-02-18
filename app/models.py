from flask_login import UserMixin, LoginManager
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_security import current_user, RoleMixin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from app.extensions import db
from flask_admin import expose

class MyModelView(ModelView):
    # Allow only admins to access the Admin views
    def is_accessible(self):
        if current_user.has_role('Administrator'):
            return True

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    email = db.Column(db.String(64))
    message = db.Column(db.Text)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def is_active(self):
        pass

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        # db is your database session.
        if self.role == role:
            return True
        return False

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blog_slug = db.Column(db.String(300))
    blog_title = db.Column(db.String(250))
    blog_author = db.Column(db.String(200))
    blog_publushed = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    blog_content = db.Column(db.Text)

    def __repr__(self):
        return '<Blog {}>'.format(self.blog_content)
    @staticmethod
    def slugify (target, value, oldvalue, initiator):
        if value and (not target.slug or value != oldvalue):
            target.slug = slugify(value)
        db.event.listen(Post.title, 'set', Post.slugify, retval=False)
