from support_main.lib_main.giao_dien import Giao_dien,sent_data_main
import path
from support_main.lib_main import load_data_csv, remove
import os,cv2
import shutil
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
from support_main.lib_main import add_giao_dien

# ds_combobox,ten_combobox,tt_combobox = load_data_csv.ds_combobox()\
path_phan_mem = path.path_phan_mem
path_list_window = path_phan_mem + "/list_window"
path_setting = path_phan_mem + "/setting"
path_list_window = remove.tao_folder(path_phan_mem + "/list_window")

def name_csv(input):
    out = ""
    for i in list(input):
        if i == ".":
            break
        out = out + i
    return out
def edit_text_label(input):
    # print(input)
    ds = str(input).split("_")
    list_out = []
    if len(ds) >= 2:
        k = 0
        out_1 = ""
        out_2 = ""
        for i0 in range(0,len(ds)):
            if k == 0:
                out_1 = ds[i0]
            if k != 0:
                if k == 1:
                    out_2 = ds[i0]
                else:
                    out_2 = out_2 + "_" + ds[i0]
            k = k+1
        list_out = [out_1,out_2]
        # print(list_out)
    return list_out
def edit_tt_label(input):
    # print(input)
    list_out = []
    for i in range(0,len(input)):
        ap = edit_text_label(input[i])
        if len(ap) > 0:
            list_out.append(ap)
    return list_out
def tt_label_new(input):
    list_new = []
    for i in range(0,len(input)):
        ap = edit_tt_label(input[i])
        if len(ap) > 0:
            list_new.append(ap)
    return list_new

class main_window:
    def __init__(self,number):
        self.ds_label = []
        self.ds_name_file = []
        self.ds_list_window = os.listdir(path_list_window)
        
        self.list_root = []
        self.list_name = []
        for i in range(0,number):
            globals()["self."+str(i)] = ""
            self.list_name.append("")
        self.giao_dien = Giao_dien()
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
            if self.list_name[i] != name_label:
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
    def khai_bao_list_window(self):
        name_update = []
        name_close = []
        if len(self.ds_name_file) == 0:
            for w1 in self.ds_list_window:
                name_update.append(w1)
        else:
            for w1 in os.listdir(path_list_window):
                const_update = 1  
                for w2 in self.ds_list_window:
                    if w1 == w2:
                        const_update = 0
                if const_update == 1:
                    name_update.append(w1)

            for w3 in self.ds_list_window:
                const_close = 1
                for w4 in os.listdir(path_list_window):
                    if w3 == w4:
                        const_close = 0
                if const_close == 1:
                    name_close.append(w3)
        self.ds_list_window = os.listdir(path_list_window)
        # print("ds_name_file = ",self.ds_name_file)
        if len(name_update) != 0:
            # print(name_update)
            for k in range(0,len(name_update)):
                self.ds_name_file.append(name_csv(name_update[k]))
                name_window,exist,stt_ok_0,stt_ok_1 = self.check_find_name_window_2(name_update[k])
                if exist == 0:
                    self.list_name[stt_ok_0] = name_update[k]
                # globals()[name_window] = Giao_dien()
                name_tt,exist_tt,stt_ok_0_tt,stt_ok_1_tt = self.check_find_name_window_2(name_update[k]+"1")
                if exist_tt == 0:
                    self.list_name[stt_ok_0_tt] = name_update[k]+"1"
                globals()[name_tt] = add_giao_dien.edit_all()
                self.ds_label.append(tt_label_new(load_data_csv.load_file_csv(path_list_window+"/"+str(name_update[k]))[0]))
                tt_window = self.ds_label[-1]
                for i in range(0,len(tt_window)):
                    if len(tt_window[i]) > 1:
                        if len(tt_window[i][1]) > 0:
                            if tt_window[i][1][1] == "root":
                                name,tt = globals()[name_tt].create_root(tt_window[i])
                                self.giao_dien.root_window(name,tt)
                            if tt_window[i][1][1] == "toplevel":
                                name,tt = globals()[name_tt].create_root(tt_window[i])
                                self.giao_dien.root_window(name,tt,new_toplever = 1)
                            if tt_window[i][1][1] == "frame":
                                name,tt1,tt2,tt3 =globals()[name_tt].create_frame(tt_window[i])
                                # print(name,tt1,tt2,tt3)
                                self.giao_dien.frame_window(name,tt1,tt2,tt3)
                            if tt_window[i][1][1] == "label":
                                name,tt1,tt2,tt3 = globals()[name_tt].create_label(tt_window[i])
                                self.giao_dien.label_window(name,tt1,tt2,tt3)
                            if tt_window[i][1][1] == "entry":
                                name,tt1,tt2,tt3 = globals()[name_tt].create_entry(tt_window[i])
                                self.giao_dien.entry_window(name,tt1,tt2,tt3)
                            if tt_window[i][1][1] == "checkbutton":
                                name,tt1,tt2,tt3 = globals()[name_tt].create_checkbutton(tt_window[i])
                                self.giao_dien.checkbutton_window(name,tt1,tt2,tt3)
                            if tt_window[i][1][1] == "radiobutton":
                                name,tt1,tt2,tt3 = globals()[name_tt].create_radiobutton(tt_window[i])
                                self.giao_dien.radiobutton_window(name,tt1,tt2,tt3)
                            if tt_window[i][1][1] == "button":
                                name,tt1,tt2,tt3 = globals()[name_tt].create_button(tt_window[i])
                                self.giao_dien.button_window(name,tt1,tt2,tt3)
                            if tt_window[i][1][1] == "canvas":
                                name,tt1,tt2,tt3,tt_scrollbar,tt_button,new_canvas,remove_button,update_button = globals()[name_tt].create_canvas(tt_window[i])
                                self.giao_dien.canvas_window(name,tt1,tt2,tt3,tt_scrollbar,tt_button,new=new_canvas,remove_button=remove_button,update_button=update_button)
                            if tt_window[i][1][1] == "frame canvas":
                                name,tt1,tt2 = globals()[name_tt].create_frame_canvas(tt_window[i])
                                self.giao_dien.frame_canvas_window(name,tt1,tt2)
                            if tt_window[i][1][1] == "menu":
                                tt = globals()[name_tt].create_menu(tt_window[i])
                                self.giao_dien.menu_window(tt)
                            if tt_window[i][1][1] == "mylist":
                                name,tt1,tt2,tt3,scrollbar,listbox = globals()[name_tt].create_mylist(tt_window[i])
                                self.giao_dien.mylist_window(name,tt1,tt2,tt3,scrollbar,listbox)
                            if tt_window[i][1][1] == "combobox":
                                name,tt1,tt2,tt3 = globals()[name_tt].create_combobox(tt_window[i])
                                self.giao_dien.combobox_window(name,tt1,tt2,tt3)
                            if tt_window[i][1][1] == "text":
                                name,tt1,tt2 = globals()[name_tt].create_text(tt_window[i])
                                self.giao_dien.text_window(name,tt1,tt2)
        if len(name_close) != 0:
            # print("close = ",name_close)
            for k in range(0,len(name_close)):
                name_window = self.name_window_da_kb(name_close[k])
                name_tt = self.name_window_da_kb(name_close[k]+"1")
                tt_window = tt_label_new(load_data_csv.load_file_csv(path_setting+"/"+str(name_close[k]))[0])
                for i in range(0,len(tt_window)):
                    if len(tt_window[i]) > 1:
                        if len(tt_window[i][1]) > 0:
                            if tt_window[i][1][1] == "root" or tt_window[i][1][1] == "toplevel":
                                name,tt = globals()[name_tt].create_root(tt_window[i])
                                self.giao_dien.destroy_window(name)
            for cl in name_close:
                for stt_cl in range(0,len(self.ds_name_file)):
                    if name_csv(cl) == self.ds_name_file[stt_cl]:
                        del self.ds_name_file[stt_cl]
                        del self.ds_label[stt_cl]
                        break
        return len(self.ds_name_file)
    def update(self,name_root):
        self.giao_dien.update_window(name_root)
    def w_h_label(self,name):
        return self.giao_dien.w_h_label(name)
    def value(self,name_value):
        return self.giao_dien.value(name_value)
    def label_img(self,name_img,name_label,img):
        self.giao_dien.label_img(name_img,name_label,img)

    def label_img2(self,name_img,name_label,path_pdf):
        return name_img,name_label,path_pdf


    def set_var_radiobutton(self,name_var,value):
        self.giao_dien.set_var_radiobutton(name_var,value)
    def get_radio_check_button(self,name):
        return self.giao_dien.get_radio_check_button(name)
    def text_in_entry(self,name,text):
        self.giao_dien.text_in_entry(name,text)
    def text_in_label(self,name,text,color = "None"):
        self.giao_dien.text_in_label(name,text,color)
    def text_in_button(self,name,text = "",color = ""):
        self.giao_dien.text_in_button(name,text,color)
    def zoom_img(self,path_padf):
        self.giao_dien.zoom_img(path_padf)
    def zoom_xy_value(self,value_zoom):
        self.giao_dien.zoom_xy_value(value_zoom)
    def canvas_window(self,name_canvas,tt_1,tt_2,tt_3,tt_scrollbar,tt_button =[],list1=[],new=1,remove_button=0,update_button = 0):
        self.giao_dien.canvas_window(name_canvas,tt_1,tt_2,tt_3,tt_scrollbar,tt_button,list1,new,remove_button,update_button)
    def wheel_0(self,delta_x=0,delta_y=0,number=1,new = 0):
        self.giao_dien.wheel_0(delta_x,delta_y,number,new)
    def reset_up_dow(self):
        self.giao_dien.reset_up_dow()
    def move_to2(self, x,y):
        self.giao_dien.move_to2(x,y)
    def reset_zoom(self):
        self.giao_dien.reset_zoom()
    def update_button_canvas_window(self,file_csv,list,remove_button=0):
        for i in range(0,len(self.ds_name_file)):
            if self.ds_name_file[i] == name_csv(file_csv):
                tt_window = self.ds_label[i]
                name_tt,exist_tt,stt_ok_0_tt,stt_ok_1_tt = self.check_find_name_window_2(str(file_csv)+"1")
                for i in range(0,len(tt_window)):
                    if len(tt_window[i]) > 1:
                        if len(tt_window[i][1]) > 0:
                            if tt_window[i][1][1] == "canvas":
                                name,tt1,tt2,tt3,tt_scrollbar,tt_button,new_canvas,remove_button0,update_button = globals()[name_tt].create_canvas(tt_window[i])
                                self.giao_dien.canvas_window(name,tt1,tt2,tt3,tt_scrollbar,tt_button,list1=list,new=0,remove_button=remove_button,update_button=1)
                break
    def color_in_window(self,name,value):
        self.giao_dien.color_in_window(name,value)
    def update_mylist(self,name_listbox = "",data = "",clear_mylist = 0):
        self.giao_dien.update_mylist(name_listbox,data,clear_mylist)
    def set_combbox(self,name_combobox,value):
        self.giao_dien.set_combbox(name_combobox,value)
    def set_ds_combobox(self,name_combobox,ds_value):
        self.giao_dien.set_ds_combobox(name_combobox,ds_value)
    def mouse_xy_label(self,name,reset = 0):
        return self.giao_dien.mouse_xy_label(name,reset)
