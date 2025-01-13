from websockets.asyncio.client import connect
import json

WEBSOCKET_URI = "ws://localhost:8765"

async def send_websocket_message(action, params=None):
    async with connect(WEBSOCKET_URI) as websocket:
        # Identify as Taipy client
        await websocket.send(json.dumps({"client_type": "taipy"}))

        message = {
            "action": action,
            "params": params or {}
        }
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        return json.loads(response)