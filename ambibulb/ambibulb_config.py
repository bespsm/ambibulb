#!/usr/bin/env python3
# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


import sys
import os, subprocess
from whiptail import Whiptail
import configparser
from shutil import copyfile
from . import image_compose


config_path = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "ambibulb-config.ini"
)

w = Whiptail(title="Ambibulb configuration.")

lirc_confpath_id_map = {"osram-rgb-led.conf": "OSRAMLED"}
lirc_conf_dir = "/etc/lirc/lircd.conf.d/"


def main():
    """ambibulb configuration script. Execution entry point."""

    # parameters object
    params = configparser.ConfigParser()

    if os.path.exists(config_path):
        params.read(config_path)
    else:
        # default parameters object
        default_params = configparser.ConfigParser()
        default_params["general"] = {
            "with_white": 1,
            "cycle_period": 0.3,
            "source": "lirc",
            "logging_level": 20,
            "cropping_mode": image_compose.CroppingMode.FULL.name
        }
        default_params["lirc"] = {
            "config_path": list(lirc_confpath_id_map.keys())[0],
            "config_id": list(lirc_confpath_id_map.values())[0],
        }
        w.msgbox(
            "Couldn't find config file. Default values are preconfigured."
        )
        params = default_params

    # main menu loop
    while True:
        main_opt_selected = w.menu(
            "Main settings menu.",
            [
                ("0", "General settings."),
                ("1", "LIRC settings."),
                ("2", "Exit."),
            ],
        )[0]

        # cancel is selected
        if main_opt_selected == "":
            quit()

        # general settings is selected
        elif main_opt_selected == "0":
            while True:
                general_opt_selected = w.menu(
                    "General settings menu.",
                    [
                        ("0", "If use white in color detection algoritm. Current: " + params["general"]["with_white"]),
                        ("1", "Enter color detection cycle period. Current: " + params["general"]["cycle_period"]),
                        ("2", "Select light source. Current: " + params["general"]["source"]),
                        ("3", "Select logging level. Current: " + params["general"]["logging_level"]),
                        ("4", "Select screen area to analyze. Current: " + params["general"]["cropping_mode"]),
                        ("5", "Back."),
                    ],
                )[0]

                if general_opt_selected == "0":
                    result = w.yesno(
                        "Use white color in the color detection algoritm?",
                        default="no",
                    )
                    str_result = str(int(not result))
                    params["general"]["with_white"] = str_result

                elif general_opt_selected == "1":
                    result = w.inputbox(
                        "Enter color detection cycle period (sec). Press TAB to switch to yes/no dialog.",
                        default=params["general"]["cycle_period"],
                    )[0]
                    if result == "":
                        w.msgbox("Cycle period was not entered.")
                        continue
                    try:
                        result_float = float(result)
                    except ValueError:
                        w.msgbox("Not correct value: " + result)
                        continue
                    params["general"]["cycle_period"] = str(result_float)

                elif general_opt_selected == "2":
                    result = w.radiolist(
                        "Press SPACE to select light source. Press TAB to switch to yes/no dialog: ",
                        ["lirc"],
                    )[0]
                    if len(result) == 0:
                        w.msgbox("Light source level was not selected.")
                        continue
                    params["general"]["source"] = result[0]
                elif general_opt_selected == "3":
                    result = w.radiolist(
                        "Press SPACE to select logging level. Press TAB to switch to yes/no dialog: ",
                        [
                            "0 - NOTSET",
                            "10 - DEBUG",
                            "20 - INFO",
                            "30 - WARNING",
                            "40 - ERROR",
                            "50 - CRITICAL",
                        ],
                    )[0]
                    if len(result) == 0:
                        w.msgbox("Logging level was not selected.")
                        continue
                    params["general"]["logging_level"] = result[0]
                elif general_opt_selected == "4":
                    result = w.radiolist(
                        "Press SPACE to select screen area to analyze. Press TAB to switch to yes/no dialog: ",
                        [name for name, member in image_compose.CroppingMode.__members__.items()],
                    )[0]
                    if len(result) == 0:
                        w.msgbox("Screen area was not selected.")
                        continue
                    params["general"]["cropping_mode"] = result[0]
                else:
                    # general_opt_selected is "" or "5"
                    # go to main menu
                    break

        # lirc settings
        elif main_opt_selected == "1":
            result = w.inputbox(
                "Enter name of the lirc config: ",
                default=params["lirc"]["config_path"],
            )[0]
            if result == "":
                continue
            if result not in lirc_confpath_id_map.keys():
                w.msgbox("Not supported/valid config: " + result)
                continue
            else:
                params["lirc"]["config_path"] = result
                params["lirc"]["config_id"] = lirc_confpath_id_map[result]

        # exit is selected
        elif main_opt_selected == "2":
            result = w.yesno(
                "Do you want to save the changes in " + config_path + "?",
                default="no",
            )
            # False in case of YES answer
            if result == False:
                lirc_selected_conf_path = os.path.join(
                    lirc_conf_dir, params["lirc"]["config_path"]
                )
                if not os.path.exists(lirc_selected_conf_path):
                    w.msgbox(
                        "WARNING. After configuration is finished, "
                        + "make sure that ambibulb lirc config: "
                        + params["lirc"]["config_path"]
                        + " is copied to lirc config directory: "
                        + lirc_conf_dir
                    )
                else:
                    w.msgbox(
                        "lirc configuration. No actions required,"
                        + " config file already exists: "
                        + lirc_selected_conf_path
                    )
                with open(config_path, "w") as cf:
                    params.write(cf)
            quit()


if __name__ == "__main__":
    main()
