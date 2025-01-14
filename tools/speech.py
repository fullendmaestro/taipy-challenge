from .websocket_client import send_websocket_message
import asyncio

def play_response(text):
    response = asyncio.run(send_websocket_message("play_response", {"text": text}))

def start_recording():
    response = asyncio.run(send_websocket_message("start_recording"))

def stop_recording():
    response = asyncio.run(send_websocket_message("stop_recording"))