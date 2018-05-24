#! /usr/bin/env python

import tkinter as Tk
import tkinter.ttk as ttk
import PIL.Image
import PIL.ImageTk
import json
import sys


class QueryFrame(Tk.Frame):
    def __init__(self, row, query, candidate, allRadioButtonResults, master=None):
        def change_state():
            allRadioButtonResults[row] = v.get() #候補にしたTop番号がここに入る
            print(allRadioButtonResults)


        Tk.Frame.__init__(self, master)
        self = Tk.LabelFrame(self, bd=2, relief="ridge", text="query {}".format(row+1))
        self.pack(fill="x", padx=5, pady=5)
        self.image = PIL.Image.open(query)
        self.image.thumbnail((120, 120), PIL.Image.ANTIALIAS)
        self.queryImg = (PIL.ImageTk.PhotoImage(self.image))
        self.query = Tk.Label(self, image=self.queryImg)
        # self.query.pack(side = 'left', padx = 10, pady = 10)
        self.query.grid(row = 1, column = 0, padx = 10, pady = 10)

        v = Tk.IntVar()
        v.set(0)
        self.candidateImg = []
        for i, file in enumerate(candidate):
            image = PIL.Image.open(file)
            image = image.resize([224, 126], resample=1)
            self.candidateImg.append(PIL.ImageTk.PhotoImage(image))
            code = "self.candidate{} = Tk.Label(self, image=self.candidateImg[{}])".format(i, i)
            exec(code)
            code = "self.candidate{}.grid(row = 1, column = {}, padx = 10, pady = 10)".format(i, i+1)
            exec(code)
            code = "self.radio{} = Tk.Radiobutton(self, text = '候補にする', variable = v, value = {}, command = change_state)".format(i, i)
            exec(code)
            code = "self.radio{}.grid(row=2, column = {}, sticky=Tk.N + Tk.S)".format(i, i+1)
            exec(code)


class MainFrame(Tk.Frame):
    # def update_scroll_region(self):
    #     ''' Call after every update to content in self.main_canvas '''
    #     self.master.update()
    #     self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def __init__(self, queryPath, candidatePath, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title("summery movie!")
        self.allRadioButtonResults = []
        for i in range(len(candidatePath)):
            self.allRadioButtonResults.append(0)

        # # Allows update in later method
        # self.master = master
        #
        # # Create scroll bar
        # self.y_axis_scrollbar = Tk.Scrollbar(self.master)
        #
        # # Create canvas with yscrollcommmand from scrollbar, use xscrollcommand for horizontal scroll
        # self.main_canvas = Tk.Canvas(self.master, yscrollcommand=self.y_axis_scrollbar.set)
        #
        # # Configure and pack/grid scrollbar to master
        # self.y_axis_scrollbar.config(command=self.main_canvas.yview)
        # self.y_axis_scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
        #
        # # This is the frame all content will go to. The 'master' of the frame is the canvas
        # self.content_frame = self.master
        #
        # # Place canvas on app pack/grid
        # self.main_canvas.pack(side='left', fill='both', expand='True')
        #
        # # create_window draws the Frame on the canvas. Imagine it as another pack/grid
        # self.main_canvas.create_window(0, 0, window=self.master, anchor='nw')
        #
        # # Call this method after every update to the canvas
        # self.update_scroll_region()

        for row in range(len(queryPath)):
            code = "self.queryFrame{} = QueryFrame(row, queryPath[row], candidatePath[row], self.allRadioButtonResults)".format(row)
            exec(code)
            code = "self.queryFrame{}.pack(anchor = Tk.NW)".format(row)
            exec(code)

        self.grid_rowconfigure(0, weight=1, minsize=0)
        self.grid_columnconfigure(0, weight=1, minsize=0)

        summeryButton = Tk.Button

if __name__ == '__main__':
    with open("query_112.json", "r") as file:
        queryPath = json.load(file)

    with open("candidate_112.json", "r") as file:
        candidatePath = json.load(file)
        # -----------------------------
        # -----------------------------
        epoch = 20
        candidatePath = candidatePath[epoch]
        # -----------------------------
        # -----------------------------

    mainFrame = MainFrame(queryPath, candidatePath)

    # mainFrame.canvas.pack()
    mainFrame.pack()
    mainFrame.mainloop()
