import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

root = tk.Tk()
root.title("MY NOTEPAD")
root.rowconfigure(0, minsize=800)
root.columnconfigure(1, minsize=800)

text_edit = tk.Text(root)
frame_button = tk.Frame(root, relief=tk.RAISED, bd=3)
button_open = tk.Button(frame_button, text="open file")
button_save = tk.Button(frame_button, text="save file")
root.mainloop()