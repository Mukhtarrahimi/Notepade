import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, font, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename


# ------------------------------
#  Functions
# ------------------------------
def new_file():
    global current_file
    if text_edit.get(1.0, tk.END).strip():
        answer = messagebox.askyesnocancel("Save", "Do you want to save changes?")
        if answer:
            save_file()
        elif answer is None:
            return
    text_edit.delete(1.0, tk.END)
    current_file = None
    root.title("MY NOTEPAD - New File")


def save_file():
    file_location = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if not file_location:
        return
    with open(file_location, "w", encoding="utf-8") as file_output:
        text = text_edit.get(1.0, tk.END)
        file_output.write(text)
    root.title(f"MY NOTEPAD - {file_location}")


def save_as_file():
    global current_file
    file_location = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if not file_location:
        return
    current_file = file_location
    save_file()


def open_file():
    file_location = askopenfilename(
        filetypes=[("Text files", ".txt"), ("All files", "*.*")]
    )
    if not file_location:
        return
    text_edit.delete(1.0, tk.END)
    with open(file_location, "r", encoding="utf-8") as file_input:
        text = file_input.read()
        text_edit.insert(tk.END, text)
    root.title(f"MY NOTEPAD - {file_location}")


def undo_text():
    text_edit.edit_undo()


def redo_text():
    text_edit.edit_redo()


def copy_text():
    text_edit.event_generate("<<Copy>>")


def paste_text():
    text_edit.event_generate("<<Paste>>")


def cut_text():
    text_edit.event_generate("<<Cut>>")


def select_font():
    def apply_font():
        fname = font_family.get()
        fsize = font_size.get()
        fstyle = "normal"
        if bold_var.get():
            fstyle = "bold"
        if italic_var.get():
            fstyle = "italic" if fstyle == "normal" else fstyle + " italic"

        text_edit.config(font=(fname, fsize, fstyle))
        font_win.destroy()

    font_win = tk.Toplevel(root)
    font_win.title("Select Font")
    font_win.geometry("300x200")
    font_win.resizable(False, False)

    tk.Label(font_win, text="Font Family:").pack()
    font_family = ttk.Combobox(font_win, values=sorted(font.families()))
    font_family.set("Arial")
    font_family.pack()

    tk.Label(font_win, text="Font Size:").pack()
    font_size = tk.IntVar(value=12)
    tk.Spinbox(font_win, from_=8, to=72, textvariable=font_size).pack()

    bold_var = tk.BooleanVar()
    italic_var = tk.BooleanVar()
    tk.Checkbutton(font_win, text="Bold", variable=bold_var).pack()
    tk.Checkbutton(font_win, text="Italic", variable=italic_var).pack()

    tk.Button(font_win, text="Apply", command=apply_font).pack(pady=5)


def update_status_bar(event=None):
    row, col = text_edit.index(tk.INSERT).split(".")
    status_bar.config(text=f"Line: {row} | Column: {col}")


def search_replace():
    search_word = simpledialog.askstring("Search", "Enter text to search:")
    replace_word = simpledialog.askstring("Replace", "Enter replacement text:")
    if search_word and replace_word is not None:
        content = text_edit.get(1.0, tk.END)
        new_content = content.replace(search_word, replace_word)
        text_edit.delete(1.0, tk.END)
        text_edit.insert(tk.END, new_content)


def about():
    messagebox.showinfo(
        "About",
        "MY NOTEPAD\n\n"
        "این برنامه توسط مختار رحیمی توسعه داده شده است.\n"
        "هدف از ساخت این نرم‌افزار، ایجاد یک ویرایشگر متن ساده و کارآمد "
        "برای یادگیری و تمرین برنامه‌نویسی پایتون با رابط کاربری گرافیکی (Tkinter) می‌باشد.\n"
        "امکانات برنامه شامل:\n"
        "- ایجاد، ذخیره، و باز کردن فایل‌های متنی\n"
        "- تغییر فونت و اندازه نوشته\n"
        "- جستجو و جایگزینی متن\n"
        "- ویرایش سریع با Undo/Redo, Copy, Paste و Cut\n\n"
        "تمام حقوق محفوظ است © 2025",
    )


# ------------------------------
#  Main UI
# ------------------------------
root = tk.Tk()
root.title("MY NOTEPAD")
root.geometry("1000x600")

text_edit = tk.Text(root, undo=True, font=("Arial", 12))
text_edit.pack(expand=True, fill="both")
text_edit.bind("<KeyRelease>", update_status_bar)

status_bar = tk.Label(root, text="Line: 1 | Column: 0", anchor="e")
status_bar.pack(fill="x", side="bottom")

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", command=undo_text)
edit_menu.add_command(label="Redo", command=redo_text)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Search & Replace", command=search_replace)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

format_menu = tk.Menu(menu_bar, tearoff=0)
format_menu.add_command(label="Select Font", command=select_font)
menu_bar.add_cascade(label="Format", menu=format_menu)

help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=about)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)
root.mainloop()
