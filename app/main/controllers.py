from flask import ( 
    Blueprint, 
    redirect, 
    url_for 
)

from flask_login import login_required, current_user

main = Blueprint('main', __name__, url_prefix='/main')

# A main route to navigate user to the proper route when opening the app
@main.route('/', methods=['GET'])
@login_required
def home():
    if current_user.is_authenticated:
        if current_user.isAdmin:
            return redirect(url_for('admin.home'))
        else:
            return redirect(url_for('document.list'))
