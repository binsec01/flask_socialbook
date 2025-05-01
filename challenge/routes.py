import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from config import Config
from utils import allowed_file, is_valid_image, sanitize_url, save_image_from_url

# create and configure app
app = Flask(__name__, static_folder='static')
app.config.from_object(Config)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    # ensure request has file or URL
    if 'file' not in request.files and 'url' not in request.form:
        flash('No file or URL provided')
        return redirect(url_for('index'))

    filename = None

    # handle direct file upload
    if 'file' in request.files:
        file = request.files['file']
        if not file or file.filename == '':
            flash('No selected file')
            return redirect(url_for('index'))
        if allowed_file(file.filename):
            # secure and unique filename
            base, ext = os.path.splitext(file.filename)
            filename = f"{base}_{uuid.uuid4()}{ext}"
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

    # handle image fetch via URL
    else:
        url = request.form.get('url', '')
        if not url:
            flash('No URL provided')
            return redirect(url_for('index'))
        if not sanitize_url(url):
            flash('Invalid URL format or contains blocked characters')
            return redirect(url_for('index'))
        filename = save_image_from_url(url)
        if not filename:
            flash('Failed to download image from URL')
            return redirect(url_for('index'))

    # redirect to profile view on success
    if filename:
        return redirect(url_for('profile', filename=filename))
    flash('Upload failed')
    return redirect(url_for('index'))


@app.route('/profile/<filename>')
def profile(filename):
    return render_template('profile.html', filename=filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)