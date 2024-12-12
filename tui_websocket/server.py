import asyncio
import websockets
import random

connected_clients = set()


async def send_random_numbers(websocket):
    while True:
        try:
            # Generate four random numbers
            numbers = [random.randint(1, 100) for _ in range(4)]
            message = ",".join(
                map(str, numbers)
            )  # Join numbers as a comma-separated string
            await websocket.send(message)
            await asyncio.sleep(0.5)  # Send numbers every 0.5 seconds
        except websockets.exceptions.ConnectionClosedOK:
            print("Client disconnected gracefully.")
            break
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
            break


async def echo(websocket):
    # Register client
    connected_clients.add(websocket)
    try:
        # Start sending random numbers to the client
        await send_random_numbers(websocket)
    finally:
        # Unregister client
        connected_clients.remove(websocket)


async def main():
    async with websockets.serve(echo, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped manually.")
