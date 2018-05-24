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
        # self.grid(padx=5, pady=5)

        self.image = PIL.Image.open(query)
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
            # code = "self.radio{}.pack(padx = 10, pady = 10, anchor = Tk.NW)".format(i, i+1)
            code = "self.radio{}.grid(row=2, column = {})".format(i, i+1)
            exec(code)


class MainFrame(Tk.Frame):
    def __init__(self, queryPath, candidatePath, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title("summery movie!")
        self.master.geometry("1500x1000")
        self.allRadioButtonResults = []
        for i in range(len(candidatePath)):
            self.allRadioButtonResults.append(0)

        self.canvas = Tk.Canvas(self, scrollregion=("0c", "0c",  "40c",  "40c"), width="10c", height="10c")
        self.canvas.create_window(0, 0, window = self)
        yScrollbar = Tk.Scrollbar(self.master, orient=Tk.VERTICAL, command=self.canvas.yview)
        yScrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
        self.canvas.grid(row=0, column=0)
        self.canvas.configure(yscrollcommand = yScrollbar.set)

        for row in range(len(queryPath)):
            code = "self.queryFrame{} = QueryFrame(row, queryPath[row], candidatePath[row], self.allRadioButtonResults)".format(row)
            exec(code)
            code = "self.queryFrame{}.pack(anchor = Tk.NW)".format(row)
            exec(code)

        self.grid_rowconfigure(0, weight=1, minsize=0)
        self.grid_columnconfigure(0, weight=1, minsize=0)

        # self.canvas.pack()
        # self.pack()

        # #クエリ画像表示
        # self.queryImg = []
        # for row, file in zip(range(len(queryPath)), queryPath):
        #     image = PIL.Image.open(file)
        #     # image = image.resize([224, 224], resample=0)
        #     self.queryImg.append(PIL.ImageTk.PhotoImage(image))
        #     code = "self.query{} = Tk.Label(self, image=self.queryImg[{}])".format(row, row)
        #     exec(code)
        #     code = "self.query{}.grid(row={}, column=0, padx = 10, pady = 10)".format(row, row)
        #     exec(code)
        #
        # #クエリごとのTop5表示
        # self.candidateImg = []
        # for row in range(len(candidatePath)):
        #     for column, candidate in enumerate(candidatePath[row]):
        #         image = PIL.Image.open(candidate)
        #         image = image.resize([224, 126], resample=1)
        #         self.candidateImg.append(PIL.ImageTk.PhotoImage(image))
        #         code = "self.candidate{} = Tk.Label(self, image=self.candidateImg[{}])".format(column, column)
        #         exec(code)
        #         code = "self.candidate{}.grid(row={}, column={}, padx = 10, pady = 10)".format(column, row, column+1)
        #         exec(code)


if __name__ == '__main__':
    with open("query.json", "r") as file:
        queryPath = json.load(file)

    with open("candidate.json", "r") as file:
        candidatePath = json.load(file)
        # -----------------------------
        # -----------------------------
        epoch = 1
        candidatePath = candidatePath[epoch]
        # -----------------------------
        # -----------------------------

    mainFrame = MainFrame(queryPath, candidatePath)

    # mainFrame.canvas.pack()
    mainFrame.pack()
    mainFrame.mainloop()


# epochごとの推論のログはここで読み込ませたいから、

# query186.log
# <query1ファイル名>
# <query2ファイル名>
# <query3ファイル名>
# <query4ファイル名>
# <query5ファイル名>
# ...

# candidate_186.py
# <q1_top1ファイル名>
# <q1_top2ファイル名>
# <q1_top3ファイル名>
# <q1_top4ファイル名>
# <q1_top5ファイル名>
# <q1_top6ファイル名>
# <q1_top7ファイル名>
# <q1_top8ファイル名>
# <q1_top9ファイル名>
# <q1_top10ファイル名>
# <q2_top1ファイル名>
# <q2_top2ファイル名>
# <q2_top3ファイル名>
# <q2_top4ファイル名>
# <q2_top5ファイル名>
# <q2_top6ファイル名>
# <q2_top7ファイル名>
# <q2_top8ファイル名>
# <q2_top9ファイル名>
# <q2_top10ファイル名>
# とかにして10個ごとにreadlineか何かで配列にすれば良いのかな、んでselectedTop5に書き出させればいいかな

# にしたい、jsonにすると処理と整形が面倒だからreadlineとかで読み込ませたいなぁ
