# Import flask dependencies
from flask import ( 
    Blueprint,
    current_app, 
    request, 
    render_template, 
    flash, 
    g, 
    session, 
    redirect, 
    url_for 
)

# Import password /encryption helper tools
# from flask_bcrypt import Bcrypt

# Import the database object from the main app module
from app import db, bcrypt, login_manager

from flask_login import login_user, current_user, logout_user, login_required, LoginManager

from app.auth.forms import LoginForm
from app.auth.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth')
app_config = current_app.config

# A user_loader callback, used to reload the user object
# from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.isAdmin:
            return redirect(url_for('admin.home'))
        else:
            return redirect(url_for('main.home'))

    form = LoginForm(request.form)
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            session.permanent = True
            return redirect(url_for('admin.home')) if user.isAdmin else redirect(url_for('main.home'))
            # next_page = request.args.get('next')
            # if next_page:
            #     return redirect(next_page)
            # else:
            #    return redirect(url_for('admin.dashboard')) if isAdmin() else redirect(url_for('main.home'))
        else:
            flash('Invalid credentials. Please try again!', 'danger')

    return render_template("auth/login.html", form=form)

@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/profile', methods=['GET'])
@login_required
def profile():
    if current_user.get_id() is not None:
        current_logged_in_user = User.query.filter_by(id=current_user.get_id()).first()
        return render_template('auth/profile.html', user=current_logged_in_user)
    else:
        return redirect(url_for('main.home'))
# def isAdmin():
#     if current_user.get_id() is not None:
#         current_logged_in_user = User.query.filter_by(
#             id=current_user.get_id()).first()
#         return current_logged_in_user.role == 1
#     else:
#         return False