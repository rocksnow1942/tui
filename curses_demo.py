"""Having fun with curses!

Curses is a native python library for creating text-based user interfaces.
It is low-level and somewhat clunky, but it is very powerful.

I don't recommend using curses for anything serious; instead, consider using
more modern libraries like prompt_toolkit or textual.
"""

import curses
import contextlib
from collections.abc import Iterator


def main(stdscr: curses.window) -> None:
    """Main function to run the curses application."""
    # Clear screen
    stdscr.clear()

    # Print a message in the center of the screen
    height, width = stdscr.getmaxyx()
    message = "Hello, Curses!" * 20
    x = width // 2 - len(message) // 2
    y = height // 2

    stdscr.addstr(y, max(x, 0), message, curses.color_pair(3))

    # Refresh the screen to show the message
    stdscr.refresh()

    # Wait for user input before exiting
    stdscr.getch()


def run_curses_app() -> None:
    """Wrapper to run the curses application."""
    curses.wrapper(main)


@contextlib.contextmanager
def init_screen() -> Iterator[curses.window]:
    """Context manager to initialize and terminate the curses screen.

    This is the low-level equivalent of curses.wrapper.
    """
    stdscr = curses.initscr()
    curses.noecho()  # Turn off automatic echoing of keys to the screen
    curses.cbreak()  # React to keys instantly, without Enter
    stdscr.keypad(True)  # Enable special keys to be interpreted (like arrows)
    try:
        yield stdscr
    except Exception:
        raise
    finally:
        # restore terminal behavior before closing
        curses.echo()
        curses.nocbreak()
        stdscr.keypad(False)
        curses.endwin()


if __name__ == "__main__":
    run_curses_app()
