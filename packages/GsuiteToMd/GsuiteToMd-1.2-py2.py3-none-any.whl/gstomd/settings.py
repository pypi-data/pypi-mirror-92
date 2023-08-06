import logging
import logging.config
from yaml import YAMLError, load

logger = logging.getLogger(__name__)

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

SETTINGS_FILE = "settings.yaml"

DEFAULT_SETTINGS = {
    "pydrive_settings": "pydrive_settings.yaml",
    "dest_folder": "./gstomd",
    "root_folder_id": "",
    "root_folder_name": "",
    "drive_id": "",
    "collections": [],
}


class SettingsError(IOError):
    """Error while loading/saving settings"""


class InvalidConfigError(IOError):
    """Error trying to read client configuration."""


def LoadSettingsFile(filename=SETTINGS_FILE):
    """Loads settings file in yaml format given file name.

    :param filename: path for settings file. 'settings.yaml' by default.
    :type filename: str.
    :raises: SettingsError
    """
    try:
        stream = open(filename, "r")
        data = load(stream, Loader=Loader)
    except (YAMLError, IOError) as e:
        from os import listdir

        logger.debug("in current directory : %s", listdir("."))
        raise SettingsError(e) from e
    return data


def SetupLogging(
    filename="logging.yaml", default_level=logging.DEBUG,
):
    """initialize logging

    Args:
        filename name (str, optional). the configuration file name
        default_level ( optional):  Defaults to logging.DEBUG.
    """
    try:
        log_cfg = LoadSettingsFile(filename=filename)
        logging.config.dictConfig(log_cfg)
    except (YAMLError, IOError) as e:
        logging.basicConfig(level=default_level)
        logging.info("No logging config file, level set to debug %s", e)
