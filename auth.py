import sqlite3
import bcrypt
import database

def hash_password(password):
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed_password):
    """Checks a password against a hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def authenticate_user(username, password):
    """
    Authenticates a user. 
    Returns the user row (dict-like) if successful, None otherwise.
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password(password, user['password_hash']):
        return user
    return None

def create_user(username, password, full_name, role='vendedor'):
    """Creates a new user."""
    conn = database.get_connection()
    c = conn.cursor()
    hashed = hash_password(password)
    try:
        c.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)",
                  (username, hashed, full_name, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Seed admin user if not exists (using this module to ensure correct hashing)
def seed_admin():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT count(*) FROM users")
    if c.fetchone()[0] == 0:
        print("Seeding admin user...")
        create_user("admin", "admin123", "System Admin", "admin")
    conn.close()

if __name__ == "__main__":
    seed_admin()
