import asyncio
from .websocket_client import send_websocket_message

def list_tabs():
    response = asyncio.run(send_websocket_message("list_tabs"))
    print("LIST TABS")
    return response['message']

def open_tab(url):
    response = asyncio.run(send_websocket_message("open_tab", {"url": url}))
    print("OPENING TAB", response)
    return response

def close_tab(tab_id):
    response = asyncio.run(send_websocket_message("close_tab", {"tab_id": tab_id}))
    print("CLOSING TAB")
    return response['message']

def switch_tab(tab_id):
    response = asyncio.run(send_websocket_message("switch_tab", {"tab_id": tab_id}))
    print("SWITCHING TAB")
    return response['message']

def get_tab_content(_):
    response = asyncio.run(send_websocket_message("get_tab_content"))
    print("GET TAB CONTENT")
    return response['message']


# Bookmark management
def list_bookmarks():
    response = asyncio.run(send_websocket_message("list_bookmarks"))
    print("LISTING BOOKMARKS")
    return response['message']

def add_bookmark(url, title):
    response = asyncio.run(send_websocket_message("add_bookmark", {"url": url, "title": title}))
    print("ADDING BOOKMARK")
    return response['message']

def delete_bookmark(id):
    response = asyncio.run(send_websocket_message("delete_bookmark", {"id": id}))
    print("DELETING BOOKMARK")
    return response['message']

# History management
def search_history(query, max_results=10):
    response = asyncio.run(send_websocket_message("search_history", {
        "query": query,
        "maxResults": max_results
    }))
    print("SEARCHING HISTORY")
    return response['message']

def delete_history_item(url):
    response = asyncio.run(send_websocket_message("delete_history_item", {"url": url}))
    print("DELETING HISTORY ITEM")
    return response['message']

# Download management
def list_downloads():
    response = asyncio.run(send_websocket_message("list_downloads"))
    print("LISTING DOWNLOADS")
    return response['message']

def download_file(url, filename=None):
    response = asyncio.run(send_websocket_message("download_file", {
        "url": url,
        "filename": filename
    }))
    print("DOWNLOADING FILE")
    return response['message']

# Window management
def create_window(url=None, incognito=False):
    response = asyncio.run(send_websocket_message("create_window", {
        "url": url,
        "incognito": incognito
    }))
    print("CREATING WINDOW")
    return response['message']

def list_windows():
    response = asyncio.run(send_websocket_message("list_windows"))
    print("LISTING WINDOWS")
    return response['message']

# Clipboard operations
def copy_to_clipboard(text):
    response = asyncio.run(send_websocket_message("copy_to_clipboard", {"text": text}))
    print("COPYING TO CLIPBOARD")
    return response['message']

def read_from_clipboard():
    response = asyncio.run(send_websocket_message("read_from_clipboard"))
    print("READING FROM CLIPBOARD")
    return response['message']

# Browser settings
def get_zoom_level():
    response = asyncio.run(send_websocket_message("get_zoom_level"))
    print("GETTING ZOOM LEVEL")
    return response['message']

def set_zoom_level(zoom_factor):
    response = asyncio.run(send_websocket_message("set_zoom_level", {"zoomFactor": zoom_factor}))
    print("SETTING ZOOM LEVEL")
    return response['message']