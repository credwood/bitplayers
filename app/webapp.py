from flask import Blueprint, current_app, redirect, render_template
from flask import request, url_for, send_from_directory
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from flask_admin import Admin, BaseView, expose

from app.extensions import db, login_inst
from app.forms import LoginForm, RegistrationForm, NewPost, ContactForm
from app.models import User, Blog, Contact

server_bp = Blueprint('main', __name__)

@server_bp.route('/')
@server_bp.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    if page:
        posts = Blog.query.order_by(Blog.blog_publushed.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
        prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
        return render_template('index.html', title='Home',
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)
    else:
        render_template('indexalt.html', title='Home')

@server_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            error = 'Invalid username or password'
            return render_template('login.html', form=form, error=error)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)

@login_inst.user_loader
def load_user(id):
    return User.query.get(id)

@server_bp.route('/logout/')
@login_required
def logout():
    logout_user()

    return redirect(url_for('main.index'))


@server_bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        email = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.login'))

    return render_template('register.html', title='Register', form=form)

@server_bp.route('/adminblog/', methods=['GET', 'POST'])
def adminblog():
    if current_user.role=='Administrator':
        form = NewPost()
        if request.method == "POST":
            new_blog = Blog(blog_title=request.form['title'], blog_content=request.form['text'], blog_slug=request.form['slug'], blog_author=request.form['author'])
            db.session.add(new_blog)
            db.session.commit()
            return render_template("index.html")
        elif request.method == "GET":
            return render_template("adminblog.html", form=form)


@server_bp.route('/')
@server_bp.route('/<slug>/', methods=['GET', 'POST'])
def single_slug(slug):
    content = Blog.query.filter_by(blog_slug=slug).first()
    if content:
        return render_template('posts.html', form=content)
    else:
        return render_template('index.html')

@server_bp.route('/contact/', methods=('GET', 'POST'))
def contact():
    form = ContactForm()
    if request.method == "POST":
        new_message = Contact(name=request.form['name'], message=request.form['body'], email=request.form['email'])
        db.session.add(new_message)
        db.session.commit()
        return render_template("success.html")
    elif request.method == "GET":
        return render_template("contact.html", form=form)

@server_bp.route('/success/', methods=('GET', 'POST'))
def success():
    return render_template('success.html')

@server_bp.route('/about/', methods=('GET', 'POST'))
def about():
    return render_template('about.html')
