import requests
import database
from datetime import datetime

FRANKFURTER_URL = "https://api.frankfurter.app/latest"

def update_rates_from_api():
    """
    Fetches the latest USD to HNL rate from Frankfurter API.
    If HNL is not supported or API fails, logs error but does not crash.
    """
    try:
        # Request USD to HNL
        # Note: Frankfurter supports EUR base by default. 
        # We can ask for ?from=USD&to=HNL
        response = requests.get(f"{FRANKFURTER_URL}?from=USD&to=HNL", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            rates = data.get('rates', {})
            
            if 'HNL' in rates:
                rate_value = rates['HNL']
                # Update DB
                database.update_exchange_rate(rate_value)
                return True, rate_value
            else:
                print("HNL rate not found in API response.")
                return False, None
        else:
            print(f"API Error: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"Forex API Exception: {e}")
        return False, None
