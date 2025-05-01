import re
import subprocess
import os
import tempfile
from flask import Flask, request, render_template, send_file

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '')
        if url:
            # Create a temporary file to store the image
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                # Vulnerable curl command with shell=True
                curl_cmd = f"curl -s -o {temp_file.name} {url}"
                subprocess.run(curl_cmd, shell=True)
                return send_file(temp_file.name, mimetype='image/jpeg')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

def sanitize_url(url):
    # Remove any characters that could be used for command injection
    url = re.sub(r'[;&|`$@]', '', url)
    # Remove any short options
    url = re.sub(r'-[a-zA-Z]', '', url)
    # Ensure URL starts with http:// or https://
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url 