import curses


def main(stdscr):
    # Clear screen
    stdscr.clear()

    # Make the text bold and large
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.addstr(5, 10, "BIG TEXT", curses.A_BOLD | curses.color_pair(1))

    stdscr.refresh()
    stdscr.getch()


# Initialize curses
curses.wrapper(main)
