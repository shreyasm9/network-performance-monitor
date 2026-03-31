import speedtest
from ping3 import ping
import csv
import time
from datetime import datetime


# 📡 Get Ping
def get_ping():
    response = ping("8.8.8.8")
    return round(response * 1000, 2) if response else None  # ms


# 🌐 Get Speed
def get_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000      # Mbps

        return round(download, 2), round(upload, 2)

    except Exception as e:
        print("Speedtest failed:", e)
        return None, None


# 🚨 Save Alerts
def save_alert(alert_type, value):
    with open("alerts.csv", "a") as f:
        f.write(f"{datetime.now()},{alert_type},{value}\n")


# 📝 Log Data
def log_data():
    with open("data/network_log.csv", "a") as file:
        writer = csv.writer(file)

        ping_val = get_ping()
        download, upload = get_speed()

        # Save normal log
        writer.writerow([datetime.now(), ping_val, download, upload])

        print(f"[{datetime.now()}] Ping: {ping_val} ms | Download: {download} Mbps | Upload: {upload} Mbps")

        # 🚨 ALERT CONDITION
        if ping_val and ping_val > 100:
            save_alert("HIGH LATENCY", f"{ping_val} ms")


# 🔁 Run continuously
while True:
    log_data()
    time.sleep(30)  # every 30 seconds
