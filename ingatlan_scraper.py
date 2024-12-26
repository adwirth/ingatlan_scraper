import cloudscraper
from bs4 import BeautifulSoup
import csv
from datetime import date
import schedule
import time

# Define the CSV file
CSV_FILE = "properties.csv"

# Initialize the CSV file with headers (if not already present)
def initialize_csv():
    try:
        with open(CSV_FILE, mode="x", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["advert_id", "price", "area", "rooms", "district", "query_date", "first_appearance"])
    except FileExistsError:
        pass

# Save data to the CSV file
def save_to_csv(data):
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([data["advert_id"], data["price"], data["area"], data["rooms"], data["district"], data["query_date"], data["first_appearance"]])

# Scraping function
def scrape_page(url):
    scraper = cloudscraper.create_scraper()  # Bypass Cloudflare
    response = scraper.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch {url}, status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract individual listings (adjust selectors to match the website's structure)
    listings = soup.find_all('div', class_='listing')
    for listing in listings:
        try:
            advert_id = listing['data-id']
            price = listing.find('div', class_='price').text.strip()
            area = listing.find('div', class_='parameter', {'data-key': 'area'}).text.strip()
            rooms = listing.find('div', class_='parameter', {'data-key': 'rooms'}).text.strip()
            district = listing.find('div', class_='parameter', {'data-key': 'district'}).text.strip()

            data = {
                'advert_id': advert_id,
                'price': price,
                'area': area,
                'rooms': rooms,
                'district': district,
                'query_date': str(date.today()),
                'first_appearance': str(date.today())
            }
            save_to_csv(data)
        except Exception as e:
            print(f"Error processing listing: {e}")

# Fallback for manual verification using Playwright
def scrape_with_playwright(url):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Use headless=False for manual CAPTCHA
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        print("Please complete any manual verification in the browser.")
        input("Press Enter after completing verification...")

        html = page.content()
        browser.close()

        # Process the HTML with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        listings = soup.find_all('div', class_='listing')
        for listing in listings:
            try:
                advert_id = listing['data-id']
                price = listing.find('div', class_='price').text.strip()
                area = listing.find('div', class_='parameter', {'data-key': 'area'}).text.strip()
                rooms = listing.find('div', class_='parameter', {'data-key': 'rooms'}).text.strip()
                district = listing.find('div', class_='parameter', {'data-key': 'district'}).text.strip()

                data = {
                    'advert_id': advert_id,
                    'price': price,
                    'area': area,
                    'rooms': rooms,
                    'district': district,
                    'query_date': str(date.today()),
                    'first_appearance': str(date.today())
                }
                save_to_csv(data)
            except Exception as e:
                print(f"Error processing listing: {e}")

# Main function to iterate over multiple pages
def scrape_all_pages(base_url, page_count):
    for i in range(1, page_count + 1):
        url = f"{base_url}?page={i}"
        print(f"Scraping page {i}: {url}")
        try:
            scrape_page(url)
        except Exception as e:
            print(f"Cloudflare block or error occurred: {e}. Falling back to manual verification.")
            scrape_with_playwright(url)

# Scheduling the task
def daily_task():
    BASE_URL = "https://ingatlan.com/listings"
    PAGE_COUNT = 5  # Adjust based on the number of pages to scrape
    scrape_all_pages(BASE_URL, PAGE_COUNT)

schedule.every().day.at("08:00").do(daily_task)

if __name__ == "__main__":
    initialize_csv()
    print("Starting scraper...")
    while True:
        schedule.run_pending()
        time.sleep(60)

