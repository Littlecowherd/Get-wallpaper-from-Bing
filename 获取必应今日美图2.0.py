#!usr/bin/env python3
# -*- coding:utf-8 -*-

"""
- author  : 小么小儿郎EL
- email   : Littlecowherd@protonmail.com
- date    : 2017/10/17 15:17
- usage   : 获取必应今日美图-GUI界面，添加一周内壁纸（重写Download）
- version : 3.0 （自用版：默认保存位置为 :/壁纸）
"""
import json
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
        # 获取不同图片的参数
        self.idx = 0
        # 默认url，尚未拼接idx=？参数
        self.base_url = 'https://www.bing.com/HPImageArchive.aspx?format=js&n=1&pid=hp'
        self.full_width = self.winfo_screenwidth()
        self.full_height = self.winfo_screenheight()
        self.infoflag = 0  # 确保只有一个info label  ！！！一定要放在这个位置才行

    def init_window(self):
        self.master.title("必应美图下载器(双击图片可查看帮助) © 2017 Littlecowherd")
        self.pack(fill=BOTH, expand=1)

    def save(self):
        path = 'D:\\壁纸'
        try:
            shutil.move(self.name, path)
        except Exception as error:
            messagebox.showerror("错误", error)

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

    def changeimg(self, event):
        """将url填充完整,下载，更新图片"""
        mouse_x = event.x
        mouse_y = event.y
        if 0 <= mouse_x <= self.full_width / 8:
            self.idx += 1
            # print("上一张" + str(self.idx))
            if self.idx > 7:
                messagebox.showinfo('提示', "已经是最后一张啦！")
            else:
                img_url = self.get_url(idx=self.idx)
                # 避免每次都下载
                try:
                    self.showimg()
                except Exception as e:
                    self.download(img_url)
                    self.showimg()
        elif self.full_width / 8 * 7 <= mouse_x <= self.full_width:
            # print('下一张'+ str(self.idx))
            self.idx -= 1
            if self.idx < 0:
                messagebox.showinfo('提示', "已经是最新的啦！")
            else:
                img_url = self.get_url(idx=self.idx)
                # 避免每次都下载
                try:
                    self.showimg()
                except Exception as e:
                    self.download(img_url)
                    self.showimg()

        elif self.full_width / 8 * 3 <= mouse_x <= self.full_width / 8 * 6:
            if self.full_height / 4 <= mouse_y <= self.full_height / 4 * 3:
                self.showinfo()
        else:
            return

    def get_url(self, idx=0):
        """获取图片链接"""
        # 合成完整asp请求 url
        url = self.base_url + "&idx=%s" % idx
        html = requests.get(url)
        data = json.loads(html.text)
        img = data['images'][0]  # 一个包含图片信息的字典
        img_url = 'https://cn.bing.com' + img['url']
        self.copyrightinfo = img['copyright']
        self.name = img['urlbase'].split('/')[-1] + '.jpg'
        return img_url

    def download(self, url):
        """根据图片链接下载图片"""
        image = requests.get(url)
        # print(image.content)
        if image.status_code == 200:
            # 直接用爬到的图片名来给文件命名
            # import time
            # time = time.strftime("%Y-%m-%d", time.localtime())
            # self.name = 'BingWallpaper-%s.jpg' % time
            # path = 'C:\\Users\\Littlecowherd\\Desktop\\'
            # open(path + self.name, 'wb').write(image.content)
            open(self.name, 'wb').write(image.content)
        else:
            self.flag = False

    # print('访问出错')

    def showimg(self):
        if self.flag:
            load = Image.open(self.name)
            # 根据屏幕大小对显示的图片进行调整

            imgg = load.resize((self.full_width, self.full_height))
            render = ImageTk.PhotoImage(imgg)

            img = Label(self, image=render)
            self.img = img
            img.image = render
            # 右键功能菜单
            img.bind("<Button-3>", func=self.rightclick)
            # 双击显示帮助信息
            img.bind("<Double-Button-1>", func=self.helpinfo)
            # 左键拖动更换图片(实现不了)，更改为点击左侧或者右侧更换图片
            img.bind("<Button-1>", func=self.changeimg)
            # 按tab查看图片信息,,改为点击图片中央位置
            # img.bind("<BackSpace>", func=self.showinfo)
            # img.place(x=0, y=0)
            img.place(x=0, y=0)
        else:
            error = Label(self, text="访问出错！")
            error.pack()

    def helpinfo(self, event):
        info = '只能查看当天的必应壁纸 \n ' \
               '右击打开功能菜单 \n' \
               '单击左侧边缘查看前一天图片\n' \
               '单击右侧边缘查看后一天图片\n' \
               '单击图片中央查看图片信息\n' \
               '如有建议请提交至:\nLittlecowherd@protonmail.com \n\n本软件仅做学习交流之用，不得用于商业用途。'
        messagebox.showinfo('提示', info)

    def showinfo(self):
        """图片信息"""
        # messagebox.showinfo('图片信息', self.copyrightinfo)
        if self.infoflag != 0:
            self.info.destroy()
            self.infoflag = 0
        else:
            self.info = Label(self, text=self.copyrightinfo)
            self.info.pack()
            self.infoflag += 1


root = Tk()
path = StringVar()
root.state("zoomed")  # 最大化窗口，只能是在Windows下生效
app = Window(root)
app.download(app.get_url())  # 默认获取当天壁纸
app.showimg()
root.mainloop()
