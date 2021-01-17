#!/usr/bin/env python3
# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


from . import EightyStateIRLightBulb, get_dominant_clr
from logging import log, INFO, DEBUG, ERROR, basicConfig
import argparse
import os
from sys import stdout
import subprocess
import time
import shutil

omxplayer_exe = "omxplayer"
screenshot_exe = "screenshot"
irsend_exe = "irsend"


def main():
    """ambibulb execution entry point."""
    # check if all dependencies installed
    if (
        shutil.which(omxplayer_exe) is None
        or shutil.which(screenshot_exe) is None
        or shutil.which(irsend_exe) is None
    ):
        log(
            ERROR,
            "one or more following dependencies are not installed: "
            + omxplayer_exe
            + " "
            + screenshot_exe
            + " "
            + irsend_exe,
        )
        return

    # parse input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("media_path", help="path to media file", type=str)
    parser.add_argument(
        "-w",
        "--with_white",
        help="use white light in the algoritm",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--cycle_period",
        help="min period color changing, sec. (Default = 0.4 sec)",
        type=float,
        default=0.4,
    )
    parser.add_argument(
        "-v", "--verbosity", help="show timing steps", action="store_true"
    )
    parser.add_argument(
        "-l",
        "--lirc_conf",
        help="lirc config name (Default = 'RGBLED')",
        type=str,
        default="RGBLED",
    )
    args = parser.parse_args()

    if args.verbosity:
        basicConfig(stream=stdout, level=DEBUG)

    abs_media_path = os.path.abspath(args.media_path)
    bulb = EightyStateIRLightBulb(args.with_white, args.lirc_conf)

    cycle_period = args.cycle_period
    cycle_period_now = 0.0

    omx = subprocess.Popen([omxplayer_exe, abs_media_path], text=True)
    try:
        while True:
            # wait if current cycle period is less then defined
            sleep_time = cycle_period - cycle_period_now
            if (sleep_time) > 0.0:
                time.sleep(sleep_time)

            screen_tic = time.perf_counter()

            # take a screenshot of dispaly and save in RAM
            log(INFO, "_____________________")
            scr = subprocess.Popen([screenshot_exe], stdout=subprocess.PIPE)
            shot = scr.communicate()[0]
            screenshot_path = "/tmp/screen.jpg"
            screenshot = open(screenshot_path, "wb")
            screenshot.write(bytearray(shot))
            screenshot.close()

            screen_toc = time.perf_counter()
            log(
                INFO,
                "screenshot time: "
                + "{:10.4f}".format(screen_toc - screen_tic),
            )

            # calculate dominant color
            color_r, color_g, color_b = get_dominant_clr(screenshot_path)

            # change curent light bulb state
            bulb.change_state(color_r, color_g, color_b)

            # check if omxplayer is exit()
            if omx.poll() is not None:
                exit()

            new_state_tic = time.perf_counter()
            cycle_period_now = new_state_tic - screen_tic
            log(
                INFO,
                "cycle time: " + "{:10.4f}".format(cycle_period_now),
            )

    except KeyboardInterrupt:
        # finish omxplayer if terminanted
        log(INFO, "finishing...")
        omx.communicate(input="q", timeout=3)
