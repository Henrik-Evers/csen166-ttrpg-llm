from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
import os
import shutil
import app

D_PATH = app.input_processing.D_PATH
RULES_PATH = app.input_processing.RULES_PATH
ADVENTURE_PATH = app.input_processing.ADVENTURE_PATH
CHARS_PATH = app.input_processing.CHARS_PATH


root = Tk(className=' LLM TTRPG')
frm_menu = None
frm_play = None
files = {}


# Draws and controls the menu.
def menu():
    global frm_menu, frm_play

    frm_menu = Frame(root, padding=10)
    frm_menu.grid()

    frm_intro = Frame(frm_menu, padding=10)
    frm_intro.grid(column=0, row=0)
    Label(frm_intro, text="LLM TTRPG").grid(column=0, row=0)
    Label(frm_intro, text="Introduction + Instructions").grid(column=0, row=1)

    Button(frm_menu, text="play", command=lambda: play()).grid(column=0, row=1)

    # If full_path is present, the file already exists.
    # sub_dir tells us which subdir of data to add to - characters, rules, or adventure.
    def add_file(sub_dir, full_path=None):
        global files

        if full_path is None:
            path = askopenfilename()
        else:
            path = full_path
        if not os.path.exists(path):
            return

        f_path = os.path.basename(path)
        f_path = os.path.join(D_PATH, sub_dir, f_path)
        
        files[f_path] = {'path': path}
        
        # Frame for this row
        frm_tmp = Frame(frm_filelist, padding=10)
        frm_tmp.grid(column=0, row=len(files))
        Label(frm_tmp, text=path).grid(column=0, row=0)
        
        # PDFs need to have a toggle for if they're converted to text or an image.
        if f_path.endswith('.pdf'):
            files[f_path]['mode'] = 'txt'
            files[f_path]['i'] = BooleanVar()
            if os.path.basename(path).startswith('i'):
                files[f_path]['i'].set(True)
            Radiobutton(frm_tmp, text='text', variable=files[f_path]['i'], value=False).grid(column=1, row=0)
            Radiobutton(frm_tmp, text='img', variable=files[f_path]['i'], value=True).grid(column=2, row=0)
        
        Button(frm_tmp, text="X", command=lambda: remove_file(f_path)).grid(column=3, row=0)

        files[f_path]['frame'] = frm_tmp

    # Unselect a file. Deletes it from the project directory.
    def remove_file(path):
        global files

        if os.path.exists(path):
            os.remove(path)
        
        files[path]['frame'].grid_remove()
        del files[path]

    # Frame for the file loading buttons
    frm_files = Frame(frm_menu, padding=10)
    frm_files.grid(column=0, row=2)
    Button(frm_files, text="Load Rules Document", command=lambda: add_file(RULES_PATH)).grid(column=0, row=0)
    Button(frm_files, text="Load Adventure Document", command=lambda: add_file(ADVENTURE_PATH)).grid(column=1, row=0)
    Button(frm_files, text="Load Character Document", command=lambda: add_file(CHARS_PATH)).grid(column=2, row=0)

    # Frame for the list of selected files
    frm_filelist = Frame(frm_menu, padding=10)
    frm_filelist.grid(column=0, row=3)

    # On load, add all files already in the folders with their current config
    for sub_path in (RULES_PATH, ADVENTURE_PATH, CHARS_PATH):
        for filename in os.listdir(os.path.join(D_PATH, sub_path)):
            file_path = os.path.join(D_PATH, sub_path, filename)
            add_file(sub_path, file_path)


# Draws and controls the interaction with the app.
def play():
    global frm_menu, frm_play, files

    # Copy over any loaded files that aren't in the project directory.
    for f_path in files:
        try:
            path = f_path
            if f_path.endswith('.pdf'):
                ht = os.path.split(f_path)
                if files[f_path]['i'].get() and not ht[1].startswith('i'):
                    path = os.path.join(ht[0], 'i' + ht[1])
                elif ht[1].startswith('i'):
                    path = os.path.join(ht[0], ht[1][1:])
            if files[f_path]['path'] != path:
                print('Copying: ' + f_path)
                print('To: ' + path)
                shutil.copy(files[f_path]['path'], path)
        except Exception as e:
            print('Could not copy: ' + files[f_path]['path'])
            print(e)

    if frm_menu is not None:
        frm_menu.grid_forget()
    
    frm_play = Frame(root, padding=10)
    frm_play.grid()
    output_txt = ScrolledText(frm_play, wrap='word', width=150)
    output_txt.grid(column=0, row=0, columnspan=2)
    output_txt.insert(END, '>>')
    output_txt.config(state=DISABLED)
    input_txt = ScrolledText(frm_play, wrap='word', height=4, width=150)
    input_txt.grid(column=0, row=1)
    Button(frm_play, text="Send", command=lambda: enter(), width=10).grid(column=1, row=1)

    root.update()

    # Trigger a message send
    def enter(event=None):
        msg = input_txt.get('1.0', 'end')
        input_txt.delete('1.0', 'end')
        submit_msg(msg)
    root.bind('<Return>', enter)

    # Send a message to the LLM and stream the response to output_txt
    def submit_msg(msg, show_prompt=True, show_response=True):

        if show_prompt:
            output_txt.config(state=NORMAL)
            output_txt.insert(END, msg)
            output_txt.config(state=DISABLED)
            root.update()

        for part in app.send_msg(msg):
            if part == -1:
                root.destroy()
                return
            if part == 0:
                output_txt.config(state=NORMAL)
                output_txt.insert(END, 'New save created. Check the project directory /saves.')
                output_txt.insert(END, '\n>>')
                output_txt.config(state=DISABLED)
                return
            if show_response:
                output_txt.config(state=NORMAL)
                output_txt.insert(END, part)
                output_txt.config(state=DISABLED)
                output_txt.see(END)
                root.update()
        
        if show_prompt or show_response:
            output_txt.config(state=NORMAL)
            output_txt.insert(END, '\n>>')
            output_txt.config(state=DISABLED)
            output_txt.see(END)
    
    app.setup()
    submit_msg('I am ready to start playing! Can you give a quick summary of the player character(s) and adventure, then get us started?', show_prompt=False)


menu()
root.mainloop()
