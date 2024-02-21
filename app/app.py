# app.py
from flask import Flask, render_template, request, jsonify
import secrets

app = Flask(__name__)

# Secret key for encoding and decoding (RC4 key)
SECRET_KEY = bytearray(secrets.token_bytes(16))

# In-memory storage for encoded passwords
encoded_passwords = {}


def rc4(text, key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    i = 0
    j = 0
    result = bytearray()

    for char in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        result.append(char ^ S[(S[i] + S[j]) % 256])

    return bytes(result)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/submit', methods=['POST'])
def submit_password():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username or password not provided'}), 400

    # Encode the password using RC4
    encoded_password = rc4(password.encode(), SECRET_KEY)

    # Store the encoded password in memory
    encoded_passwords[username] = encoded_password

    # Convert bytes to base64-encoded string
    encoded_password_str = encoded_password.decode('latin-1')

    return jsonify({'encoded_password': encoded_password_str}), 200


@app.route('/api/retrieve', methods=['POST'])
def retrieve_password():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username not provided'}), 400

    # Retrieve the encoded password from memory
    encoded_password = encoded_passwords.get(username)

    if not encoded_password:
        return jsonify({'error': 'No encoded password found for the username'}), 404

    # Decode the password using RC4
    decoded_password = rc4(encoded_password, SECRET_KEY).decode()

    # Convert bytes to base64-encoded string
    encoded_password_str = encoded_password.decode('latin-1')

    return jsonify({'encoded_password': encoded_password_str, 'decoded_password': decoded_password}), 200


if __name__ == '__main__':
    app.run(debug=True)
