"""Classes helpfull to implement Tetris"""

from typing import List
import random as r
import copy
import nesdata as nd
import logging as log


class Tile:
    """A tile represents one of the faces of a Tetrominoe"""

    def __init__(self, boolarray: List[List[int]]):
        self.height = 0
        self.width = 0

        self._validate_boolarray(boolarray)
        self.boolarray = boolarray

    def __repr__(self) -> str:
        return "Tile(" + repr(self.boolarray) + ")"

    @property
    def array(self) -> List[List[int]]:
        """short for self.boolarray"""
        return self.boolarray

    def __eq__(self, rhs) -> bool:
        if self is rhs:
            return True
        if not isinstance(rhs, Tile):
            return False
        return (
            self.height == rhs.height
            and self.width == rhs.width
            and self.array == rhs.array
        )

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

    def __eq__(self, rhs) -> bool:
        if self is rhs:
            return True
        if not isinstance(rhs, Tetrominoe):
            return False
        return (
            self.rotation == rhs.rotation
            and self.color == rhs.color
            and self.tiles == rhs.tiles
        )

    def __repr__(self) -> str:
        return "Tetrominoe(" + repr(self.tiles) + ", " + repr(self.color) + ")"

    def __str__(self) -> str:
        """Creates a string representation of the current tile"""
        cur_tile = self.tile()

        tile_board = [
            "".join([self.color + " " if cell else "  " for cell in line])
            for line in cur_tile.array
        ]

        strrep = "\n".join(tile_board)

        return strrep

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

    styles = ["NTSC", "PAL"]

    def __init__(self, width=_DEF_WIDTH, height=_DEF_HEIGHT, style="NTSC"):
        if style not in Tetris.styles:
            raise ValueError(f"style should be one of {Tetris.styles}")
        self.width, self.height = width, height
        self._style = style
        self._tetrominoes = [LINE, MEL, EL, CUBE, ES, TABLE, MES]
        self.current = copy.deepcopy(r.choice(self._tetrominoes))
        self.next = copy.deepcopy(r.choice(self._tetrominoes))
        self.tet_height = 0
        # Used as index, hence use integer division
        self.tet_width = self.width // 2 - self.current.width // 2
        self._board = [
            [" " for column in range(self.width)] for row in range(self.height)
        ]
        self.game_over = False
        self._score = 0
        self._num_successive = 0
        self.lines = 0

    def _paint_current(self, board: List[List[str]]) -> None:
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
        ret = "".join(["-" for row in range(self.width * 2 + 1)]) + "\n"
        copy = self._copy_board()

        # "paint" current in copy of board
        self._paint_current(copy)

        for row in copy:
            dotted_row = [char + "!" for char in row]
            dotted_row[-1] = dotted_row[-1][0]  # strip trailing .
            ret += "".join(["|", "".join(dotted_row), "|\n"])
        ret += "".join(["-" for row in range(self.width * 2 + 1)])
        return ret

    def _copy_board(self) -> List[List[str]]:
        """Returns a temporary copy of the board"""
        copy = [[line[i] for i in range(len(line))] for line in self._board]
        return copy

    def _setup_new(self):
        """Use the next tetrominoe and compute new next"""
        self.current = self.next
        self.next = copy.deepcopy(r.choice(self._tetrominoes))
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

    def _calc_score(self, num_lines: int) -> int:
        """Compute the score for a number of lines cleared"""
        if not 0 < num_lines <= 4:
            raise ValueError("Num lines must be one of: [1,2,3,4]")
        scores = [40, 100, 300, 1200]
        return scores[num_lines - 1] * (self.level + 1)

    def _check_score(self):
        """Checks the whether some rows are complete. Updates
        the score and board accordingly.
        """
        collection = [row for row in range(len(self._board)) if self._is_row_full(row)]
        assert 0 <= len(collection) <= 4
        self.lines += len(collection)

        if not collection:
            return

        self._score += self._calc_score(len(collection))

        # clear full lines
        self._board = [
            row for index, row in enumerate(self._board) if index not in collection
        ]
        # create a set of empty lines
        empty = [[" " for col in range(self.width)] for row in range(len(collection))]
        # concat empty lines and board with full lines removed
        self._board = empty + self._board

    @property
    def score(self) -> int:
        """Get the score"""
        return self._score

    @property
    def level(self) -> int:
        """Get the current level"""
        return self.lines // 10

    @property
    def fall_duration(self) -> float:
        """Returns the duration when the block should fall for one level"""
        if self._style == "NTSC":
            num_frames = nd.NTSC_NF_DESCENT[self.level]
            return num_frames * (1 / nd.NTSC_FPS)
        elif self._style == "PAL":
            num_frames = nd.PAL_NF_DESCENT[self.level]
            return num_frames * (1 / nd.PAL_FPS)
        else:
            raise ValueError("Unexpected/unhandled value encountered")

    def increment(self) -> None:
        """Make the tetrominoe advance one position"""
        self.tet_height += 1
        if self._collision():
            self.tet_height -= 1
            self._paint_current(self._board)
            self._check_score()
            self._setup_new()

    def drop(self) -> None:
        """drop the tetrominoe as far to the bottom as possible"""
        last_height = self.tet_height
        log.info("dropping")
        while True:
            self.increment()
            log.debug(f"last_height = {last_height}, tet_height={self.tet_height}")
            if last_height >= self.tet_height:
                break
            last_height = self.tet_height

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

    def set_game_over(self):
        """Marks the game Game Over"""
        self.game_over = True

    @staticmethod
    def str_width():
        """Calculates the width of the __str___ representation"""
        side_bars = 2
        columns = 10
        num_dots = columns - 1
        return side_bars + columns + num_dots

    @staticmethod
    def str_height():
        """Calculates the height of the __str___ representation"""
        bars = 2
        rows = 20
        return bars + rows
