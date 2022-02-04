from app import db
from app.document.models import File
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from hashlib import sha256
from app.errors.filesError import (
    FileAlreadyExistsError,
    FileInsertionError
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
        # A way of transactional insert
        try:
            cls.__save_file_db(f_hash, filename, size, user_id)
        except Exception as e:
            # st.logger.exception(e)
            raise FileInsertionError(filename)
        else:
            # cls.__save_file_disk(uploaded_file, filename)
            db.session.commit()

    @classmethod
    def __save_file_db(cls, f_hash: str, filename: str, size: int, user_id: int):
        file = File(title=filename, file_size=size,
                    file_hash=f_hash, owner_id=user_id)
        db.session.add(file)

