import os
from app import db
from app.document.models import File
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from hashlib import sha256
from app.services.UserService import UserService
from config import BASE_DIR
from flask import send_from_directory
from flask_login import login_required

from app.errors.filesError import (
    FileAlreadyExistsError,
    FileInsertionError,
    FileNotExistsError,
    FileDeletionError
)

from app.services.Logger import EventType, Logger

class FileService:

    # Get all the associated files for a user, sort the file by created date in a descending order
    # Params:
    # - user_id: The id of the user to fetch the files for
    # Returns;
    # - all the available files for the user
    @classmethod
    @login_required
    def get_user_files(cls, user_id: int):
        files = db.session.query(File).filter_by(owner_id=user_id).order_by(
            File.created_at.desc()
        )
        Logger.logEvent(message="View Documents", type=EventType.EVENT)
        return files

    # Upload a file to the server and insert a record into the database
    # Params:
    # - uploaded_file: the file to be uploaded
    # - user_id: the user id who owns the file
    @classmethod
    @login_required
    def create_file(cls, uploaded_file: FileStorage, user_id: int):
        
        # use secure_filename to make sure the file name is not an executable/harmful format
        filename = secure_filename(uploaded_file.filename)

        # query the database to make sure no file with the same name exists
        if db.session.query(File).filter_by(owner_id=user_id, title=filename).first() is not None:
            raise FileAlreadyExistsError(filename)

        # some operator to read the file, calculate file's size and hash it
        blob = uploaded_file.read()
        uploaded_file.stream.seek(0)
        size = len(blob)

        # file hash can be used to check the file integrity to ensure the file content is not modified 
        # while it is being uploaded.
        f_hash = sha256(blob).hexdigest()

        try:
            # save the file record into the database
            cls.__save_file_db(f_hash, filename, size, user_id)
        except Exception as e:
            Logger.logEvent(message="Failed to upload file. Filename:" + filename, type=EventType.ERROR)
            raise FileInsertionError(filename)
        else:
            Logger.logEvent(message="Upload file successfully. Filename:" + filename, type=EventType.EVENT)

            # upload the physical file to the server
            cls.__save_file_disk(uploaded_file, filename)
            db.session.commit()

    # Performs saving the file to the database
    @classmethod
    @login_required
    def __save_file_db(cls, f_hash: str, filename: str, size: int, user_id: int):
        file = File(title=filename, file_size=size,
                    file_hash=f_hash, owner_id=user_id)
        db.session.add(file)

    # Gets the upload folder for the current logged-in user
    # The pattern is to get the upload folder, then create separate folder using the user's email
    @classmethod
    @login_required
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

    # Performs uploading the file to the server (local server for now)
    @classmethod
    @login_required
    def __save_file_disk(cls, file: FileStorage, filename: str):
        path = os.path.join(cls.__get_upload_dir(), filename)
        file.save(path)
        return path

    # Gets the physical file from the server in case user wants to download the file
    @classmethod
    @login_required
    def get_file_from_disk(cls, filename):
        if not os.path.exists(os.path.join(cls.__get_upload_dir(), filename)):
            # Raise an error if the file doesn't exist
            raise FileNotExistsError(filename=filename)
        # Otherwise, use send_from_directory() to safely serve user-requested paths from within a directory.
        # https://flask.palletsprojects.com/en/2.0.x/api/#flask.send_from_directory
        return send_from_directory(directory=cls.__get_upload_dir(), path=filename, as_attachment=True)

    # A helper method to query the existing file by its title
    @classmethod
    @login_required
    def get_file_by_title(cls, filename: str):
        file = db.session.query(File).filter_by(title=filename).first()
        if file is None:
            # raise an error if the file doesn't exist.
            # otherwise, returns the file
            raise FileNotExistsError(filename)
        return file

    # Performs file deletion for the current logged-in user
    @classmethod
    @login_required
    def delete_file(cls, file: File):
        try:
            # delete file record from the database
            db.session.delete(file)
        except Exception as e:
            Logger.logEvent(message="Failed to delete file. Filename:" + file.title, type=EventType.ERROR)
            raise FileDeletionError(file.title)
        else:
            Logger.logEvent(message="Delete file successfully. Filename:" + file.title, type=EventType.EVENT)
            # remove the physical file from the server
            os.remove(os.path.join(cls.__get_upload_dir(), file.title))
        
        # commit the change to the database
        db.session.commit()

    # A helper tool for admin, to get the upload directory for a user
    # This will support the user's file deletion upon request
    @classmethod
    @login_required
    def __get_upload_dir_for_user(cls, email):
        upload_folder = os.path.join(BASE_DIR + '/app/uploads/', email + '/')

        if os.path.exists(upload_folder) and os.path.isdir(upload_folder):
            return upload_folder
        else:
            try:
                os.mkdir(upload_folder)
            except FileExistsError:
                pass

    # Performs user's file deletion upon request
    @classmethod
    @login_required
    def delete_all_files_for_user(cls, user_id, email):
        files = cls.get_user_files(user_id)
        for file in files:
            file_path = cls.__get_upload_dir_for_user(email)
            if os.path.exists(file_path):
                db.session.delete(file)
                os.remove(os.path.join(file_path, file.title))
        
        db.session.commit()