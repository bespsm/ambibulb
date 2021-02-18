# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


from logging import log, INFO, DEBUG
import time
from sklearn.cluster import MiniBatchKMeans
import numpy as np
from PIL import Image


def get_dominant_clr(raw_image, image_width, image_height):
    """calculates dominant color of input image path.

    Args:
        img_path: input image path.
    Returns:
        tuple(int, int, int): position of dominant color on RGB plane.
    """
    # open image
    image_open_tic = time.perf_counter()
    opened_image = Image.frombytes(mode="RGB", size=(image_width, image_height), data=raw_image)
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

    # reshape image to 1-dimensional array
    np_image = np.array(opened_image)
    reshaped_image = np_image.reshape(
        (np_image.shape[0] * np_image.shape[1], 3)
    )

    # calculate dominant color
    clt = MiniBatchKMeans(
        n_clusters=1, max_iter=10, verbose=0, compute_labels=False, tol=0.1
    )
    clt.fit(reshaped_image)
    dominant = clt.cluster_centers_.astype("uint8")
    dominant_color_toc = time.perf_counter()
    log(
        DEBUG,
        "dominant color time: "
        + "{:10.4f}".format(dominant_color_toc - image_resize_tic),
    )
    return dominant[0][0], dominant[0][1], dominant[0][2]
