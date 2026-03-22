import os
import csv
import exifread

IMAGE_FOLDER = "izmir"
OUTPUT_CSV = "photos.csv"


def dms_to_decimal(dms, ref):
    d = float(dms.values[0].num) / float(dms.values[0].den)
    m = float(dms.values[1].num) / float(dms.values[1].den)
    s = float(dms.values[2].num) / float(dms.values[2].den)

    decimal = d + (m / 60.0) + (s / 3600.0)

    if ref in ["S", "W"]:
        decimal = -decimal

    return decimal


rows = []

for filename in os.listdir(IMAGE_FOLDER):
    if not filename.lower().endswith((".jpg", ".jpeg")):
        continue

    path = os.path.join(IMAGE_FOLDER, filename)

    try:
        with open(path, "rb") as f:
            tags = exifread.process_file(f, details=False)

            lat = tags.get("GPS GPSLatitude")
            lat_ref = tags.get("GPS GPSLatitudeRef")
            lon = tags.get("GPS GPSLongitude")
            lon_ref = tags.get("GPS GPSLongitudeRef")

            if lat and lat_ref and lon and lon_ref:
                latitude = dms_to_decimal(lat, lat_ref.values)
                longitude = dms_to_decimal(lon, lon_ref.values)
            else:
                latitude, longitude = None, None

            rows.append({
                "filename": filename,
                "latitude": latitude,
                "longitude": longitude
            })

    except Exception as e:
        print(f"Hata: {filename} -> {e}")

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["filename", "latitude", "longitude"])
    writer.writeheader()
    writer.writerows(rows)

print("DONE ✅ photos.csv hazır")