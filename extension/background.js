// Allows users to open the side panel by clicking on the action toolbar icon
chrome.sidePanel
  .setPanelBehavior({ openPanelOnActionClick: true })
  .catch((error) => console.error(error));

chrome.commands.onCommand.addListener((command, tab) => {
  if (command === "open taipy") {
    chrome.sidePanel.open({ windowId: tab.windowId });
  }
});
