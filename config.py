import logging
import json
import os
import sys
from pathlib import Path

import pdb

_XDG_CONFIG_HOME = "XDG_CONFIG_HOME"
_APPDATA = "APPDATA"
_HOME = "HOME"
_DIRNAME = "ascii-tetris"
_CONF_FILE_NAME = "ascii-tetris.json"

class ConfigFile:
    """A class that represents a configuration file"""

    def __init__(self):
        self.filename =self._get_filename()
        dirname = os.path.dirname(self.filename)
        if os.path.exists(dirname):
            if not os.path.isdir(dirname):
                raise RuntimeError(f"The dirname'{dirname}' exists but ain't no dir")
        else:
            os.makedirs(dirname)


    def read(self) -> dict:
        """Read the config file, might return empty dict
        when it wasn't present before."""
        ret = {}
        filename = self._get_filename()
        try:
            logging.info(f"Trying to open {filename} for reading")
            with open(filename, 'r') as infile:
                ret = json.load(infile)
        except IOError as error:
            logging.error(str(error))
        return ret

    def write(self, config:dict)->None:
        """Read the config file, might return empty dict
        when it wasn't present before."""
        filename = self._get_filename()
        logging.info(f"Trying to open {filename} for reading")
        with open(filename, 'w') as outfile:
            json.dump(config, outfile, indent=4)

    @staticmethod
    def _get_filename()->str:
        """Get and/or create the config file name"""
        filename = None
        if _XDG_CONFIG_HOME in os.environ:
            filename = Path(os.environ[_XDG_CONFIG_HOME])
            filename = filename / _DIRNAME / _CONF_FILE_NAME
        elif _HOME in os.environ:
            filename = Path(os.environ[_HOME])
            filename = filename / ".config/" / _DIRNAME / _CONF_FILE_NAME
        elif _APPDATA in os.environ:
            filename = Path(os.environ[_APPDATA])
            filename = filename / _DIRNAME / _CONF_FILE_NAME
        else:
            raise RuntimeError("No suitable folder for config data found.")

        return str(filename)
