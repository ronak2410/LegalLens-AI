/**
 * LegalLens AI - Background Service Worker
 */

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "legallens_scan_selection",
    title: "Scan selection with LegalLens AI",
    contexts: ["selection"]
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "legallens_scan_selection" && info.selectionText) {
    chrome.action.openPopup();
  }
});
