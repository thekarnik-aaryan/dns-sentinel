# 🛡️ DNS Sentinel
Production-ready cybersecurity platform for real-time DNS monitoring.
Here are the exact steps to start **DNS Sentinel** whenever you open VS Code or start your PC:

1. **Start the Backend (Terminal 1)**
Open a terminal in VS Code and run:
```powershell
cd D:\dnssen\dns-sentinel\backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000

```


*(Keep this terminal running in the background).*
2. **Start the Frontend (Terminal 2)**
Open a **new** terminal tab (`Ctrl + Shift + ` ` ` or click `+` in the terminal panel) and run:
```powershell
cd D:\dnssen\dns-sentinel\frontend
npm run dev

```


3. **Open the SOC Dashboard**
Navigate to **`http://localhost:3000`** in your web browser.

---

### Optional: Inject Fresh Threats

If you want to add new simulated threat alerts to the dashboard at any time, open a new terminal tab and run:

```powershell
cd D:\dnssen\dns-sentinel\backend
.\venv\Scripts\activate
python inject_threats.py

```
