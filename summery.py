import os
import sys
import glob
import copy
from PIL import Image
import PIL.Image, PIL.ImageTk
import pickle
import random
import numpy as np
import tkinter

def main():
    root = tkinter.Tk()
    root.title("summery movie!")
    root.geometry("1200x800")

    root.queryImg = displayImage(root, "/Users/ryou/Documents/SourceTree/movie_summery/1.png", 200,200,400,400)
    query = tkinter.Label(root, image = root.queryImg)
    query.pack(padx = 5, pady = 10)

    root.mainloop()


def ImageLoader(filepath):
    img_raw = Image.open(filepath)
    img_mat = np.array(img_raw, np.float32)
    img = img_mat.astype(np.uint8)
    img = PIL.Image.fromarray(img)
    img = PIL.ImageTk.PhotoImage(img)

    return img


def displayImage(root, filepath, x,y,w,h):
    img = ImageLoader(filepath)
    canvas = tkinter.Canvas(width = w, height = h)
    canvas.create_image(x, y, image = img)
    canvas.place(x=x, y=y)


if __name__ == '__main__':
    main()

#
# class Img():
#     def __init__(self, filepath):
#         img_raw = Image.open(filepath)
#         img_mat = np.array(img_raw, np.float32)
#         img = PIL.ImageTk.PhotoImage(img_mat)
#         img = PIL.Image.fromarray(img)
