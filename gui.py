from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
import os
import shutil

D_PATH = './data'
RULES_PATH = 'rules'
ADVENTURE_PATH = 'adventure'
CHARS_PATH = 'characters'


root = Tk(className=' LLM TTRPG')
frm_menu = None
frm_play = None
files = {}
# filename = askopenfilename()


def menu():
    global frm_menu, frm_play

    if frm_play is not None:
        frm_play.grid_forget()

    if frm_menu is not None:
        frm_menu.grid()
        return

    frm_menu = Frame(root, padding=10)
    frm_menu.grid()

    frm_intro = Frame(frm_menu, padding=10)
    frm_intro.grid(column=0, row=0)
    Label(frm_intro, text="LLM TTRPG").grid(column=0, row=0)
    Label(frm_intro, text="Introduction + Instructions").grid(column=0, row=1)

    Button(frm_menu, text="play", command=lambda: play()).grid(column=0, row=1)

    def add_file(sub_dir):
        global files

        path = askopenfilename()
        if not os.path.exists(path):
            return

        f_path = os.path.basename(path)
        f = {}
        
        f_path = os.path.join(D_PATH, sub_dir, f_path)

        try:
            shutil.copy(path, f_path)
        except:
            return

        frm_tmp = Frame(frm_filelist, padding=10)
        frm_tmp.grid(column=0, row=len(files))
        Label(frm_tmp, text=path).grid(column=0, row=0)
        
        if f_path.endswith('.pdf'):
            f['mode'] = 'txt'
            f['t'] = BooleanVar()
            Radiobutton(frm_tmp, text='text', variable=f['t'], value=False).grid(column=1, row=0)
            Radiobutton(frm_tmp, text='img', variable=f['t'], value=True).grid(column=2, row=0)
        
        Button(frm_tmp, text="X", command=lambda: remove_file(f_path)).grid(column=3, row=0)

        f['frame'] = frm_tmp
        files[f_path] = f

    def remove_file(path):
        global files

        if os.path.exists(path):
            os.remove(path)
        
        files[path]['frame'].grid_remove()
        del files[path]

    frm_files = Frame(frm_menu, padding=10)
    frm_files.grid(column=0, row=2)
    Button(frm_files, text="Load Rules Document", command=lambda: add_file(RULES_PATH)).grid(column=0, row=0)
    Button(frm_files, text="Load Adventure Document", command=lambda: add_file(ADVENTURE_PATH)).grid(column=1, row=0)
    Button(frm_files, text="Load Character Document", command=lambda: add_file(CHARS_PATH)).grid(column=2, row=0)

    frm_filelist = Frame(frm_menu, padding=10)
    frm_filelist.grid(column=0, row=3)


def play():
    global frm_menu, frm_play

    if frm_menu is not None:
        frm_menu.grid_forget()
    
    if frm_play is not None:
        frm_play.grid()
        return
    
    frm_play = Frame(root, padding=10)
    frm_play.grid()
    Label(frm_play, text="Playing").grid(column=0, row=0)
    Button(frm_play, text="menu", command=lambda: menu()).grid(column=1, row=0)


menu()
root.mainloop()
