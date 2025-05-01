import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    BASE_DIR = os.path.dirname(__file__)
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    BLOCKED_CHARACTERS = ['&', '|', ';', '`', '$', '(', ')', ' ', '\n', '\r', '\t','--']
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024 # 4MB max file size
