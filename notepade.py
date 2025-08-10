import tkinter as tk
from tkinter import messagebox, simpledialog, colorchooser, font
from tkinter.filedialog import askopenfilename, asksaveasfilename

current_file = None
dark_mode_on = False

# -------------------- Functions --------------------


# Function: Create a new file
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


# Function: Save file
def save_file():
    global current_file
    if current_file:
        file_location = current_file
    else:
        file_location = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )
        if not file_location:
            return
        current_file = file_location
    with open(file_location, "w", encoding="utf-8") as file_output:
        file_output.write(text_edit.get(1.0, tk.END))
    root.title(f"MY NOTEPAD - {file_location}")


# Function: Save as file
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


# Function: Open file
def open_file():
    global current_file
    file_location = askopenfilename(
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not file_location:
        return
    with open(file_location, "r", encoding="utf-8") as file_input:
        text_edit.delete(1.0, tk.END)
        text_edit.insert(tk.END, file_input.read())
    current_file = file_location
    root.title(f"MY NOTEPAD - {file_location}")


# Function: Undo
def undo_text():
    text_edit.edit_undo()


# Function: Redo
def redo_text():
    text_edit.edit_redo()


# Function: Copy
def copy_text():
    text_edit.event_generate("<<Copy>>")


# Function: Paste
def paste_text():
    text_edit.event_generate("<<Paste>>")


# Function: Cut
def cut_text():
    text_edit.event_generate("<<Cut>>")


# Function: Font selector
def select_font():
    font_name = simpledialog.askstring("Font", "Enter font family (e.g., Arial):")
    font_size = simpledialog.askinteger("Font Size", "Enter font size:")
    if font_name and font_size:
        text_edit.config(font=(font_name, font_size))


# Function: Update status bar
def update_status_bar(event=None):
    row, col = text_edit.index(tk.INSERT).split(".")
    status_bar.config(text=f"Line: {row} | Column: {col}")


# Function: Search and replace
def search_replace():
    search_word = simpledialog.askstring("Search", "Enter text to search:")
    replace_word = simpledialog.askstring("Replace", "Enter replacement text:")
    if search_word and replace_word is not None:
        content = text_edit.get(1.0, tk.END)
        new_content = content.replace(search_word, replace_word)
        text_edit.delete(1.0, tk.END)
        text_edit.insert(tk.END, new_content)


# Function: Dark mode
def toggle_dark_mode():
    global dark_mode_on
    dark_mode_on = not dark_mode_on
    if dark_mode_on:
        text_edit.config(bg="#1e1e1e", fg="white", insertbackground="white")
    else:
        text_edit.config(bg="white", fg="black", insertbackground="black")


# Function: About
def show_about():
    about_text = (
        "MY NOTEPAD\n"
        "---------------------------------\n"
        "این برنامه توسط مختار رحیمی توسعه داده شده است.\n"
        "هدف این برنامه ارائه یک ویرایشگر متن ساده، سریع و کاربرپسند است "
        "که امکانات اساسی مانند ذخیره، ویرایش، جستجو و تغییر ظاهر را فراهم می‌کند.\n"
        "\n"
        "توسعه یافته برای آموزش و تمرین برنامه‌نویسی با Python و Tkinter.\n"
        "سال توسعه: 2025"
    )
    messagebox.showinfo("About", about_text)


# -------------------- UI --------------------

root = tk.Tk()
root.title("MY NOTEPAD")
root.geometry("900x600")

text_edit = tk.Text(root, undo=True, wrap="word", font=("Arial", 12))
text_edit.pack(fill="both", expand=True)
text_edit.bind("<KeyRelease>", update_status_bar)

status_bar = tk.Label(root, text="Line: 1 | Column: 0", anchor="e")
status_bar.pack(fill="x", side="bottom")

# Menus
menu_bar = tk.Menu(root)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)

# Edit menu
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

# View menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)
view_menu.add_command(label="Select Font", command=select_font)
menu_bar.add_cascade(label="View", menu=view_menu)

# Help menu
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="About", command=show_about)
menu_bar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menu_bar)

root.mainloop()
