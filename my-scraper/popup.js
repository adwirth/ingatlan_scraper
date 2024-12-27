document.getElementById("scrape-btn").addEventListener("click", () => {
  chrome.storage.local.get("scrapedData", (result) => {
    const output = document.getElementById("output");
    output.textContent = JSON.stringify(result.scrapedData, null, 2);
  });
});
