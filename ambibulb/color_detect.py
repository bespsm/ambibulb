# MIT License
# Copyright (c) 2021 Sergey B <dkc.sergey.88@hotmail.com>


from logging import log, DEBUG
import time
from sklearn.cluster import MiniBatchKMeans
import numpy as np


def get_dominant_clr(image):
    """calculates dominant color of input image object.

    Args:
        image: input image object.
    Returns:
        tuple(int, int, int): position of dominant color on RGB plane.
    """
    dominant_color_tic = time.perf_counter()
    # reshape image to 1-dimensional array
    np_image = np.array(image)
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
        + "{:10.4f}".format(dominant_color_toc - dominant_color_tic),
    )
    return dominant[0][0], dominant[0][1], dominant[0][2]
