import os
from flask import Blueprint, current_app, redirect, render_template, \
    request, flash, url_for
from werkzeug.utils import secure_filename

from puzzleske.db import get_db

bp = Blueprint('index', __name__)


@bp.route('/', methods=('GET', 'POST'))
def home():
    """
    :the index page operations
    """

    try:
        db = get_db()
        db_images = db.execute(
            """SELECT * FROM items"""
        ).fetchall()
    except Exception as e:
        flash(str(e))

    return render_template('index.html')


@bp.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def user_profile(user_id):
    """
    look at the user profile and or edit it
    : upload sale items to the site
    """
    return render_template('profile.html')


@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    """
    :Uploads images paths to the database and saves them to the file
    """
    if request.method == 'POST':
        if request.files:
            # get the image
            image = request.files['file']
            # save image to upload path
            image.save(os.path.join(current_app.config['UPLOAD_PATH'], secure_filename(image.filename)))
            filename = secure_filename(image.filename)
            description = request.form['description']
            quantity = request.form['quantity']
            price = request.form['price']

            try:
                # save filepath to the database
                db = get_db()
                db.execute(
                    """INSERT INTO items (image, description, quantity, price)
                        VALUES (?, ?, ?, ?)""", (filename, description, quantity, price,)
                )
                db.commit()
                return redirect(url_for('index.home'))
            except Exception as e:
                flash(e)

    return render_template('upload/upload.html')


@bp.route('/cart/<int:item_id>', methods=['POST', 'GET'])
def add_to_cart(item_id):
    """
    :Add items to the cart by id
    """
    db = get_db()
    # get item from items
    item = db.execute(
        """SELECT * FROM items WHERE id=?""", (item_id,)
    ).fetchone()
    image = item['image']
    quantity = item['quantity']
    price = item['price']
    description = item['description']
    try:
        db.execute(
            """INSERT INTO cart (image, name, quantity, price) VALUES (?, ?, ?, ?)""",
            (image, description, quantity, price,)
        )
        db.commit()
        flash('item added')
    except Exception as e:
        flash(e)
    return redirect(url_for('index.home'))


@bp.route('/cart', methods=['GET', 'POST'])
def cart():
    """
    :Holds the cart items
    """
    return render_template('cart/cart.html')


@bp.route('/remove/<int:item_id>', methods=['GET', 'POST'])
def remove_cart(item_id):
    """
    :Remove item from cart
    """
    try:
        db = get_db()
        db.execute(
            """DELETE FROM cart WHERE id=?""", (item_id,)
        )
        db.commit()
        flash('item deleted')
    except Exception as e:
        flash(e)

    return redirect(url_for('index.cart'))


@bp.route('/games')
def games():
    return render_template('games.html')


@bp.route('/Coaching')
def coaching():
    return render_template('coaching.html')
