#!/usr/bin/env python3

__author__ = 'Shake'
__version__ = '1.0.0'


import os
import tkinter.messagebox
from tkinter import *
from mttkinter import *
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import subprocess
from shlex import split
from functools import partial
import json
import matplotlib.pyplot as plt

def start(pathname, is_save, is_video):

    #first check path: 1.a single file 2.folder contains subfolders 3.invaild path
    if os.path.isdir(pathname):
        isdir = True
    elif os.path.isfile(pathname):
        isdir = False
    else:
        tkinter.messagebox.showerror(title='Error', message='Input is not a vaild file or folder.')
        return -1

    win = Toplevel()
    win.title('Analyze results')
    win.geometry('920x570+350+100')
    win.resizable(width=False, height=True)
    win.configure(bg='#191919')

    canvas = Win_Canvas(win)

    #if pathname is a folder, find all subfolders; if pathname is a file, just put it in the list.
    dirs_for_analyze = [pathname]
    for root, dirs, files in os.walk(pathname):
        for dir in dirs:
            dirs_for_analyze.append(os.path.join(root, dir))
    # print(dirs_for_analyze)

    # About to call external process and change the window with button
    # First prepare the arguments
    arguments = './test.py -j '
    if is_video:
        arguments += '-V '
        if is_save:
            tkinter.messagebox.showwarning(title='Warning', message='Saving every result frame from a video will greatly slow down the speed and cost lots of space. So the program will not save the result frame.')
    elif is_save:
        arguments += '-s '
    

    global results
    button = {}
    results = {}

    def finished(result, path):
        ret, out, err = result
        if ret == 0:
            show_fig = partial(show_figure, path=path)
            button[path].change_look(win, True, show_fig)
        else:
            msg = 'Error occured.'
            show_err = partial(show_error, msg = msg)
            button[path].change_look(win, False, show_err)

    pool = ThreadPool(cpu_count())
    for path in dirs_for_analyze:
        btn = Win_Button(canvas.frame, path)
        button[path] = btn
        canvas.put_button(win, btn.button)
        canvas.put_text(win, btn.text)
        
        argument = ''
        argument += arguments
        argument += path
        finish_callback = partial(finished, path=path)
        results[path] = pool.apply_async(call_proc, (argument,), callback=finish_callback)

    pool.close()


    win.mainloop()

def call_proc(cmd):
    p = subprocess.Popen(split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return (p.returncode, out, err)

def show_figure(path):
    global results
    ret, out, err = results[path].get()
    content = json.loads(out.decode('utf-8'))
    # content = {'path':'/home/shake', 'max':3.9, 'stdevp':2.8, '1.jpg':2, '2.mim':3.6, '4.jpg':1.7, '5.png':2.5}
    draw_fig(content)

def show_error(msg):
    tkinter.messagebox.showerror(title='Error', message=msg)

def draw_fig(content):
    fig = plt.figure(figsize=(12,7), facecolor='gray', edgecolor='#191919')
    ax = plt.subplot()
    fig.canvas.set_window_title(content['path'])

    plt.ylim(0, content['max']+0.5)
    x = list(content.keys())[3:]
    y = list(content.values())[3:]

    max = 'max: ' + str(content['max'])
    stdevp = 'stdevp: ' + str(content['stdevp'])

    ax.scatter(x, y, s=50, color='red', marker='o', label=max)
    ax.plot(x, y, color='blue', linestyle=':', linewidth=0.5, label=stdevp)
    
    for i in list(content.keys())[3:]:
        ax.annotate(content[i], xy=(i,content[i]+0.02), fontsize=10, color='green', xycoords='data')

    plt.legend()
    
    plt.show()

def print1():
    print('fuck')

class Win_Canvas(object):
    def __init__(self, root):
        self.__row_button = 0
        self.__column_button = 0
        self.__row_text = 1
        self.__column_text =0

        self.scrollbar = Scrollbar(root, bg='black', troughcolor='#191919', width=8)
        self.scrollbar.pack(side='right', fill='y')
        self.canvas = Canvas(root, bg='#191919', yscrollcommand=self.scrollbar.set)
        self.canvas.pack(expand=True, fill=BOTH)
        self.scrollbar.config(command=self.canvas.yview)

        self.frame = Frame(self.canvas, bg='#393e46')
        # self.frame.pack(expand=True, fill=BOTH)
        self.frame_id = self.canvas.create_window(0, 0, window=self.frame, anchor='nw')
        # self.canvas.bind('<Configure>', self.resize_frame)

        # j = 0
        # a = 0
        # for i in range(50):
            # self.button = Button(self.frame, text=i)
            # self.button.grid(row=j, column=a)
            # a += 1
            # if i % 6 == 0:
                # j += 1
                # a = 0
            # # self.button.pack()
            # root.update()
            # self.canvas.config(scrollregion=self.canvas.bbox('all'))
    # def resize_frame(self, e):
        # self.canvas.itemconfig(self.frame_id, height=e.height, width=e.width)

    def put_button(self, root, button):
        button.grid(row=self.__row_button, column=self.__column_button, padx=20, pady=20)
        if self.__column_button == 5:
            self.__column_button = 0
            self.__row_button += 2
        else:
            self.__column_button += 1
        root.update()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
    def put_text(self, root, text):
        text.grid(row=self.__row_text, column=self.__column_text)
        if self.__column_text == 5:
            self.__column_text = 0
            self.__row_text += 2
        else:
            self.__column_text += 1
        root.update()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

class Win_Button(object):
    def __init__(self, root, id):

        self.right = PhotoImage(file='./right.png')
        self.wrong = PhotoImage(file='./wrong.png')
        self.loading = PhotoImage(file='./loading.png')
        self.button = Button(root,  image=self.loading, height=110, width=110, bg='#222831', bd=0, highlightthickness=0, command=DISABLED)
        self.id = id
        self.text = Frame(root, height=40, width=150, bg='#222831')
        self.text.pack_propagate(0)
        self.sb = Scrollbar(self.text, bg='#222831', troughcolor='#222831', width=5)
        self.label = Text(self.text, font=('Calibri', 10), fg='#eeeeee', bg='#222831', bd=0, highlightthickness=0, yscrollcommand=self.sb.set)
        self.label.insert(INSERT, self.id)
        self.label.configure(state=DISABLED)
        self.sb.pack(side='right', fill='y')
        self.label.pack(side='left', fill=BOTH)
        self.sb.config(command=self.label.yview)

    def change_look(self, master, is_ok, command):
        if is_ok:
            # self.button['text'] = None
            # self.button['image'] = self.right
            self.button.configure(image=self.right, command=command)
        else:
            self.button.configure(image=self.wrong, command=command)
        master.update()

if __name__ == '__main__':
    start('/home/shake/Projects/TrackAcc', True, False)
