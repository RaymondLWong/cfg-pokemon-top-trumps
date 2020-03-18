import asyncio
import websockets

DEFAULT_PORT = 8765


async def hello():
    uri = f'ws://localhost:{DEFAULT_PORT}'
    async with websockets.connect(uri) as ws:
        name = input("What's your name? ")

        await ws.send(name)
        print(f"> {name}")

        greeting = await ws.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
