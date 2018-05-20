#! /usr/bin/env python

import tkinter as Tk
import PIL.Image, PIL.ImageTk

file = '/Users/ryou/Documents/SourceTree/movie_summery/1.png'

class Frame(Tk.Frame):
    def __init__(self, filepath, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title("summery movie!")
        self.master.geometry("1200x800")

        image = PIL.Image.open(filepath)
        self.img = PIL.ImageTk.PhotoImage(image)

        il = Tk.Label(self, image=self.img)
        il.pack()


if __name__ == '__main__':
    queryImgs = []

    queryImgs.append(Frame(filepath = '/Users/ryou/Documents/SourceTree/movie_summery/1.png'))
    queryImgs.append(Frame(filepath = '/Users/ryou/Documents/SourceTree/movie_summery/2.png'))

    queryImgs[0].pack(padx = 10, pady = 10, anchor = Tk.NW)
    queryImgs[0].mainloop()

    queryImgs[1].pack(padx = 10, pady = 10, anchor = Tk.NW)
    queryImgs[1].mainloop()
