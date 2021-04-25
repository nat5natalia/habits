from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import select, text, table, column
from werkzeug.utils import redirect

from a import db
from models import Habit

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/start')
def index():
    return render_template('start_page.html', title='Добро пожаловать', registred=current_user.is_authenticated)


@main.route('/profile')
@login_required
def profile():
    return render_template('my_page.html', username=current_user.name,
                           email=current_user.email,
                           now=False if current_user.habit == 1 else True, copr=str(current_user.count),
                           title='Профиль', registred=True)


@main.route('/habit')
@login_required
def habit():
    a = int(current_user.habit)
    r = db.session.execute(f"""SELECT habit.name, habit.nowday, habit.allday FROM habit JOIN user ON habit.id = 
    user.habit WHERE habit.id = {a}""").fetchone()
    return render_template('my_habit.html',
                           countyes=str(r[1]), countno=str(r[2] - r[1]), name=r[0],
                           title='Моя привычка', registred=True)


@main.route('/okk')
def okk():
    day = db.session.execute(f"""SELECT habit.nowday, habit.allday, habit.data FROM habit WHERE habit.id = {current_user.habit}""").fetchall()
    today = datetime.now().date()
    # if today - data > timedelta(day=1):
    nowday = day[0][0]
    allday = day[0][1]
    if allday - nowday > 0:
        a = db.session.execute(
            text(f"""UPDATE habit SET nowday = {nowday + 1}, data = {today} WHERE id = {current_user.habit}""").execution_options(
                autocommit=True))
        print(today)
    else:
        a = db.session.execute(
            text(f"""UPDATE user SET habit = 1, count = {current_user.count + 1}  WHERE name = '{current_user.name}'""").execution_options(
                autocommit=True))
    db.session.commit()
    return redirect(url_for('main.habit'))



@main.route('/top')
def top():
    userlist = db.session.execute(f"""SELECT user.name, user.count FROM user ORDER BY user.count DESC""").fetchall()
    print(userlist)
    return render_template('top.html', userlist=userlist,
                           title='Рейтинг', registred=current_user.is_authenticated)
