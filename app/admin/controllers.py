from app.services.Logger import Event, EventType, Logger

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
from app.auth.models import User

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
            user = User.query.filter_by(email=unquote(search)).first()
            logs = Logger.get_logs_for_user(unquote(search))
            if not user:
                flash('No User Found', 'danger')

            return render_template("admin/dashboard.html", user=user, logs=logs, performingSearch=True)
        else:
            return render_template("admin/dashboard.html", user=None, logs=[], performingSearch=False)
    else:
        return redirect(url_for('main.home'))
