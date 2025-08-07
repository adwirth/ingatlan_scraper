# Property Listing Scraper

## Overview

This project consists of a Chrome extension for scraping property listings and a Python script for processing the collected data into a structured CSV summary. The CSV output tracks each property by advertId, recording details such as district, query dates, price changes, and other attributes over time.

## Features

### Chrome Extension (my-scraper/)

Scrapes property listings from a real estate website.

Extracts key details such as:

advertId: Unique property identifier.

district: Location of the property.

price: Listing price.

area: Property size (square meters).

rooms: Number of rooms (converts " + 1 fél" notation into decimal).

Saves the scraped data as a downloadable JSON file.

### Python Processor (json_to_csv_processor.py)

Reads multiple JSON files containing scraped data.

Generates a CSV summary with:

advertId: Unique identifier.

district: Property location.

first_query_date: Date when the listing was first recorded.

elapsed_days: Number of days between first and last query.

first_price: Initial listing price.

last_price: Most recent listing price.

area: Property size in square meters.

rooms: Number of rooms, ensuring numerical formatting.

Cleans and formats data (e.g., removing "m2" from area, ensuring decimal notation in price).

## Installation

1. Clone the repository:
```
git clone https://github.com/adwirth/ingatlan_scraper
```
cd property-scraper

2. Install Python dependencies:
```
pip install -r requirements.txt
```
3. Load the Chrome extension:

Open Chrome and navigate to chrome://extensions/

Enable Developer Mode.

Click Load Unpacked and select the my-scraper/ folder.

4. Collect Data:

Navigate to the property listing website.

Click the extension icon to start scraping.

Download the JSON file and place it in the json_data/ directory.

5. Process Data:

Run the Python script to process the JSON files and generate a structured CSV summary:
```
python json_to_csv_processor.py
```
The output file will be advert_summary.csv.

## File Structure
```
property-scraper/
│── my-scraper/                # Chrome extension folder
│   ├── manifest.json          # Extension manifest
│   ├── background.js          # Background script
│   ├── content.js             # Content script for scraping
│   ├── popup.html             # Extension popup UI
│   ├── popup.js               # Logic for UI interactions
│── json_to_csv_processor.py   # Python script for processing data
│── json_data/                 # Folder for storing scraped JSON files
│── advert_summary.csv         # Output CSV file
│── README.md                  # Documentation
│── requirements.txt           # Python dependencies
```
## Example Output

### CSV Output (advert_summary.csv)

advertId,district,first_query_date,elapsed_days,first_price,last_price,area,rooms
34378761,"Budapest III. kerület, Tarhos utca 156.","2024-12-26",15,179.90,199.90,112,5
34144137,"Budapest III. kerület, Aranyhegy","2024-12-20",10,149.00,155.00,95,3.5

## License

This project is licensed under the MIT License.

