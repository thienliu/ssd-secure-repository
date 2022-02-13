from app.services.FileService import FileService
from app.services.Logger import EventType, Logger

from flask import (
    Blueprint,
    redirect,
    render_template,
    url_for,
    request,
    flash
)

from urllib.parse import unquote
from flask_login import login_required, current_user
from app.services.UserService import UserService
from app.services.FileService import FileService
from app.errors.authErrors import UserNotExistError

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/', methods=['GET'])
@login_required

# This decorator could be enabled to notify users that they authorized to view this screen
# However, from the security perspective, this could potentially expose the protected resources,
# and the attackers may try different ways to break the protection.

#@authorize.has_role('admin')

# Thus, the manual check `is_authenticated`` and `isAdmin`` are used here
def home():

    # Only logged-in user with admin role can perform searching
    if current_user.is_authenticated and current_user.isAdmin:
        search = request.args.get('search_term')

        if search:
            Logger.logEvent(message="Search for " + '`' + search + '`', type=EventType.EVENT)

            # Find the user and their activity logs 
            # Using unquote to decode the url parameters
            # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.unquote
        
            user = UserService.get_user_by_email(unquote(search))
            logs = Logger.get_logs_for_user(unquote(search))

            if not user:
                flash('No User Found', 'danger')

            return render_template(
                "admin/dashboard.html", 
                user=user,
                logs=logs,
                performingSearch=True
            )
        else:
            return render_template(
                "admin/dashboard.html", 
                user=None, 
                logs=[], 
                performingSearch=False
            )
    else:
        return redirect(url_for('main.home'))

@admin.route('/delete/<email>', methods=['POST'])
@login_required
def delete(email):

     # Only logged-in user with admin role can perform user deletion
    if current_user.is_authenticated and current_user.isAdmin:
        try:
            # Firstly try to get the user associated with the provided email
            user = UserService.get_user_by_email(email)
        except UserNotExistError as e:

            # Raise an error if the user doesn't exists
            return f'User: {e.user_email} does not exists!', 404
        
        # Delete the user
        UserService.delete_user(user)

        # Delete the user's activity logs
        Logger.delete_logs_for_user(email)

        # Delete the user's files
        FileService.delete_all_files_for_user(user_id=user.id, email=user.email)

    return redirect(url_for('admin.home'))
        