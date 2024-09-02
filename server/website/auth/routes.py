from website.auth import blueprint
from website.home import blueprint as home_blueprint
from flask import render_template, redirect, url_for, request, jsonify, current_app as app, flash
from website import db
from flask_login import login_user, logout_user, login_required, current_user
from website.auth.forms import LoginForm, ForgotPasswordForm
from website.auth.models import User
from website.auth.utils.loginUtils import verify_pass



@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_blueprint.index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and verify_pass(form.password.data, user.password):
            login_user(user)
            user.last_login_at = db.func.now()
            db.session.commit()
            flash(f'{user.username} logged in successfully', 'success')
            return redirect(url_for('home_blueprint.index'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('auth/login.html', form=form)

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html')

@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_blueprint.index'))

#TODO: Add profile page
# @blueprint.route('/profile')

@blueprint.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        print(f'Forgot password')
    return render_template('auth/forgot-password.html' , form=form)