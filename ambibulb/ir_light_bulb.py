# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


from logging import log, INFO, DEBUG
import subprocess
import time


class EightyStateIRLightBulb:
    """Class holds color state of IR light bulb.

    This class holds and changes light state of a LED RBG bulb.
    The changinng happend based on input color (RGB position).
    Algoritm calculates the shortest distance amonhg 80
    possible light bulb color states and input color on RGB plane.

    Attributes:
        brightess_clr_to_positions: dict among the light bulb color states
            and appropriate points on RGB plane.
        init_brightess_clr_to_positions: initialized instance of
            brightess_clr_to_positions attribute.
        brightness_values: possible values of brightess parameter for irsend.
        color_values: possible values of brightess parameter for irsend.
        with_white: the flag defines if white color will be used.
        br_state: current brightess state of the light bulb.
        off: the flag defines if the light bulb is OFF.
        clr_state: current color state of the light bulb.
        sender_proc: irsend process execution object.
        lirc_source_id: lirc config name.
    """

    brightess_clr_to_positions = {
        (0, "BLACK"): [(18, 18, 18)],
        (1, "RED"): [(51, 14, 14)],
        (1, "ORANGE"): [(51, 21, 14)],
        (1, "YELLOW_DARK"): [(51, 24, 14)],
        (1, "YELLOW_GREENISH"): [(51, 35, 14)],
        (1, "YELLOW"): [(51, 42, 14)],
        (1, "GREEN"): [(24, 91, 14), (14, 91, 14)],
        (1, "TURQUOISE"): [(22, 51, 33)],
        (1, "TURQUOISE_LIGHT"): [(22, 38, 51)],
        (1, "BLUE_LIGHT"): [(22, 38, 51)],
        (1, "BLUE_PASTEL"): [(22, 31, 51)],
        (1, "BLUE"): [(14, 14, 51)],
        (1, "BLUE_PURPLE"): [(27, 14, 51)],
        (1, "PURPLE"): [(35, 22, 51)],
        (1, "PURPLE_PINKISH"): [(44, 22, 51)],
        (1, "PINK"): [(51, 22, 51)],
        (1, "WHITE"): [(51, 51, 51), (51, 42, 37)],
        (2, "RED"): [(92, 25, 25)],
        (2, "ORANGE"): [(92, 39, 25)],
        (2, "YELLOW_DARK"): [(92, 49, 25)],
        (2, "YELLOW_GREENISH"): [(92, 62, 25)],
        (2, "YELLOW"): [(92, 75, 25)],
        (2, "GREEN"): [(49, 131, 25), (25, 131, 25)],
        (2, "TURQUOISE"): [(40, 92, 60)],
        (2, "TURQUOISE_LIGHT"): [(22, 51, 43)],
        (2, "BLUE_LIGHT"): [(40, 69, 92)],
        (2, "BLUE_PASTEL"): [(40, 56, 92)],
        (2, "BLUE"): [(25, 25, 92)],
        (2, "BLUE_PURPLE"): [(49, 25, 92)],
        (2, "PURPLE"): [(62, 40, 92)],
        (2, "PURPLE_PINKISH"): [(79, 40, 92)],
        (2, "PINK"): [(92, 40, 92)],
        (2, "WHITE"): [(92, 92, 92), (92, 75, 66)],
        (3, "RED"): [(133, 36, 36)],
        (3, "ORANGE"): [(133, 56, 36)],
        (3, "YELLOW_DARK"): [(133, 71, 36)],
        (3, "YELLOW_GREENISH"): [(133, 90, 36)],
        (3, "YELLOW"): [(133, 108, 36)],
        (3, "GREEN"): [(71, 133, 36), (36, 133, 36)],
        (3, "TURQUOISE"): [(58, 133, 87)],
        (3, "TURQUOISE_LIGHT"): [(40, 92, 77)],
        (3, "BLUE_LIGHT"): [(58, 99, 133)],
        (3, "BLUE_PASTEL"): [(58, 81, 133)],
        (3, "BLUE"): [(36, 36, 132)],
        (3, "BLUE_PURPLE"): [(71, 36, 133)],
        (3, "PURPLE"): [(90, 58, 133)],
        (3, "PURPLE_PINKISH"): [(146, 58, 133)],
        (3, "PINK"): [(132, 58, 132)],
        (3, "WHITE"): [(132, 132, 132), (133, 108, 95)],
        (4, "RED"): [(173, 47, 47)],
        (4, "ORANGE"): [(173, 73, 47)],
        (4, "YELLOW_DARK"): [(173, 93, 47)],
        (4, "YELLOW_GREENISH"): [(173, 117, 47)],
        (4, "YELLOW"): [(173, 142, 47)],
        (4, "GREEN"): [(93, 173, 47), (47, 173, 47)],
        (4, "TURQUOISE"): [(75, 173, 113)],
        (4, "TURQUOISE_LIGHT"): [(75, 173, 146)],
        (4, "BLUE_LIGHT"): [(75, 130, 173)],
        (4, "BLUE_PASTEL"): [(75, 105, 173)],
        (4, "BLUE"): [(47, 47, 173)],
        (4, "BLUE_PURPLE"): [(93, 47, 173)],
        (4, "PURPLE"): [(117, 75, 173)],
        (4, "PURPLE_PINKISH"): [(150, 75, 173)],
        (4, "PINK"): [(173, 75, 173)],
        (4, "WHITE"): [(173, 173, 173), (173, 142, 125)],
        (5, "RED"): [(214, 58, 58)],
        (5, "ORANGE"): [(214, 90, 58)],
        (5, "YELLOW_DARK"): [(214, 115, 58)],
        (5, "YELLOW_GREENISH"): [(214, 145, 58)],
        (5, "YELLOW"): [(214, 175, 58)],
        (5, "GREEN"): [(115, 214, 58), (58, 214, 58)],
        (5, "TURQUOISE"): [(93, 214, 140)],
        (5, "TURQUOISE_LIGHT"): [(93, 214, 180)],
        (5, "BLUE_LIGHT"): [(93, 160, 214)],
        (5, "BLUE_PASTEL"): [(93, 130, 214)],
        (5, "BLUE"): [(58, 58, 214)],
        (5, "BLUE_PURPLE"): [(115, 58, 214)],
        (5, "PURPLE"): [(145, 58, 214)],
        (5, "PURPLE_PINKISH"): [(185, 58, 214)],
        (5, "PINK"): [(214, 58, 214)],
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

    def __init__(self, with_white, lirc_source_id):
        """Initialize the instance of the class.

        To syncronize real light bulb color state,
            initialized with border parameters.

        Args:
            with_white: the flag defines if white color will be used.
            lirc_source_id: lirc source id, lirc.conf is available as name.
        """

        self.init_brightess_clr_to_positions = (
            EightyStateIRLightBulb.brightess_clr_to_positions
        )

        # remove white color points
        if not with_white:
            keys_to_remove = [
                (5, "WHITE"),
                (4, "WHITE"),
                (3, "WHITE"),
                (2, "WHITE"),
                (1, "WHITE"),
            ]
            for key_to_remove in keys_to_remove:
                if key_to_remove in self.init_brightess_clr_to_positions:
                    del self.init_brightess_clr_to_positions[key_to_remove]

        # initial bulb state
        self.br_state = 5
        self.off = False
        self.clr_state = "WHITE"
        self.sender_proc = None
        self.lirc_source_id = lirc_source_id

    def __action_detector(self, red_c, green_c, blue_c):
        """calculates required color and brightness.

        Args:
            red_c: input red color position.
            green_c: input green color position.
            blue_c: input blue color position.
        Returns:
            tuple(int, str): required color and brightness states.
        """
        log(
            DEBUG,
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
        ) in self.init_brightess_clr_to_positions.items():
            for position in positions:
                cur_distance = (red_c - position[0]) ** 2
                cur_distance += (green_c - position[1]) ** 2
                cur_distance += (blue_c - position[2]) ** 2

                if min_distance is None or cur_distance < min_distance:
                    min_distance = cur_distance
                    brightess = brightess_clr[0]
                    clr = brightess_clr[1]

        log(DEBUG, "new brightnes: " + str(brightess))
        log(DEBUG, "new color: " + clr)
        return brightess, clr

    def __change_brightnes_cmds(self, new_state):
        """generates irsend commands to change brightness state.

        Args:
            new_state: required brightness state to change.
        Returns:
            set(str): commands to change the brightness.
        """
        if new_state not in EightyStateIRLightBulb.brightness_values:
            raise ValueError("Unexpected value")
        commands = []
        # control off-on parameter
        if new_state == 0 and self.off == False:
            self.off = True
            commands.extend(["TURN_OFF"])
        elif new_state != 0 and self.off == True:
            self.off = False
            commands.extend(["TURN_ON"])

        # control brightness level parameter
        if self.br_state != new_state and self.off == False:
            diff = self.br_state - new_state
            for _ in range(abs(diff)):
                if diff < 0:
                    commands.extend(["HIGHER"])
                else:
                    commands.extend(["LOWER"])
            log(DEBUG, "new brightnes state: " + str(new_state))
            self.br_state = new_state
        return commands

    def __change_color_cmds(self, new_state):
        """generates irsend commands to change color state.

        Args:
            new_state: required color state to change.
        Returns:
            set(str): commands to change the color.
        """
        if new_state not in EightyStateIRLightBulb.color_values:
            raise ValueError("Unexpected value")
        commands = []
        if self.clr_state != new_state and new_state != "BLACK":
            commands.extend([new_state])
            log(DEBUG, "new color state: " + str(new_state))
            self.clr_state = new_state
        return commands

    def change_state(self, red_c, green_c, blue_c):
        """changes the current state of the LED RBG bulb.

        Args:
            red_c: input red color position.
            green_c: input green color position.
            blue_c: input blue color position.
        """
        action_tic = time.perf_counter()
        # detect required BULB state changes
        new_br_state, new_clr_state = self.__action_detector(
            red_c, green_c, blue_c
        )
        action_toc = time.perf_counter()
        log(
            DEBUG,
            "action detection time: "
            + "{:10.4f}".format(action_toc - action_tic),
        )
        codes = []
        # get color brightnes cmds
        codes.extend(self.__change_brightnes_cmds(new_br_state))
        # if does not come TURN_OFF brightness
        if new_br_state != 0:
            # get color change cmds
            codes.extend(self.__change_color_cmds(new_clr_state))

        # there are codes to apply
        if len(codes) != 0:
            terminal_cmd = ["irsend", "SEND_ONCE", self.lirc_source_id]
            terminal_cmd.extend(codes)
            log(INFO, "codes: " + " ".join(map(str, terminal_cmd)))
            # wait prev. process to finish
            if self.sender_proc is not None:
                self.sender_proc.communicate()
            # send new ir changes
            self.sender_proc = subprocess.Popen(terminal_cmd)
        send_tic = time.perf_counter()
        log(
            DEBUG,
            "send actions time: " + "{:10.4f}".format(send_tic - action_toc),
        )
