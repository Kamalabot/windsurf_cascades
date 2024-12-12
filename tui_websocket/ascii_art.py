import pyfiglet

from rich.console import Console

console = Console()
font_list = pyfiglet.FigletFont.getFonts()
# print(font_list)
ascii_art = pyfiglet.figlet_format("BIG TEXT", font="5x8")
console.print(f"[bold cyan]{ascii_art}[/bold cyan]")
