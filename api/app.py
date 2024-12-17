# Application basique contenant des vulnérabilités
import sqlite3
from flask import Flask, request, jsonify
import hashlib
import ftplib
import subprocess

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    c.execute(query)
    user = c.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid credentials."}), 401

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    password_hash = hashlib.md5(password.encode()).hexdigest()

    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully!"})

@app.route('/debug', methods=['GET'])
def debug():
    debug_code = request.args.get('code', '')
    try:
        result = eval(debug_code)
        return jsonify({"debug": str(result)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/ftp', methods=['GET'])
def ftp_access():
    ftp = ftplib.FTP('ftp.example.com')
    ftp.login(user='admin', passwd='hardcodedpassword')
    files = ftp.nlst()
    ftp.quit()
    return jsonify({"files": files})

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return jsonify({"stdout": stdout.decode(), "stderr": stderr.decode()})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
