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
from app.document.forms import UploadForm
from app.services.FileService import FileService
from app.errors.filesError import (
    FileAlreadyExistsError,
    FileInsertionError,
    FileNotExistsError
)

document = Blueprint('document', __name__, url_prefix='/document')


@document.route('/', methods=['GET', 'POST'])
@login_required
def list():
    files = FileService.get_user_files(user_id=current_user.id)
    return render_template('document/repository.html', files=files)

@document.route('/upload', methods=['POST'])
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        file = form.file.data
        try:
            FileService.create_file(file, user_id=current_user.id)
        except FileAlreadyExistsError as e:
            return f'File: {e.filename} already exists!', 400
        except FileInsertionError as e:
            return f'File: {e.filename} insertion failed!', 500
        else:
            return redirect(url_for('document.list'))

    return render_template('document/upload.html', form=form)

@document.route('/download/<file_name>', methods=['POST'])
@login_required
def download(file_name):
    try:
        file = FileService.get_file_from_disk(file_name)
    except FileNotExistsError as e:
        return f'File: {e.filename} does not exists!', 404
    return file

@document.route('/delete/<file_name>', methods=['POST', 'DELETE'])
@login_required
def delete(file_name):
    try:
        file = FileService.get_file_by_title(file_name)
    except FileNotExistsError as e:
        return f'File: {e.filename} does not exists!', 404

    FileService.delete_file(file)
    
    return redirect(url_for('document.list'))