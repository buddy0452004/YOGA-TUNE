import csv
import os
from datetime import datetime

CSV_FILE = "static/user_history.csv"

def log_to_csv(issue, recommendation):
    if not os.path.exists("static"):
        os.mkdir("static")

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["Date", "Issue", "Recommendation", "Yoga Asanas"])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            issue,
            recommendation.get("Health Issue", ""),
            recommendation.get("Yoga Asanas", "")
        ])
