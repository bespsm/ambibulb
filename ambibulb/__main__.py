#!/usr/bin/env python3
# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


from . import ir_light_bulb, color_detect, image_compose
from logging import log, INFO, DEBUG, ERROR, basicConfig
import argparse
import os
from sys import stdout
import subprocess
import time
import shutil
from systemd.daemon import notify, Notification
import signal
import configparser
from .snapshot_bcm import ffi, lib

irsend_exe = "irsend"
run = True


def signals_handler(signum, frame):
    global run
    run = False


def main():
    """ambibulb execution entry point."""

    global run
    signal.signal(signal.SIGINT, signals_handler)
    signal.signal(signal.SIGTERM, signals_handler)

    if shutil.which(irsend_exe) is None:
        log(
            ERROR,
            "lirc is not installed, please run: " + "apt install lirc",
        )
        return

    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config_path",
        help="path to config ini file",
        type=str,
        default=os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "ambibulb-config.ini"
        ),
    )
    args = parser.parse_args()

    if not os.path.exists(args.config_path):
        log(
            ERROR,
            "couldn't find config ini file: "
            + args.config_path
            + ". Please run ambibulb-config to create it.",
        )
        return

    params = configparser.ConfigParser()
    params.read(args.config_path)

    basicConfig(level=int(params["general"]["logging_level"]))

    bulb = ir_light_bulb.EightyStateIRLightBulb(
        params["general"].getboolean("with_white"), params["lirc"]["config_id"]
    )

    cycle_period = float(params["general"]["cycle_period"])
    cycle_period_now = 0.0

    cropping_mode = image_compose.CroppingMode(
        params["general"]["cropping_mode"]
    )

    # init screenshot module
    lib.snapshot_bcm_init()
    screenshot = lib.snapshot_bcm_init_snapshot()

    # systemd notification
    notify(Notification.READY)

    try:
        while run:
            # wait if current cycle period is less then defined
            sleep_time = cycle_period - cycle_period_now
            if (sleep_time) > 0.0:
                time.sleep(sleep_time)

            screen_tic = time.perf_counter()

            # take a screenshot of dispaly
            log(DEBUG, "_____________________")
            lib.snapshot_bcm_take_snapshot(screenshot)
            raw_image = ffi.buffer(screenshot.buffer, screenshot.size)

            screen_toc = time.perf_counter()
            log(
                DEBUG,
                "screenshot time: "
                + "{:10.4f}".format(screen_toc - screen_tic),
            )

            # compose image
            compoed_image = image_compose.image_compose(
                raw_image,
                screenshot.width,
                screenshot.height,
                cropping_mode
            )

            # calculate dominant color
            color_r, color_g, color_b = color_detect.get_dominant_clr(
                compoed_image
            )

            # change curent light bulb state
            bulb.change_state(color_r, color_g, color_b)

            new_state_tic = time.perf_counter()
            cycle_period_now = new_state_tic - screen_tic
            log(
                DEBUG,
                "cycle time: " + "{:10.4f}".format(cycle_period_now),
            )

    finally:
        notify(Notification.STOPPING)
        log(INFO, "finishing...")
        lib.snapshot_bcm_free_snapshot(screenshot)
        lib.snapshot_bcm_free()


if __name__ == "__main__":
    main()
