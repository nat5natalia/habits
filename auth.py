import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash

from a import db

from models import User, Habit

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html', title='Вход')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['pass']

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Нет почты с таким паролем')
        return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('regestration.html', title='Регистрация', create='Регистрация')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    re_pass = request.form['repass']

    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database
    user2 = User.query.filter_by(
        name=name).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Почта уже используется')
        return redirect(url_for('auth.signup'))
    elif user2:
        flash('Имя уже занято')
        return redirect(url_for('auth.signup'))
    if password == re_pass:
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), count=0, habit=1)
    else:
        flash('Разные пароли')
        return redirect(url_for('auth.signup'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/newhabit')
@login_required
def habit():
    return render_template('new_habit.html', title='Новая привычка')


@auth.route('/newhabit', methods=['POST'])
@login_required
def habited():
    name = request.form['name']
    allday = int(request.form['num'])
    new_habit = Habit(name=name, allday=allday, nowday=0, data=datetime.datetime.now())
    db.session.add(new_habit)
    db.session.commit()
    habitid = db.session.execute(f"""SELECT habit.id FROM habit WHERE habit.name = '{name}'""").fetchone()
    edit_habit = db.session.execute(text(f"""UPDATE user SET habit = {habitid[0]} WHERE name = '{current_user.name}'""").execution_options(autocommit=True))
    db.session.commit()

    return redirect(url_for('main.habit'))


