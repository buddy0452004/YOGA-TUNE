import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import re
import os

# ------------------ Load Dataset ------------------
data_file = "static/yoga_health_dataset.csv"
if not os.path.exists(data_file):
    raise FileNotFoundError(f"{data_file} not found.")
data = pd.read_csv(data_file)

# ------------------ Health Report Parsing ------------------
def parse_health_report(text):
    issues_detected = []
    markers = {
        "B12": r"B12\s*[:\-]?\s*(\d+)",
        "Blood Pressure": r"BP\s*[:\-]?\s*(\d+/\d+)",
        "Blood Sugar": r"(Fasting|Random)?\s*Blood Sugar\s*[:\-]?\s*(\d+)",
        "Uric Acid": r"Uric Acid\s*[:\-]?\s*(\d+\.\d+)",
        "TSH": r"TSH\s*[:\-]?\s*(\d+\.\d+)"
    }
    for issue, pattern in markers.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if issue == "Blood Pressure":
                bp = match.group(1)
                if int(bp.split("/")[0]) > 130:
                    issues_detected.append("Hypertension")
            elif issue == "Blood Sugar":
                sugar = int(match.group(2))
                if sugar > 130:
                    issues_detected.append("Diabetes")
            elif issue == "Uric Acid" and float(match.group(1)) > 7:
                issues_detected.append("High Uric Acid")
            elif issue == "TSH" and float(match.group(1)) > 4.0:
                issues_detected.append("Thyroid Issues")
            elif issue == "B12" and int(match.group(1)) < 200:
                issues_detected.append("Fatigue")
    return list(set(issues_detected))

# ------------------ Recommendation Engine ------------------
def recommend_plan(user_issue):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(data["Health Issue"])
    input_vector = vectorizer.transform([user_issue])
    model = NearestNeighbors(n_neighbors=1, metric='cosine')
    model.fit(tfidf_matrix)
    distance, index = model.kneighbors(input_vector)
    return data.iloc[index[0][0]].to_dict()

# ------------------ Weekly Plan Generator ------------------
def generate_weekly_plan(recommendation):
    # Use CSV poses but images are always pose1.png → pose18.png
    all_poses = [pose.strip() for pose in recommendation['Yoga Asanas'].split(',')]
    random.shuffle(all_poses)

    # 18 images in static/poses/pose1.png … pose18.png
    pose_images_list = [f"pose{i+1}.png" for i in range(18)]
    random.shuffle(pose_images_list)

    weekly_plan = {}
    poses_per_day = 3
    daily_focus = ["Warm-up", "Core", "Legs", "Chest", "Twists", "Balance", "Relax"]

    pose_idx = 0
    for i in range(7):
        day_key = f"Day {i+1} ({daily_focus[i % len(daily_focus)]})"
        day_poses = []

        for _ in range(poses_per_day):
            if pose_idx >= len(all_poses):
                # Loop back to start if poses run out
                pose_idx = 0
            pose_name = all_poses[pose_idx]
            pose_image = pose_images_list[pose_idx % len(pose_images_list)]

            pose_info = {
                "name": pose_name,
                "duration": f"{random.choice([20, 30, 40])} secs",
                "sets": f"{random.choice([2, 3])} sets",
                "image": f"static/poses/{pose_image}"
            }
            day_poses.append(pose_info)
            pose_idx += 1

        weekly_plan[day_key] = day_poses

    return weekly_plan
