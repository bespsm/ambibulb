#!/usr/bin/env python3
# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


from . import OsramIRLightBulb, get_dominant_clr
from logging import log, INFO, DEBUG, basicConfig
import argparse
import os
from sys import stdout
import subprocess
import time


def main():
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
        help="min period color changing, sec. (Default = 0.5 sec)",
        type=float,
        default=0.5,
    )
    parser.add_argument(
        "-v", "--verbosity", help="show timing steps", action="store_true"
    )
    args = parser.parse_args()

    if args.verbosity:
        basicConfig(stream=stdout, level=DEBUG)

    abs_media_path = os.path.abspath(args.media_path)
    bulb = OsramIRLightBulb(args.with_white)

    cycle_period = args.cycle_period
    cycle_period_now = 0.0

    omx = subprocess.Popen(["omxplayer", abs_media_path], text=True)
    try:
        while True:
            # wait if current cycle period is less then defined
            sleep_time = cycle_period - cycle_period_now
            if (sleep_time) > 0.0:
                log(INFO, "sleep for sec.: " + "{:10.4f}".format(sleep_time))
                time.sleep(sleep_time)

            screen_tic = time.perf_counter()

            log(INFO, "_____________________")
            scr = subprocess.Popen(["screenshot"], stdout=subprocess.PIPE)
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

            color_r, color_g, color_b = get_dominant_clr(screenshot_path)

            color_tic = time.perf_counter()
            log(
                INFO,
                "color detection time: "
                + "{:10.4f}".format(color_tic - screen_toc),
            )

            bulb.change_state(color_r, color_g, color_b)

            # check if omxplayer is exit()
            if omx.poll() is not None:
                exit()

            new_state_tic = time.perf_counter()
            cycle_period_now = new_state_tic - screen_tic

    except KeyboardInterrupt:
        log(INFO, "finishing...")
        omx.communicate(input="q", timeout=3)
