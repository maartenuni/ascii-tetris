import json
import os
from pathlib import Path

_XDG_CONFIG_HOME = "XDG_CONFIG_HOME"
_APPDATA = "APPDATA"
_HOME = "HOME"
_DIRNAME = "ascii-tetris"


def _create_file_from_env_var(envar: str, dirname=_DIRNAME) -> str:
    """This creates the filename, but has an important side effect
    that if the config folder doesn't exits it is created, its an error
    when the directory exists but ain't no folder."""
    conf_name = Path(os.environ[envar])
    dirname = conf_name / "ascii-tetris"
    filename = "ascii-tetris.json"
    if not dirname.exists():
        os.makedirs(dirname)
    if not dirname.is_dir():
        raise RuntimeError(f"'{dirname}': exists but is not a directory")
    final_name = str(dirname / filename)
    return final_name


class ConfigFile:
    """A class that represents a configuration file"""

    def read(self) -> dict:
        """Read the config file, might return empty dict
        when it wasn't present before."""
        ret = {}
        try:
            with open(self._get_filename(), 'r') as infile:
                ret = json.load(infile)
        finally:
            return ret

    def write(self, config:dict)->None:
        """Read the config file, might return empty dict
        when it wasn't present before."""
        with open(self._get_filename(), 'w') as outfile:
            json.dump(config, outfile, indent=4)


    @staticmethod
    def _get_filename():
        """Get and/or create the config file name"""
        filename = None
        if _XDG_CONFIG_HOME in os.environ:
            filename = _create_file_from_env_var(_XDG_CONFIG_HOME)
        elif _APPDATA in os.environ:
            filename = _create_file_from_env_var(_APPDATA)
        else:
            filename = _create_file_from_env_var(_HOME, "." + _DIRNAME)

        return filename
