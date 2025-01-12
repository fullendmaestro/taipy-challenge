// sidepanel

// WebSocket connection
let socket;

function connectWebSocket() {
  socket = new WebSocket("ws://localhost:8765");

  socket.onopen = function (e) {
    console.log("[open] Connection established");
    // Identify as Extension client
    socket.send(JSON.stringify({ client_type: "extension" }));
  };

  socket.onmessage = function (event) {
    console.log(`[message] Data received from server: ${event.data}`);
    handleMessage(JSON.parse(event.data));
  };

  socket.onclose = function (event) {
    if (event.wasClean) {
      console.log(
        `[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`
      );
    } else {
      console.log("[close] Connection died");
    }
    // Attempt to reconnect after 5 seconds
    setTimeout(connectWebSocket, 5000);
  };

  socket.onerror = function (error) {
    console.log(`[error] ${error.message}`);
  };
}

function handleMessage(data) {
  switch (data.action) {
    case "list_tabs":
      chrome.tabs.query({}, function (tabs) {
        let tabList = tabs.map((tab) => ({ id: tab.id, url: tab.url }));
        sendResponse({ status: "success", tabs: tabList });
      });
      break;
    case "open_tab":
      chrome.tabs.create({ url: data.params.url }, function (tab) {
        sendResponse({
          status: "success",
          message: `Tab opened with ID: ${tab.id}`,
        });
      });
      break;
    case "close_tab":
      chrome.tabs.remove(parseInt(data.params.tab_id), function () {
        sendResponse({ status: "success", message: `Tab closed` });
      });
      break;
    case "switch_tab":
      chrome.tabs.update(
        parseInt(data.params.tab_id),
        { active: true },
        function () {
          sendResponse({ status: "success", message: `Switched to tab` });
        }
      );
      break;
    case "get_tab_content":
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        if (tabs[0]) {
          chrome.tabs.sendMessage(
            tabs[0].id,
            { action: "getContent" },
            function (response) {
              sendResponse({ status: "success", content: response.content });
            }
          );
        } else {
          sendResponse({ status: "error", message: "No active tab" });
        }
      });
      break;
    default:
      sendResponse({ status: "error", message: "Unknown action" });
  }
}

function sendResponse(response) {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify(response));
  } else {
    console.error("WebSocket is not connected");
  }
}

// Connect to WebSocket when the extension is loaded
connectWebSocket();
