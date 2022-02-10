import os
from app import db
# from app.document.controllers import upload
from app.document.models import File
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from hashlib import sha256
from app.services.UserService import UserService
from config import BASE_DIR
from flask import send_from_directory

from app.errors.filesError import (
    FileAlreadyExistsError,
    FileInsertionError,
    FileNotExistsError,
    FileDeletionError
)

class FileService:
    @classmethod
    def get_user_files(cls, user_id: int):
        files = db.session.query(File).filter_by(owner_id=user_id).order_by(
            File.created_at.desc()
        )
        return files

    @classmethod
    def create_file(cls, uploaded_file: FileStorage, user_id: int):
        filename = secure_filename(uploaded_file.filename)
        if db.session.query(File).filter_by(owner_id=user_id, title=filename).first() is not None:
            raise FileAlreadyExistsError(filename)
        blob = uploaded_file.read()
        # FileStorage class (which is the class to handle uploaded file in Flask)
        # points to end of file after every action (saving or reading).
        uploaded_file.stream.seek(0)
        size = len(blob)
        f_hash = sha256(blob).hexdigest()

        try:
            cls.__save_file_db(f_hash, filename, size, user_id)
        except Exception as e:
            # st.logger.exception(e)
            raise FileInsertionError(filename)
        else:
            cls.__save_file_disk(uploaded_file, filename)
            db.session.commit()

    @classmethod
    def __save_file_db(cls, f_hash: str, filename: str, size: int, user_id: int):
        file = File(title=filename, file_size=size,
                    file_hash=f_hash, owner_id=user_id)
        db.session.add(file)

    @classmethod
    def __get_upload_dir(cls):
        email = UserService.get_current_user_email()

        upload_folder = os.path.join(BASE_DIR + '/app/uploads/', email + '/')

        if os.path.exists(upload_folder) and os.path.isdir(upload_folder):
            return upload_folder
        else:
            try:
                os.mkdir(upload_folder)
            except FileExistsError:
                pass

    @classmethod
    def __save_file_disk(cls, file: FileStorage, filename: str):
        path = os.path.join(cls.__get_upload_dir(), filename)
        file.save(path)
        return path

    @classmethod
    def get_file_from_disk(cls, filename):
        if not os.path.exists(os.path.join(cls.__get_upload_dir(), filename)):
            raise FileNotExistsError(filename=filename)
        return send_from_directory(directory=cls.__get_upload_dir(), path=filename, as_attachment=True)

    @classmethod
    def get_file_by_title(cls, filename: str):
        file = db.session.query(File).filter_by(title=filename).first()
        if file is None:
            raise FileNotExistsError(filename)
        return file

    @classmethod
    def delete_file(cls, file: File):
        try:
            db.session.delete(file)
        except Exception as e:
            # st.logger.exception(e)
            raise FileDeletionError(file.title)
        else:
            os.remove(os.path.join(cls.__get_upload_dir(), file.title))
        db.session.commit()
    
    @classmethod
    def get_file_path(cls, filename: str):
        file_path = os.path.join(cls.__get_upload_dir(), filename)
        if not os.path.exists(file_path):
            raise FileNotExistsError(filename=filename)
        return file_path
