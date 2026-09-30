import datetime
import random
from app.database.database import init_db, SessionLocal
from app.services.dns_service import process_incoming_query

def generate_threat_campaigns():
    init_db()
    db = SessionLocal()
    now = datetime.datetime.utcnow()
    print("Injecting multi-vector DNS threat campaign...")

    # 1. CRITICAL: High-Volume Data Exfiltration / Tunneling
    for i in range(5):
        sub = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=55))
        process_incoming_query(db, {
            "timestamp": now - datetime.timedelta(seconds=i * 10),
            "source_ip": "10.0.4.15",
            "destination_ip": "1.1.1.1",
            "query_name": f"{sub}.data-exfil.attacker-c2.com",
            "query_type": "TXT",
            "response_code": "NOERROR",
            "packet_size": 450,
            "response_time": 65.0
        })

    # 2. HIGH: DGA (Domain Generation Algorithm) Botnet Traffic
    dga_stems = ["zxcvbnm9876", "asdfghjkl5432", "qwertyuiop1234", "mnbvcxz0987", "poiuytrewq567"]
    for stem in dga_stems:
        process_incoming_query(db, {
            "timestamp": now - datetime.timedelta(minutes=random.randint(1, 10)),
            "source_ip": "192.168.1.105",
            "destination_ip": "8.8.8.8",
            "query_name": f"{stem}x99.biz",
            "query_type": "A",
            "response_code": "NXDOMAIN",
            "packet_size": 68,
            "response_time": 12.0
        })

    # 3. MEDIUM: NXDOMAIN Reconnaissance / Port Scan
    for i in range(6):
        process_incoming_query(db, {
            "timestamp": now - datetime.timedelta(seconds=i * 2),
            "source_ip": "192.168.1.220",
            "destination_ip": "8.8.8.8",
            "query_name": f"scanner-test-node-{i}.internal-local.net",
            "query_type": "A",
            "response_code": "NXDOMAIN",
            "packet_size": 54,
            "response_time": 8.0
        })

    # 4. NORMAL: Standard background noise
    for domain in ["github.com", "stackoverflow.com", "aws.amazon.com", "reddit.com"]:
        process_incoming_query(db, {
            "timestamp": now,
            "source_ip": "192.168.1.50",
            "destination_ip": "8.8.8.8",
            "query_name": domain,
            "query_type": "A",
            "response_code": "NOERROR",
            "packet_size": 64,
            "response_time": 15.0
        })

    db.close()
    print("Check your SOC dashboard.")

if __name__ == "__main__":
    generate_threat_campaigns()