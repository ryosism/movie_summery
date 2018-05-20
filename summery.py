#! /usr/bin/env python

import tkinter as Tk
import PIL.Image, PIL.ImageTk


class Frame(Tk.Frame):
    def __init__(self, filepath, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title("summery movie!")
        self.master.geometry("1200x800")

        self.queryImg = []
        for i, file in enumerate(filepath):
            image = PIL.Image.open(file)
            self.queryImg.append(PIL.ImageTk.PhotoImage(image))

            code = "self.query{} = Tk.Label(self, image=self.queryImg[{}])".format(i, i)
            exec(code)

            code = "self.query{}.pack(padx = 10, pady = 10, anchor = Tk.NW)".format(i)
            exec(code)


if __name__ == '__main__':
    filepath = [
        '/Users/ryou/Documents/SourceTree/movie_summery/1.png',
        '/Users/ryou/Documents/SourceTree/movie_summery/2.png',
        '/Users/ryou/Documents/SourceTree/movie_summery/3.png',
        '/Users/ryou/Documents/SourceTree/movie_summery/4.png']

    f = Frame(filepath)
    f.pack(anchor = Tk.NW)
    f.mainloop()
