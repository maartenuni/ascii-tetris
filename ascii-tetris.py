#!/usr/bin/env python3
"""Play Tetᴙis in ascii-style"""

import copy
import curses
import argparse as ap
import sys
from typing import Dict
import time
import logging

from config import ConfigFile
from tetris import Tetris, LINE, MEL, EL, CUBE, MES, TABLE, ES


# Dict that maps a letter to a terminal color
COLOR_PAIRS: Dict[str, int] = {"!": curses.A_DIM}

# Store config info
_config = None


def _draw_in_color(stdscr, tgame: Tetris) -> None:
    """Draw the TetrisGame in color"""
    strrep = str(tgame)

    for row, line in enumerate(strrep.split("\n")):
        for col, char in enumerate(line):
            try:
                stdscr.addstr(row, col, char, COLOR_PAIRS[char])
            except KeyError:
                stdscr.addstr(
                    row, col, char, curses.color_pair(0)
                )  # default color pair


def _game_loop(args, tgame: Tetris, stdscr, win, next_win=None, score_win=None) -> None:
    """Runs the game loop until the user exits the game or
    is game over."""
    global _config
    ACTIONS = {
        "KEY_LEFT": tgame.move_left,
        "KEY_RIGHT": tgame.move_right,
        "KEY_DOWN": tgame.increment,
        "KEY_UP": tgame.rotate,
        "q": tgame.set_game_over,
        " ": tgame.drop,
    }
    start = time.time()
    running_time_inc = start

    win.nodelay(True)

    did_something = True  # draw something at first iteration
    score = -1
    next_tile = None
    level = tgame.level

    highscore = 0
    player = ""
    try:
        highscore = _config["score"]["highscore"]
        player = _config["score"]["player"]
    except KeyError as _error:
        _config["score"] = {"highscore": 0, "player": ""}
        highscore = _config["score"]["highscore"]
        player = _config["score"]["player"]

    while not tgame.game_over:
        temp_level = level
        key = "some key"

        try:
            key = stdscr.getkey()
            did_something = True
        except Exception:  # No key has been pressed.
            pass

        if key in ACTIONS:
            ACTIONS[key]()
            did_something = True

        now = time.time()
        if now - running_time_inc > tgame.fall_duration:  # make the tetrominoe fall
            logging.debug(f"now = {now}, inc_timeout = {tgame.fall_duration}")
            tgame.increment()
            running_time_inc += tgame.fall_duration
            did_something = True

        time.sleep(0.001)

        if did_something:  # only draw at change of state
            win.clear()  ## clear screen
            if not args.black_and_white:
                _draw_in_color(win, tgame)
            else:
                win.addstr(str(tgame))
            win.refresh()
            did_something = False

        if next_win and tgame.next != next_tile:
            next_tile = copy.deepcopy(tgame.next)
            next_win.clear()
            if not args.black_and_white:
                _draw_in_color(next_win, next_tile)
            else:
                next_win.addstr(str(next_tile))
            next_win.refresh()

        if score_win and tgame.score != score or temp_level != level:
            # update the score_win if we have one
            score = tgame.score
            level = temp_level
            score_win.clear()
            score_win.addstr(f"Score:\n  {score}\n")
            score_win.addstr(f"Level:\n  {level}\n")
            score_win.addstr(f"High score:\n  {highscore}")
            score_win.refresh()

        if level != tgame.level:
            level = tgame.level


def _curses_main(stdscr, args) -> int:
    """Play tetris using curses. This function sets up the windows
    and prepares the game to run."""

    tgame = Tetris(style=args.style)

    width, height = curses.COLS, curses.LINES

    if height < Tetris.str_height() or width < Tetris.str_width():
        raise RuntimeError(
            "Terminal size is {} * {}, min = {}*{}".format(
                width, height, Tetris.str_width(), Tetris.str_height()
            )
        )

    stdscr.nodelay(True)

    if curses.has_colors():  # init global color pairs
        logging.info("Running with colors")
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        COLOR_PAIRS[LINE.color] = curses.color_pair(1) | curses.A_BOLD

        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        COLOR_PAIRS[MEL.color] = curses.color_pair(2) | curses.A_BOLD

        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        COLOR_PAIRS[EL.color] = curses.color_pair(3) | curses.A_BOLD

        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        COLOR_PAIRS[CUBE.color] = curses.color_pair(4) | curses.A_BOLD

        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)
        COLOR_PAIRS[ES.color] = curses.color_pair(5) | curses.A_BOLD

        curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        COLOR_PAIRS[TABLE.color] = curses.color_pair(6) | curses.A_BOLD

        curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
        COLOR_PAIRS[MES.color] = curses.color_pair(7) | curses.A_BOLD
    else:
        logging.info("Running without colors")
        args.black_and_white = True

    board_win = curses.newwin(Tetris.str_height() + 1, Tetris.str_width() + 1)
    next_win = curses.newwin(8, 8, 2, Tetris.str_width() + 4)
    score_win = curses.newwin(10, 20, Tetris.str_height() // 2, Tetris.str_width() + 4)

    _game_loop(args, tgame, stdscr, board_win, next_win, score_win)

    return tgame.score


def main():
    """Main entry point for a text based Tetris"""
    loglevelmap = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }
    cmdparser = ap.ArgumentParser("Tetris", "Play Tetᴙis in ASCII style", "Enjoy!!")
    cmdparser.add_argument(
        "-b", "--black-and-white", action="store_true", help="Play in color"
    )
    cmdparser.add_argument(
        "-l", "--log-file", type=str, help="specify a log file to log to."
    )
    cmdparser.add_argument(
        "-L",
        "--log-level",
        type=str,
        choices=loglevelmap.keys(),
        default="info",
        help="specify the desired loglevel.",
    )
    cmdparser.add_argument(
        "-s",
        "--style",
        choices=["NTSC", "PAL"],
        default="NTSC",
        help=(
            "Determines the emulating a NTSC or PAL NES, this affects the "
            "speed that the tetrominoes are falling"
        ),
    )

    args = cmdparser.parse_intermixed_args()

    if args.log_file:
        level = loglevelmap[args.log_level]
        logging.basicConfig(filename=args.log_file, level=logging.DEBUG)
        logging.info("logging with loglevel: {}".format(args.log_level.upper()))

    try:
        global _config
        _config = ConfigFile().read()

        score = curses.wrapper(_curses_main, args)

        if score > _config["score"]["highscore"]:
            player = input("New highscore enter player name:")
            _config["score"] = {"highscore": score, "player": player}
            ConfigFile().write(_config)
        print(f"Score = {score}\nGame Over...")
    except RuntimeError as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
