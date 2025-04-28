from flask import Flask, request, render_template, redirect, url_for, flash
import re
import subprocess
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def sanitize_url(url):
    # Block dangerous characters
    blocked_chars = [';', '&', '|', '`', '$(', ')', '\n', '%20', '--']
    for char in blocked_chars:
        if char in url:
            return False
    
    # Only allow http/https URLs
    if not re.match(r'^https?://', url):
        return False
    
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-url', methods=['POST'])
def upload_url():
    image_url = request.form.get('image_url', '')
    
    if not image_url:
        flash('Please provide an image URL')
        return redirect(url_for('index'))
    
    if not sanitize_url(image_url):
        flash('Invalid URL format or contains blocked characters')
        return redirect(url_for('index'))
    
    try:
        # Run the fetcher script
        result = subprocess.run(
            f"python3 fetcher.py {image_url}",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Extract the saved filename from the output
            filename = result.stdout.strip().split()[-1]
            return render_template('index.html', image=filename)
        else:
            flash(f'Error: {result.stderr}')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs('static/uploads', exist_ok=True)
    app.run(host='0.0.0.0', port=5000) 