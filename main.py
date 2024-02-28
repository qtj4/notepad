import re

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.font import families
from tkinter.ttk import *
from datetime import datetime
from tkinter import messagebox, filedialog, simpledialog, scrolledtext, colorchooser, font
from winsound import *



root = Tk()
root.title('Notepad')
root.resizable(0, 0)

notepad = scrolledtext.ScrolledText(root, width=90, height=40, undo=True)
current_file_path = None
fileName = ' '

notepad.pack()
fontname = "Consolas"
fontsize = 12

def play_sound(sound_type):
    if sound_type == "click":
        PlaySound("SystemAsterisk", SND_ALIAS)
    elif sound_type == "keyboard":
        PlaySound("SystemExclamation", SND_FILENAME)

def cmdNew():
    play_sound("keyboard")
    global current_file_path
    if len(notepad.get('1.0', END+'-1c'))>0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmdSave()
    notepad.delete(0.0, END)
    current_file_path = None
    root.title("Notepad")

def cmdOpen():
    play_sound("keyboard")
    global current_file_path
    fd = filedialog.askopenfile(parent=root, mode='r')
    if fd is not None:
        current_file_path = fd.name
        root.title(f"Notepad - {current_file_path}")
        t = fd.read()
        notepad.delete(0.0, END)
        notepad.insert(0.0, t)
        fd.close()

def cmdSave():
    play_sound("keyboard")
    global current_file_path
    if current_file_path is None:
        fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
        if fd is not None:
            current_file_path = fd.name
            root.title(f"Notepad - {current_file_path}")
            data = notepad.get('1.0', END)
            try:
                fd.write(data)
                fd.close()
            except:
                messagebox.showerror(title="Error", message="Not able to save file!")
    else:
        fd = open(current_file_path, 'w')
        data = notepad.get('1.0', END)
        try:
            fd.write(data)
            fd.close()
        except:
            messagebox.showerror(title="Error", message="Not able to save file!")

def cmdSaveAs():
    play_sound("keyboard")
    global current_file_path
    play_sound("click")
    fd = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if fd is not None:
        current_file_path = fd.name
        root.title(f"Notepad - {current_file_path}")
        t = notepad.get(0.0, END)
        try:
            fd.write(t.rstrip())
            fd.close()
        except:
            messagebox.showerror(title="Error", message="Not able to save file!")

def cmdExit():
    play_sound("keyboard")
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        root.destroy()



def cmdCut():
    play_sound("click")
    notepad.event_generate("<<Cut>>")

def cmdCopy():
    play_sound("click")
    notepad.event_generate("<<Copy>>")

def cmdPaste():
    play_sound("click")
    notepad.event_generate("<<Paste>>")

def cmdDelete():
    play_sound("click")
    notepad.event_generate("<<Clear>>")

def cmdUndo():
    play_sound("click")
    notepad.edit_undo()

def cmdRedo():
    play_sound("click")
    notepad.edit_redo()

def cmdSelectAll():
    play_sound("click")
    notepad.tag_add('sel','1.0','end')

def cmdFind():
    play_sound("click")
    findstring = simpledialog.askstring("Find...", "Enter text")
    textdata = notepad.get('1.0', END)
    occurance = textdata.upper().count(findstring.upper())
    if textdata.upper().count(findstring.upper())>0:
        label = messagebox.showinfo("Results", findstring + " has multiple occurances, " + str(occurance))
    else:
        label = messagebox.showinfo("Results", "Nothing found")

def cmdTimeDate():
    play_sound("click")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")
    notepad.insert(INSERT, current_time + " " + current_date)

def cmdAbout():
    messagebox.showinfo("About Notepad", "This is a simple notepad application created using Python and Tkinter.")

def cmdChangeBackground():
    play_sound("click")
    color = askcolor(title = "Select Background Color")
    notepad.config(bg = color[1])

def cmdChangeFont():
    play_sound("click")
    fonts = list(families())
    font = simpledialog.askstring("Font", "Enter font name", initialvalue = "Consolas")
    if font in fonts:
        notepad.config(font = (font, fontsize))
    else:
        messagebox.showerror("Font", "Invalid font name")

def cmdChangeFontSize():
    play_sound("click")
    global fontsize
    size = simpledialog.askinteger("Font Size", "Enter font size", initialvalue = 12)
    if size > 0:
        fontsize = size
        notepad.config(font = (fontname, fontsize))
    else:
        messagebox.showerror("Font Size", "Invalid font size")


context_menu = Menu(root, tearoff=0)

context_menu.add_command(label="Cut", command=cmdCut)
context_menu.add_command(label="Copy", command=cmdCopy)
context_menu.add_command(label="Paste", command=cmdPaste)
context_menu.add_command(label="Delete", command=lambda: notepad.delete('sel.first', 'sel.last'))
context_menu.add_command(label="Select All", command=cmdSelectAll)
context_menu.add_command(label="Undo", command=cmdUndo)
context_menu.add_command(label="Redo", command=cmdRedo)

def show_context_menu(event):
    play_sound("click")
    context_menu.tk_popup(event.x_root, event.y_root)

notepad.bind("<Button-3>", show_context_menu)


menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=cmdNew)
filemenu.add_command(label="Open", command=cmdOpen)
filemenu.add_command(label="Save", command=cmdSave)
filemenu.add_command(label="Save As", command=cmdSaveAs)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=cmdExit)


editmenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Cut", command=cmdCut)
editmenu.add_command(label="Copy", command=cmdCopy)
editmenu.add_command(label="Paste", command=cmdPaste)
editmenu.add_command(label="Select All", command=cmdSelectAll)
editmenu.add_command(label="Undo", command=cmdUndo)
editmenu.add_command(label="Redo", command=cmdRedo)
editmenu.add_separator()
editmenu.add_command(label="Find", command = cmdFind)
editmenu.add_command(label="Time/Date", command = cmdTimeDate)


formatmenu = Menu(menu, tearoff = 0)

menu.add_cascade(label="Format", menu = formatmenu)
formatmenu.add_command(label="Change Background", command = cmdChangeBackground)
formatmenu.add_command(label="Change Font", command = cmdChangeFont)
formatmenu.add_command(label="Change Font Size", command = cmdChangeFontSize)


helpmenu = Menu(menu, tearoff = 0)
menu.add_cascade(label="Help", menu = helpmenu)
helpmenu.add_command(label="About Notepad", command = cmdAbout)


notepad.pack()
root.mainloop()
