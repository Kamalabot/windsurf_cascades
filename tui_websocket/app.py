import asyncio
import websockets
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from itertools import zip_longest

# WebSocket server address
SERVER_URI = "ws://localhost:8765"


async def send_message(websocket):
    session = PromptSession()
    while True:
        message = await session.prompt_async("You: ")
        await websocket.send(message)


async def receive_message(websocket):
    buffer = []  # Buffer to hold the received numbers

    while True:
        try:
            message = await websocket.recv()
            buffer.append(message)

            if len(buffer) >= 4:
                # Group numbers into 2x2 columns
                formatted_output = []
                for row in zip_longest(*[iter(buffer)] * 2, fillvalue=""):
                    formatted_row = "  ".join(
                        [f"\x1b[1m{num}\x1b[0m" for num in row]
                    )  # Bold formatting
                    formatted_output.append(formatted_row)

                # Clear screen and display formatted output
                print_formatted_text(
                    FormattedText([("", ""), ("", "\n".join(formatted_output))])
                )
                buffer = []  # Reset buffer

        except websockets.exceptions.ConnectionClosed:
            print("Connection to server closed.")
            break


async def main():
    async with websockets.connect(SERVER_URI) as websocket:
        # Start sending and receiving messages concurrently
        await asyncio.gather(
            # send_message(websocket),
            receive_message(websocket),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Chat application stopped manually.")
