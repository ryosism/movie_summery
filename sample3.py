
from tkinter import *
import time

def a(event):
    canvas2.scan_mark(event.x, event.y)

def b(event):
    canvas2.scan_dragto(event.x, event.y, gain=1)

class ResizeCanvas(Canvas):

    def __init__(self, *args,**kwargs):
        super().__init__(*args, **kwargs)
        self.frame = args[0]
        self.bind("<Configure>", self.on_resize)

    def on_resize(self,event):
        # 右下のCanvasをリサイズに合わせて高さを自動調整
        self.height = self.frame.winfo_height() - 30 # 30 == canvas.height
        self.config(height=self.height)


if __name__ == '__main__':
    w, h = 200, 200        # ウィンドウサイズ
    r = 20                # 円の半径

    root = Tk()
    pw = PanedWindow(root, sashwidth = 10, orient = HORIZONTAL)

    # ウィンドウ左側のリストボックス
    listbox = Listbox(pw)
    for i in range(50):
        listbox.insert(END, i+1)
    pw.add(listbox)

    # ウィンドウ右側のスクロール可能Canvas
    frame = Frame(root)

    canvas = Canvas(frame, width = w, height=30, bg = "#aaaaaa")
    canvas2 = ResizeCanvas(frame, width = w, height = h, bg = "#cccccc", scrollregion=(0, 0, w*2, h*2))


    # キャンバス描画
    oval = canvas2.create_oval(w-r, h-r, w+r, h+r)

    canvas2.bind("<ButtonPress-1>",a)
    canvas2.bind("<B1-Motion>",b)


    # ウィジェットの配置
    canvas.grid(row=0, column=0, sticky=E+W)
    # スクロールバーの配置
    xscroll = Scrollbar(frame, orient=HORIZONTAL, command=canvas2.xview)
    xscroll.grid(row=3, column=0, sticky=E+W)
    yscroll = Scrollbar(frame, orient=VERTICAL, command=canvas2.yview)
    yscroll.grid(row=2, column=1, sticky=N+S)

    canvas2.config(xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
    canvas2.grid(row=2, column=0, sticky=N+E+W+S)

    # rowconfigureで一行目を固定
    frame.grid_rowconfigure(0, weight=0)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid(sticky=N+E+W+S)

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    pw.add(frame)
    pw.pack(expand = True, fill = BOTH)

    root.mainloop()
