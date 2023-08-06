import configparser
import os
import logging
from PyQt5 import QtCore


SETTINGS_FILE_NAME_STR = "settings.ini"

config_parser = None


def get_config_parser() -> configparser.ConfigParser:
    global config_parser
    if config_parser is None:
        config_parser = configparser.ConfigParser()
        config_parser.optionxform = str
    return config_parser


def get_appl_path(*args) -> str:
    application_dir_str = os.path.dirname(os.path.dirname(__file__))
    # application_dir_str = os.path.dirname(__file__)
    full_path_str = application_dir_str
    for arg in args:
        full_path_str = os.path.join(full_path_str, arg)
    return full_path_str


def _get_config_path(*args) -> str:
    return get_appl_path(*args)
    config_dir = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.ConfigLocation)[0]
    config_dir = os.path.join(config_dir, "kammanta")
    # if testing_bool or example_bool:
    #     config_dir = os.path.join(config_dir, "example_testing")
    full_path_str = config_dir
    for arg in args:
        full_path_str = os.path.join(full_path_str, arg)
    os.makedirs(os.path.dirname(full_path_str), exist_ok=True)
    return full_path_str


def add_string_to_config(i_section: str, i_key: str, i_value: str):
    config_file_path_str = _get_config_path(SETTINGS_FILE_NAME_STR)
    config_parser = get_config_parser()
    config_parser.read(config_file_path_str)
    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
    config_parser.set(i_section, i_key, i_value)
    with open(config_file_path_str, "w") as file:
        config_parser.write(file)


def get_string_from_config(i_section: str, i_key: str, i_default_value: str) -> str:
    def set_default_value():
        config_parser.set(i_section, i_key, i_default_value)
        with open(config_file_path_str, "w") as file:
            config_parser.write(file)

    config_parser = get_config_parser()
    config_file_path_str = _get_config_path(SETTINGS_FILE_NAME_STR)
    config_parser.read(config_file_path_str)

    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
    if not config_parser.has_option(i_section, i_key):
        set_default_value()

    ret_value_str = config_parser[i_section][i_key]
    if not ret_value_str:
        # -possible addition for files and dirs: or os.path.exists(ret_value_str):
        logging.warning("Looking in the config file a key was found but the value was empty, using a default value")
        set_default_value()
        ret_value_str = config_parser[i_section][i_key]

    return ret_value_str


def get_dictionary_from_config(i_section: str) -> dict:
    # FAV_PREF_STR
    # , i_default_value: dict
    config_parser = get_config_parser()
    config_file_path_str = _get_config_path(SETTINGS_FILE_NAME_STR)
    config_parser.read(config_file_path_str)

    if not config_parser.has_section(i_section):
        config_parser.add_section(i_section)
        with open(config_file_path_str, "w") as file:
            config_parser.write(file)

    ret_value_str = dict(config_parser.items(i_section))
    return ret_value_str


def get_start_dir() -> str:
    default_str = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.MusicLocation)[0]
    start_dir_str = get_string_from_config("general", "start-dir", default_str)
    return start_dir_str


def set_start_dir(i_start_dir: str) -> None:
    add_string_to_config("general", "start-dir", i_start_dir)


def get_fav_dict() -> dict:
    fav_dict = get_dictionary_from_config("favorites")
    return fav_dict


def set_start_volume(i_vol: int) -> None:
    add_string_to_config("general", "start-volume", str(i_vol))


def get_start_volume() -> int:
    vol_str = get_string_from_config("general", "start-volume", "40")
    vol_int = int(vol_str)
    return vol_int


def set_start_fade(i_fade_secs: int) -> None:
    add_string_to_config("general", "start-fade", str(i_fade_secs))


def get_start_fade() -> int:
    fade_secs_str = get_string_from_config("general", "start-fade", "5")
    fade_secs_int = int(fade_secs_str)
    return fade_secs_int


def set_dictionary(i_section: str, i_dict: dict):
    config_parser = get_config_parser()
    config_file_path_str = _get_config_path(SETTINGS_FILE_NAME_STR)
    config_parser.read(config_file_path_str)
    if not config_parser.has_section(i_section):
        config_parser.remove_section(i_section)
    config_parser[i_section] = i_dict
    with open(config_file_path_str, "w") as file:
        config_parser.write(file)


def set_fav_dict(i_favs: dict) -> None:
    set_dictionary("favorites", i_favs)


def set_playlist_dir(i_dir: str) -> None:
    add_string_to_config("general", "playlist-dir", i_dir)


def get_playlist_dir() -> str:
    default_str = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.MusicLocation)[0]
    pl_dir_str = get_string_from_config("general", "playlist-dir", default_str)
    return pl_dir_str


def set_win_width(i_width_px: int):
    add_string_to_config("gui-layout", "win-width", str(i_width_px))


def set_win_x(i_x: int):
    add_string_to_config("gui-layout", "win-x", str(i_x))


def set_win_y(i_y: int):
    add_string_to_config("gui-layout", "win-y", str(i_y))


def set_win_height(i_height_px: int):
    add_string_to_config("gui-layout", "win-height", str(i_height_px))


def get_win_width() -> int:
    win_width_str = get_string_from_config("gui-layout", "win-width", "750")
    win_width_int = int(win_width_str)
    return win_width_int


def get_win_height() -> int:
    win_height_str = get_string_from_config("gui-layout", "win-height", "600")
    win_height_int = int(win_height_str)
    return win_height_int


def get_win_x() -> int:
    win_x_str = get_string_from_config("gui-layout", "win-x", "100")
    win_x_int = int(win_x_str)
    return win_x_int


def get_win_y() -> int:
    win_y_str = get_string_from_config("gui-layout", "win-y", "50")
    win_y_int = int(win_y_str)
    return win_y_int

