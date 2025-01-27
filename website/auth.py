from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .user import create_user, get_user_by_email, verify_password

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = get_user_by_email(email)
        if user:
            if verify_password(user['password'], password):
                session['user_id'] = str(user['_id'])
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('User does not exist.', category='error')
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        success = create_user(email, password)
        if success:
            flash('User created! You can now log in.', category='success')
            return redirect(url_for('auth.login'))
        else:
            flash('User already exists.', category='error')
    return render_template('login.html', signup=True)

@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', category='info')
    return redirect(url_for('auth.login'))
