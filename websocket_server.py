import asyncio
import websockets
import json
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)

class ClientType(Enum):
    TAIPY = "taipy"
    EXTENSION = "extension"

class Client:
    def __init__(self, websocket, client_type):
        self.websocket = websocket
        self.client_type = client_type

# Store connected clients
taipy_client = None
extension_client = None

async def handle_client(websocket):
    global taipy_client, extension_client
    client = None

    try:
        # Determine client type
        client_type_msg = await websocket.recv()
        client_type_data = json.loads(client_type_msg)
        client_type = ClientType(client_type_data.get('client_type'))

        if client_type == ClientType.TAIPY:
            taipy_client = Client(websocket, ClientType.TAIPY)
            client = taipy_client
            logging.info("Taipy client connected")
        elif client_type == ClientType.EXTENSION:
            extension_client = Client(websocket, ClientType.EXTENSION)
            client = extension_client
            logging.info("Extension client connected")

        async for message in websocket:
            try:
                data = json.loads(message)
                logging.info(f"Received message from {client.client_type.value}: {data}")

                # Forward the message to the other client
                if client.client_type == ClientType.TAIPY and extension_client:
                    await extension_client.websocket.send(message)
                elif client.client_type == ClientType.EXTENSION and taipy_client:
                    await taipy_client.websocket.send(message)
                else:
                    logging.warning(f"No {ClientType.EXTENSION.value if client.client_type == ClientType.TAIPY else ClientType.TAIPY.value} client connected to forward the message")

            except json.JSONDecodeError:
                logging.error("Invalid JSON received")

    except websockets.exceptions.ConnectionClosed:
        logging.info(f"{client.client_type.value if client else 'Unknown'} client connection closed")
    finally:
        if client:
            if client.client_type == ClientType.TAIPY:
                taipy_client = None
            else:
                extension_client = None
            logging.info(f"{client.client_type.value} client disconnected")

async def main():
    server = await websockets.serve(handle_client, "localhost", 8765)
    logging.info("WebSocket server started on ws://localhost:8765")
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())

