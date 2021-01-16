# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


from logging import log, INFO, DEBUG
import subprocess
import time
from sklearn.cluster import MiniBatchKMeans
import numpy as np
from PIL import Image


class OsramIRLightBulb:
    """
    docstring
    """

    brightess_clr_to_positions = {
        (0, "BLACK"): [(18, 18, 18)],
        (1, "RED"): [(51, 14, 14)],
        (1, "ORANGE"): [(51, 21, 14)],
        (1, "YELLOW_DARK"): [(51, 24, 14)],
        (1, "YELLOW_GREENISH"): [(51, 35, 14)],
        (1, "YELLOW"): [(51, 42, 22)],
        (1, "GREEN"): [(42, 91, 26), (29, 51, 29)],
        (1, "TURQUOISE"): [(22, 51, 33)],
        (1, "TURQUOISE_LIGHT"): [(22, 38, 51)],
        (1, "BLUE_LIGHT"): [(22, 38, 51)],
        (1, "BLUE_PASTEL"): [(22, 31, 51)],
        (1, "BLUE"): [(22, 22, 51)],
        (1, "BLUE_PURPLE"): [(27, 22, 51)],
        (1, "PURPLE"): [(35, 22, 51)],
        (1, "PURPLE_PINKISH"): [(44, 22, 51)],
        (1, "PINK"): [(51, 33, 51)],
        (1, "WHITE"): [(51, 51, 51), (51, 42, 37)],
        (2, "RED"): [(92, 25, 25)],
        (2, "ORANGE"): [(92, 39, 25)],
        (2, "YELLOW_DARK"): [(92, 49, 25)],
        (2, "YELLOW_GREENISH"): [(92, 62, 25)],
        (2, "YELLOW"): [(92, 75, 40)],
        (2, "GREEN"): [(76, 131, 47), (52, 92, 92, 52)],
        (2, "TURQUOISE"): [(40, 92, 60)],
        (2, "TURQUOISE_LIGHT"): [(22, 51, 43)],
        (2, "BLUE_LIGHT"): [(40, 69, 92)],
        (2, "BLUE_PASTEL"): [(40, 56, 92)],
        (2, "BLUE"): [(40, 40, 92)],
        (2, "BLUE_PURPLE"): [(49, 40, 92)],
        (2, "PURPLE"): [(62, 40, 92)],
        (2, "PURPLE_PINKISH"): [(79, 40, 92)],
        (2, "PINK"): [(92, 60, 92)],
        (2, "WHITE"): [(92, 92, 92), (92, 75, 66)],
        (3, "RED"): [(133, 36, 36)],
        (3, "ORANGE"): [(133, 56, 36)],
        (3, "YELLOW_DARK"): [(133, 71, 36)],
        (3, "YELLOW_GREENISH"): [(133, 90, 36)],
        (3, "YELLOW"): [(133, 108, 58)],
        (3, "GREEN"): [(109, 172, 68), (74, 133, 74)],
        (3, "TURQUOISE"): [(58, 133, 87)],
        (3, "TURQUOISE_LIGHT"): [(40, 92, 77)],
        (3, "BLUE_LIGHT"): [(58, 99, 133)],
        (3, "BLUE_PASTEL"): [(58, 81, 133)],
        (3, "BLUE"): [(58, 58, 132)],
        (3, "BLUE_PURPLE"): [(71, 58, 133)],
        (3, "PURPLE"): [(90, 58, 133)],
        (3, "PURPLE_PINKISH"): [(146, 58, 133)],
        (3, "PINK"): [(132, 87, 132)],
        (3, "WHITE"): [(132, 132, 132), (133, 108, 95)],
        (4, "RED"): [(173, 47, 47)],
        (4, "ORANGE"): [(173, 73, 47)],
        (4, "YELLOW_DARK"): [(173, 93, 47)],
        (4, "YELLOW_GREENISH"): [(173, 117, 47)],
        (4, "YELLOW"): [(173, 142, 76)],
        (4, "GREEN"): [(142, 173, 89), (97, 173, 97)],
        (4, "TURQUOISE"): [(75, 173, 113)],
        (4, "TURQUOISE_LIGHT"): [(75, 173, 146)],
        (4, "BLUE_LIGHT"): [(75, 130, 173)],
        (4, "BLUE_PASTEL"): [(75, 105, 173)],
        (4, "BLUE"): [(76, 76, 173)],
        (4, "BLUE_PURPLE"): [(93, 75, 173)],
        (4, "PURPLE"): [(117, 75, 173)],
        (4, "PURPLE_PINKISH"): [(150, 75, 173)],
        (4, "PINK"): [(173, 114, 173)],
        (4, "WHITE"): [(173, 173, 173), (173, 142, 125)],
        (5, "RED"): [(214, 58, 58)],
        (5, "ORANGE"): [(214, 90, 58)],
        (5, "YELLOW_DARK"): [(214, 115, 58)],
        (5, "YELLOW_GREENISH"): [(214, 145, 58)],
        (5, "YELLOW"): [(214, 175, 93)],
        (5, "GREEN"): [(176, 214, 110), (120, 214, 120)],
        (5, "TURQUOISE"): [(93, 214, 140)],
        (5, "TURQUOISE_LIGHT"): [(93, 214, 180)],
        (5, "BLUE_LIGHT"): [(93, 160, 214)],
        (5, "BLUE_PASTEL"): [(93, 130, 214)],
        (5, "BLUE"): [(93, 93, 214)],
        (5, "BLUE_PURPLE"): [(115, 93, 214)],
        (5, "PURPLE"): [(145, 93, 214)],
        (5, "PURPLE_PINKISH"): [(185, 93, 214)],
        (5, "PINK"): [(214, 140, 214)],
        (5, "WHITE"): [(214, 214, 214), (214, 175, 154)],
    }

    brightness_values = range(6)
    color_values = (
        "RED",
        "ORANGE",
        "YELLOW_DARK",
        "YELLOW_GREENISH",
        "YELLOW",
        "GREEN",
        "TURQUOISE",
        "TURQUOISE_LIGHT",
        "BLUE_LIGHT",
        "BLUE_PASTEL",
        "BLUE",
        "BLUE_PURPLE",
        "PURPLE",
        "PURPLE_PINKISH",
        "PINK",
        "WHITE",
        "BLACK",
    )

    def __init__(self, with_white):
        # init values
        self.with_white = with_white
        self.br_state = 0
        self.off = True
        self.clr_state = "PURPLE"
        self.sender_proc = None

    # def __del__(self):
    #     # body of destructor

    def __action_detector(self, red_c, green_c, blue_c):
        log(
            INFO,
            "new color: "
            + str(red_c)
            + ":"
            + str(green_c)
            + ":"
            + str(blue_c),
        )

        brightess = None
        clr = None
        min_distance = None
        for (
            brightess_clr,
            positions,
        ) in OsramIRLightBulb.brightess_clr_to_positions.items():
            for position in positions:
                cur_distance = (red_c - position[0]) ** 2
                cur_distance += (green_c - position[1]) ** 2
                cur_distance += (blue_c - position[2]) ** 2

                if min_distance is None or cur_distance < min_distance:
                    min_distance = cur_distance
                    brightess = brightess_clr[0]
                    clr = brightess_clr[1]

        log(INFO, "new brightnes: " + str(brightess))
        log(INFO, "new color: " + clr)
        return brightess, clr

    def __change_brightnes_cmds(self, new_state):
        if new_state not in OsramIRLightBulb.brightness_values:
            raise ValueError("Unexpected value")
        commands = []
        if self.br_state != new_state:
            if new_state == 0:
                self.off = True
                commands.extend(["TURN_OFF"])
            else:
                if self.off:
                    self.off = False
                    commands.extend(["TURN_ON"])
                diff = self.br_state - new_state
                for _ in range(abs(diff)):
                    if diff < 0:
                        commands.extend(["HIGHER"])
                    else:
                        commands.extend(["LOWER"])
                log(INFO, "new brightnes state: " + str(new_state))
            self.br_state = new_state
        return commands

    def __change_color_cmds(self, new_state):
        if new_state not in OsramIRLightBulb.color_values:
            raise ValueError("Unexpected value")
        commands = []
        if self.clr_state != new_state and new_state != "BLACK":
            commands.extend([new_state])
            log(INFO, "new color state: " + str(new_state))
            self.clr_state = new_state
        return commands

    def __white_clr_check(self, br_state, clr_state):
        if not self.with_white and clr_state == "WHITE":
            log(INFO, "no_white mode is ON")
            return 0, "BLACK"
        else:
            return br_state, clr_state

    def change_state(self, red_c, green_c, blue_c):
        action_tic = time.perf_counter()
        # detect required BULB state changes
        new_br_state, new_clr_state = self.__action_detector(
            red_c, green_c, blue_c
        )
        action_toc = time.perf_counter()
        log(
            INFO,
            "action detection time: "
            + "{:10.4f}".format(action_toc - action_tic),
        )
        codes = []
        # check with_white option
        br_state, clr_state = self.__white_clr_check(
            new_br_state, new_clr_state
        )
        # get color brightnes cmds
        codes.extend(self.__change_brightnes_cmds(br_state))
        # if does not come TURN_OFF brightness
        if br_state != 0:
            # get color change cmds
            codes.extend(self.__change_color_cmds(clr_state))

        # there are codes to apply
        if len(codes) != 0:
            terminal_cmd = ["irsend", "SEND_ONCE", "RGBLED"]
            terminal_cmd.extend(codes)
            log(DEBUG, "codes: " + " ".join(map(str, terminal_cmd)))
            # wait prev. process to finish
            if self.sender_proc is not None:
                self.sender_proc.communicate()
            # send new ir changes
            self.sender_proc = subprocess.Popen(terminal_cmd)
        send_tic = time.perf_counter()
        log(
            INFO,
            "send actions time: " + "{:10.4f}".format(send_tic - action_toc),
        )


def get_dominant_clr(img_path):

    image_open_tic = time.perf_counter()
    img1 = Image.open(img_path)
    image_open_toc = time.perf_counter()
    log(
        INFO,
        "image open time: "
        + "{:10.4f}".format(image_open_toc - image_open_tic),
    )

    # resize image
    img1.thumbnail((400, 400), Image.BICUBIC)
    image_resize_tic = time.perf_counter()
    log(
        INFO,
        "image resize time: "
        + "{:10.4f}".format(image_resize_tic - image_open_toc),
    )

    im = np.array(img1)
    img = im.reshape((im.shape[0] * im.shape[1], 3))
    clt = MiniBatchKMeans(
        n_clusters=1, max_iter=10, verbose=0, compute_labels=False
    )
    clt.fit(img)
    out = clt.cluster_centers_.astype("uint8")
    dominant_color_toc = time.perf_counter()
    log(
        INFO,
        "dominant color time: "
        + "{:10.4f}".format(dominant_color_toc - image_resize_tic),
    )
    return out[0][0], out[0][1], out[0][2]
