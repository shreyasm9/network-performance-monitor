
import speedtest
from ping3 import ping
import psutil
import csv
import time
from datetime import datetime

def get_ping():
    response = ping("8.8.8.8")
    return round(response * 1000, 2) if response else None  # ms

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

def log_data():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ping_val = get_ping()
    download, upload = get_speed()

    with open("data/network_log.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, ping_val, download, upload])

    print(f"[{timestamp}] Ping: {ping_val} ms | Download: {download or 'N/A'} Mbps | Upload: {upload or 'N/A'} Mbps")

if __name__ == "__main__":
    while True:
        log_data()
        time.sleep(30)  # runs every 30 seconds
