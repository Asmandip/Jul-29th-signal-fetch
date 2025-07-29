from datetime import datetime

def format_symbol(symbol):
    """Standardize symbol format."""
    return symbol.upper().replace("_UMCBL", "")

def get_current_time():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def percent_change(open_price, close_price):
    """Calculate percentage change between two prices."""
    return round(((close_price - open_price) / open_price) * 100, 2)