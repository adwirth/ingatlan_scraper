// Function to scrape data
function scrapeData() {
  const listings = document.querySelectorAll(".listing-card");
  const scrapedData = [];

  listings.forEach((listing) => {
    const advertId = listing.getAttribute("data-listing-id");
    const price = listing.querySelector(".fw-bold.fs-5.text-onyx")?.innerText.trim() || "N/A";
    const district = listing.querySelector(".d-block.fw-500.fs-7.text-onyx")?.innerText.trim() || "N/A";

    // Find "Alapterület" and extract its sibling's text
    const areaTag = Array.from(listing.querySelectorAll("span"))
      .find(el => el.textContent.includes("Alapterület"));
    const area = areaTag ? areaTag.nextElementSibling?.textContent.trim() : "N/A";

    // Find "Szobák" and extract its sibling's text
    const roomsTag = Array.from(listing.querySelectorAll("span"))
      .find(el => el.textContent.includes("Szobák"));
    const rooms = roomsTag ? roomsTag.nextElementSibling?.textContent.trim() : "N/A";

    scrapedData.push({ advertId, price, district, area, rooms });
  });

  console.log("Scraped Data:", scrapedData);
  return scrapedData;
}

function downloadDataAsJson(data, filename) {
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a); // Required for Firefox
  a.click();
  document.body.removeChild(a); // Cleanup the DOM

  URL.revokeObjectURL(url); // Cleanup the blob URL
}

// Execute scraping
const data = scrapeData();

// Save to local storage
chrome.storage.local.set({ scrapedData: data }, () => {
  console.log("Data saved to local storage");
});

const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
downloadDataAsJson(data, `scraped-data-${timestamp}.json`);

