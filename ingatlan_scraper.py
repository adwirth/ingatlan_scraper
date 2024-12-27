from playwright.sync_api import sync_playwright
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

# Scraping function using Playwright with Firefox
def scrape_page_with_playwright(url):
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)  # Set headless=False for debugging
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.wait_for_load_state("networkidle")
        print("Solve the CAPTCHA manually, then press Enter to continue...")
        input()
        html = page.content()
        browser.close()

        # Parse the HTML using BeautifulSoup
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        listings = soup.find_all('a', class_='listing-card')
        for listing in listings:
            try:
                # Extract advert ID
                advert_id = listing.get('data-listing-id', 'N/A')

                # Extract price
                price_tag = listing.find('span', class_='fw-bold fs-5 text-onyx me-3 font-family-secondary')
                price = price_tag.text.strip() if price_tag else 'N/A'

                # Extract district
                district_tag = listing.find('span', class_='d-block fw-500 fs-7 text-onyx font-family-secondary')
                district = district_tag.text.strip() if district_tag else 'N/A'

                # Extract area
                area_tag = listing.find('span', text='Alapterület')
                area = area_tag.find_next_sibling('span', class_='fs-7 text-onyx fw-bold').text.strip() if area_tag else 'N/A'

                # Extract number of rooms
                rooms_tag = listing.find('span', text='Szobák')
                rooms = rooms_tag.find_next_sibling('span', class_='fs-7 text-onyx fw-bold').text.strip() if rooms_tag else 'N/A'

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
        scrape_page_with_playwright(url)

# Scheduling the task
def daily_task():
    BASE_URL = "https://ingatlan.com/lista/elado+haz+90-130-m2+luxus+duplakomfortos+osszkomfortos+ujszeru+uj-epitesu+200-500-m2telek+csaladi-haz+ikerhaz+epitve-2011-utan+ii-ker+iii-ker+xi-ker+xii-ker"
    PAGE_COUNT = 1  # Adjust based on the number of pages to scrape
    scrape_all_pages(BASE_URL, PAGE_COUNT)


daily_task()
exit()

schedule.every().day.at("08:00").do(daily_task)

if __name__ == "__main__":
    initialize_csv()
    print("Starting scraper...")
    while True:
        schedule.run_pending()
        time.sleep(60)
