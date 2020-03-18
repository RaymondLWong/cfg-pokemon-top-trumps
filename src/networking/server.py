import asyncio
import websockets

DEFAULT_PORT = 8765


async def hello(ws, path):
    name = await ws.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await ws.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "localhost", DEFAULT_PORT)

print('starting server...')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
