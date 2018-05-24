from tkinter import *

root = Tk()
root.option_add("*font", ("FixedSys", 14))

# 式を格納するオブジェクト
buffer = StringVar()
buffer.set("")

# Entry の生成
e = Entry(root, textvariable = buffer)

# Listbox の生成
lb = Listbox(root)

# Scrollbar の生成
sb1 = Scrollbar(root, orient = 'v', command = lb.yview)
sb2 = Scrollbar(root, orient = 'h', command = lb.xview)

# Listbox の設定
lb.configure(yscrollcommand = sb1.set)
lb.configure(xscrollcommand = sb2.set)

# 計算
def calc(event):
    expr = buffer.get()
    lb.insert('end', expr)
    lb.see('end')
    value = eval(expr)
    buffer.set(str(value))

# 式の取り出し
def get_expr(event):
    buffer.set(lb.get('active'))

# バインディング
e.bind('<Return>', calc)
lb.bind('<Double-1>', get_expr)

# grid による配置
e.grid(row = 0, columnspan = 2, sticky = 'ew')
lb.grid(row = 1, column = 0, sticky = 'nsew')
sb1.grid(row = 1, column = 1, sticky = 'ns')
sb2.grid(row = 2, column = 0, sticky = 'ew')

# フォーカスの設定
e.focus_set()

root.mainloop()
