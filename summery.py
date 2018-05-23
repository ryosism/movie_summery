#! /usr/bin/env python

import tkinter as Tk
import PIL.Image
import PIL.ImageTk
import json
import sys


class Frame(Tk.Frame):
    def __init__(self, queryPath, candidatePath, master=None):
        Tk.Frame.__init__(self, master)
        self.master.title("summery movie!")
        self.master.geometry("1200x800")

        self.candidateImg = []

        #クエリ画像表示
        self.queryImg = []
        for row, file in zip(range(len(queryPath)), queryPath):
            image = PIL.Image.open(file)
            # image = image.resize([224, 224], resample=0)
            self.queryImg.append(PIL.ImageTk.PhotoImage(image))
            code = "self.query{} = Tk.Label(self, image=self.queryImg[{}])".format(row, row)
            exec(code)
            code = "self.query{}.grid(row={}, column=0, padx = 10, pady = 10)".format(row, row)
            exec(code)

        #クエリごとのTop5表示
        self.candidateImg = []
        for row in range(len(candidatePath)):
            for column, candidate in enumerate(candidatePath[row]):
                image = PIL.Image.open(candidate)
                image = image.resize([224, 126], resample=1)
                self.candidateImg.append(PIL.ImageTk.PhotoImage(image))
                code = "self.candidate{} = Tk.Label(self, image=self.candidateImg[{}])".format(column, column)
                exec(code)
                code = "self.candidate{}.grid(row={}, column={}, padx = 10, pady = 10)".format(column, row, column+1)
                exec(code)


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

    f = Frame(queryPath, candidatePath)
    f.pack(anchor = Tk.NW)
    f.mainloop()


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
