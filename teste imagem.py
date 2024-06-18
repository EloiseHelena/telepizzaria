from PIL import Image, ImageTk 
import tkinter as tk 

root = tk.Tk()
tkimage = ImageTk.PhotoImage(Image.open("imagens\Pizza-3007395.jpg"))
tk.Label(root, image=tkimage).pack()
root.mainloop()