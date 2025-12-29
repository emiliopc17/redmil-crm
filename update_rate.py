import database
try:
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO exchange_rates (rate_value, source) VALUES (?, ?)", (26.4730, 'BCH Web'))
    conn.commit()
    conn.close()
    print("SUCCESS: Rate updated to 26.4730")
except Exception as e:
    print(f"ERROR: {e}")
