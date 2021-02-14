#!/usr/bin/env python3
# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


import sys
import os, subprocess
from whiptail import Whiptail
import configparser
from shutil import copyfile


config_path = os.path.abspath("./ambibulb-config.ini")

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
            "logging": 1,
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
                        ("0", "Use white color in the detection algoritm."),
                        ("1", "Color detection cycle period."),
                        ("2", "Light source."),
                        ("3", "Enable logging."),
                        ("4", "Back."),
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
                        "Enter color detection cycle period (sec):",
                        default=params["general"]["cycle_period"],
                    )[0]
                    if result == "":
                        continue
                    try:
                        result_float = float(result)
                    except ValueError:
                        w.msgbox("Not correct value: " + result)
                        continue
                    params["general"]["cycle_period"] = str(result_float)

                elif general_opt_selected == "2":
                    result = w.radiolist("Choose light source:", ["lirc"])
                    if result == "":
                        continue
                    params["general"]["source"] = "lirc"  # stub
                elif general_opt_selected == "3":
                    result = w.yesno(
                        "Do you want to enable logging?", default="no"
                    )
                    str_result = str(int(not result))
                    params["general"]["logging"] = str_result
                else:
                    # general_opt_selected is "" or "4"
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