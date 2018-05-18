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


class App():
    def __init__(self, master=None):
        self.queryImg = displayImage(self, "/Users/Sobue/Downloads/2.png", 200,200,400,400)

        app.title("summery movie!")
        app.geometry("1200x800")
        self.init()
        self.pack()


# class Img():
    # def __init__(self, filepath):
        # img_raw = Image.open(filepath)
        # img_mat = np.array(img_raw, np.float32)
        # img = PIL.ImageTk.PhotoImage(img_mat)
        # img = PIL.Image.fromarray(img)


def displayImage(app, filepath, x,y,w,h):
    # image = Img(filepath)
    # print(image)
    canvas = tkinter.Canvas(app, width = w, height = h)
    img = ImageTk.PhotoImage(file=filepath)
    canvas.create_image(x, y, image = image)
    canvas.place(x=x, y=y)


if __name__ == '__main__':
    app = App()
    app.pack()
    app.mainloop()
