import json
import csv
import os
from datetime import datetime, timedelta
import re
from collections import defaultdict

# Directory where the JSON files are stored
JSON_DIR = "./json_data"
# Output CSV file
CSV_FILE = "advert_summary.csv"

# Function to clean area and price values
def clean_value(value, pattern):
    if value:
        return re.sub(pattern, "", value).strip()
    return "N/A"

# Function to format room numbers
def format_rooms(rooms):
    if rooms:
        rooms = rooms.replace(" + 1 fél", ".5")
        return rooms.strip()
    return "N/A"

# Function to format price with a decimal point
def format_price(price):
    if price:
        return re.sub(r",", ".", clean_value(price, r"\s*M\s*Ft"))
    return "N/A"

# Function to process JSON files and generate summary
def process_json_files(json_dir, csv_file):
    adverts = defaultdict(lambda: {
        "district": "N/A",
        "first_query_date": None,
        "last_query_date": None,
        "elapsed_days": 0,
        "first_price": "N/A",
        "last_price": "N/A",
        "area": "N/A",
        "rooms": "N/A"
    })

    last_query_time = None

    # Process each JSON file
    for filename in os.listdir(json_dir):
        print(filename)
        if filename.endswith(".json"):
            json_path = os.path.join(json_dir, filename)
            
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
                # Extract timestamp from filename
                try:
                    timestamp_str = filename.replace("scraped-data-", "").replace(".json", "")
                    query_time = datetime.strptime(timestamp_str, "%Y-%m-%dT%H-%M-%S")
                except ValueError:
                    # If timestamp parsing fails, use the file's last modified time
                    query_time = datetime.fromtimestamp(os.path.getmtime(json_path))
                if last_query_time != None:
                    if query_time > last_query_time:
                        last_query_time = query_time
                else:
                    last_query_time = query_time

                # Process each property listing
                for property_data in data:
                    advert_id = property_data.get("advertId", "N/A")
                    district = property_data.get("district", "N/A")
                    price = format_price(property_data.get("price", "N/A"))
                    area = clean_value(property_data.get("area", "N/A"), r"\s*m2")
                    rooms = format_rooms(property_data.get("rooms", "N/A"))

                    # Update or initialize advert entry
                    if adverts[advert_id]["first_query_date"] is None or query_time < adverts[advert_id]["first_query_date"]:
                        adverts[advert_id]["first_query_date"] = query_time
                        adverts[advert_id]["first_price"] = price

                    if adverts[advert_id]["last_query_date"] is None or query_time > adverts[advert_id]["last_query_date"]:
                        adverts[advert_id]["last_query_date"] = query_time
                        adverts[advert_id]["last_price"] = price

                    adverts[advert_id]["district"] = district
                    adverts[advert_id]["area"] = area
                    adverts[advert_id]["rooms"] = rooms

    print(last_query_time)
    # Compute derived variables
    for advert_id, data in adverts.items():
        if data["first_query_date"] and data["last_query_date"]:
            if (last_query_time - data["last_query_date"]) > timedelta(hours=2):
                data["live"] = False
            else:
                data["live"] = True
            data["elapsed_days"] = (data["last_query_date"] - data["first_query_date"]).days
            data["first_query_date"] = data["first_query_date"].strftime("%Y-%m-%d")
            data["last_query_date"] = data["last_query_date"].strftime("%Y-%m-%d")
                                
        data["price_change"] = float(data['last_price']) - float(data['first_price'])
        data['unit_price'] = float(data['last_price']) / float(data['area'])
        

    # Write summary to CSV
    header = ["advertId", "live", "district", "first_query_date", "last_query_date","elapsed_days", "first_price", "last_price", "area", "rooms", "unit_price", "price_change"]
    with open(csv_file, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        
        for advert_id, data in adverts.items():
            writer.writerow([
                advert_id,
                data["live"],
                data["district"],
                data["first_query_date"],
                data["last_query_date"],
                data["elapsed_days"],
                data["first_price"],
                data["last_price"],
                data["area"],
                data["rooms"],
                data["unit_price"],
                data["price_change"]
            ])

if __name__ == "__main__":
    process_json_files(JSON_DIR, CSV_FILE)
    print(f"Summary data successfully written to {CSV_FILE}")
