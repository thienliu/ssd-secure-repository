from flask import ( 
    Blueprint, 
    request, 
    render_template, 
    flash, 
    g, 
    session, 
    redirect, 
    url_for 
)

from flask_login import login_required, current_user

main = Blueprint('main', __name__, url_prefix='/main')

@main.route('/', methods=['GET'])
@login_required
def home():
    if current_user.is_authenticated:
        if current_user.isAdmin:
            return redirect(url_for('admin.home'))
        else:
            return redirect(url_for('document.documents_home'))
