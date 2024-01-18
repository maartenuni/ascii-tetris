"""Classes helpfull to implement Tetris"""


from typing import List, Dict
import random as r
import sys
import curses
import time
import argparse as ap

# Dict that maps a letter to a terminal color
COLOR_PAIRS: Dict[str, int] = {}


class Tile:
    """A tile represents one of the faces of a Tetrominoe"""

    def __init__(self, boolarray: List[List[int]]):
        self.height = 0
        self.width = 0

        self._validate_boolarray(boolarray)
        self.boolarray = boolarray

    @property
    def array(self) -> List[List[int]]:
        """short for self.boolarray"""
        return self.boolarray

    def _validate_boolarray(self, arr):
        typeerr_msg = "Array isn't a rectangular list of list of int"
        valid_numbers = [0, 1]

        if not isinstance(arr, list):
            raise TypeError(typeerr_msg)

        self.height = len(arr)

        for intlist in arr:
            if not isinstance(intlist, list):
                raise TypeError(typeerr_msg)
            if len(intlist) != self.width and self.width != 0:
                raise ValueError("Arr isn't rectangular")
            self.width = len(intlist)
            for num in intlist:
                if num not in valid_numbers:
                    raise ValueError("Oops expected rectangular array with 0's and 1's")

        if not (0 < self.height < 5) and (0 < self.width < 5):
            raise ValueError(
                "Width and height are should be between in the range [1,4]"
            )


class Tetrominoe:
    """A class that represents the multiple faces of a Tetromino"""

    def __init__(self, tiles: List[Tile], color: str):
        self.rotation = 0
        self.color = color
        self.tiles = tiles

    def tile(self) -> Tile:
        """Returns a tuple with the list that holds the current Tile"""
        return self.tiles[self.rotation]

    def rotate_right(self) -> None:
        """Rotate the Tetrominoe to the right"""
        self.rotation = (self.rotation + 1) % len(self.tiles)

    def rotate_left(self) -> None:
        """Rotate the Tetromminoe to the left"""
        self.rotation = self.rotation - 1
        if self.rotation < 0:
            self.rotation = len(self.tiles) - 1

    def reset(self) -> None:
        """Resets rotation to orgin"""
        self.rotation = 0

    def orginal(self) -> Tile:
        """Get the original face of the Tetrominoe"""
        return self.tiles[0]

    @property
    def width(self):
        """Obtain the width given the current rotation"""
        return self.tiles[self.rotation].width

    @property
    def height(self):
        """Obtain the height given the current rotation"""
        return self.tiles[self.rotation].height


# Turn off black to improve readabilty

# fmt: off

# line Cyan
#         #
# #### or #
#         #
#         #

LINE1 = Tile([[1, 1, 1, 1]])
LINE2 = Tile([
    [1],
    [1],
    [1],
    [1]
])

LINE = Tetrominoe([LINE1, LINE2], "C")


# mirrored el Blue
# .#     #..    ##     ###
# .#  or ### or #.  or ..#
# ##            #.
MEL1 = Tile([
    [0, 1],
    [0, 1],
    [1, 1]
])
MEL2 = Tile([
    [1, 0, 0],
    [1, 1, 1]
])
MEL3 = Tile([
    [1, 1],
    [1, 0],
    [1, 0]
])
MEL4 = Tile([
    [1, 1, 1],
    [0, 0, 1]
])

MEL = Tetrominoe([MEL1, MEL2, MEL3, MEL4], "B")

# el orange
#  #.    ###    ##      ..#
#  #. or #.. or .#   or ###
#  ##           .#
EL1 = Tile([
    [1, 0],
    [1, 0],
    [1, 1]
])
EL2 = Tile([
    [1, 1, 1],
    [1, 0, 0]
])
EL3 = Tile([
    [1, 1],
    [0, 1],
    [0, 1]
])
EL4 = Tile([
    [0, 0, 1],
    [1, 1, 1]
])
EL = Tetrominoe([EL1, EL2, EL3, EL4], "O")

# Cube Yellow
# ##
# ##

CUBE1 = Tile([
    [1, 1],
    [1, 1]
])

CUBE = Tetrominoe([CUBE1], "Y")

# es Green
# #.     .##
# ## or  ##.
# .#

ES1 = Tile([
    [1, 0],
    [1, 1],
    [0, 1]
])
ES2 = Tile([
    [0, 1, 1],
    [1, 1, 0]
])

ES = Tetrominoe([ES1, ES2], "G")

# Table Purple
# .#.    #.    ###     #
# ### or ## or  #  or ##
#        #.            #

TABLE1 = Tile([
    [0, 1, 0],
    [1, 1, 1]
])
TABLE2 = Tile([
    [1, 0],
    [1, 1],
    [1, 0]
])
TABLE3 = Tile([
    [1, 1, 1],
    [0, 1, 0]
])
TABLE4 = Tile(
    [
        [0, 1],
        [1, 1],
        [0, 1],
    ]
)

TABLE = Tetrominoe([TABLE1, TABLE2, TABLE3, TABLE4], "P")


# mirrored es Red
# .#     ##.
# ## or  .##
# #.
MES1 = Tile([[0, 1], [1, 1], [1, 0]])
MES2 = Tile([[1, 1, 0], [0, 1, 1]])

MES = Tetrominoe([MES1, MES2], "R")

# fmt: on


_DEF_HEIGHT = 20
_DEF_WIDTH = 10


class Tetris:
    """Basic playing board for playing tetris"""

    def __init__(self, width=_DEF_WIDTH, height=_DEF_HEIGHT):
        self.width, self.height = width, height
        self._tetrominoes = [LINE, MEL, EL, CUBE, ES, TABLE, MES]
        self.current = r.choice(self._tetrominoes)
        self.next = r.choice(self._tetrominoes)
        self.tet_height = 0
        # Used as index, hence use integer division
        self.tet_width = self.width // 2 - self.current.width // 2
        self._board = [
            [" " for column in range(self.width)] for row in range(self.height)
        ]
        self.game_over = False
        self._score = 0
        self._num_successive = 0

    def _paint(self, board: List[List[str]]) -> None:
        """Paint the current in the board. Board maybe a copy
        or self._board, in the latter case the state of the Tetris window
        is updated"""
        tile = self.current.tile()

        for row in range(tile.height):
            for col in range(tile.width):
                copy_col = self.tet_width + col
                copy_row = self.tet_height + row
                if tile.array[row][col]:
                    board[copy_row][copy_col] = self.current.color

    def __str__(self) -> str:
        """Return a string repr of self"""
        ret = "".join(["-" for row in range(self.width + 2)]) + "\n"
        copy = self._copy_board()

        # "paint" current in copy of board
        self._paint(copy)

        for row in copy:
            ret += "".join(["|", "".join(row), "|\n"])
        ret += "".join(["-" for row in range(self.width + 2)])
        return ret

    def _copy_board(self) -> List[List[str]]:
        """Returns a temporary copy of the board"""
        copy = [[line[i] for i in range(len(line))] for line in self._board]
        return copy

    def _setup_new(self):
        """Use the next tetrominoe and compute new next"""
        self.current = self.next
        self.next = r.choice(self._tetrominoes)
        self.tet_height = 0
        self.tet_width = self.width // 2 - self.current.width // 2
        if self._collision():
            self.game_over = True

    def _collision(self) -> bool:
        """Computes whether the current state represents a collision"""
        if self.tet_width < 0:  # collison with left wall
            return True
        if (
            self.tet_width + self.current.width > self.width
        ):  # collision with right wall
            return True
        if self.tet_height + self.current.height > self.height:
            return True

        tile = self.current.tile()
        for row in range(tile.height):
            for col in range(tile.width):
                bcol = self.tet_width + col  # indices on the board
                brow = self.tet_height + row
                if tile.array[row][col] and self._board[brow][bcol] != " ":
                    return True
        return False

    def _is_row_full(self, row) -> bool:
        """Checks whether the row is full"""
        if " " in self._board[row]:
            return False
        return True

    def _check_score(self):
        """Checks the whether some rows are complete. Updates
        the score and board accordingly.
        """
        scores = [100, 200, 400, 800]

        collection = [row for row in range(len(self._board)) if self._is_row_full(row)]
        assert 0 <= len(collection) <= 4

        if not collection:
            return

        score = scores[len(collection) - 1]
        if len(collection) == 4:
            self._num_successive += 1
        else:
            self._num_successive = 0

        score += 1200 * self._num_successive
        self._score += score

        # clear full lines
        self._board = [
            row for index, row in enumerate(self._board) if index not in collection
        ]
        # create a set of empty lines
        empty = [[" " for col in range(self.width)] for row in range(len(collection))]
        # concat empty lines and board with full lines removed
        self._board = empty + self._board

    @property
    def score(self):
        return self._score

    def increment(self):
        """Make the tetrominoe advance one position"""
        self.tet_height += 1
        if self._collision():
            self.tet_height -= 1
            self._paint(self._board)
            self._check_score()
            self._setup_new()

    def move_left(self) -> None:
        """Moves the current tetrominoe to the left if it
        doesn't result in a collision"""
        self.tet_width -= 1
        if self._collision():
            self.tet_width += 1

    def move_right(self) -> None:
        """Moves the current tetrominoe to the left if it
        doesn't result in a collision"""
        self.tet_width += 1
        if self._collision():
            self.tet_width -= 1

    def rotate(self):
        """Rotate the current widget"""
        self.current.rotate_right()
        if self._collision():
            self.current.rotate_left()


def _draw_in_color(stdscr, tgame: Tetris) -> None:
    """Draw the TetrisGame in color"""
    strrep = str(tgame)

    for row, line in enumerate(strrep.split("\n")):
        for col, char in enumerate(line):
            try:
                stdscr.addstr(row, col, char, curses.color_pair(COLOR_PAIRS[char]))
            except KeyError:
                stdscr.addstr(
                    row, col, char, curses.color_pair(0)
                )  # default color pair


def _curses_main(stdscr, args) -> int:
    """Play tetris using curses"""

    tgame = Tetris()

    actions = {
        "KEY_LEFT": tgame.move_left,
        "KEY_RIGHT": tgame.move_right,
        "KEY_DOWN": tgame.increment,
        "KEY_UP": tgame.rotate,
    }

    stdscr.nodelay(True)
    if args.color:
        if curses.has_colors():  # init global color pairs
            COLOR_PAIRS[LINE.color] = 1
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

            COLOR_PAIRS[MEL.color] = 2
            curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)

            COLOR_PAIRS[EL.color] = 3
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

            COLOR_PAIRS[CUBE.color] = 4
            curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

            COLOR_PAIRS[ES.color] = 5
            curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

            COLOR_PAIRS[TABLE.color] = 6
            curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

            COLOR_PAIRS[MES.color] = 7
            curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
        else:
            print("Running without colors", file=sys.stderr)
            args.color = False

    start = time.time()
    running_time = start

    did_something = True  # draw something at first iteration

    while not tgame.game_over:
        key = "some key"

        try:
            key = stdscr.getkey()
            did_something = True
        except Exception:
            pass

        if key in actions:
            actions[key]()
            did_something = True

        now = time.time()
        if now - running_time > 1.0:
            tgame.increment()
            running_time += 1.0
            did_something = True
        time.sleep(0.025)

        if did_something:  # only draw at change of state
            stdscr.clear()  ## clear screen
            if args.color:
                _draw_in_color(stdscr, tgame)
            else:
                stdscr.addstr(str(tgame))
            # stdscr.refresh()
            did_something = False

    return tgame.score


def main():
    """Main entry point for a text based Tetris"""
    cmdparser = ap.ArgumentParser("Tetris", "Play Tetris in ASCII style", "Enjoy!!")
    cmdparser.add_argument("-c", "--color", action="store_true", help="Play in color")

    args = cmdparser.parse_intermixed_args()

    score = curses.wrapper(_curses_main, args)
    print(f"Score = {score}\nGame Over...")


if __name__ == "__main__":
    main()
