# Import flask dependencies
from flask import ( 
    Blueprint,
    current_app, 
    request, 
    render_template, 
    flash, 
    session, 
    redirect, 
    url_for 
)

# Import the database object from the main app module
from app import bcrypt, login_manager
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from app.auth.forms import LoginForm
from app.auth.models import User
from app.services.Logger import EventType, Logger

auth = Blueprint('auth', __name__, url_prefix='/auth')
app_config = current_app.config

# A user_loader callback, used to reload the user object
# from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# A route to handle user login
# This route is reusable for both user and admin
# A better solution is to separate user and admin login into 2 different systems
# because we don't want to expose the admin system to the world outside

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

        # Validate the user hashed password rather than plain text
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            session.permanent = True
            Logger.logEvent(message="Logged In", type=EventType.EVENT)
            return redirect(url_for('admin.home')) if user.isAdmin else redirect(url_for('main.home'))
        else:
            Logger.logEvent(message="Invalid Credentials", type=EventType.ERROR)
            flash('Invalid credentials. Please try again!', 'danger')

    return render_template("auth/login.html", form=form)

# A route to handle user logout
@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    Logger.logEvent(message="Logged Out", type=EventType.EVENT)
    return redirect(url_for('main.home'))

# A route to handle user profile, currently this is share between an admin and an user
# Admin should have a separate system for security purpose
@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if current_user.get_id() is not None:
        user = User.query.filter_by(id=current_user.get_id()).first()

        Logger.logEvent(message="View Profile", type=EventType.EVENT)
        return render_template('auth/profile.html', user=user)
    else:
        Logger.logEvent(message="Failed to View Profile. Current login is invalid", type=EventType.EVENT)
        return redirect(url_for('main.home'))