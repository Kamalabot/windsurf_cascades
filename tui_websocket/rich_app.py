import asyncio
import websockets
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from itertools import zip_longest
import pyfiglet

# WebSocket server address
SERVER_URI = "ws://localhost:8765"

console = Console()


async def receive_message(websocket):
    buffer = []  # Buffer to hold the received numbers

    while True:
        try:
            message = await websocket.recv()
            buffer.extend(message.split(","))  # Add received numbers to buffer
            # print("buffer", buffer)
            if len(buffer) >= 16:
                # Create four 2x2 tables
                small_boxes = []
                for i in range(4):
                    table = Table(
                        show_header=False, box=None, expand=True, padding=(1, 4)
                    )
                    # for row in zip_longest(*[iter(buffer[i : (i + 1)])], fillvalue=""):
                    #     table.add_row(*[f"[bold cyan]{num}[/bold cyan]" for num in row])
                    f = pyfiglet.Figlet(font="dos_rebel", width=20)
                    # f = pyfiglet.Figlet(font="calvin_s", width=30)
                    # table.add_row(f"[bold cyan]{buffer[i]}[/bold cyan]")
                    table.add_row(f.renderText(buffer[i]))
                    small_boxes.append(
                        Panel(table, border_style="cyan", padding=(1, 2))
                    )

                # Arrange the small boxes in a grid
                grid_layout = Layout()
                grid_layout.split_column(
                    Layout(name="row1", ratio=1),
                    # Layout(name="row2", ratio=1),
                )
                grid_layout["row1"].split_row(
                    Layout(small_boxes[0], size=45), Layout(small_boxes[1], size=45)
                )
                # grid_layout["row2"].split_row(
                #     Layout(small_boxes[2], size=45), Layout(small_boxes[3], size=35)
                # )

                # Wrap the grid in a larger box
                large_box = Panel(
                    grid_layout,
                    title="[bold magenta]Numbers[/bold magenta]",
                    border_style="magenta",
                    padding=(1, 5),
                )

                console.clear()
                console.print(large_box, height=console.height)
                buffer.clear()  # Reset buffer

        except websockets.exceptions.ConnectionClosed:
            console.print("[red]Connection to server closed.[/red]")
            break


async def main():
    async with websockets.connect(SERVER_URI) as websocket:
        # Start receiving messages
        await receive_message(websocket)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("[yellow]Application stopped manually.[/yellow]")
