from flask import (
    Blueprint,
    render_template
)

from flask_login import login_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/', methods=['GET'])
@login_required
def home():
    return render_template("admin/dashboard.html")
