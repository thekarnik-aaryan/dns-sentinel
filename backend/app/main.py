from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.database import init_db
from app.api import routes_dns, routes_alerts, routes_stats

app = FastAPI(title="DNS Sentinel API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup_event(): init_db()

@app.get("/api/health")
def health_check(): return {"status": "healthy", "service": "dns-sentinel"}

app.include_router(routes_dns.router)
app.include_router(routes_alerts.router)
app.include_router(routes_stats.router)
