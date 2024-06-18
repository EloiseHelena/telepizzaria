from PIL import Image, ImageTk 
import tkinter as tk 

root = tk.Tk()
tkimage = ImageTk.PhotoImage(Image.open("imagens\pizza1.avif"))
tk.Label(root, image=tkimage).pack()
root.mainloop()