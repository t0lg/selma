import csv
import json
from math import radians, sin, cos, sqrt, atan2

INPUT_CSV = "photos.csv"
OUTPUT_JSON = "locations.json"
BASE_PATH = "izmir/"


def haversine(lat1, lon1, lat2, lon2):
    r = 6371000  # metres
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    )
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return r * c


THRESHOLD_METERS = 40

photos = []

with open(INPUT_CSV, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row["latitude"] or not row["longitude"]:
            continue

        photos.append({
            "filename": row["filename"],
            "lat": float(row["latitude"]),
            "lng": float(row["longitude"])
        })

groups = []

for photo in photos:
    added = False

    for group in groups:
        distance = haversine(
            photo["lat"], photo["lng"],
            group["lat"], group["lng"]
        )

        if distance <= THRESHOLD_METERS:
            group["photos"].append(BASE_PATH + photo["filename"])

            count = len(group["photos"])
            group["lat"] = ((group["lat"] * (count - 1)) + photo["lat"]) / count
            group["lng"] = ((group["lng"] * (count - 1)) + photo["lng"]) / count

            added = True
            break

    if not added:
        groups.append({
            "title": "Yeni Lokasyon",
            "lat": photo["lat"],
            "lng": photo["lng"],
            "note": "",
            "photos": [BASE_PATH + photo["filename"]]
        })

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(groups, f, ensure_ascii=False, indent=2)

print(f"{OUTPUT_JSON} oluşturuldu.")