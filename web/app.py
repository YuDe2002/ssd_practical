import os
import re
from datetime import datetime

import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.urandom(24)  # important for session

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def is_password_in_common_list(password):
    """Check if the password exists in the common passwords table."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM common_passwords WHERE password = %s", (password,))
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists

def validate_password(password):
    """
    OWASP ASVS Level 1 password requirements:
    - Minimum length 8 characters
    - Not present in known common passwords list
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if is_password_in_common_list(password):
        return False, "This password is too common. Please choose a stronger one."

    return True, ""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        valid, message = validate_password(password)
        if not valid:
            # Stay on home page and show error
            return render_template('index.html', error=message)

        # Password meets requirements – log the user
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO "2402056" (username, created_at) VALUES (%s, %s)',
            (username, datetime.utcnow())
        )
        conn.commit()
        cur.close()
        conn.close()

        # Store password in session to display on welcome page
        session['password'] = password
        return redirect(url_for('welcome'))

    return render_template('index.html')

@app.route('/welcome')
def welcome():
    if 'password' not in session:
        return redirect(url_for('index'))
    password = session['password']
    return render_template('welcome.html', password=password)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run with HTTPS using the self-signed certs
    app.run(host='0.0.0.0', port=443, ssl_context=('/certs/cert.pem', '/certs/key.pem'))