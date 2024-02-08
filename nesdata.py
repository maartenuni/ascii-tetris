"""This module defines some data regarding the NES, this data is adopted
from https://listfist.com/list-of-tetris-levels-by-speed-nes-ntsc-vs-pal
"""

# These are frame rates of the NES, not PAL, nor NTSC
# The NES frames are different for both television signals though.
PAL_FPS = 50.0070
NTSC_FPS = 60.0988

PAL_FRAME_DUR = 1.0 / PAL_FPS
NTSC_FRAME_DUR = 1.0 / NTSC_FPS

# number of frames it takes for the tetrominoes to fall one row for NTSC
NTSC_NF_DESCENT = {
    0: 48,
    1: 43,
    2: 38,
    3: 33,
    4: 28,
    5: 23,
    6: 18,
    7: 13,
    8: 8,
    9: 6,
    10: 5,
    11: 5,
    12: 5,
    13: 4,
    14: 4,
    15: 4,
    16: 3,
    17: 3,
    18: 3,
    19: 2,
    20: 2,
    21: 2,
    22: 2,
    23: 2,
    24: 2,
    25: 2,
    26: 2,
    27: 2,
    28: 2,
}

for i in range(29, 300):
    NTSC_NF_DESCENT[i] = 1

PAL_NF_DESCENT = {
    0: 36,
    1: 32,
    2: 29,
    3: 25,
    4: 22,
    5: 18,
    6: 15,
    7: 11,
    8: 7,
    9: 5,
    10: 4,
    11: 4,
    12: 4,
    13: 3,
    14: 3,
    15: 3,
    16: 2,
    17: 2,
    18: 2,
}

for i in range(19, 300):
    PAL_NF_DESCENT[i] = 1
