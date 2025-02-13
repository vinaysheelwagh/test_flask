from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from app.models import User
from flask_login import login_required
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app import db

@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'Vinaysheel'}
    posts = [
        {
            'author' : 'Amar',
            'body' : 'I am a data scintist at Unitek.'
        },
        {
            'author' : 'Vishakha',
            'body' : ' I am a production engineer at Intel.'
        }
    ]
    return render_template('index.html', title='Home', posts = posts)
    #return 'Hello World!'

@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)





