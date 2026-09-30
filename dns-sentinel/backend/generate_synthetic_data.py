import datetime, random
from app.database.database import init_db, SessionLocal
from app.services.dns_service import process_incoming_query

def generate_synthetic():
    init_db()
    db = SessionLocal()
    now = datetime.datetime.utcnow()
    for domain in ["google.com", "github.com", "microsoft.com", "cloudflare.com"]:
        process_incoming_query(db, {"timestamp": now, "source_ip": "192.168.1.10", "destination_ip": "8.8.8.8", "query_name": domain, "query_type": "A", "response_code": "NOERROR", "packet_size": 64})
    
    sub = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=45))
    process_incoming_query(db, {"timestamp": now, "source_ip": "192.168.1.105", "destination_ip": "1.1.1.1", "query_name": f"{sub}.exfil.test.com", "query_type": "TXT", "response_code": "NOERROR", "packet_size": 320})
    db.close()
    print("Synthetic dataset successfully generated!")

if __name__ == "__main__": generate_synthetic()
