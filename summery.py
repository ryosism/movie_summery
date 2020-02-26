#! /usr/bin/env python

import tkinter as Tk
from tkinter import messagebox
import PIL.Image
import PIL.ImageTk
import random
import json
import sys, os
import ffmpeg
import subprocess as sp
from glob import glob
from pathlib import Path
import matplotlib
matplotlib.use('tkagg')
#
# print("Configureing moviepy...")
# from moviepy import editor as mp


class QueryFrame(Tk.Frame):
    def __init__(self, parent, row, query, candidate, allRadioButtonResults, allTextBoxStrings, master=None):
        def change_state():#---------------------------------------------
            allRadioButtonResults[row] = v.get() #候補にしたTop番号がここに入る
            print(allRadioButtonResults)
        #----------------------------------------------------------------

        def loadMore():#---------------------------------------------
            unusedArray = self.candidate[0:5]
            del self.candidate[0:5]
            self.candidate += unusedArray

            for i in range(5):
                image = PIL.Image.open(self.candidate[i])
                image.thumbnail((180, 180), PIL.Image.ANTIALIAS)
                self.candidateImg.append(PIL.ImageTk.PhotoImage(image))
                code = "self.candidate{} = Tk.Label(self, image=self.candidateImg[{}])".format(i, i)
                exec(code)
                code = "self.candidate{}.grid(row = 1, column = {}, padx = 5)".format(i, i+1)
                exec(code)
        #---------------------------------------------

        def textOk():#---------------------------------------------
            self.doneLabel.configure(text = "✅")
            allTextBoxStrings[row] = self.textBox.get()
            print(allTextBoxStrings)
        #---------------------------------------------

        def prevScene(candidateNum):
            def x():
                currentPath = candidate[candidateNum]
                fileName = currentPath.split('/')[-1]
                timeSecond, ext = os.path.splitext(fileName)
                timeSecond = int(timeSecond)-600
                fileName = str(timeSecond).zfill(7) + ext
                dirPathArray = currentPath.split('/')
                dirPathArray.pop()
                dirPath = ""
                for path in dirPathArray:
                    dirPath += path + "/"

                newPath = dirPath + fileName
                self.candidate[candidateNum] = newPath

                # これを動かしたい
                candidatePath[row] = self.candidate

                image = PIL.Image.open(newPath)
                image.thumbnail((180, 180), PIL.Image.ANTIALIAS)
                self.candidateImg[candidateNum] = image

                self.candidateImg = []
                for i in range(5):
                    image = PIL.Image.open(self.candidate[i])
                    image.thumbnail((180, 180), PIL.Image.ANTIALIAS)
                    self.candidateImg.append(PIL.ImageTk.PhotoImage(image))
                    code = "self.candidate{} = Tk.Label(self, image=self.candidateImg[{}])".format(i, i)
                    exec(code)
                    code = "self.candidate{}.grid(row = 1, column = {}, padx = 5)".format(i, i+1)
                    exec(code)
            return x

        def nextScene(candidateNum):
            def x():
                currentPath = candidate[candidateNum]
                fileName = currentPath.split('/')[-1]
                timeSecond, ext = os.path.splitext(fileName)
                timeSecond = int(timeSecond)+600
                fileName = str(timeSecond).zfill(7) + ext
                dirPathArray = currentPath.split('/')
                dirPathArray.pop()
                dirPath = ""
                for path in dirPathArray:
                    dirPath += path + "/"

                newPath = dirPath + fileName
                self.candidate[candidateNum] = newPath

                # これを動かしたい
                candidatePath[row] = self.candidate

                image = PIL.Image.open(newPath)
                image.thumbnail((180, 180), PIL.Image.ANTIALIAS)
                self.candidateImg[candidateNum] = image

                self.candidateImg = []
                for i in range(5):
                    image = PIL.Image.open(self.candidate[i])
                    image.thumbnail((180, 180), PIL.Image.ANTIALIAS)
                    self.candidateImg.append(PIL.ImageTk.PhotoImage(image))
                    code = "self.candidate{} = Tk.Label(self, image=self.candidateImg[{}])".format(i, i)
                    exec(code)
                    code = "self.candidate{}.grid(row = 1, column = {}, padx = 5)".format(i, i+1)
                    exec(code)
            return x


        super().__init__(parent, master)
        self = Tk.LabelFrame(self, bd=2, relief="ridge", text="query {}".format(row+1))
        self.pack(fill="x", padx=5, pady=5)
        self.image = PIL.Image.open(query)
        self.image.thumbnail((180, 180), PIL.Image.ANTIALIAS)
        self.queryImg = (PIL.ImageTk.PhotoImage(self.image))
        self.query = Tk.Label(self, image=self.queryImg)
        self.query.grid(row = 1, rowspan = 3, column = 0, padx = 10, pady = 10)
        self.candidate = candidate

        v = Tk.IntVar()
        v.set(0)
        self.candidateImg = []
        for i in range(5):
            image = PIL.Image.open(self.candidate[i])
            image.thumbnail((180, 180), PIL.Image.ANTIALIAS)
            self.candidateImg.append(PIL.ImageTk.PhotoImage(image))
            code = "self.candidate{} = Tk.Label(self, image=self.candidateImg[{}])".format(i, i)
            exec(code)
            code = "self.candidate{}.grid(row = 1, column = {}, padx = 5)".format(i, i+1)
            exec(code)
            code = "self.radio{} = Tk.Radiobutton(self, text = 'Set as keyframe', variable = v, value = {}, command = change_state)".format(i, i)
            exec(code)
            code = "self.radio{}.grid(row=3, column = {}, pady = 5, sticky=Tk.N + Tk.S)".format(i, i+1)
            exec(code)
            code = "self.prevButton{} = Tk.Button(self, text = '◀︎-20(sec)', command = prevScene(i)).grid(row = 2, column = {}, padx = 2, sticky = Tk.W)".format(i, i+1)
            exec(code)
            code = 'self.nextButton{} = Tk.Button(self, text = "+20(sec)▶︎", command = nextScene(i)).grid(row = 2, column = {}, padx = 2, sticky = Tk.E)'.format(i, i+1)
            exec(code)

        # self.reloadButton = Tk.Button(self, text = '次の候補', command = loadMore)
        # self.reloadButton.grid(row = 1, column = 6, padx = 10, pady = 10)

        self.textBox = Tk.Entry(self, font=("",12))
        self.textBox.insert(Tk.END,"Input scene description")
        self.textBox.grid(row = 1, column = 6, columnspan = 9, sticky = Tk.W + Tk.E, padx = 10, pady = 10)

        self.textOkButton = Tk.Button(self, text = "Apply description", command = textOk)
        self.textOkButton.grid(row = 2, column = 6)

        self.doneLabel = Tk.Label(self, text = "　 ")
        self.doneLabel.grid(row = 2, column = 7, pady = 10)



class MainFrame(Tk.Frame):
    def __init__(self, parent, queryPath, candidatePath, fullVideoPath, master=None):
        def doSummery():#------------------------------------------------------------------------------------
            print("summerizing... by",self.allRadioButtonResults)
            timeSeconds = []
            movieClips = []

            concat = open("concat.txt", "w")
            zimaku = open("zimaku.srt", "w")

            secondsForScene = int(50/len(queryPath))

            concat.write("file clopMovie_{}.mp4\n".format(str(len(queryPath))))
            zimaku.write("1\n")
            zimaku.write("00:00:00,000 --> 00:00:{},000\n".format(str(secondsForScene).zfill(2)))
            zimaku.write("{}\n\n".format(self.lastEntry.get()))

            for row in range(len(queryPath)):
                filePath = candidatePath[row][self.allRadioButtonResults[row]]
                fileName = filePath.split('/')[-1]
                timeSecond, ext = os.path.splitext(fileName)
                timeSeconds.append(timeSecond)
                clopMoviename = "clopMovie_{}.mp4".format(row+1)

                cmd = "ffmpeg -hide_banner -y -r 90 -ss {} -i {} -t {} {}".format((int(timeSecond)/30)-(secondsForScene/2), str(fullVideoPath), secondsForScene, clopMoviename)
                sp.call(cmd, shell = True)

                # video = mp.VideoFileClip("clopMovie_{}.mp4".format(row+1))
                # txt_clip = mp.TextClip(self.allTextBoxStrings[row],fontsize=40,color='white').set_position('center','South').set_duration(10)
                # result = mp.CompositeVideoClip([video, txt_clip])
                # result.write_videofile("clopMovie_{}_edited.mp4",format(row+1),fps=30)

                concat.write("file " + clopMoviename + "\n")

                zimaku.write("{}\n".format(row+2))
                zimaku.write("00:00:{},000 --> 00:00:{},000\n".format(str((row+1) * secondsForScene).zfill(2), str((row+2) * secondsForScene).zfill(2)))
                zimaku.write(self.allTextBoxStrings[row] +"\n\n")

            zimaku.close()
            concat.close()

            cmd = "ffmpeg -hide_banner -y -f concat -i concat.txt -c copy summerizedMovie.mp4"
            sp.call(cmd, shell = True)
            cmd = "ffmpeg -i summerizedMovie.mp4 -vf subtitles=zimaku.srt:force_style=FontSize=40 summerizedMovie_srt.mp4"
            sp.call(cmd, shell = True)

            messagebox.showinfo("summery movie!", "Done!")
            # sys.exit()
        #--------------------------------------------------------------------------------------------------------

        super().__init__(parent)
        # self.master.title("summery movie!")
        self.stream = ffmpeg.input(str(fullVideoPath))

        self.allRadioButtonResults = []
        self.allTextBoxStrings = []
        for i in range(len(candidatePath)):
            self.allRadioButtonResults.append(0)

        for i in range(len(candidatePath)):
            self.allTextBoxStrings.append("")

        for row in range(len(queryPath)):
            code = "self.queryFrame{} = QueryFrame(self, row, queryPath[row], candidatePath[row], self.allRadioButtonResults, self.allTextBoxStrings)".format(row)
            exec(code)
            code = "self.queryFrame{}.pack(anchor = Tk.NW)".format(row)
            exec(code)

        self.summeryButton = Tk.Button(self, text = "Summarize movie by selected keyframe!", command = doSummery, padx = 10, pady = 10)
        self.summeryButton.pack(side="bottom")

        # # 一番最後のフレームをとる！
        self.lastFlame = Tk.Frame(self)
        self.lastText = Tk.Label(self.lastFlame, text = "Please input title text.")
        self.lastText.grid(row = 0, column = 0, padx = 5, pady = 5)

        self.lastEntry = Tk.Entry(self.lastFlame, font=("",12))
        self.lastEntry.insert(Tk.END,"input title")
        self.lastEntry.grid(row = 1, column = 0, columnspan = 1, sticky = Tk.S + Tk.E + Tk.W, padx = 10, pady = 10)
        # self.lastFlamelabel = Tk.LabelFrame(self, bd=2, relief="ridge", text="openning & closing")
        # self.lastFlamelabel.pack(padx=5, pady=5)
        #
        # frames = glob("/Users/ryou/Downloads/Yummy_FTP_Watcher/triplet/Hamburg_mitsuru30_resize/*")
        # frames.sort()
        # self.lastText = Tk.Label(self.lastFlame, text = "一番美味しそうな動画フレームを選んでください")
        # self.lastText.grid(row = 0, column = 0, padx = 5, pady = 5)
        #
        # self.lastImage = PIL.Image.open(frames[-1])
        # self.lastImage.thumbnail((180, 180), PIL.Image.ANTIALIAS)
        # self.lastImg = PIL.ImageTk.PhotoImage(self.lastImage)
        # self.lastFrameImg = Tk.Label(self.lastFlame, image=self.lastImg)
        # self.lastFrameImg.grid(row = 1, column = 9, padx = 5, pady = 5)
        #
        self.lastFlame.pack(anchor = Tk.S, side = 'bottom')

class App:

    def __init__(self, master, queryPath, candidatePath, fullVideoPath):
        # Allows update in later method
        self.master = master
        self.master.title("movie summery")
        self.master.geometry("1920x1000")

        # Create scroll bar
        self.y_axis_scrollbar = Tk.Scrollbar(self.master)
        self.x_axis_scrollbar = Tk.Scrollbar(self.master)

        # Create canvas with yscrollcommmand from scrollbar, use xscrollcommand for horizontal scroll
        self.main_canvas = Tk.Canvas(self.master, yscrollcommand=self.y_axis_scrollbar.set, xscrollcommand=self.x_axis_scrollbar.set)
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox('all'))




        # Configure and pack/grid scrollbar to master
        self.y_axis_scrollbar.configure(command=self.main_canvas.yview)
        self.y_axis_scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)

        self.x_axis_scrollbar.configure(command=self.main_canvas.xview)
        self.x_axis_scrollbar.pack(side=Tk.BOTTOM, fill=Tk.X)

        # This is the frame all content will go to. The 'master' of the frame is the canvas
        self.content_frame = MainFrame(self.main_canvas, queryPath, candidatePath, fullVideoPath)

        # Place canvas on app pack/grid


        #マウスカーソルが乗ったときX軸Y軸スクロールバーをバインド



        # create_window draws the Frame on the canvas. Imagine it as another pack/grid
        self.main_canvas.create_window(0, 0, window=self.content_frame)
        self.main_canvas.pack(side='left', fill=Tk.BOTH, expand='True')

        self.master.grid_rowconfigure(0, weight=0, minsize=0)
        # self.master.grid_rowconfigure(1, weight=1, minsize=0)

        self.y_axis_scrollbar.bind('<MouseWheel>', lambda e:self.main_canvas.yview_scroll(-1*(1 if e.delta>0 else -1),UNITS))
        self.y_axis_scrollbar.bind('<Enter>',lambda e:self.y_axis_scrollbar.focus_set())
        self.main_canvas.bind('<Enter>',lambda e:self.y_axis_scrollbar.focus_set())
        self.x_axis_scrollbar.bind('<MouseWheel>', lambda e:self.main_canvas.xview_scroll(-1*(1 if e.delta>0 else -1),UNITS))
        self.x_axis_scrollbar.bind('<Enter>',lambda e:self.x_axis_scrollbar.focus_set())

        # Call this method after every update to the canvas
        self.update_scroll_region()


    def update_scroll_region(self):
        ''' Call after every update to content in self.main_canvas '''
        self.master.update()
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox('all'))
        self.master.grid_rowconfigure(0, weight=0, minsize=0)
        self.master.grid_rowconfigure(1, weight=1, minsize=0)
        print(self.main_canvas.bbox('all'))


def fixButtonLabel():
    a = root.winfo_geometry().split('+')[0]
    b = a.split('x')
    w = int(b[0])
    h = int(b[1])
    root.geometry('%dx%d' % (w+1,h+1))



if __name__ == '__main__':
    fullVideoPath = Path(sys.argv[1])

    with open("015_whole_query.json", "r") as file:
        queryPath = json.load(file)

    with open("015_merge_candidate_detection_wo100words_noun.json", "r") as file:
        candidatePath = json.load(file)

    epoch = random.randint(0, len(candidatePath))
    candidatePath = candidatePath[epoch]
    paths = glob("*.mp4")
    for path in paths:
        os.remove(path)
    if os.path.exists("concat.txt"):
        os.remove("concat.txt")
    if os.path.exists("*.srt"):
        os.remove("*.srt")

    root = Tk.Tk()
    app = App(root, queryPath, candidatePath, fullVideoPath)
    root.update()
    root.after(0, fixButtonLabel)

    root.mainloop()
