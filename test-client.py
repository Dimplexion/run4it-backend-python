import asyncio
import websockets
import sys

async def hello(uri, player_name):
    async with websockets.connect(uri) as websocket:
        await websocket.send(player_name)
        response = await websocket.recv()
        print(f'Response: {response}')

        await websocket.send(f"{player_name} test send")

        response = await websocket.recv()
        print(f'Response: {response}')
        
player_name = sys.argv[1]
asyncio.get_event_loop().run_until_complete(
    hello('ws://127.0.0.1:8765', player_name))


