#!/usr/bin/env python3


__author__ = 'Shake'
__version__ = '1.0.0'

from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
from start_analyzing import start

def main():
    main_win = Tk()
    main_win.title('TrackAcc')
    main_win.geometry("650x480+300+150")
    main_win.resizable(width=True, height=True)
    main_win.configure(bg='#34495e')

    global path
    path = StringVar()
    path.set('Enter image path')

    frame = Frame(main_win, bg='#191919', border=2)
    frame.pack(fill=BOTH, expand=True, padx=75, pady=50)
    
    title_frame = Frame(frame, bg='#191919')
    title_frame.pack(pady=15)
    title_label = Label(title_frame, text='TrackAcc', font=('sans-serif', 20), bg='#191919', fg='white').pack(pady=25)
    
    frame_for_input = Frame(frame, width=200, height=30, bg='#191919')
    frame_for_input.pack(pady=15)
    file_input = Entry(frame_for_input, width=29, borderwidth=1, textvariable=path, font=('sans-serif', '10',), fg='white', bg='#191919', highlightbackground='#3498db', highlightthickness=1, highlightcolor='blue', insertbackground='gray', justify='center')
    file_input.pack(side='left', anchor='n', pady=5, ipady=4)
    
    open_image = PhotoImage(file='open_ico.png')
    open_button = Button(frame_for_input, image=open_image, width=19, height=19, bg='#191919', bd=0, highlightbackground='#191919', highlightcolor='blue', highlightthickness=2, activebackground='gray', command=open_file)
    open_button.pack(side='right', padx=3)
    
    frame_for_check = Frame(frame, highlightbackground='#3498db', highlightthickness=1, highlightcolor='blue')
    frame_for_check.pack( anchor ='n', side='top', pady=10)
    global save
    global video
    save = IntVar()
    video = IntVar()
    check_save = Checkbutton(frame_for_check, width=14, justify='right', text='保存处理后的图片', font=('sans-serif', 10), bg='#191919', fg='gray', highlightbackground='#191919', highlightcolor='blue', highlightthickness=0, activebackground='blue', onvalue=1, offvalue=0, variable=save, command=is_save)
    check_video = Checkbutton(frame_for_check, width=13, justify='right', text='处理视频', font=('sans-serif', 10), bg='#191919', fg='gray', highlightbackground='#191919', highlightcolor='blue', highlightthickness=0, activebackground='blue', onvalue=1, offvalue=0, variable=video, command=is_video)
    check_save.pack(side='left', anchor='w')
    check_video.pack(side='left')
    
    confirm_frame = Frame(frame, bg='#191919', highlightbackground='#3498db', highlightthickness=1, highlightcolor='blue')
    confirm_frame.pack(anchor='n', pady=20)
    confirm = Button(confirm_frame, text='Start analyzing', font=('sans-serif', 12), fg='white', bg='#191919', highlightbackground='#191919', highlightcolor='blue', highlightthickness=0, activebackground='blue', command=start_analyzing)
    confirm.pack()
    
    
    help_button = Button(main_win, text='Help', font=('sans-serif', 8, 'bold', 'italic'), underline=0, fg='black', bg='#34495e', activebackground='#344940', bd=0, highlightthickness=0, command=help)
    help_button.pack(anchor='se')
    
    about_button = Button(main_win, text='About', font=('sans-serif', 8, 'bold', 'italic'), underline=0, fg='black', bg='#34495e', activebackground='#344940', bd=0, highlightthickness=0, command=about)
    about_button.pack(anchor='se')
    

    main_win.mainloop()

def help():
    tkinter.messagebox.showinfo(title='Help', message='Usage:\n\r选择或者键入图片路径或包含图片的文件夹路径，点击Start Analyzing开始分析。\n\r如果想看分析中产生的中间结果图片，请勾选保存分析后的图片。\n\r但是请注意：保存图片会增加分析时间。')

def about():
    tkinter.messagebox.showinfo(title='About', message='TrackAccUI'+__version__+'\n\rCopyright (c) 2020, Weng Kaiqiang. All rights reserved.')

def open_file():
    global path
    pathname = tkinter.filedialog.askdirectory()
    path.set(pathname)
    
def is_save():
    global save
    print(save.get())

def is_video():
    global video
    print(video.get())

def start_analyzing():
    global path
    global save, video
    pathname = path.get()
    if save.get() == 1:
        is_save = True
    else:
        is_save = False
    if video.get() == 1:
        is_video = True
    else:
        is_video = False
    start(pathname, is_save, is_video)

if __name__ == '__main__':
    main()
