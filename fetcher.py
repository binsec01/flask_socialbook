#!/usr/bin/env python3
import sys
import os
import subprocess
import random
import string
from PIL import Image
import io
import requests

def is_valid_image(data):
    try:
        Image.open(io.BytesIO(data))
        return True
    except:
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 fetcher.py <image_url>")
        sys.exit(1)

    image_url = sys.argv[1]
    
    # Generate random filename
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    temp_file = f"/tmp/{random_name}"
    final_file = f"static/uploads/{random_name}.jpg"
    
    # Download the image using curl
    try:
        subprocess.run(f"curl {image_url} -o {temp_file}", shell=True, check=True)
        
        # Verify it's an image
        with open(temp_file, 'rb') as f:
            if not is_valid_image(f.read()):
                print("Error: Not a valid image file")
                os.remove(temp_file)
                sys.exit(1)
        
        # Move to uploads directory
        os.makedirs("static/uploads", exist_ok=True)
        os.rename(temp_file, final_file)
        print(f"Image saved as {final_file}")
        
    except subprocess.CalledProcessError:
        print("Error downloading image")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        if os.path.exists(temp_file):
            os.remove(temp_file)
        sys.exit(1)

if __name__ == "__main__":
    main() 