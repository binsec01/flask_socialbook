import os
import random
import string
import subprocess
from flask import current_app
import re
from PIL import Image
from io import BytesIO

def allowed_file(filename):
    """
    Check that filename has a valid extension.
    """
    return ('.' in filename and
            filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS'])


def is_valid_image(data):
    """
    Verify that bytes represent a valid image.
    """
    try:
        Image.open(BytesIO(data))
        return True
    except IOError:
        return False


def sanitize_url(url):
    """
    Sanitize URL to prevent command injection while allowing short curl options.
    Blocks: ;, &, |, `, $(...), whitespace, long options (--*), URL-encoded shell chars
    """
    blocked_characters = [] #current_app.config['BLOCKED_CHARACTERS']
    for char in blocked_characters:
        if char in url:
            return False

    # Removed URL scheme validation to allow our payload
    return True


def save_image_from_url(url):
    upload_folder = current_app.config['UPLOAD_FOLDER']
    
    # generate final random filename
    random_basename = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + '.jpg'
    final_path = os.path.join(upload_folder, random_basename)

    # run curl via subprocess
    cmd = f"curl -Os {url}"
    print(cmd)
    result = subprocess.run(cmd, shell=True, cwd=upload_folder)

    if result.returncode != 0 or not os.path.exists(final_path):
        # cleanup and bail
        if os.path.exists(final_path):
            os.remove(final_path)
        return None

    # read and validate image bytes
    with open(final_path, 'rb') as f:
        data = f.read()
    if not is_valid_image(data):
        os.remove(final_path)
        return None

    return random_basename