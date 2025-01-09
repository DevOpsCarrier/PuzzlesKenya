import functools
from flask import Blueprint, g, request, redirect, session, url_for, flash, render_template
from werkzeug.security import check_password_hash, generate_password_hash

from puzzleske.db import get_db

# Define blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    :Register users to the site
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'

        if error is None:
            try:
                db.execute(
                    """INSERT INTO users (username, password, email)
                        VALUES (?, ?, ?)""", (username, generate_password_hash(password), email)
                )
                db.commit()
            except db.IntegrityError:
                error = f'Username is already taken.'
            else:
                return redirect(url_for('auth.login'))
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        users = db.execute(
            """SELECT * FROM users WHERE username=?""", (username,)
        ).fetchone()

        if users is None:
            error = 'Check your username.'
        elif not check_password_hash(users['password'], password):
            error = 'Check your password'

        if error is None:
            session.clear()
            session['user_id'] = users['id']
            return redirect(url_for('index.home'))
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """
    : check if user is logged in and logs them
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            """SELECT * FROM users WHERE id=?""", (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    """
    : log out user
    """
    session.clear()
    return redirect(url_for('index.home'))


def login_required(view):
    """
    : A decorator to ensure a user is logged in
    """

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        else:
            return view(**kwargs)

    return wrapped_view
