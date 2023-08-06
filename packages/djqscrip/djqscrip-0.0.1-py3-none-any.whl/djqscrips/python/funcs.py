# -*- encoding: utf-8 -*-
'''
@File    :   funcs.py
@Time    :   2021/01/22 16:47:40
@Author  :   Jiaqi Duan
@Version :   0.0.1
'''

# here put the import lib
import cv2


def cv_show(imgs, max_size=None, debug=True):
    """show opencv images

    Args:
        imgs (list): [("test", img), ...]
        max_size (int, optional): The longest side of the displayed image. Defaults to None.
        debug (bool, optional): Display when debugging, not when running. Defaults to True.
    """
    if debug:
        for info in imgs:
            h, w = info[1].shape[:2]
            if max_size is not None:
                m = min(w, h)
                ratio = float(max_size) / float(m)
                w, h = int(ratio * w), int(ratio *h)
            cv2.imshow(info[0], cv2.resize (info[1], (w, h)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()