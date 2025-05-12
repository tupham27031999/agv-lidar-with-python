from tkinter import *
from tkinter import ttk
import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk
from datetime import datetime
from support_main.lib_main import load_data_csv
from tkinter.messagebox import showerror, showwarning, showinfo
import functools

ds_cong_com = []
ds_bau = ["9600","19200","115200","256000","921600"]

sent_data = ""
def img_resize_vid(video, resize_x, resize_y):
    img_rs = cv2.resize(video, (int(resize_x),int(resize_y)))
    img_rs = cv2.cvtColor(img_rs, cv2.COLOR_BGR2RGB)
    img_rs = ImageTk.PhotoImage(Image.fromarray(img_rs))
    return img_rs
def img_resize_path(path, resize_x, resize_y):
    img_rs = cv2.imread(path)
    img_rs = cv2.resize(img_rs, (int(resize_x),int(resize_y)))
    img_rs = cv2.cvtColor(img_rs, cv2.COLOR_BGR2RGB)
    img_rs = ImageTk.PhotoImage(Image.fromarray(img_rs))
    return img_rs
def sent_data_main():
    global sent_data
    return str(sent_data)

def reset_data():
    global sent_data
    # print(sent_data)
    sent_data = ""
def load_name(input):
    ds = str(input).split("_")
    k = len(ds)
    name_new = ""
    if ds[-1] == "int":
        for i in range(0,k):
            if i == k - 1:
                break
            if i == 0:
                name_new = ds[i]
            else:
                name_new = name_new +"_"+ ds[i]
    else:
        name_new = input
    return name_new
class AutoScrollbar(ttk.Scrollbar):
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')
    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')
def func(name):
    global sent_data
    sent_data = name
    print(name)

class Giao_dien:
    def __init__(self,number=2000):
        self.number = number
        self.list_name = []
        for i in range(0,self.number):
            globals()["self."+str(i)] = ""
            self.list_name.append("")
            
        self.list_globals = {}
        self.list_tt_frame_canvas = []
        self.mousewheel_window = ""

        self.x = -1
        self.y = -1
        self.x1= -1
        self.y1= -1
        self.tien = 0
        self.lui = 0
        self.trai = 0
        self.phai = 0
        self.khai_bao_mouse = 0
    def root_window(self,name,tt_root,new_toplever=0,close_root=0):
        # if new_toplever == 0:
        #     self.list_name = []
        #     for i in range(0,self.number):
        #         globals()["self."+str(i)] = ""
        #         self.list_name.append("")
        name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window_2(name)
        # print(self.list_name,"self.list_name")
        if exist == 0:
            self.list_name[stt_ok_0] = name
            if new_toplever == 0:
                globals()[name_window] = tk.Tk()
            else:
                for i in range(0,len(tt_root)):
                    if load_name(tt_root[i][0]) == "thuoc_frame":
                        name_root = self.name_window_da_kb(tt_root[i][1])
                        globals()[name_window]  = Toplevel(globals()[name_root])
        for i2 in range(0,len(tt_root)):
            if tt_root[i2][0] == "geometry":
                globals()[name_window].geometry(tt_root[i2][1])
            if tt_root[i2][0] == "bg":
                globals()[name_window]["bg"] = tt_root[i2][1]
            if tt_root[i2][0] == "columnconfigure":
                for col in range(0,len(tt_root[i2][1])):
                    globals()[name_window].columnconfigure(col,weight=tt_root[i2][1][col])
            if tt_root[i2][0] == "rowconfigure":
                for rw in range(0,len(tt_root[i2][1])):
                    globals()[name_window].rowconfigure(rw,weight=tt_root[i2][1][rw])
            if tt_root[i2][0] == "title":
                globals()[name_window].title(tt_root[i2][1])
            if tt_root[i2][0] == "protocol":
                globals()[name_window].protocol("WM_DELETE_WINDOW", functools.partial(func,tt_root[i2][1]))
    def menu_window(self,tt):
        name_thuoc_frame = "NA"
        add_const_value = "NA"
        loai = "NA"
        thuoc_root = "NA"
        value_cmd = "NA"
        new_item = "NA"
        text = "NA"
        name_window_item = "NA"
        name_thuoc_root = "NA"
        for i in range(0,len(tt)):
            if str(tt[i][0]) == "name_window":
                name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window_2(tt[0][1])
                if exist == 0:
                    self.list_name[stt_ok_0] = tt[i][1]
            if str(tt[i][0]) == "loai":
                loai = str(tt[i][1])
            if str(tt[i][0]) == "thuoc_root":
                thuoc_root = str(tt[i][1])
                if thuoc_root != "NA":
                    name_thuoc_root,exist_root,stt_ok_0_root,stt_ok_1_root = self.check_find_name_window_2(tt[i][1])
                    if exist_root == 0:
                        self.list_name[stt_ok_0_root] = tt[i][1]
            if str(tt[i][0]) == "thuoc_frame":
                name_thuoc_frame = self.name_window_da_kb(str(tt[i][1]))
            if str(tt[i][0]) == "value_cmd":
                value_cmd = str(tt[i][1])
            if str(tt[i][0]) == "new_item":
                if tt[i][1] != "NA":
                    name_window_item,exist_item,stt_ok_0_item,stt_ok_1_item = self.check_find_name_window_2(tt[i][1])
                    if exist_item == 0:
                        self.list_name[stt_ok_0_item] = tt[i][1]
            if str(tt[i][0]) == "add_const_value":
                add_const_value = str(tt[i][1])
            if str(tt[i][0]) == "text":
                text = str(tt[i][1])
        if loai == "menu" and name_window != "NA" and name_thuoc_frame != "None" and name_thuoc_frame != "NA":
            if thuoc_root == "root":
                globals()[name_window] = Menu(globals()[name_thuoc_frame])
                globals()[name_window_item] = Menu(globals()[name_window])
                globals()[name_thuoc_frame].config(menu=globals()[name_window])
            if thuoc_root != "root" and add_const_value == "add":
                globals()[name_window] = Menu(globals()[name_thuoc_frame], tearoff=0)
                globals()[name_thuoc_root].add_cascade(label=text,menu=globals()[name_window],command = functools.partial(func,str(value_cmd)))
            if thuoc_root != "root" and add_const_value == "const":
                globals()[name_thuoc_root].add_command(label=text,command = functools.partial(func,str(value_cmd)))
            # globals()[name_thuoc_frame].update()
    def name_window_thuoc_frame(self,name_label,tt_label):
        stt = 0
        stt_frame = 0
        # tim thuoc frame
        for i in range(0,len(self.list_name)):
            if self.list_name[i] != tt_label[0][1]:
                stt_frame = stt_frame + 1
            else:
                break
        name_thuoc_frame = "self." +str(stt_frame)
        # khai bao label, tim name_window
        for i in range(0,len(self.list_name)):
            if self.list_name[i] != "":
                stt = stt + 1
            else:
                break
        self.list_name[stt] = name_label
        name_window = "self." +str(stt)
        return name_window,name_thuoc_frame
    def name_window_da_kb(self,name_label):
        stt = 0
        ok = 0
        for i in range(0,len(self.list_name)):
            if self.list_name[i] != name_label:
                stt = stt + 1
            else:
                ok = 1
                break
        if ok == 1:
            name_window = "self." +str(stt)
        else:
            name_window = "None"
        return name_window
    def check_find_name_window_2(self,name_label):
        stt_ok_1 = 0
        stt_ok_0 = 0
        ok_1 = 0
        ok_0 = 0
        exist = 0
        for i in range(0,len(self.list_name)):
            if self.list_name[i] == "" and ok_0 == 0:
                ok_0 = 1
            if ok_0 == 0:
                stt_ok_0 = stt_ok_0 + 1
            if self.list_name[i] != name_label and ok_1 == 0:
                stt_ok_1 = stt_ok_1 + 1
            else:
                ok_1 = 1
                break
        if ok_1 == 1:
            name_window = "self." +str(stt_ok_1)
            exist = 1
        else:
            name_window = "self." +str(stt_ok_0)
        return name_window,exist,stt_ok_0,stt_ok_1
    def check_find_name_window(self,name_label,tt_label):

        stt_ok_1 = 0
        stt_ok_0 = 0
        ok_1 = 0
        ok_0 = 0
        exist = 0
        stt_frame = 0
        # tim thuoc frame
        for i in range(0,len(self.list_name)):
            if self.list_name[i] != tt_label:
                stt_frame = stt_frame + 1
            else:
                break
        name_thuoc_frame = "self." +str(stt_frame)
        for i in range(0,len(self.list_name)):
            if self.list_name[i] == "" and ok_0 == 0:
                ok_0 = 1
            if ok_0 == 0:
                stt_ok_0 = stt_ok_0 + 1
            if self.list_name[i] != name_label and ok_1 == 0:
                stt_ok_1 = stt_ok_1 + 1
            else:
                ok_1 = 1
                break
        if ok_1 == 1:
            name_window = "self." +str(stt_ok_1)
            exist = 1
        else:
            name_window = "self." +str(stt_ok_0)
        return name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame
    def edit_window(self,name_window,tt_label):
        for i3 in range(0,len(tt_label)):
            if tt_label[i3][1] != "NA":
                if str(tt_label[i3][0]).split("_")[0]  == "command":
                    globals()[name_window].configure(command = functools.partial(func,str(tt_label[i3][1])))
                else:
                    if str(tt_label[i3][0]).split("_")[0]  == "variable":
                        name_variable = self.name_window_da_kb(str(tt_label[i3][1]))
                        globals()[name_window].configure(variable = globals()[name_variable])
                    else:
                        if str(tt_label[i3][0]).split("_")[-1] == "int" :
                            globals()[name_window][str(tt_label[i3][0]).split("_")[0]] = int(tt_label[i3][1])
                        else:
                            globals()[name_window][str(tt_label[i3][0]).split("_")[0]] = tt_label[i3][1]
    def edit_gird_window(self,name_window,tt_label):
        for i3 in range(0,len(tt_label)):
            if tt_label[i3][1] != "NA":
                if load_name(tt_label[i3][0])== "column":
                    globals()[name_window].grid(column=int(tt_label[i3][1]))
                if load_name(tt_label[i3][0]) == "row":
                    globals()[name_window].grid(row=int(tt_label[i3][1]))
                if load_name(tt_label[i3][0]) == "ipadx":
                    globals()[name_window].grid(ipadx = int(tt_label[i3][1]))
                if load_name(tt_label[i3][0]) == "ipady":
                    globals()[name_window].grid(ipady =int(tt_label[i3][1]))
                if load_name(tt_label[i3][0]) == "padx":
                    globals()[name_window].grid(padx=int(tt_label[i3][1]))
                if load_name(tt_label[i3][0])== "pady":
                    globals()[name_window].grid(pady=int(tt_label[i3][1]))
                if load_name(tt_label[i3][0]) == "rowspan":
                    globals()[name_window].grid(rowspan = int(tt_label[i3][1]))
                if load_name(tt_label[i3][0]) == "columnspan":
                    globals()[name_window].grid(columnspan = int(tt_label[i3][1]))
                if load_name(tt_label[i3][0]) == "sticky":
                    globals()[name_window].grid(sticky = str(tt_label[i3][1]))
    def label_window(self,name,tt_1,tt_2,tt_3,new=1,close = 0):
        if new == 1:
            for i2 in range(0,len(tt_1)):
                if load_name(tt_1[i2][0]) == "thuoc_frame":
                    name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                    if exist == 0:
                        self.list_name[stt_ok_0] = name
            globals()[name_window] = Label(globals()[name_thuoc_frame])
        else:
            name_window = self.name_window_da_kb(name)
        # print("name_window2",name_window)
        if name_window != "None":
            for i2 in range(1,len(tt_1)):
                if load_name(tt_1[i2][0]) == "font":
                    font = tt_1[i2][1]
                if load_name(tt_1[i2][0]) == "font_size":
                    fontsize = str(tt_1[i2][1])
                if load_name(tt_1[i2][0]) == "net_chu":
                    net_chu = tt_1[i2][1]
            if font != "NA" and fontsize != "NA":
                if net_chu != "NA":
                    globals()[name_window].configure(font=(font,fontsize,net_chu))
                else:
                    globals()[name_window].configure(font=(font,fontsize))
            self.edit_gird_window(name_window,tt_2)
            self.edit_window(name_window,tt_3)
    def button_window(self,name,tt_1,tt_2,tt_3,new=1,close = 0):
        if new == 1:
            for i2 in range(0,len(tt_1)):
                if load_name(tt_1[i2][0]) == "thuoc_frame":
                    name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                    if exist == 0:
                        self.list_name[stt_ok_0] = name
            globals()[name_window] = Button(globals()[name_thuoc_frame])
        else:
            name_window = self.name_window_da_kb(name)
        if name_window != "None":
            for i2 in range(1,len(tt_1)):
                if load_name(tt_1[i2][0]) == "font":
                    font = tt_1[i2][1]
                if load_name(tt_1[i2][0]) == "font_size":
                    fontsize = int(tt_1[i2][1])
                if load_name(tt_1[i2][0]) == "net_chu":
                    net_chu = tt_1[i2][1]
            if font != "NA" and fontsize != "NA":
                if net_chu != "NA":
                    globals()[name_window].configure(font=(font,fontsize,net_chu))
                else:
                    globals()[name_window].configure(font=(font,fontsize))
            self.edit_gird_window(name_window,tt_2)
            self.edit_window(name_window,tt_3)
    def entry_window(self,name,tt_1,tt_2,tt_3,new=1,close = 0):
        if new == 1:
            for i2 in range(0,len(tt_1)):
                if load_name(tt_1[i2][0]) == "thuoc_frame":
                    name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                    if exist == 0:
                        self.list_name[stt_ok_0] = name
            globals()[name_window] = Entry(globals()[name_thuoc_frame])
        else:
            name_window = self.name_window_da_kb(name)
        if name_window != "None":
            for i2 in range(1,len(tt_1)):
                if load_name(tt_1[i2][0]) == "font":
                    font = tt_1[i2][1]
                if load_name(tt_1[i2][0]) == "font_size":
                    fontsize = tt_1[i2][1]
                if load_name(tt_1[i2][0]) == "net_chu":
                    net_chu = tt_1[i2][1]
            if font != "NA" and fontsize != "NA":
                if net_chu != "NA":
                    globals()[name_window].configure(font=(font,int(fontsize),net_chu))
                else:
                    globals()[name_window].configure(font=(font,int(fontsize)))
            
            self.edit_gird_window(name_window,tt_2)
            self.edit_window(name_window,tt_3)
    def radiobutton_window(self,name,tt_1,tt_2,tt_3,new=1,close = 0):
        name_variable = "None"
        da_khai_bao = 0
        for i in range(0,len(tt_3)):
            if load_name(tt_3[i][0]) == "variable":
                if self.name_window_da_kb(tt_3[i][1]) != "None":
                    name_variable = self.name_window_da_kb(tt_3[i][1])
                    da_khai_bao = 1
        if da_khai_bao == 0:
            for i in range(0,len(tt_3)):
                if load_name(tt_3[i][0]) == "variable":
                    name_variable,exist_var1,stt_ok_01,stt_ok_11 = self.check_find_name_window_2(tt_3[i][1])
                    if exist_var1 ==0:
                        self.list_name[stt_ok_01] = tt_3[i][1]
                    globals()[name_variable] = IntVar()
                    # globals()[name_variable].set(1)
        if name_variable != "None":
            if new == 1:
                for i2 in range(0,len(tt_1)):
                    if load_name(tt_1[i2][0]) == "thuoc_frame":
                        name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                        if exist == 0:
                            self.list_name[stt_ok_0] = name
                
                globals()[name_window] = ttk.Radiobutton(globals()[name_thuoc_frame])
            else:
                name_window = self.name_window_da_kb(name)
            if name_window != "None":
                for i2 in range(1,len(tt_1)):
                    if load_name(tt_1[i2][0]) == "font":
                        font = tt_1[i2][1]
                    if load_name(tt_1[i2][0]) == "font_size":
                        fontsize = tt_1[i2][1]
                if font != "NA" and fontsize != "NA":
                    style = ttk.Style()
                    style.configure("TRadiobutton", font=(font, fontsize))
                self.edit_gird_window(name_window,tt_2)
                self.edit_window(name_window,tt_3)
    # def set_radiobutton(self,tt_3,number_set):
    #     name_variable = "None"
    #     for i in range(0,len(tt_3)):
    #         if load_name(tt_3[i][0]) == "variable":
    #             name_variable = self.check_find_name_window_2(tt_3[i][1])
    #     if name_variable != "None":
    #         globals()[name_variable].set(int(number_set))
    def mylist_window(self,name,tt_1,tt_2,tt_3,scrollbar,listbox,new=1,close = 0):
        if new == 1:
            for i2 in range(0,len(tt_1)):
                if load_name(tt_1[i2][0]) == "thuoc_frame":
                    name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                    if exist == 0:
                        self.list_name[stt_ok_0] = name
            globals()[name_window] = Label(globals()[name_thuoc_frame])
        else:
            name_window = self.name_window_da_kb(name)
        if name_window != "None":
            # print("name1 = ", name_window)
            for i2 in range(1,len(tt_1)):
                if load_name(tt_1[i2][0]) == "font":
                    font = tt_1[i2][1]
                if load_name(tt_1[i2][0]) == "font_size":
                    fontsize = tt_1[i2][1]
                if load_name(tt_1[i2][0]) == "net_chu":
                    net_chu = tt_1[i2][1]
            if font != "NA" and fontsize != "NA":
                if net_chu != "NA":
                    globals()[name_window].configure(font=(font,int(fontsize),net_chu))
                else:
                    globals()[name_window].configure(font=(font,int(fontsize)))
            
            self.edit_gird_window(name_window,tt_2)
            self.edit_window(name_window,tt_3)
        da_khai_bao_scrollbar = 0

        for i in range(0,len(scrollbar)):
            if load_name(scrollbar[i][0]) == "scrollbar":
                if self.name_window_da_kb(scrollbar[i][1]) != "None":
                    name_scrollbar = self.name_window_da_kb(scrollbar[i][1])
                    da_khai_bao_scrollbar = 1
        if da_khai_bao_scrollbar == 0:
            for i in range(0,len(scrollbar)):
                if load_name(scrollbar[i][0]) == "scrollbar":
                    name_scrollbar,exist_var,stt_ok_0,stt_ok_1 = self.check_find_name_window_2(scrollbar[i][1])
                    if exist_var ==0:
                        self.list_name[stt_ok_0] = scrollbar[i][1]
                    globals()[name_scrollbar] = Scrollbar(globals()[name_window])
                    globals()[name_scrollbar].pack( side = RIGHT, fill = Y )
                    da_khai_bao_scrollbar = 1
                    

        da_khai_bao = 0
        if da_khai_bao_scrollbar == 1:
            for i in range(0,len(listbox)):
                if load_name(listbox[i][0]) == "listbox":
                    if self.name_window_da_kb(listbox[i][1]) != "None":
                        name_listbox = self.name_window_da_kb(listbox[i][1])
                        da_khai_bao = 1
            if da_khai_bao == 0:
                for i in range(0,len(listbox)):
                    if load_name(listbox[i][0]) == "listbox":
                        name_listbox,exist_var,stt_ok_0,stt_ok_1 = self.check_find_name_window_2(listbox[i][1])
                        if exist_var ==0:
                            self.list_name[stt_ok_0] = listbox[i][1]
                        globals()[name_listbox] = Listbox(globals()[name_window], yscrollcommand = globals()[name_scrollbar].set)
                        globals()[name_listbox].configure(font=(font,int(fontsize)))
                        # self.edit_window(name_listbox,tt_3)
                        # globals()[name_listbox].pack( side = LEFT, fill = BOTH )
                        globals()[name_listbox].pack(fill = BOTH, expand = True)
                        # globals()[name_listbox].grid(column=0)
                        # globals()[name_listbox].grid(row=0)
                        # globals()[name_window].grid(ipadx = int(tt_label[i3][1]))
                        # globals()[name_window].grid(ipady =int(tt_label[i3][1]))
                        # globals()[name_window].grid(padx=int(tt_label[i3][1]))
                        # globals()[name_window].grid(pady=int(tt_label[i3][1]))
                        # globals()[name_window].grid(rowspan = int(tt_label[i3][1]))
                        # globals()[name_window].grid(columnspan = int(tt_label[i3][1]))
                        # globals()[name_listbox].grid(sticky = "nsew")
                        globals()[name_scrollbar].config(command = globals()[name_listbox].yview)

    def combobox_window(self,name,tt_1,tt_2,tt_3,new=1,close = 0):
        da_khai_bao_stringvar = 0

        for i in range(0,len(tt_3)):
            if load_name(tt_3[i][0]) == "stringvar":
                if self.name_window_da_kb(tt_3[i][1]) != "None":
                    name_stringvar = self.name_window_da_kb(tt_3[i][1])
                    da_khai_bao_stringvar = 1
        if da_khai_bao_stringvar == 0:
            for i in range(0,len(tt_3)):
                if load_name(tt_3[i][0]) == "stringvar":
                    name_stringvar,exist_var,stt_ok_0,stt_ok_1 = self.check_find_name_window_2(tt_3[i][1])
                    if exist_var ==0:
                        self.list_name[stt_ok_0] = tt_3[i][1]
                    globals()[name_stringvar] = tk.StringVar()

        
        if new == 1:
            for i2 in range(0,len(tt_1)):
                if load_name(tt_1[i2][0]) == "thuoc_frame":
                    name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                    if exist == 0:
                        self.list_name[stt_ok_0] = name
            # globals()[name_window] = Label(globals()[name_thuoc_frame])
            state = 0
            for i in range(0,len(tt_3)):
                if load_name(tt_3[i][0]) == "state":
                    if load_name(tt_3[i][1]) == "NA":
                        globals()[name_window]= ttk.Combobox(globals()[name_thuoc_frame],
                                         textvariable=globals()[name_stringvar])
                    else:
                        globals()[name_window]= ttk.Combobox(globals()[name_thuoc_frame],
                                         textvariable=globals()[name_stringvar],state="readonly")
                    state = 1
                if state == 1 and load_name(tt_3[i][0]) == "ds_combobox":
                    globals()[name_window]['values'] = globals()[load_name(tt_3[i][1])]
        else:
            name_window = self.name_window_da_kb(name)
        
        if name_window != "None":
            for i2 in range(1,len(tt_1)):
                if load_name(tt_1[i2][0]) == "font":
                    font = tt_1[i2][1]
                if load_name(tt_1[i2][0]) == "font_size":
                    fontsize = tt_1[i2][1]
                if load_name(tt_1[i2][0]) == "net_chu":
                    net_chu = tt_1[i2][1]
            if font != "NA" and fontsize != "NA":
                if net_chu != "NA":
                    globals()[name_window].configure(font=(font,int(fontsize),net_chu))
                else:
                    globals()[name_window].configure(font=(font,int(fontsize)))
            self.edit_gird_window(name_window,tt_2)
        globals()[name_window].current()
    def checkbutton_window(self,name,tt_1,tt_2,tt_3,new=1,close = 0):
        name_variable = "None"
        da_khai_bao = 0
        for i in range(0,len(tt_3)):
            if load_name(tt_3[i][0]) == "variable":
                if self.name_window_da_kb(tt_3[i][1]) != "None":
                    name_variable = self.name_window_da_kb(tt_3[i][1])
                    da_khai_bao = 1
        if da_khai_bao == 0:
            for i in range(0,len(tt_3)):
                if load_name(tt_3[i][0]) == "variable":
                    name_variable,exist_var,stt_ok_0,stt_ok_1 = self.check_find_name_window_2(tt_3[i][1])
                    if exist_var ==0:
                        self.list_name[stt_ok_0] = tt_3[i][1]
                    globals()[name_variable] = IntVar()
                    # globals()[name_variable].set(1)
        if name_variable != "None":
            if new == 1:
                for i2 in range(0,len(tt_1)):
                    if load_name(tt_1[i2][0]) == "thuoc_frame":
                        name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                        if exist == 0:
                            self.list_name[stt_ok_0] = name
                globals()[name_window] = Checkbutton(globals()[name_thuoc_frame])

            else:
                name_window = self.name_window_da_kb(name)
            if name_window != "None":
                for i2 in range(1,len(tt_1)):
                    if load_name(tt_1[i2][0]) == "font":
                        font = tt_1[i2][1]
                    if load_name(tt_1[i2][0]) == "font_size":
                        fontsize = int(tt_1[i2][1])
                    if load_name(tt_1[i2][0]) == "net_chu":
                        net_chu = tt_1[i2][1]
                if font != "NA" and fontsize != "NA":
                    if net_chu != "NA":
                        globals()[name_window].configure(font=(font,fontsize,net_chu))
                    else:
                        globals()[name_window].configure(font=(font,fontsize))
                self.edit_gird_window(name_window,tt_2)
                self.edit_window(name_window,tt_3)
    def text_window(self,name,tt_1,tt_2,new=1,close = 0):
        if new == 1:
            for i2 in range(0,len(tt_1)):
                if load_name(tt_1[i2][0]) == "thuoc_frame":
                    name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                    if exist == 0:
                        self.list_name[stt_ok_0] = name
            globals()[name_window] = Text(globals()[name_thuoc_frame],width = 100,heigh = 20)
        else:
            name_window = self.name_window_da_kb(name)
        if name_window != "None":
            for i2 in range(1,len(tt_1)):
                if load_name(tt_1[i2][0]) == "font":
                    font = tt_1[i2][1]
                if load_name(tt_1[i2][0]) == "font_size":
                    fontsize = str(tt_1[i2][1])
                if load_name(tt_1[i2][0]) == "net_chu":
                    net_chu = tt_1[i2][1]
            if font != "NA" and fontsize != "NA":
                if net_chu != "NA":
                    globals()[name_window].configure(font=(font,fontsize,net_chu))
                else:
                    globals()[name_window].configure(font=(font,fontsize))
            self.edit_gird_window(name_window,tt_2)
            Fact = '''b'''
            globals()[name_window].insert(tk.END, Fact)
    def frame_window(self,name,tt_1,tt_2,tt_3,new=1,close = 0):
        if new == 1:
            for i2 in range(0,len(tt_1)):
                if load_name(tt_1[i2][0]) == "thuoc_frame":
                    name_window,exist,stt_ok_0,stt_ok_1,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                    if exist == 0:
                        self.list_name[stt_ok_0] = name
            globals()[name_window] = Frame(globals()[name_thuoc_frame])
        else:
            name_window = self.name_window_da_kb(name)
        if name_window != "None":
            for f1 in range(0,len(tt_1)):
                if tt_1[f1][1] != "NA":
                    if load_name(tt_1[f1][0]) == "columnconfigure":
                        for col in range(0,len(tt_1[f1][1])):
                            globals()[name_window].columnconfigure(col,weight=tt_1[f1][1][col])
                    if load_name(tt_1[f1][0] )== "rowconfigure":
                        for rw in range(0,len(tt_1[f1][1])):
                            globals()[name_window].rowconfigure(rw,weight=tt_1[f1][1][rw])
            self.edit_gird_window(name_window,tt_2)
            self.edit_window(name_window,tt_3)
    # font_button= "TkDefaultFont",fontsizre_button=12,width=20,color="white"
    def canvas_window(self,name_canvas,tt_1,tt_2,tt_3,tt_scrollbar,tt_button =[],list1=[],new=1,remove_button=0,update_button = 0):
        name_window,name_frame,name_scrollbar,sticky2,width_text = ["None","None","None","None","None"]
        for i2 in range(0,len(tt_1)):
            if load_name(tt_1[i2][0]) == "thuoc_frame":
                name_window,exist_cas,stt_ok_0_cas,stt_ok_1_cas,name_thuoc_frame = self.check_find_name_window(name_canvas,tt_1[i2][1])
                if exist_cas == 0:
                    self.list_name[stt_ok_0_cas] = name_canvas
            if load_name(tt_1[i2][0]) == "name_scrollbar":
                name_scrollbar,exist_scr,stt_ok_0_scr,stt_ok_1_scr,name_thuoc_frame_canvas = self.check_find_name_window(tt_1[i2][1],tt_1[i2][1])
                if exist_scr == 0:
                    self.list_name[stt_ok_0_scr] = tt_1[i2][1]
            if load_name(tt_1[i2][0]) == "name_img":
                name_frame,exist_img,stt_ok_0_img,stt_ok_1_img,name_thuoc_frame_img = self.check_find_name_window(tt_1[i2][1],tt_1[i2][1])
                if exist_img == 0:
                    self.list_name[stt_ok_0_img] = tt_1[i2][1]
            if load_name(tt_1[i2][0]) == "sticky2":
                sticky2 = tt_1[i2][1]
            if load_name(tt_1[i2][0]) == "width_text":
                width_text = int(tt_1[i2][1])
        if name_window != "None" and name_frame != "None" and name_scrollbar != "None":
            if remove_button == 1:
                globals()[name_frame].destroy()
                globals()[name_scrollbar].destroy()
                globals()[name_window].destroy()
            if remove_button == 1 or new == 1:
                globals()[name_window] = tk.Canvas(globals()[name_thuoc_frame])
                globals()[name_frame]=Frame(globals()[name_window])
                globals()[name_scrollbar]=Scrollbar(globals()[name_thuoc_frame],orient="vertical",command=globals()[name_window].yview)
                globals()[name_window].create_window((0,0),window=globals()[name_frame],anchor='nw')
                
                globals()[name_window].configure(scrollregion = globals()[name_window].bbox("all"))

                # globals()[name_window].bind("<MouseWheel>", lambda event: globals()[name_window].yview_scroll(int(-1*(event.delta/120)), "units"))
                globals()[name_window].bind("<Up>",  lambda event: globals()[name_window].yview_scroll( -1, "units"))
                globals()[name_window].bind("<Down>",  lambda event: globals()[name_window].yview_scroll( 1, "units"))
                globals()[name_window].focus_set()
            
                self.mousewheel_window = name_window
            if update_button == 1:
                font = "NA"
                bg = "NA"
                fontsize = "NA"
                width2 = "NA"
                width2 = "NA"
                for tt in range(0,len(tt_button)):
                    if load_name(tt_button[tt][0]) == "font_button":
                        font = tt_button[tt][1]
                    if load_name(tt_button[tt][0]) == "fontsize_button":
                        fontsize = tt_button[tt][1]
                    if load_name(tt_button[tt][0]) == "width_button1":
                        width1 = tt_button[tt][1]
                    if load_name(tt_button[tt][0]) == "width_button2":
                        width2 = tt_button[tt][1]
                    if load_name(tt_button[tt][0]) == "bg_button1":
                        bg1 = tt_button[tt][1]
                    if load_name(tt_button[tt][0]) == "bg_button2":
                        bg2 = tt_button[tt][1]
                for it in range(0,len(list1)):
                    globals()["button"+str(2*it)] = Radiobutton(globals()[name_frame],text=str(list1[it]).split("_")[0],command=functools.partial(func,str(list1[it]))
                                                                ,value=str(it),indicator = 0,anchor="w")
                    globals()["button"+str(2*it+1)] = Radiobutton(globals()[name_frame],text=str(list1[it]).split("_")[1],command=functools.partial(func,str(list1[it]))
                                                ,anchor="w",indicator = 0,value=str(it))
                    if width2 != "NA" and width2 != "NA":
                        globals()["button"+str(2*it+1)].configure(width = int(width2))
                        globals()["button"+str(2*it)].configure(width= int(width1))
                    if bg1 != "NA":
                        globals()["button"+str(2*it)].configure(bg = bg1)
                        globals()["button"+str(2*it)].configure(background = bg1)
                    if bg2 != "NA":
                        globals()["button"+str(2*it+1)].configure(bg = bg2)
                        globals()["button"+str(2*it+1)].configure(background = bg2)
                    if font != "NA" and fontsize != "NA":
                        globals()["button"+str(2*it+1)].configure(font = (font,int(fontsize)))
                        globals()["button"+str(2*it)].configure(font = (font,int(fontsize)))
                    
                    globals()["button"+str(2*it)].grid(column=0,row=it,sticky="nsw")
                    globals()["button"+str(2*it+1)].grid(column=1,row=it,sticky="nsew")
                    globals()["button"+str(2*it+1)].bind('<Double-1>', self.edit_diff_same) 
            
            globals()[name_frame].update()
            globals()[name_window].configure(yscrollcommand=globals()[name_scrollbar].set, scrollregion="0 0 0 %s" % globals()[name_frame].winfo_height())
            if new == 1 or remove_button == 1:
                self.edit_gird_window(name_window,tt_2)
                self.edit_gird_window(name_scrollbar,tt_scrollbar)
            self.edit_window(name_window,tt_3)
    def frame_canvas_window(self,name,tt_1,tt_2,new=1):
        if new == 1:
            for i2 in range(0,len(tt_1)):
                if load_name(tt_1[i2][0]) == "thuoc_frame":
                    name_window,exist_cas,stt_ok_0_cas,stt_ok_1_cas,name_thuoc_frame = self.check_find_name_window(name,tt_1[i2][1])
                    if exist_cas == 0:
                        self.list_name[stt_ok_0_cas] = name
            k = 0
            for i in range(0,len(self.list_name)):
                if self.list_name[i] == "":
                    if k == 0:
                        self.list_globals.update({"name_vbar_1":i})
                    if k == 1:
                        self.list_globals.update({"name_hbar_1":i})
                    if k == 2:
                        self.list_globals.update({"name_height":i})
                    if k == 3:
                        self.list_globals.update({"name_imscale":i})
                    if k == 4:
                        self.list_globals.update({"name_delta":i})
                    if k == 5:
                        self.list_globals.update({"name_container":i})
                    if k == 6:
                        self.list_globals.update({"name_width":i})
                    if k == 7:
                        self.list_globals.update({"name_img":i})
                    k = k + 1
                    self.list_name[i] = name+str(i)
                if k == 8:
                    break
            self.list_tt_frame_canvas = {"name_frame_canvas":name,"name_window":name_window,"tt_canvas_1":tt_1,"tt_canvas_2":tt_2}
            globals()["self."+str(self.list_globals["name_vbar_1"])] = AutoScrollbar(globals()[name_thuoc_frame], orient='vertical')
            globals()["self."+str(self.list_globals["name_hbar_1"])] = AutoScrollbar(globals()[name_thuoc_frame], orient='horizontal')
            globals()["self."+str(self.list_globals["name_vbar_1"])].grid(row=0, column=1, sticky='ns')
            globals()["self."+str(self.list_globals["name_hbar_1"])].grid(row=1, column=0, sticky='we')
            globals()[name_window] = Canvas(globals()[name_thuoc_frame], highlightthickness=0,xscrollcommand=globals()["self."+str(self.list_globals["name_hbar_1"])].set
                                            , yscrollcommand=globals()["self."+str(self.list_globals["name_vbar_1"])].set)
            globals()[name_window].update()  # wait till canvas is created
            globals()["self."+str(self.list_globals["name_vbar_1"])].configure(command=lambda: self.scroll_y(name_canvas=str(name)
                                                                                                             ,name_container=str(self.list_globals["name_hbar_1"])))
            globals()["self."+str(self.list_globals["name_hbar_1"])].configure(command=lambda: self.scroll_x(name_canvas=str(name)
                                                                                                             ,name_container=str(self.list_globals["name_vbar_1"])))
            globals()[name_thuoc_frame].rowconfigure(0, weight=1)
            globals()[name_thuoc_frame].columnconfigure(0, weight=1)
            self.edit_gird_window(name_window,tt_2)
            # self.edit_window(name_window,tt_canvas_3)

    def zoom_img(self,img):
        if len(self.list_tt_frame_canvas) != 0:
            tt_canvas_1 = self.list_tt_frame_canvas["tt_canvas_1"]
            tt_canvas_2 = self.list_tt_frame_canvas["tt_canvas_2"]
            ten_frame_canvas = self.list_tt_frame_canvas["name_frame_canvas"]
            if self.list_globals != "":
                for i2 in range(0,len(tt_canvas_1)):
                    if tt_canvas_1[i2][0] == "thuoc_frame":
                        name_window,exist_cas,stt_ok_0_cas,stt_ok_1_cas,name_thuoc_frame = self.check_find_name_window(ten_frame_canvas,tt_canvas_1[i2][1])
                        if exist_cas == 0:
                            self.list_name[stt_ok_0_cas] = ten_frame_canvas
                self.list_tt_frame_canvas = {"name_frame_canvas":ten_frame_canvas,"name_window":name_window,"tt_canvas_1":tt_canvas_1,"tt_canvas_2":tt_canvas_2}
                globals()["self."+str(self.list_globals["name_vbar_1"])] = AutoScrollbar(globals()[name_thuoc_frame], orient='vertical')
                globals()["self."+str(self.list_globals["name_hbar_1"])] = AutoScrollbar(globals()[name_thuoc_frame], orient='horizontal')
                globals()["self."+str(self.list_globals["name_vbar_1"])].grid(row=0, column=1, sticky='ns')
                globals()["self."+str(self.list_globals["name_hbar_1"])].grid(row=1, column=0, sticky='we')
                globals()[name_window] = Canvas(globals()[name_thuoc_frame], highlightthickness=0,xscrollcommand=globals()["self."+str(self.list_globals["name_hbar_1"])].set
                                                , yscrollcommand=globals()["self."+str(self.list_globals["name_vbar_1"])].set)
                globals()[name_window].update()  # wait till canvas is created
                globals()["self."+str(self.list_globals["name_vbar_1"])].configure(command=lambda: self.scroll_y(name_canvas=str(ten_frame_canvas)
                                                                                                                ,name_container=str(self.list_globals["name_hbar_1"])))
                globals()["self."+str(self.list_globals["name_hbar_1"])].configure(command=lambda: self.scroll_x(name_canvas=str(ten_frame_canvas)
                                                                                                                ,name_container=str(self.list_globals["name_vbar_1"])))
                globals()[name_thuoc_frame].rowconfigure(0, weight=1)
                globals()[name_thuoc_frame].columnconfigure(0, weight=1)
                self.edit_gird_window(name_window,tt_canvas_2)
                # self.edit_window(name_window,tt_canvas_3)
                ###########
                globals()[name_window].bind('<ButtonPress-1>',self.move_from)
                globals()[name_window].bind('<B1-Motion>',self.move_to)
                globals()[name_window].bind('<MouseWheel>',self.wheel)  # with Windows and MacOS, but not Linux
                globals()[name_window].bind('<Button-5>',self.wheel)  # only with Linux, wheel scroll down
                globals()[name_window].bind('<Button-4>',self.wheel)  # only with Linux, wheel scroll up
                globals()["self."+str(self.list_globals["name_img"])] = img  # open image
                globals()["self."+str(self.list_globals["name_width"])], globals()["self."+str(self.list_globals["name_height"])] = globals()["self."+str(self.list_globals["name_img"])].size
                globals()["self."+str(self.list_globals["name_imscale"])] = 1.0  # scale for the canvaas image
                globals()["self."+str(self.list_globals["name_delta"])] = 1.5  # zoom magnitude
                globals()["self."+str(self.list_globals["name_container"])] = globals()[name_window].create_rectangle(0, 0, globals()["self."+str(self.list_globals["name_width"])]
                                                                                                        ,globals()["self."+str(self.list_globals["name_height"])], width=0)
                self.show_image()
    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        if len(self.list_tt_frame_canvas) != 0:
            globals()[self.list_tt_frame_canvas["name_window"]].yview(*args, **kwargs)  # scroll vertically
            self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        if len(self.list_tt_frame_canvas) != 0:
            globals()[self.list_tt_frame_canvas["name_window"]].xview(*args, **kwargs)  # scroll horizontally
            self.show_image()  # redraw the image

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        if len(self.list_tt_frame_canvas) != 0:
            globals()[self.list_tt_frame_canvas["name_window"]].scan_mark(event.x, event.y)
            self.show_image()

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        if len(self.list_tt_frame_canvas) != 0:
            globals()[self.list_tt_frame_canvas["name_window"]].scan_dragto(event.x, event.y, gain=1)
            self.show_image()  # redraw the image

    def wheel(self, event):
        # print(21)
        if len(self.list_tt_frame_canvas) != 0:
            name_window = self.list_tt_frame_canvas["name_window"]
            ''' Zoom with mouse wheel '''
            x = globals()[name_window].canvasx(event.x)
            y = globals()[name_window].canvasy(event.y)
            bbox = globals()[name_window].bbox(globals()["self."+str(self.list_globals["name_container"])])  # get image area
            if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: 
                pass  # Ok! Inside the image
            else: 
                return  # zoom only inside image area
            scale = 1.0
            # Respond to Linux (event.num) or Windows (event.delta) wheel event
            if event.num == 5 or event.delta == -120:  # scroll down
                i = min(globals()["self."+str(self.list_globals["name_width"])],globals()["self."+str(self.list_globals["name_height"])])
                if int(i * globals()["self."+str(self.list_globals["name_imscale"])]) < 30: 
                    return  # image is less than 30 pixels
                globals()["self."+str(self.list_globals["name_imscale"])] /= globals()["self."+str(self.list_globals["name_delta"])]
                scale /= globals()["self."+str(self.list_globals["name_delta"])]
            if event.num == 4 or event.delta == 120:  # scroll up
                i = min(globals()[name_window].winfo_width(), globals()[name_window].winfo_height())
                if i < globals()["self."+str(self.list_globals["name_imscale"])]: 
                    return  # 1 pixel is bigger than the visible area
                
                globals()["self."+str(self.list_globals["name_imscale"])] *= globals()["self."+str(self.list_globals["name_delta"])]
                scale *= globals()["self."+str(self.list_globals["name_delta"])]
            globals()[name_window].scale('all', x, y, scale, scale)  # rescale all canvas objects
            self.show_image()
            # globals()[name_window].update()  # wait till canvas is created
    def zoom_xy_value(self,x_move,y_move,value_zoom):
        if len(self.list_tt_frame_canvas) != 0:
            name_window = self.list_tt_frame_canvas["name_window"]
            globals()[name_window].update()
            globals()[name_window].scan_dragto(-(x_move), -(y_move), gain=1)
            for i in range(0,value_zoom):
                x= int(x_move)
                y= int(y_move)
                bbox = globals()[name_window].bbox(globals()["self."+str(self.list_globals["name_container"])])  # get image area
                if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]: pass  # Ok! Inside the image
                else: return  # zoom only inside image area
                scale = 1.0
                i = min(globals()[name_window].winfo_width(), globals()[name_window].winfo_height())
                if i < globals()["self."+str(self.list_globals["name_imscale"])]: 
                    return  # 1 pixel is bigger than the visible area
                
                globals()["self."+str(self.list_globals["name_imscale"])] /= globals()["self."+str(self.list_globals["name_delta"])]
                scale /= globals()["self."+str(self.list_globals["name_delta"])]
                globals()[name_window].scale('all', x, y, scale, scale)  # rescale all canvas objects
                self.show_image()
            self.show_image()
    def show_image(self, event=None):

        if len(self.list_tt_frame_canvas) != 0:
            name_window = self.list_tt_frame_canvas["name_window"]
            globals()[name_window].update()
            ''' Show image on the Canvas '''
            bbox1 = globals()[name_window].bbox(globals()["self."+str(self.list_globals["name_container"])])  # get image area
            # Remove 1 pixel shift at the sides of the bbox1
            bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
            bbox2 = (globals()[name_window].canvasx(0),  # get visible area of the canvas
                    globals()[name_window].canvasy(0),
                    globals()[name_window].canvasx(globals()[name_window].winfo_width()),
                    globals()[name_window].canvasy(globals()[name_window].winfo_height()))
            bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                    max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
            if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
                bbox[0] = bbox1[0]
                bbox[2] = bbox1[2]
            if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
                bbox[1] = bbox1[1]
                bbox[3] = bbox1[3]
            globals()[name_window].configure(scrollregion=bbox)  # set scroll region
            x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
            y1 = max(bbox2[1] - bbox1[1], 0)
            x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
            y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
            if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
                x = min(int(x2 / globals()["self."+str(self.list_globals["name_imscale"])]), globals()["self."+str(self.list_globals["name_width"])])
                y = min(int(y2 / globals()["self."+str(self.list_globals["name_imscale"])]), globals()["self."+str(self.list_globals["name_height"])])
                image = globals()["self."+str(self.list_globals["name_img"])].crop((int(x1 / globals()["self."+str(self.list_globals["name_imscale"])])
                                                                               , int(y1 / globals()["self."+str(self.list_globals["name_imscale"])]), x, y))
                imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
                imageid = globals()[name_window].create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                                anchor='nw', image=imagetk)
                globals()[name_window].lower(imageid)  # set image into background
                globals()[name_window].imagetk = imagetk  # keep an extra reference to prevent garbage-collection
    def w_h_label(self,name):
        name_window = self.name_window_da_kb(name)
        w = globals()[name_window].winfo_width()
        h = globals()[name_window].winfo_height()
        return w,h
    def value(self,name_value):
        name_window = self.name_window_da_kb(name_value)
        out = ""
        try:
            out = globals()[name_window].get()
        except:
            out = globals()[name_window]['text']
        return out
    def label_img(self,name_img,name_label,img):
        name_window = self.name_window_da_kb(name_label)
        name_window_img,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window_2(name_img)
        if exist == 0:
            self.list_name[stt_ok_0] = name_img
        globals()[name_window_img] = img
        globals()[name_window].configure(image=globals()[name_window_img])
        # print(name_img,name_label,img)
    def insert_entry(self,name_entry,value):
        name_window = self.name_window_da_kb(name_entry)
        globals()[name_window].insert(END, str(value))
    def set_var_radiobutton(self,name_var,value):
        name_window = self.name_window_da_kb(name_var)
        globals()[name_window].set(int(value))
    def set_combbox(self,name_combobox,value):
        name_window = self.name_window_da_kb(name_combobox)
        globals()[name_window].set(str(value))
    def set_ds_combobox(self,name_combobox,ds_value):
        # combobox['values'] = ('value1', 'value2', 'value3')
        name_window = self.name_window_da_kb(name_combobox)
        globals()[name_window]['values'] = ds_value
    def get_radio_check_button(self,name):
        out = "None"
        name_variable = self.name_window_da_kb(name)
        out = globals()[name_variable].get()
        return out
    def text_in_entry(self,name,text):
        name_window = self.name_window_da_kb(name)
        globals()[name_window].delete(0, tk.END)
        globals()[name_window].insert(0, text)
    def text_in_label(self,name,text,color = "None"):
        name_window = self.name_window_da_kb(name)
        globals()[name_window].configure(text = text)
        if color != "None":
            globals()[name_window].configure(fg = color)
    def text_in_button(self,name,text= "",bg = ""):
        name_window = self.name_window_da_kb(name)
        if text != "":
            globals()[name_window].configure(text = text)
        if bg != "":
            globals()[name_window].configure(bg = bg)
    def color_in_window(self,name,value):
        name_window = self.name_window_da_kb(name)
        globals()[name_window].configure(bg = value)
    def edit_diff_same(self,event):
        func("diff_same")
    def mouse_xy_label(self,name,reset = 0):
        if self.khai_bao_mouse == 0:
            self.khai_bao_mouse = 1
            name_window = self.name_window_da_kb(name)
            # globals()[name_window].bind('<Button-1>', self.callback_left_click)
            # globals()[name_window].bind('<Button-2>', self.callback_mid_click)
            # globals()[name_window].bind('<Button-3>', self.callback_right_click)
            globals()[name_window].bind('<Button-1>',self.callback)
            # globals()[name_window].bind('<MouseWheel>', self.mouse_wheel)
            globals()[name_window].bind('<Motion>',self.di_chuyen)
            globals()[name_window].bind_all("<Up>",  self.up)
            globals()[name_window].bind_all("<Down>",  self.dow)
            globals()[name_window].bind_all("<Left>",  self.left)
            globals()[name_window].bind_all("<Right>",  self.right)
            globals()[name_window].focus_set()
        if reset == 1:
            self.tien = 0
            self.lui = 0
            self.trai = 0
            self.phai = 0
            self.x = -1
            self.y = -1
        return self.x,self.y,self.x1,self.y1,self.tien,self.lui,self.trai,self.phai
    def di_chuyen(self,event):
        self.x1= event.x
        self.y1= event.y
    def callback_left_click(self, event):
        self.x = event.x
        self.y = event.y
        # print(f"Left click at ({self.x}, {self.y})")
    def mouse_wheel(self, event):
        if event.delta > 0:
            print("Mouse wheel scrolled up")
        else:
            print("Mouse wheel scrolled down")
    def callback(self, event):
        self.x = event.x
        self.y = event.y
        print(f"Mid click at ({self.x}, {self.y})")

    def callback_right_click(self, event):
        self.x = event.x
        self.y = event.y
        print(f"Right click at ({self.x}, {self.y})")
    # def callback(self,event):
    #     self.x= event.x
    #     self.y= event.y
    def up(self,event):
        self.tien = 1
    def dow(self,event):
        self.lui = 1
    def left(self,event):
        self.trai = 1
    def right(self,event):
        self.phai = 1
    def destroy_window(self,name):
        name_window = self.name_window_da_kb(name)
        ok = 0
        for i in range(0,len(self.list_name)):
            if self.list_name[i] == name:
                self.list_name[i] = ""
                ok = 1
        if ok == 1:
            globals()[name_window].destroy()
            
    def update_mylist(self,name_listbox = "",data = "",clear_mylist = 0):
        name_window = self.name_window_da_kb(name_listbox)
        if name_window != "":
            # print("name2 = ",name_window)
            if clear_mylist == 0:
                globals()[name_window].insert(END,data)
            if clear_mylist == 1:
                globals()[name_window].delete(0,'end')
            clear_mylist = None
    def update_window(self,name_root):
        name_window = self.name_window_da_kb(name_root)
        if name_window != "None":
            globals()[name_window].update()