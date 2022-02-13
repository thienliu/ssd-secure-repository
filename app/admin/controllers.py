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
    if current_user.is_authenticated and current_user.isAdmin:
        search = request.args.get('search_term')

        if search:
            Logger.logEvent(message="Search for " + '`' + search + '`', type=EventType.EVENT)
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
def delete(email):
    try:
        user = UserService.get_user_by_email(email)
    except UserNotExistError as e:
        return f'User: {e.user_email} does not exists!', 404
    
    UserService.delete_user(user)
    Logger.delete_logs_for_user(email)

    return redirect(url_for('admin.home'))
        