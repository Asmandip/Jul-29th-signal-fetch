from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "")
client = MongoClient(MONGO_URI)
db = client["asmandip_bot"]
pnl_collection = db["pnl_logs"]

def log_trade(symbol, pnl, status):
    pnl_collection.insert_one({
        "symbol": symbol,
        "pnl": pnl,
        "status": status
    })

def get_total_pnl():
    total = 0.0
    for trade in pnl_collection.find():
        total += trade.get("pnl", 0.0)
    return round(total, 2)

def get_trade_count():
    return pnl_collection.count_documents({})