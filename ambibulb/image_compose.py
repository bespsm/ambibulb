# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


from logging import log, DEBUG
import time
from PIL import Image
from enum import Enum


class CroppingMode(Enum):
    """Defines possible image cropping modes. For example,
    LEFT means that only left part of the image get saved.
    """

    FULL = "FULL"
    LEFT = "LEFT"
    TOP = "TOP"
    RIGHT = "RIGHT"
    BOTTOM = "BOTTOM"


def image_compose(
    raw_image, image_width, image_height, cropping_mode: CroppingMode
):
    """1. Convert binary image blob with given width and height to
    pil-understandable format.
    2. reduce image size while preserving asptect ratio (350x350)
    3. crop the image, keeping only one of the side from original image

    Args:
        raw_image: binary image blob in rgb888 format.
        image_width: image width.
        image_height: image height.
        cropping_mode: cropping mode.
    Returns:
        :py:class:`~PIL.Image.Image` object.: composed image
    """
    # open image
    image_open_tic = time.perf_counter()
    opened_image = Image.frombytes(
        mode="RGB", size=(image_width, image_height), data=raw_image
    )
    image_open_toc = time.perf_counter()
    log(
        DEBUG,
        "image open time: "
        + "{:10.4f}".format(image_open_toc - image_open_tic),
    )

    # resize image
    opened_image.thumbnail((350, 350), Image.BICUBIC)
    image_resize_tic = time.perf_counter()
    log(
        DEBUG,
        "image resize time: "
        + "{:10.4f}".format(image_resize_tic - image_open_toc),
    )

    # crop image if needed
    width, height = opened_image.size
    # default values of cropped image points (0 in top left corner)
    left = 0
    top = 0
    right = width
    bottom = height

    # change point position by keeping 10% from original image
    if cropping_mode == CroppingMode.LEFT:
        right = width / 10
    elif cropping_mode == CroppingMode.TOP:
        bottom = height / 10
    elif cropping_mode == CroppingMode.RIGHT:
        left = 9 * width / 10
    elif cropping_mode == CroppingMode.BOTTOM:
        top = 9 * height / 10
    else:
        pass  # NONE

    cropped_image = opened_image.crop((left, top, right, bottom))
    image_crop_toc = time.perf_counter()
    log(
        DEBUG,
        "image cropping time: "
        + "{:10.4f}".format(image_crop_toc - image_resize_tic),
    )
    return cropped_image