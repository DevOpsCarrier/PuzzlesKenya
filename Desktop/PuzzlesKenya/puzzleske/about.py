from flask import Blueprint, Flask, render_template


bp = Blueprint('about', __name__)

@bp.route('/about', methods=('GET', 'POST'))
def about():
    return render_template('about.html')

@bp.route('/construction', methods=('GET',))
def construction():
    return render_template('construction.html')