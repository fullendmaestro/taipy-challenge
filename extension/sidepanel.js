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

let speechEnabled = true;
const synth = window.speechSynthesis;
const recognition = new webkitSpeechRecognition();

// Configure speech recognition
recognition.continuous = true;
recognition.interimResults = false;
recognition.lang = "en-US";

recognition.onresult = function (event) {
  const transcript = event.results[event.results.length - 1][0].transcript;
  sendResponse({
    status: "success",
    action: "transcript",
    message: transcript,
  });
};

recognition.onerror = function (event) {
  console.error("Speech recognition error:", event.error);
  sendResponse({
    status: "error",
    action: "transcript",
    message: `Speech recognition error: ${event.error}`,
  });
};

function handleMessage(data) {
  switch (data.action) {
    // Existing tab management
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

    // Bookmark management
    case "list_bookmarks":
      chrome.bookmarks.getTree(function (bookmarkTreeNodes) {
        sendResponse({ status: "success", bookmarks: bookmarkTreeNodes });
      });
      break;
    case "add_bookmark":
      chrome.bookmarks.create(
        {
          title: data.params.title,
          url: data.params.url,
        },
        function (bookmark) {
          sendResponse({
            status: "success",
            message: `Bookmark created with ID: ${bookmark.id}`,
          });
        }
      );
      break;
    case "delete_bookmark":
      chrome.bookmarks.remove(data.params.id, function () {
        sendResponse({ status: "success", message: "Bookmark deleted" });
      });
      break;

    // History management
    case "search_history":
      chrome.history.search(
        {
          text: data.params.query,
          maxResults: data.params.maxResults,
        },
        function (historyItems) {
          sendResponse({ status: "success", history: historyItems });
        }
      );
      break;
    case "delete_history_item":
      chrome.history.deleteUrl({ url: data.params.url }, function () {
        sendResponse({ status: "success", message: "History item deleted" });
      });
      break;

    // Download management
    case "list_downloads":
      chrome.downloads.search({}, function (downloads) {
        sendResponse({ status: "success", downloads: downloads });
      });
      break;
    case "download_file":
      chrome.downloads.download(
        {
          url: data.params.url,
          filename: data.params.filename,
        },
        function (downloadId) {
          sendResponse({
            status: "success",
            message: `Download started with ID: ${downloadId}`,
          });
        }
      );
      break;

    // Window management
    case "create_window":
      chrome.windows.create(
        {
          url: data.params.url,
          incognito: data.params.incognito,
        },
        function (window) {
          sendResponse({
            status: "success",
            message: `Window created with ID: ${window.id}`,
          });
        }
      );
      break;
    case "list_windows":
      chrome.windows.getAll({ populate: true }, function (windows) {
        sendResponse({ status: "success", windows: windows });
      });
      break;

    // Clipboard operations
    case "copy_to_clipboard":
      navigator.clipboard
        .writeText(data.params.text)
        .then(() => {
          sendResponse({
            status: "success",
            message: "Text copied to clipboard",
          });
        })
        .catch((err) => {
          sendResponse({ status: "error", message: "Failed to copy text" });
        });
      break;
    case "read_from_clipboard":
      navigator.clipboard
        .readText()
        .then((text) => {
          sendResponse({ status: "success", text: text });
        })
        .catch((err) => {
          sendResponse({
            status: "error",
            message: "Failed to read clipboard",
          });
        });
      break;

    // Browser settings
    case "get_zoom_level":
      chrome.tabs.getZoom(function (zoomFactor) {
        sendResponse({ status: "success", zoomFactor: zoomFactor });
      });
      break;
    case "set_zoom_level":
      chrome.tabs.setZoom(data.params.zoomFactor, function () {
        sendResponse({ status: "success", message: "Zoom level updated" });
      });
      break;
    case "play_response":
      if (speechEnabled) {
        const utterance = new SpeechSynthesisUtterance(data.params.text);
        synth.speak(utterance);
        sendResponse({
          status: "success",
          message: "Playing response",
        });
      }
      break;

    case "start_recording":
      try {
        recognition.start();
        sendResponse({
          status: "success",
          message: "Started recording",
        });
      } catch (error) {
        sendResponse({
          status: "error",
          message: `Failed to start recording: ${error.message}`,
        });
      }
      break;

    case "stop_recording":
      try {
        recognition.stop();
        sendResponse({
          status: "success",
          message: "Stopped recording",
        });
      } catch (error) {
        sendResponse({
          status: "error",
          message: `Failed to stop recording: ${error.message}`,
        });
      }
      break;

    case "disable_speech":
      speechEnabled = false;
      if (synth.speaking) {
        synth.cancel();
      }
      sendResponse({
        status: "success",
        message: "Speech disabled",
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
