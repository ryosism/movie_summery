import tkinter as tk

root = tk.Tk()
text = tk.Text(root, height=10, width=40)
text.pack(side=tk.LEFT, fill=tk.Y)

canvas = tk.Canvas(root, width = 1500, height = 3000)
canvas.place(width = 0, height = 0)


scroll = tk.Scrollbar(root)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
scroll.config(command=canvas.yview)
# text.config(yscrollcommand=scroll.set)
canvas.configure(yscrollcommand = scroll.set)

for i in range(50):
    text.insert(tk.END, "message" + str(i) + "\n")

root.mainloop()
