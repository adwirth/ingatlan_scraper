chrome.runtime.onInstalled.addListener(() => {
  console.log("Custom Scraper installed!");
});

chrome.action.onClicked.addListener((tab) => {
  chrome.scripting.executeScript({
    target: { tabId: tab.id },
    files: ["content.js"],
  });
});
