from app.services.Logger import Event

from flask import (
    Blueprint,
    redirect,
    render_template,
    url_for
)

from app import authorize, db

from flask_login import login_required, current_user

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
        # logs = db.session.query(Event).filter_by(user_email=current_user)
        logs = Event.query.all()
        return render_template("admin/dashboard.html", logs=logs)
    else:
        return redirect(url_for('main.home'))
