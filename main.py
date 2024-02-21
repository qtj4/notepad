import re
from tkinter import *
from tkinter.ttk import *
from datetime import datetime
from tkinter import messagebox
from tkinter import filedialog,simpledialog
from tkinter.scrolledtext import ScrolledText
from tkinter.colorchooser import askcolor
from tkinter.font import Font, families

root = Tk()
root.title('Notepad')
root.resizable(0, 0)


notepad = ScrolledText(root, width = 90, height = 40)
fileName = ' '

def cmdNew():
    global fileName
    if len(notepad.get('1.0', END+'-1c'))>0:
        if messagebox.askyesno("Notepad", "Do you want to save changes?"):
            cmdSave()
    notepad.delete(0.0, END)
    root.title("Notepad")

def cmdOpen():
    fd = filedialog.askopenfile(parent = root, mode = 'r')
    t = fd.read()
    notepad.delete(0.0, END)
    notepad.insert(0.0, t)

def cmdSave():
    fd = filedialog.asksaveasfile(mode = 'w', defaultextension = '.txt')
    if fd!= None:
        data = notepad.get('1.0', END)
        try:
            fd.write(data)
        except:
            messagebox.showerror(title="Error", message = "Not able to save file!")

def cmdSaveAs(): #file menu Save As option
    fd = filedialog.asksaveasfile(mode='w', defaultextension = '.txt')
    t = notepad.get(0.0, END)
    try:
        fd.write(t.rstrip())
    except:
        messagebox.showerror(title="Error", message = "Not able to save file!")

def cmdExit():
    if messagebox.askyesno("Notepad", "Are you sure you want to exit?"):
        root.destroy()

def cmdCut():
    notepad.event_generate("<<Cut>>")

def cmdCopy():
    notepad.event_generate("<<Copy>>")

def cmdPaste():
    notepad.event_generate("<<Paste>>")

def cmdDelete():
    notepad.event_generate("<<Clear>>")

def cmdSelectAll():
    notepad.tag_add('sel','1.0','end')

def cmdFind():
    findstring = simpledialog.askstring("Find...", "Enter text")
    textdata = notepad.get('1.0', END)
    occurance = textdata.upper().count(findstring.upper())
    if textdata.upper().count(findstring.upper())>0:
        label = messagebox.showinfo("Results", findstring + " has multiple occurances, " + str(occurance))
    else:
        label = messagebox.showinfo("Results", "Nothing found")

def cmdTimeDate():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%d/%m/%Y")
    notepad.insert(INSERT, current_time + " " + current_date)

def cmdAbout():
    messagebox.showinfo("About Notepad", "This is a simple notepad application created using Python and Tkinter.")

def cmdChangeBackground():
    color = askcolor(title = "Select Background Color")
    notepad.config(bg = color[1])

def cmdChangeFont():
    fonts = list(families())
    font = simpledialog.askstring("Font", "Enter font name", initialvalue = "Arial")
    if font in fonts:
        notepad.config(font = (font, fontsize))
    else:
        messagebox.showerror("Font", "Invalid font name")

def cmdChangeFontSize():
    global fontsize
    size = simpledialog.askinteger("Font Size", "Enter font size", initialvalue = 12)
    if size > 0:
        fontsize = size
        notepad.config(font = (fontname, fontsize))
    else:
        messagebox.showerror("Font Size", "Invalid font size")


menu = Menu(root)
root.config(menu=menu)


filemenu = Menu(menu, tearoff = 0)

menu.add_cascade(label="File", menu = filemenu)
filemenu.add_command(label="New", command = cmdNew)
filemenu.add_command(label="Open", command = cmdOpen)
filemenu.add_command(label="Save", command = cmdSave)
filemenu.add_command(label="Save As", command = cmdSaveAs)
filemenu.add_separator()
filemenu.add_command(label="Exit", command = cmdExit)


editmenu = Menu(menu, tearoff = 0)

menu.add_cascade(label="Edit", menu = editmenu)
editmenu.add_command(label="Cut", command = cmdCut)
editmenu.add_command(label="Copy", command = cmdCopy)
editmenu.add_command(label="Paste", command = cmdPaste)
editmenu.add_command(label="Delete", command = cmdDelete)
editmenu.add_separator()
editmenu.add_command(label="Find", command = cmdFind)
editmenu.add_command(label="Select All", command = cmdSelectAll)
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


fontname = "Arial"
fontsize = 12

root.mainloop()
