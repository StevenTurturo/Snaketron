import os

from flask import (Flask, g, render_template, flash,jsonify, redirect,request, url_for)
from flask_bcrypt import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, login_user, logout_user, login_required,
                         current_user)
from flask_assets import Environment, Bundle


import old_models
import forms

app = Flask(__name__)
app.secret_key = '3a5s1df6a3sd85a3se1f5aw23e1f3s813as8e565a951ef3a861wea1'
app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('css/scss/styles.css.scss', filters='pyscss',
              depends='css/scss/*.scss',output='snaketron_styles.css')
assets.register('scss_all',scss)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return old_models.User.get(old_models.User.id == user_id)
    except old_models.DoesNotExist:
        return None


@app.before_request
def before_request():
    g.db = old_models.psql_db
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """ Close the database connection"""
    g.db.close()
    return response


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = forms.RegistrationForm()
        if form.validate_on_submit():
            flash('You have Successfully Registered!', 'success')
            old_models.User.create_user(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data
            )
            return redirect(url_for('home'))
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = forms.LoginForm()
        if form.validate_on_submit():
            try:
                user = old_models.User.get(old_models.User.username == form.username.data)
            except old_models.DoesNotExist:
                flash("Your username or password do not match our records",
                      "error")
            else:
                if check_password_hash(user.password, form.password.data):
                    login_user(user)
                    flash('You have successfully logged in!')
                    return redirect(url_for('home'))
                else:
                    flash("Your username or password do not match our records")
        return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!")
    return redirect( url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
@login_required
def home():
    return render_template('landing_page.html')

@app.route('/project')
@app.route('/project/<int:project_id>')
@login_required
def project(project_id=None):
    return render_template('project.html')


@app.route('/profile')
@app.route('/profile/<username>')
@login_required
def profile(username=None):
    return render_template('profile.html')

@app.route('/create_project',methods=['GET','POST'])
def create_project():
    if request.method == 'GET':
        form = forms.ProjectForm()
        return render_template('register.html',form=form)
    elif request.method == 'POST':
        try:
                old_models.Project.create_project(
                    title=request.form['title'],
                    description=-request.form['description'],
                    author_id=current_user.id
                )
                return jsonify({'status':'OK'})
        except ValueError as e:
            return jsonify(e)
    else:
        return 'DID NOT COMPUTE'

@app.route('/list_all_projects', methods=['GET','POST'])
@login_required
def all_projects():
    if request.method == 'GET':
        return render_template('projects.html')
    else:
        return 'DID NOT CREATE DATA!!!!'


@app.route('/project_one')
@login_required
def project_one():
    return render_template('project.html')


@app.route('/project_two')
@login_required
def project_two():
    return render_template('project2.html')

if __name__ == '__main__':
    old_models.initialize()
    try:
        old_models.User.create_user(
            username='athena',
            first_name='Athena',
            last_name='Turturo',
            email='athena@gmail.com',
            password='password',
            company_employee=True,
            company_manager=True
        )
    except ValueError as e:
        print(e)
    app.run()
