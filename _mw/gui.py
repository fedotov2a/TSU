# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import filedialog

from PIL import Image, ImageTk

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Laser surface scanner')
        self.root.geometry('1000x600')
        self.root.resizable(width = False, height = False)

        self.canvas = Canvas(root, width = 640, height = 480)
        self.canvas.pack()
        self.canvas.place(x = 1000-640)
        self.canvas.bind("<Button-1>", self.click_on_canvas)

        self.open_btn = Button(root)
        self.open_btn.place(x = 10, y = 10, width = 70, height = 40)
        self.open_btn.configure(text = 'Open')
        self.open_btn.bind('<Button-1>', self.open_video)

        self.start_scan_btn = Button(root)
        self.start_scan_btn.place(x = 90, y = 10, width = 70, height = 40)
        self.start_scan_btn.configure(text = 'Start scan')
        self.start_scan_btn.bind('<Button-1>', self.start_scan)

        self.instruct_lbl = Label(root)
        self.instruct_lbl.place(x = 5, y = 100, height=300, width=200)
        self.instruct_lbl.configure(text = 
        '''Instructions:
        1. Open video file
        2. Define points on top area
            2.1. Top left point
            2.2. Top right point
            2.3. Bottom left point
            2.4. Bottom right point
        3. Define points on bottom area
            3.1. Top left point
            3.2. Top right point
            3.3. Bottom left point
            3.4. Bottom right point
        4. Define points on left area
            4.1. Top left point
            4.2. Top right point
            4.3. Bottom left point
            4.4. Bottom right point
        5. Define points on right area
            5.1. Top left point
            5.2. Top right point
            5.3. Bottom left point
            5.4. Bottom right point
        ''', justify = LEFT)


        self.out_lbl = Label(root)
        self.out_lbl.place(x = 10, y = 400, height=80, width=150)
        self.out_lbl.configure(text = 'Out')

        self.im = ImageTk.PhotoImage(Image.open('scan1_r.jpg').resize((640, 480)))

        self.canvas.create_image(0, 0, image = self.im, anchor = NW)

    def open_video(self, event):
        file_name = filedialog.askopenfilename(title = "Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        if file_name == '':
            return
        print(file_name)

    def start_scan(self, event):
        print('start_scan')

    def click_on_canvas(self, event):
        self.canvas.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill = 'red')

    def set_image_on_canvas(self, image):
        pass

root = Tk()
gui = GUI(root)
mainloop()