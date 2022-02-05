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
from app.document.forms import FileForm
from app.services.FileService import FileService
from app.errors.filesError import (
    FileAlreadyExistsError,
    FileInsertionError
)

document = Blueprint('document', __name__, url_prefix='/document')

@document.route('/', methods=['GET', 'POST'])
@login_required
def documents_home():
    form = FileForm()
    if form.validate_on_submit():
        file = form.file.data
        try:
            FileService.create_file(file, user_id=current_user.id)
        except FileAlreadyExistsError as e:
            return f'File: {e.filename} already exists!', 400
        except FileInsertionError as e:
            return f'File: {e.filename} insertion failed!', 500

    files = FileService.get_user_files(user_id=current_user.id)

    return render_template('document/repository.html', files=files, form=form)

@document.route('/action/<file_id>', methods=['POST'])
@login_required
def documents_action(file_id):    
    print('selected file:', file_id)
    return redirect(url_for('document.documents_home'))