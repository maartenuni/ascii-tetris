
import curses as c


def mainloop(stdscr):
    """Print keys that are typed"""

    stdscr.nodelay(True) # don't wait for enter

    stdscr.addstr("Press q to quit")
    stdscr.refresh()

    char = ""

    while True:
        if char == "q":
            break

        try:
            char = stdscr.getkey()
            stdscr.clear()
            stdscr.addstr("You typed: " + char)
            stdscr.refresh()
        except:
            pass
        



c.wrapper(mainloop)
