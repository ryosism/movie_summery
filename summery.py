#! /usr/bin/env python

import tkinter as Tk
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk
import json
import sys, os
import ffmpeg
import subprocess as sp


class QueryFrame(Tk.Frame):
    def __init__(self, row, query, candidate, allRadioButtonResults, allTextBoxStrings, master=None):
        def change_state():#---------------------------------------------
            allRadioButtonResults[row] = v.get() #候補にしたTop番号がここに入る
            print(allRadioButtonResults)
        #----------------------------------------------------------------

        def loadMore():#---------------------------------------------
            print("loadMore")
            unusedArray = self.candidate[0:5]
            del self.candidate[0:5]
            self.candidate += unusedArray

            for i in range(5):
                image = PIL.Image.open(self.candidate[i])
                image.thumbnail((120, 120), PIL.Image.ANTIALIAS)
                self.candidateImg.append(PIL.ImageTk.PhotoImage(image))
                code = "self.candidate{} = Tk.Label(self, image=self.candidateImg[{}])".format(i, i)
                exec(code)
                code = "self.candidate{}.grid(row = 1, column = {}, padx = 10, pady = 10)".format(i, i+1)
                exec(code)
        #---------------------------------------------

        def textOk():#---------------------------------------------
            print("write!")
            self.doneLabel.configure(text = "✅")
            allTextBoxStrings[row] = self.textBox.get()
            print(allTextBoxStrings)
        #---------------------------------------------

        Tk.Frame.__init__(self, master)
        self = Tk.LabelFrame(self, bd=2, relief="ridge", text="query {}".format(row+1))
        self.pack(fill="x", padx=5, pady=5)
        self.image = PIL.Image.open(query)
        self.image.thumbnail((120, 120), PIL.Image.ANTIALIAS)
        self.queryImg = (PIL.ImageTk.PhotoImage(self.image))
        self.query = Tk.Label(self, image=self.queryImg)
        self.query.grid(row = 1, rowspan = 3, column = 0, padx = 10, pady = 10)
        self.candidate = candidate

        v = Tk.IntVar()
        v.set(0)
        self.candidateImg = []
        for i in range(5):
            image = PIL.Image.open(self.candidate[i])
            image.thumbnail((120, 120), PIL.Image.ANTIALIAS)
            self.candidateImg.append(PIL.ImageTk.PhotoImage(image))
            code = "self.candidate{} = Tk.Label(self, image=self.candidateImg[{}])".format(i, i)
            exec(code)
            code = "self.candidate{}.grid(row = 1, column = {}, padx = 10, pady = 10)".format(i, i+1)
            exec(code)
            code = "self.radio{} = Tk.Radiobutton(self, text = '候補にする', variable = v, value = {}, command = change_state)".format(i, i)
            exec(code)
            code = "self.radio{}.grid(row=2, column = {}, sticky=Tk.N + Tk.S)".format(i, i+1)
            exec(code)

        self.reloadButton = Tk.Button(self, text = '次の候補', command = loadMore)
        self.reloadButton.grid(row = 1, column = 6, padx = 10, pady = 10)

        self.textBox = Tk.Entry(self)
        self.textBox.insert(Tk.END,"シーンの注釈を入力")
        self.textBox.grid(row = 3, column = 1, columnspan = 5, sticky = Tk.W + Tk.E, padx = 10, pady = 10)

        self.textOkButton = Tk.Button(self, text = "注釈を設定", command = textOk)
        self.textOkButton.grid(row = 3, column = 6, pady = 10)

        self.doneLabel = Tk.Label(self, text = "　 ")
        self.doneLabel.grid(row = 3, column = 7, pady = 10)



class MainFrame(Tk.Frame):
    def __init__(self, parent, queryPath, candidatePath, master=None):
        def doSummery():#------------------------------------------------------------------------------------
            print("summerizing... by",self.allRadioButtonResults)
            timeSeconds = []
            movieClips = []

            f = open("concat.txt", "w")

            for row in range(len(queryPath)):
                filePath = candidatePath[row][self.allRadioButtonResults[row]]
                fileName = filePath.split('/')[-1]
                timeSecond, ext = os.path.splitext(fileName)
                timeSeconds.append(timeSecond)
                cropMoviename = "clopMovie_{}.mp4".format(row+1)
                output = ffmpeg.output(self.stream, "clopMovie_{}.mp4".format(row+1), t = 20, ss = int(timeSecond)-10)
                ffmpeg.run(output)

                cmd = "ffmpeg -hide_banner -y -vf setpts=PTS/2.0 -af atempo=2.0 -ss {} -i {} -t {} clopMovie_{}.mp4".format(
                    (int(timeSecond)/30)-5, "/Users/Sobue/Downloads/YummyFTP/RakutenDS/Hamburg_mitsuru_2018-01-08.mp4", 20, row+1)
                f.write("file " + cropMoviename + "\n")
                sp.call(cmd, shell = True)

            f.close()
            cmd = "ffmpeg -hide_banner -y -f concat -i concat.txt -c copy summerizedMovie.mp4"
            sp.call(cmd, shell = True)
            messagebox.showinfo("summery movie!", "Done!")
        #--------------------------------------------------------------------------------------------------------

        super().__init__(parent)
        # self.master.title("summery movie!")
        self.stream = ffmpeg.input('/Users/Sobue/Downloads/YummyFTP/RakutenDS/Hamburg_mitsuru_2018-01-08.mp4')

        self.allRadioButtonResults = []
        self.allTextBoxStrings = []
        for i in range(len(candidatePath)):
            self.allRadioButtonResults.append(0)

        for i in range(len(candidatePath)):
            self.allTextBoxStrings.append("")

        for row in range(len(queryPath)):
            code = "self.queryFrame{} = QueryFrame(row, queryPath[row], candidatePath[row], self.allRadioButtonResults, self.allTextBoxStrings)".format(row)
            exec(code)
            code = "self.queryFrame{}.pack(anchor = Tk.NW)".format(row)
            exec(code)

        self.summeryButton = Tk.Button(parent, text = "選択したキーフレームで動画要約開始", command = doSummery, padx = 10, pady = 10)
        self.summeryButton.pack(side="bottom")

class App:

    def __init__(self, master, queryPath, candidatePath):
        # Allows update in later method
        self.master = master

        # Create scroll bar
        self.y_axis_scrollbar = Tk.Scrollbar(self.master)

        # Create canvas with yscrollcommmand from scrollbar, use xscrollcommand for horizontal scroll
        self.main_canvas = Tk.Canvas(self.master, yscrollcommand=self.y_axis_scrollbar.set)
        self.main_canvas.configure(scrollregion=(0,0,800,1000))

        # Configure and pack/grid scrollbar to master
        self.y_axis_scrollbar.configure(command=self.main_canvas.yview)
        self.y_axis_scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)

        # This is the frame all content will go to. The 'master' of the frame is the canvas
        self.content_frame = MainFrame(self.main_canvas, queryPath, candidatePath)

        # Place canvas on app pack/grid


        # create_window draws the Frame on the canvas. Imagine it as another pack/grid
        self.main_canvas.create_window(0, 0, width = 800, height = 1000, window=self.content_frame)
        self.main_canvas.pack(side='left', fill=Tk.BOTH, expand='True')

        self.master.grid_rowconfigure(0, weight=0, minsize=0)
        self.master.grid_rowconfigure(1, weight=1, minsize=0)


        # Call this method after every update to the canvas
        self.update_scroll_region()


    def update_scroll_region(self):
        ''' Call after every update to content in self.main_canvas '''
        self.master.update()
        self.main_canvas.configure(scrollregion=(0,0,800,1000))
        self.master.grid_rowconfigure(0, weight=0, minsize=0)
        self.master.grid_rowconfigure(1, weight=1, minsize=0)
        print(self.main_canvas.bbox('all'))


if __name__ == '__main__':
    with open("query_112.json", "r") as file:
        queryPath = json.load(file)

    with open("candidate_112.json", "r") as file:
        candidatePath = json.load(file)
        # -----------------------------
        # -----------------------------
        epoch = int(sys.argv[1])
        candidatePath = candidatePath[epoch]
        # -----------------------------
        # -----------------------------
    if os.path.exists("*.mp4"):
        os.remove("*.mp4")
    if os.path.exists("concat.txt"):
        os.remove("concat.txt")

    root = Tk.Tk()
    app = App(root, queryPath, candidatePath)

    root.mainloop()
