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

main = Blueprint('main', __name__, url_prefix='/main')

@main.route('/', methods=['GET', 'POST'])
def home():
    return render_template("main/home.html")