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

