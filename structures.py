"""
Collection of namedtuples used across the application
"""

from collections import namedtuple

Options = namedtuple(
    "Options",
    [
        "csvfolder",
        "statistics",
        "maskfolder",
        "diagnoalconnectivity",
        "threshold",
        "filetype"
    ])

ChannelInfo = namedtuple("ChannelInfo", "folder, unique, datafolder")
