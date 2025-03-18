chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension Installed");
});

chrome.sidePanel.setOptions({
    enabled: true,
    path: "index.html"
});
