#!usr/bin/env python3
# -*- coding:utf-8 -*-

"""
- author  : 小么小儿郎EL
- email   : Littlecowherd@protonmail.com
- date    : 2017/10/17 15:17
- usage   : 获取必应今日美图-GUI界面
- version : 2.0 （发行版）
"""
import os
import requests
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from PIL import Image, ImageTk
import shutil


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        self.flag = True

    def init_window(self):
        self.master.title("必应美图下载器(双击图片可查看帮助) © 2017 Littlecowherd")
        self.pack(fill=BOTH, expand=1)

        # download_button = Button(text='保存', command=self.save)
        # download_button.pack()
        #
        # delete_button = Button(text='删除', command=self.delete)
        # delete_button.pack()
        # # 实例化一个Menu对象，这个在主窗体添加一个菜单
        # menu = Menu(self.master)
        # self.master.config(menu=menu)
        #
        # # 创建File菜单，下面有Save和Exit两个子菜单
        # file = Menu(menu)
        # # file.add_command(label='Save')
        # file.add_command(label='Save', accelerator='Ctrl+s', command=self.save, underline=0)
        # file.add_command(label='Save As', accelerator='Ctrl+s', command=self.save, underline=0)
        # file.add_command(label='Exit', command=self.client_exit)
        # menu.add_cascade(label='File', menu=file)

    def save(self):
         pass
    """
		path = 'D:\\壁纸'
        try:
            shutil.move(self.name, path)
        except Exception as error:
            messagebox.showerror("错误", error)
			"""

    def delete(self):
        os.unlink(self.name)

    def saveas(self):
        path_ = askdirectory()
        # path.set(path_) # 将路径设置为 选择好的路径
        try:
            if not path_:
                return
            shutil.move(self.name, path_)
        except Exception as error:
            messagebox.showerror("错误", error)

        # 额外弹出一个窗口
        # spath = Toplevel()
        # Label(spath, text="目标路径:").grid(row=0, column=0)
        # Entry(spath, textvariable=path).grid(row=0, column=1)
        # Button(spath, text="路径选择", command=self.selectpath).grid(row=0, column=2)

    def rightclick(self, event):
        menu = Menu(self.img, tearoff=0)
        menu.add_command(label="保存", command=self.save)
        menu.add_command(label="另存为", command=self.saveas)
        menu.add_command(label="删除", command=self.delete)

        menu.post(event.x_root, event.y_root)

    def download(self):
        url = 'http://area.sinaapp.com/bingImg/'
        image = requests.get(url)
        # print(image.content)
        if image.status_code == 200:
            import time
            time = time.strftime("%Y-%m-%d", time.localtime())
            self.name = 'BingWallpaper-%s.jpg' % time
            # path = 'C:\\Users\\Littlecowherd\\Desktop\\'
            # open(path + self.name, 'wb').write(image.content)
            open(self.name, 'wb').write(image.content)
        else:
            self.flag = False

    # print('访问出错')

    def showimg(self):
        if self.flag:
            load = Image.open(self.name)
            render = ImageTk.PhotoImage(load)

            img = Label(self, image=render)
            self.img = img
            img.image = render
            img.bind("<Button-3>", func=self.rightclick)
            img.bind("<Double-Button-1>", func=self.helpinfo)
            img.place(x=0, y=0)
        else:
            error = Label(self, text="访问出错！")
            error.pack()

    def helpinfo(self, event):
        info = '只能查看当天的必应壁纸 \n 右击打开功能菜单 \n' \
               ' 如有建议请提交至：\nLittlecowherd@protonmail.com \n\n 本软件仅做学习交流之用，不得用于商业用途。'
        messagebox.showinfo('提示', info)


root = Tk()
path = StringVar()
root.state("zoomed")  # 最大化窗口，只能是在Windows下生效
app = Window(root)
app.download()
app.showimg()

root.mainloop()
