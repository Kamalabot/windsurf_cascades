# Python TUI Packages

Text User Interfaces (TUIs) allow developers to create interactive command-line applications. Below are some popular Python packages for building TUIs, along with examples and links to their documentation.

## 1. **Curses**
- **Description**: A built-in library for creating TUIs in Python. It provides functions to control terminal display and handle keyboard input.
- **Example**:
    ```python
    import curses

    def main(stdscr):
        curses.curs_set(0)  # Hide the cursor
        stdscr.clear()      # Clear the screen
        stdscr.addstr(0, 0, "Hello, World!")  # Print text
        stdscr.refresh()    # Refresh the screen
        stdscr.getch()      # Wait for user input

    curses.wrapper(main)
    ```
- **Link**: [Curses Documentation](https://docs.python.org/3/library/curses.html)

## 2. **Rich**
- **Description**: A modern library for rich text and beautiful formatting in the terminal. It supports text styling, tables, progress bars, and more.
- **Example**:
    ```python
    from rich.console import Console

    console = Console()
    console.print("Hello, [bold magenta]World![/bold magenta]")
    ```
- **Link**: [Rich Documentation](https://rich.readthedocs.io/en/stable/)

## 3. **Textual**
- **Description**: A TUI framework for Python that allows you to build interactive applications using a modern approach with async support.
- **Example**:
    ```python
    from textual.app import App
    from textual.widgets import Button

    class MyApp(App):
        async def on_mount(self):
            button = Button("Click Me!")
            await self.view.dock(button)

    MyApp.run()
    ```
- **Link**: [Textual Documentation](https://textual.textualize.io/)

## 4. **Prompt Toolkit**
- **Description**: A library for building interactive command-line applications. It provides features like syntax highlighting, autocompletion, and multi-line editing.
- **Example**:
    ```python
    from prompt_toolkit import prompt

    user_input = prompt("Enter something: ")
    print(f"You entered: {user_input}")
    ```
- **Link**: [Prompt Toolkit Documentation](https://python-prompt-toolkit.readthedocs.io/en/master/)

## 5. **PyInquirer**
- **Description**: A library for creating interactive command-line interfaces with prompts and questions.
- **Example**:
    ```python
    from PyInquirer import prompt

    questions = [
        {
            'type': 'input',
            'name': 'name',
            'message': 'What is your name?',
        }
    ]

    answers = prompt(questions)
    print(f"Hello, {answers['name']}!")
    ```
- **Link**: [PyInquirer Documentation](https://github.com/CITGuru/PyInquirer)

## 6. **Urwid**
- **Description**: A library for creating console user interfaces with widgets and a flexible layout system.
- **Example**:
    ```python
    import urwid

    def exit_on_q(key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    text = urwid.Text("Hello, World!")
    fill = urwid.Filler(text, valign='middle')
    loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
    loop.run()
    ```
- **Link**: [Urwid Documentation](http://urwid.org/)

## Conclusion
These packages provide a range of options for building interactive TUIs in Python, each with its own strengths and use cases. Depending on your project requirements, you can choose the one that best fits your needs.