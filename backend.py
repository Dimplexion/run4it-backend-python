import asyncio
import websockets

players_waiting = []
matches = {}
async def hello(player_websocket, path):
    global players_waiting
    global matches

    player_name = await player_websocket.recv()
    print("< {}".format(player_name))
    
    if len(players_waiting) == 0:
        players_waiting.append((player_name, player_websocket))
    else:
        opponent_name, opponent_websocket = players_waiting.pop()
        matches[player_websocket] = opponent_websocket
        matches[opponent_websocket] = player_websocket

        # Send the player names to both participants
        await matches[player_websocket].send(opponent_name)
        await matches[opponent_websocket].send(player_name)
        
    while True:
        if player_websocket in matches:
            async for message in player_websocket:
                await matches[player_websocket].send(message)
        else:
            print(f'{player_name} waiting for a match...')
            await asyncio.sleep(1)

PORT = 8765
print('Starting the server...')
start_server = websockets.serve(hello, 'localhost', PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


