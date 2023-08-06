# -*- encoding: utf-8 -*-
'''
@File    :   scrips.py
@Time    :   2021/01/22 16:47:35
@Author  :   Jiaqi Duan
@Version :   0.0.1
'''

# here put the import lib
import argparse
import cv2


def cv_resize_img():
    parser = argparse.ArgumentParser()
    parser.add_argument("img_path", 
                        help="The path of the image to be resized.",
                        type=str)
    parser.add_argument("w", 
                        help="The width of the image after resize.",
                        type=int)
    parser.add_argument("h", 
                        help="The height of the image after resize.",
                        type=int)
    parser.add_argument("out_path", 
                        help="Output path of the resized image.",
                        type=str)
    args = parser.parse_args()

    img = cv2.imread(args.img_path)
    img_res = cv2.resize (img, (int(args.w), int(args.h)))
    cv2.imwrite(args.out_path, img_res)