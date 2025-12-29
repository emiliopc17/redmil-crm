import sqlite3
import os
import hashlib

DB_NAME = "redmil_pro.db"

def get_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def init_db():
    """Initializes the database table structure."""
    conn = get_connection()
    c = conn.cursor()
    
    # Enable foreign keys
    c.execute("PRAGMA foreign_keys = ON;")

    # Users Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'vendedor',
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Products Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_code TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            brand TEXT,
            cost_usd REAL,
            cost_lps REAL,
            stock_quantity INTEGER DEFAULT 0,
            category TEXT,
            image_url TEXT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Exchange Rates Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rate_date DATE DEFAULT (DATE('now')),
            rate_value REAL NOT NULL,
            source TEXT
        );
    """)

    # Margins Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS margins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            brand TEXT UNIQUE,
            margin_percentage REAL NOT NULL,
            updated_by INTEGER,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(updated_by) REFERENCES users(id)
        );
    """)

    # Clients Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            rtn_id TEXT UNIQUE,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Quotes Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            user_id INTEGER,
            quote_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expiration_date DATE,
            total_amount_lps REAL,
            status TEXT DEFAULT 'draft',
            pdf_path TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    """)

    # Quote Items Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS quote_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote_id INTEGER,
            product_id INTEGER,
            quantity INTEGER NOT NULL,
            unit_price_lps REAL NOT NULL,
            total_lps REAL NOT NULL,
            FOREIGN KEY(quote_id) REFERENCES quotes(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        );
    """)

    # Create a default admin user if no users exist
    c.execute("SELECT count(*) FROM users")
    if c.fetchone()[0] == 0:
        # Default password is 'admin123' - In production, force change
        # Simple hash for demo; use bcrypt in real auth module
        default_pass = "admin123" 
        # Note: We will use a proper auth module for hashing later, 
        # but for initial seed we'll just put a placeholder or basic hash if needed.
        # Actually, let's just insert it. The auth module will handle verification.
        # For now we will assume the auth module does the hashing. 
        # I'll modify this once I write auth.py, but for now let's leave it empty 
        # or rely on the auth module to seed it.
        pass

    
    # Brands Table (New - for persistence after clearing products)
    c.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
    """)

    # Price History Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS product_price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            old_cost_usd REAL,
            new_cost_usd REAL,
            change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            changed_by TEXT, 
            FOREIGN KEY(product_id) REFERENCES products(id)
        );
    """)

    # Historical Quotes Table (Snapshot)
    c.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones_historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_name TEXT,
            client_details TEXT, -- JSON structure
            products_json TEXT, -- JSON structure with price snapshots
            total_lps REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # System Config Table
    c.execute("""
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            value TEXT
        );
    """)
    
    # Default configs
    c.execute("INSERT OR IGNORE INTO system_config (key, value) VALUES ('quote_header', 'REDMIL TECHNOLOGY\nSan Pedro Sula, Honduras\nRTN: 05019012345678')")
    c.execute("INSERT OR IGNORE INTO system_config (key, value) VALUES ('quote_footer', 'Gracias por su preferencia.')")

    conn.commit()

    conn.close()
    print("Database initialized successfully.")

def upsert_product(product_data, user_name="System"):
    """Inserts or updates a product. Logs price changes."""
    conn = get_connection()
    c = conn.cursor()
    try:
        # Check if exists
        c.execute("SELECT id FROM products WHERE product_code = ?", (product_data['product_code'],))
        exists = c.fetchone()
        
        # Ensure brand exists in brands table
        brand_name = product_data.get('brand')
        if brand_name:
            try:
                c.execute("INSERT OR IGNORE INTO brands (name) VALUES (?)", (brand_name,))
            except:
                pass

        if exists:
            # Check for price change
            current_id = exists['id']
            # Get current price to compare
            c.execute("SELECT cost_usd FROM products WHERE id = ?", (current_id,))
            current_price = c.fetchone()[0]
            new_price = float(product_data['cost_usd'])
            
            if abs(current_price - new_price) > 0.001:
                # Price changed, log it
                c.execute("""
                    INSERT INTO product_price_history (product_id, old_cost_usd, new_cost_usd, changed_by)
                    VALUES (?, ?, ?, ?)
                """, (current_id, current_price, new_price, user_name))
            
            c.execute("""
                UPDATE products SET 
                    description = ?, 
                    cost_usd = ?, 
                    cost_lps = ?,
                    brand = COALESCE(?, brand),
                    category = COALESCE(?, category),
                    stock_quantity = COALESCE(?, stock_quantity),
                    last_updated = CURRENT_TIMESTAMP
                WHERE product_code = ?
            """, (
                product_data['description'], 
                product_data['cost_usd'], 
                product_data.get('cost_lps', 0), 
                product_data.get('brand'),
                product_data.get('category'),
                product_data.get('stock_quantity'),
                product_data['product_code']
            ))
        else:
            c.execute("""
                INSERT INTO products (product_code, description, brand, cost_usd, cost_lps, stock_quantity, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                product_data['product_code'],
                product_data['description'],
                product_data.get('brand', 'Unknown'),
                product_data['cost_usd'],
                product_data.get('cost_lps', 0),
                product_data.get('stock_quantity', 0),
                product_data.get('category', 'General')
            ))
            
            # Log initial price? Maybe not needed for history, but good for tracking.
            # Let's just track changes for now to keep it clean.
            
        conn.commit()
        return True
    except Exception as e:
        print(f"Error upserting product: {e}")
        return False
    finally:
        conn.close()

def get_all_products():
    """Returns all products as a list of dicts."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM products ORDER BY brand, product_code")
    products = [dict(row) for row in c.fetchall()]
    conn.close()
    conn.close()
    return products

def get_product_history(product_id):
    """Returns price history for a product."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM product_price_history WHERE product_id = ? ORDER BY change_date DESC", (product_id,))
    history = [dict(row) for row in c.fetchall()]
    conn.close()
    return history

def get_product_quotes(product_id):
    """Returns quotes that include this product."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT q.id, q.quote_date, q.total_amount_lps, c.full_name as client_name, qi.quantity, qi.unit_price_lps
        FROM quote_items qi
        JOIN quotes q ON qi.quote_id = q.id
        LEFT JOIN clients c ON q.client_id = c.id
        WHERE qi.product_id = ?
        ORDER BY q.quote_date DESC
    """, (product_id,))
    quotes = [dict(row) for row in c.fetchall()]
    conn.close()
    return quotes

def get_all_brands():
    """Returns a list of distinct brands."""
    conn = get_connection()
    c = conn.cursor()
    
    # Try getting from brands table first
    try:
        c.execute("SELECT name FROM brands ORDER BY name")
        brands = [row[0] for row in c.fetchall()]
        
        # If empty, fallback to products (migration) or return empty
        if not brands:
             c.execute("SELECT DISTINCT brand FROM products WHERE brand IS NOT NULL AND brand != '' ORDER BY brand")
             brands = [row[0] for row in c.fetchall()]
             # Migrate found brands
             for b in brands:
                 c.execute("INSERT OR IGNORE INTO brands (name) VALUES (?)", (b,))
             conn.commit()
    except:
        # Fallback if table doesn't exist yet (though init_db calls it)
        c.execute("SELECT DISTINCT brand FROM products WHERE brand IS NOT NULL AND brand != '' ORDER BY brand")
        brands = [row[0] for row in c.fetchall()]
        
    conn.close()
    return brands

def clear_database_keep_brands():
    """Clears all data except brands and users/admin."""
    conn = get_connection()
    c = conn.cursor()
    
    # 1. Back up distinct brands from products if brands table is empty
    c.execute("SELECT count(*) FROM brands")
    if c.fetchone()[0] == 0:
        c.execute("SELECT DISTINCT brand FROM products WHERE brand IS NOT NULL AND brand != ''")
        brands = [row[0] for row in c.fetchall()]
        for b in brands:
            c.execute("INSERT OR IGNORE INTO brands (name) VALUES (?)", (b,))
            
    # 2. Delete tables
    try:
        c.execute("DELETE FROM products")
        c.execute("DELETE FROM clients")
        c.execute("DELETE FROM quote_items")
        c.execute("DELETE FROM quotes")
        # Keep users, margins (if relevant), and brands
        conn.commit()
        return True
    except Exception as e:
        print(f"Error clearing DB: {e}")
        return False
    finally:
        conn.close()

def get_current_exchange_rate():
    """Returns the latest exchange rate (LPS per USD). Defaults to 25.00 if not found."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT rate_value FROM exchange_rates ORDER BY rate_date DESC, id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return 25.00 # Default fallback

def get_all_clients():
    """Returns all clients."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM clients ORDER BY full_name")
    clients = [dict(row) for row in c.fetchall()]
    conn.close()
    return clients

def create_client(client_data):
    """Creates a new client."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO clients (full_name, rtn_id, phone, email, address)
            VALUES (?, ?, ?, ?, ?)
        """, (
            client_data['full_name'],
            client_data.get('rtn_id'),
            client_data.get('phone'),
            client_data.get('email'),
            client_data.get('address')
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("Client exists or error.")
        return False
    finally:
        conn.close()




def create_quote(quote_data, items_list):
    """Creates a new quote and its items TRANSACTIONALLY."""
    conn = get_connection()
    c = conn.cursor()
    try:
        # Insert Quote
        c.execute("""
            INSERT INTO quotes (client_id, user_id, expiration_date, total_amount_lps, status)
            VALUES (?, ?, DATE('now', '+15 days'), ?, 'draft')
        """, (
            quote_data['client_id'],
            quote_data.get('user_id'), # Can be None if generic
            quote_data['total_amount_lps']
        ))
        
        quote_id = c.lastrowid
        
        # Insert Items
        for item in items_list:
            c.execute("""
                INSERT INTO quote_items (quote_id, product_id, quantity, unit_price_lps, total_lps)
                VALUES (?, ?, ?, ?, ?)
            """, (
                quote_id,
                item['product_id'],
                item['quantity'],
                item['unit_price_lps'],
                item['total_lps']
            ))
            
        conn.commit()
        return quote_id
    except Exception as e:
        conn.rollback()
        print(f"Error creating quote: {e}")
        return None
    finally:
        conn.close()



def save_quote_history(client_name, client_details_json, products_json, total_lps):
    """Saves a snapshot of a generated quote."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO cotizaciones_historico (client_name, client_details, products_json, total_lps)
            VALUES (?, ?, ?, ?)
        """, (client_name, client_details_json, products_json, total_lps))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error saving history: {e}")
        return False
    finally:
        conn.close()

def get_all_quotes():
    """Returns all quotes with client names."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT q.id, q.quote_date, q.total_amount_lps, q.status, c.full_name as client_name 
        FROM quotes q
        LEFT JOIN clients c ON q.client_id = c.id
        ORDER BY q.quote_date DESC
    """)
    quotes = [dict(row) for row in c.fetchall()]
    conn.close()
    return quotes

def get_current_exchange_rate_full():
    """Returns the latest exchange rate dict (rate_value, rate_date)."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT rate_value, rate_date FROM exchange_rates ORDER BY rate_date DESC, id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        return {'rate_value': row[0], 'rate_date': row[1]}
    return {'rate_value': 25.00, 'rate_date': '2023-01-01'}

def update_exchange_rate(new_rate):
    """Inserts a new exchange rate."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO exchange_rates (rate_value, source) VALUES (?, ?)", (new_rate, "Manual Update"))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating rate: {e}")
        return False
    finally:
        conn.close()

def create_user(username, password, full_name, role="vendedor"):
    """Creates a new user."""
    conn = get_connection()
    c = conn.cursor()
    try:
        # Simple hash for demo purposes. Use bcrypt/argon2 in production!
        # Assuming app.py handles hashing or we do it here. 
        # For simplicity, we'll store as is here, but app should hash.
        # WAIT, auth.py implies hashing. Let's assume input 'password' is raw and we hash it here
        # or we just store it. Given previous seed_admin used cleartext 'admin123' logic in my head 
        # but let's be slightly better.
        # Actually, let's just store it as text for this prototype as requested by 'Simple' constraint 
        # unless user asked for security.
        # Plan said "simple hashing".
        import hashlib
        pwd_hash = hashlib.sha256(password.encode()).hexdigest()
        
        c.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES (?, ?, ?, ?)", 
                  (username, pwd_hash, full_name, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_users():
    """Returns all users."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, full_name, role, created_at FROM users ORDER BY id")
    users = [dict(row) for row in c.fetchall()]
    conn.close()
    return users

def get_all_quotes_history():
    """Returns all quotes from the historical table."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM cotizaciones_historico ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_config(key, default=""):
    """Gets a config value by key."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT value FROM system_config WHERE key = ?", (key,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else default

def set_config(key, value):
    """Sets a config value."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO system_config (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()
    return True

def delete_user(user_id):
    """Deletes a user by ID."""
    conn = get_connection()
    c = conn.cursor()
    # Prevent deleting the last admin? Check logic later.
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True

def get_exchange_rate_history(limit=50):
    """Returns historical exchange rates."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM exchange_rates ORDER BY rate_date DESC, id DESC LIMIT ?", (limit,))
    rates = [dict(row) for row in c.fetchall()]
    conn.close()
    return rates

def clear_quote_history():
    """Clears all records from the cotizaciones_historico table."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM cotizaciones_historico")
        conn.commit()
        return True
    except Exception as e:
        print(f"Error clearing history: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
