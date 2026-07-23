import requests
import os
import sys

BASE_URL = "https://localhost"
# Ignore self-signed certificate
session = requests.Session()
session.verify = False
# Suppress only the InsecureRequestWarning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_weak_password_rejected():
    """Passwords that are common or too short should return 200 (stay on page) with error."""
    resp = session.post(BASE_URL, data={"username": "testuser", "password": "password"}, allow_redirects=False)
    assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
    # Check that error message is present in the page
    assert b"too common" in resp.content.lower() or b"at least 8" in resp.content.lower(), "Error message not found"

def test_short_password_rejected():
    resp = session.post(BASE_URL, data={"username": "user", "password": "1234567"}, allow_redirects=False)
    assert resp.status_code == 200
    assert b"at least 8" in resp.content.lower()

def test_strong_password_accepted():
    """A password that meets requirements should redirect to /welcome."""
    import time
    # Use a unique password that is definitely not in the common list
    unique_pass = f"StrongPass{int(time.time())}!"
    resp = session.post(BASE_URL, data={"username": "happy_user", "password": unique_pass}, allow_redirects=False)
    assert resp.status_code == 302, f"Expected redirect, got {resp.status_code}"
    assert "/welcome" in resp.headers.get("Location", ""), "Redirect location wrong"

    # Follow redirect to welcome page
    resp2 = session.get(BASE_URL + "/welcome", allow_redirects=False)
    assert resp2.status_code == 200
    assert unique_pass.encode() in resp2.content, "Password not displayed on welcome page"

def test_database_logging():
    """Check that the user's login was recorded in the 2402056 table."""
    import psycopg2
    import time
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres",
        dbname="password_checker"
    )
    cur = conn.cursor()
    # We'll just verify that at least one row exists with the username used earlier.
    cur.execute('SELECT username FROM "2402056" WHERE username = %s', ("happy_user",))
    result = cur.fetchone()
    assert result is not None, "No log entry found for happy_user"
    cur.close()
    conn.close()

if __name__ == "__main__":
    print("Running integration tests...")
    test_weak_password_rejected()
    test_short_password_rejected()
    test_strong_password_accepted()
    test_database_logging()
    print("All integration tests passed!")