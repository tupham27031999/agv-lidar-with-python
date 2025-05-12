from . import ket_noi_esp
from support_main.lib_main import remove, load_data_csv, edit_csv_tab, convert
from support_main.lib_main.giao_dien import Giao_dien,sent_data_main,reset_data
from support_main.connect_lidar import main_lidar, disconnect_lidar,return_data
from support_main.lib_main.list_window import main_window
from support_main import connect_plc, process_lidar_2, tim_duong_di
from sklearn.cluster import DBSCAN
import path
import numpy as np
import shutil
import os,cv2,math
from tkinter import filedialog
import threading
from datetime import datetime
import serial.tools.list_ports
import time
def edit_path(input):
    output = ""
    for i in input:
        if i == "\\":
            output = output + "/"
        else:
            output = output + i
    return output

path_phan_mem = path.path_phan_mem
path_list_window = path_phan_mem + "/list_window"
path_giao_dien = path_phan_mem + "/setting/giao_dien_chinh.csv"
path_setting_plc = path_phan_mem + "/setting/setting_plc.csv"
path_admin = path_phan_mem + "/setting/admin_window.csv"
if os.name == "nt":
    print("Hệ điều hành là Windows")
    # Đọc file cài đặt cho Windows
    path_admin = path_phan_mem + "/setting/admin_window.csv"
elif os.name == "posix":
    print("Hệ điều hành là Ubuntu (Linux)")
    # Đọc file cài đặt cho Ubuntu
    path_admin = path_phan_mem + "/setting/admin_ubuntu.csv"
path_data_input_output = path_phan_mem + "/data_input_output"

path_map_test_icp = remove.tao_folder(path_data_input_output + "/map_test_icp")


data_setting_plc = edit_csv_tab.load_all_stt(path_setting_plc)
path_data_map = path_phan_mem + "/data_input_output/map"
remove.tao_folder(path_data_map)
for i in range(0,len(data_setting_plc)):
    if len(data_setting_plc[i]) > 1:
        if data_setting_plc[i][0] == "connect_plc":
            address = data_setting_plc[i][1]
        if data_setting_plc[i][0] == "port":
            port = data_setting_plc[i][1]
ds_cong_com = []

def load_cong_com():
    ports = serial.tools.list_ports.comports()
    ds_cong_com = []
    for port, desc, hwid in sorted(ports):
        ds_cong_com.append(str(port))
    return ds_cong_com

def read_map(path_map):
    data_map = edit_csv_tab.load_all_stt(path_map)
    map_x = []
    map_y = []
    for i in range(0,len(data_map)):
        if len(data_map[i]) > 1:
            if data_map[i][0] == "window_size_x":
                window_size_x = int(data_map[i][1])
            if data_map[i][0] == "window_size_y":
                window_size_y = int(data_map[i][1])
            if data_map[i][0] == "scaling_factor":
                scaling_factor = float(data_map[i][1])
            if data_map[i][0] == "data":
                map_x.append(int(float(data_map[i][1])))
                map_y.append(int(float(data_map[i][2])))
    return map_x,map_y,window_size_x,window_size_y,scaling_factor

# def update_line():
#     global sx,sy,gx,gy,grid_size,robot_radius,ox,oy,rx,ry,up_line
#     rx,ry = dijkstra_tim_duong_di.main(sx,sy,gx,gy,grid_size,robot_radius,ox,oy)
#     rx.reverse()
#     ry.reverse()
#     up_line = 0
#     print("upline2")
def create_map(px,py,window_size_x,window_size_y):
    arr_goc = []
    arr_goc = np.ones((3,px.shape[0]+1))
    arr_goc[0,:] = np.append(px,np.array([int(window_size_x/2)]))
    arr_goc[1,:] = np.append(py,np.array([int(window_size_y/2)]))
    arr_goc[2,:] = np.ones(px.shape[0]+1)
    return arr_goc

# tao ten file log theo ma seri va thoi gian
def time_now():
    dt = datetime.now()
    time_0 = str(dt.year) +'/'+ str(dt.month) + '/' + str(dt.day) + ' ' + str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)
    time_1 = str(dt.year) +'_'+ str(dt.month) + '_' + str(dt.day) + '_' + str(dt.hour) + '_' + str(dt.minute) + '_' + str(dt.second)
    return time_0,time_1
name_error,name_warning = ["",""]

def reset_warning():
    global warning,error,name_error,name_warning
    warning,error,name_error,name_warning = [0,0,"",""]

def load_folder():
    # file_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
    file_path = filedialog.askdirectory() # folder  
    return file_path
def load_link_csv():
    # Mở hộp thoại chọn file và chỉ cho phép chọn các file .png
    file_path = filedialog.askopenfilename(
        title="Chọn file PNG",
        filetypes=[("PNG files", "*.png")]
    )
    # file_path = filedialog.askdirectory() # folder  
    return file_path# Sử dụng DBSCAN để phân cụm và loại bỏ các cụm có ít điểm
def filter_clusters(points_x,point_y, min_samples=5, eps=10):
    points_x_out = []
    point_y_out = []
    points = np.array([points_x,point_y]).T
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(points)
    labels = db.labels_

    # Lọc các cụm có ít điểm
    unique_labels = set(labels)
    filtered_points = []
    for label in unique_labels:
        if label == -1:
            continue  # Bỏ qua các điểm nhiễu
        cluster_points = points[labels == label]
        if len(cluster_points) >= min_samples:
            filtered_points.extend(cluster_points)
    filtered_points = np.array(filtered_points)
    points_x_out = np.array(filtered_points[:,0])
    point_y_out = np.array(filtered_points[:,1])
    return points_x_out,point_y_out


class main_sp:
    def __init__(self,name_window = "main_window"):
        self.name_window = name_window
        self.name_warning,self.name_error,self.link1,self.link2,self.link3 = ["","","","",""]
        
        self.warning,self.error,self.time_now0,self.time_now1 = np.zeros(4,int)
        self.connect_window = True
        self.time_0,self.time_1 = time_now()

        remove.remove_all_file_in_folder(path_list_window)
        shutil.copy(path_giao_dien,path_list_window+"/"+str(path_giao_dien).split("/")[-1])
        self.window = main_window(2000)
        self.window.khai_bao_list_window()
        self.window.update(self.name_window)
        self.update_giao_dien = 0

        self.com_lidar = ""
        self.bau_lidar = ""

        self.window.set_combbox("ds_bau","256000")
        self.window.set_ds_combobox("ds_com",ds_cong_com)
        
        self.window.set_var_radiobutton("variable_1","1")
        self.window.set_var_radiobutton("variable_2","1")
        self.window.set_var_radiobutton("variable_3","1")
        self.window.set_var_radiobutton("variable_4","1")

        self.plc = ""
        self.connect_plc = 0

        self.lidar = ""
        self.connect_lidar = 0

        self.address = address
        self.port = port
        self.window.text_in_entry("link_en_2",self.address)
        self.window.text_in_entry("link_en_3",self.port)

        self.window_size_x_all = 1000
        self.window_size_y_all = 1000
        self.window_size_x = 500
        self.window_size_y = 500
        self.scaling_factor = 0.03

        self.scan = np.array([[0],[0],[0]])
        
        self.img0 = np.zeros((self.window_size_y_all , self.window_size_x_all , 3)).astype("uint8")
        
        self.rmse1 = 4
        self.rmse2 = 3

        self.window.text_in_entry("link_en_map1",path_data_map)

        self.detect_lidar = process_lidar_2.process_data_lidar()
        self.detect_lidar.setting_data(self.window_size_x,self.window_size_y,self.window_size_x_all,self.window_size_y_all,self.scaling_factor,self.rmse1,self.rmse2)
        # self.detect_lidar.rotation
        self.update_map = 0

        self.chon_dich = 0
        self.chon_duong_di = 0
        self.run = 0
        self.upload_run = 0
        self.ds_dich = []
        self.ds_duong_di = []
        self.ds_duong_di_dich = []
        self.done = 0
        self.ds_duong_di_new = []
        self.ds_dich_new = []
        self.text_duong_di = ""
        self.text_duong_di_new = ""
        self.text_dich_new = ""

        self.them_map = 0
        self.xoa_map = 0
        self.edit_x = []
        self.edit_y = []
        self.load_map_goc = 0

        self.ty_le_x = 1
        self.ty_le_y = 1

        self.trang_thai_tien_lui = "tien"
        self.trang_thai_lui_trai = 0
        self.trang_thai_lui_phai = 0
        self.trang_thai_tien_trai = 0
        self.trang_thai_tien_phai = 0
        self.trang_thai_goc = 0
        self.end_point = [0,0]

        self.new_map = 1
        self.x_new_map = 0
        self.y_new_map = 0
        self.ang_new_map = 0

        try:
            pass
            threading.Thread(target=ket_noi_esp.python_esp32).start() ######`##################
        except OSError as e:
            print("khong ket noi duoc esp")
            pass

        self.angle = 0
        self.ang_plc = 0

        self.window.text_in_button("save_angle_0",color="yellow")

        self.new_start_point = 0
        self.input_8 = 0
        self.angle_start_point = 0
    def vong_while(self):
        self.setup_line()
        if self.window.get_radio_check_button("variable_2") == 1:
            self.detect_lidar.update_map = True
        else:
            self.detect_lidar.update_map = False
        if self.connect_lidar != 0:
            self.scan,check = return_data()
            self.scan = np.array(self.scan)
            if self.scan.shape[1] != 1 and check == True: # map goc
                self.scan = self.scan[(self.scan[:, 1] < 130) | (self.scan[:, 1] > 200)]
                # self.detect_lidar.process_data_lidar(self.scan,self.new_map)
                self.detect_lidar.process_data_lidar(self.scan,self.new_map,self.x_new_map,self.y_new_map,self.ang_new_map)

            self.window.text_in_button("reset_lidar","reset_lidar: " + str(int(float(self.detect_lidar.rmse)*100)/100))
            self.new_start_points()
        if self.update_giao_dien == 0:
            self.window.update(self.name_window)
            self.add_or_del_map()
            if self.check_connect_COM(load_cong_com()) == 0:
                self.window.set_combbox("ds_com","")
            self.window.set_ds_combobox("ds_com",load_cong_com())
            self.dk_ban_phim()
            self.run_agv()
            
            self.hien_thi()
            
            self.window.mouse_xy_label("img0",reset=1) 
        else:
            if self.window.khai_bao_list_window() != 0:
                self.update_giao_dien = 0
                self.window.set_combbox("ds_bau","256000")
                self.window.set_ds_combobox("ds_com",ds_cong_com)
                self.window.set_var_radiobutton("variable_1","1")
                self.window.set_var_radiobutton("variable_2","1")
                self.window.text_in_entry("link_en_map1",path_data_map)
            shutil.copy(path_giao_dien,path_list_window+"/"+str(path_giao_dien).split("/")[-1])
            self.window.khai_bao_list_window()
            self.window.update(self.name_window)
        self.load_input_8()
        self.check_button()
        self.thong_bao()

    def load_angle_esp(self):
        angle,load_angle = ket_noi_esp.load_data_angle()
        # print(self.detect_lidar.rotation*180/np.pi,angle)
        self.angle = angle + self.detect_lidar.rotation*180/np.pi
        # self.angle = self.detect_lidar.rotation*180/np.pi
        return self.angle,load_angle
    def dk_ban_phim(self):
        if self.ang_plc == 1:
            _,_,_,_,tien,lui,trai,phai = self.window.mouse_xy_label("img0")
            ang_plc = self.angle
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2 and self.detect_lidar.rmse <= self.rmse1:
                if tien == 1:
                    if self.input_8 == 1 or (ang_plc >= - 10 and ang_plc <= 10):
                        data = self.plc.sent_data("tien",vt_trai = "1000",vt_phai = "1000")
                    elif ang_plc > 10 and self.input_8 == 0:
                        data = self.plc.sent_data("tien",vt_trai = "0",vt_phai = "800")
                    elif ang_plc < -10 and self.input_8 == 0:
                        data = self.plc.sent_data("tien",vt_trai = "800",vt_phai = "0")
                    self.window.text_in_button("tien","Tiến","yellow")
                else:
                    self.window.text_in_button("tien","Tiến","white")
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2:
                if (tien != 1 and trai != 1 and phai != 1 and lui != 1) or self.detect_lidar.rmse > self.rmse1:
                    data = self.plc.sent_data("tien",vt_trai = "0",vt_phai = "0")
                    print("stop")
                    self.window.text_in_button("stop_agv","Stop","red")
                else:
                    self.window.text_in_button("stop_agv","Stop","white")
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2 and self.detect_lidar.rmse <= self.rmse1:
                if lui == 1:
                    if self.input_8 == 1 or (ang_plc >= - 10 and ang_plc <= 10):
                        data = self.plc.sent_data("lui",vt_trai = "1000",vt_phai = "1000")
                    elif ang_plc > 10 and self.input_8 == 0:
                        data = self.plc.sent_data("lui",vt_trai = "800",vt_phai = "0")
                    elif ang_plc < -10 and self.input_8 == 0:
                        data = self.plc.sent_data("lui",vt_trai = "0",vt_phai = "800")
                    self.window.text_in_button("lui","Lùi","yellow")
                else:
                    self.window.text_in_button("lui","Lùi","white")
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2 and self.detect_lidar.rmse <= self.rmse1:
                if trai == 1:
                    if self.angle > 70 or self.angle < - 70:
                        vt_trai = "1000"
                        vt_phai = "1000"
                    else:
                        vt_trai = "0"
                        vt_phai = "800"
                    data = self.plc.sent_data("lui",vt_trai = vt_trai,vt_phai = vt_phai)
                    self.window.text_in_button("trai","Trái","yellow")
                else:
                    self.window.text_in_button("trai","Trái","white")
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2 and self.detect_lidar.rmse <= self.rmse1:
                if phai == 1:
                    # data = self.plc.sent_data("tien",vt_trai = "800",vt_phai = "0")
                    if self.angle > 70 or self.angle < - 70:
                        vt_trai = "1000"
                        vt_phai = "1000"
                    else:
                        vt_trai = "800"
                        vt_phai = "0"
                    data = self.plc.sent_data("lui",vt_trai = vt_trai,vt_phai = vt_phai)
                    self.window.text_in_button("phai","Phải","yellow")
                else:
                    self.window.text_in_button("phai","Phải","white")
    def new_start_points(self):
        # if self.detect_lidar.edit_close == 1:
        #     self.new_start_point = 1
        #     self.detect_lidar.load_map_goc = 1
        #     self.new_map = 1

        if self.new_start_point != 0:
            self.new_map = 0
            x,y,x1,y1,_,_,_,_ = self.window.mouse_xy_label("img0")
            if x != -1 and y != -1:
                x = int(x * self.ty_le_x)
                y = int(y * self.ty_le_y)
                self.window.text_in_entry("gia_tri_x",str(x))
                self.window.text_in_entry("gia_tri_y",str(y))
            if self.window.value("gia_tri_x") != "" and self.window.value("gia_tri_y") != "" and self.window.value("gia_tri_x") != "-" and self.window.value("gia_tri_y") != "-":
                self.x_new_map = self.window.value("gia_tri_x")
                self.y_new_map = self.window.value("gia_tri_y")
            else:
                self.x_new_map = 0
                self.y_new_map = 0
            if self.window.value("gia_tri_angle") != "" and self.window.value("gia_tri_angle") != "-":
                self.ang_new_map = self.window.value("gia_tri_angle")


                    

    def reset_lidar(self):
        if os.path.exists(self.window.value("link_en_1")) == True:
            # file_pyc = self.window.value("link_en_1").split(".")[0]  + ".npy"
            # self.detect_lidar.x_goc,self.detect_lidar.y_goc,self.detect_lidar.rotation = np.load(file_pyc)
            # self.detect_lidar.rotation = 0
            self.detect_lidar.map_all = cv2.imread(self.window.value("link_en_1"))
            self.new_map = 0
        else:
            self.detect_lidar.load_map_goc = 0
            self.new_map = 1

    def hien_thi(self):
        if self.new_start_point == 0:
            self.img0 = self.detect_lidar.img2.copy()
        else:
            self.img0 = self.detect_lidar.edit_img.copy()
        for i in range(0,len(self.ds_duong_di)): 
            if i == 0:
                cv2.line(self.img0,(int(self.detect_lidar.x_goc),int(self.detect_lidar.y_goc)),(int(self.ds_duong_di[i][0]),int(self.ds_duong_di[i][1])),(0,255,0),1)
            else:
                cv2.line(self.img0,(int(self.ds_duong_di[i-1][0]),int(self.ds_duong_di[i-1][1])),(int(self.ds_duong_di[i][0]),int(self.ds_duong_di[i][1])),(0,255,0),1)
            cv2.circle(self.img0,(int(self.ds_duong_di[i][0]),int(self.ds_duong_di[i][1])),5,(155,0,0),-1)
        for i in range(0,len(self.ds_dich)):
            if len(self.ds_duong_di) != 0:
                cv2.line(self.img0,(int(self.ds_duong_di[-1][0]),int(self.ds_duong_di[-1][1])),(int(self.ds_dich[0][0]),int(self.ds_dich[0][1])),(0,255,255),1)
            else:
                cv2.line(self.img0,(int(self.detect_lidar.x_goc),int(self.detect_lidar.y_goc)),(int(self.ds_dich[0][0]),int(self.ds_dich[0][1])),(0,255,255),1)
            if i != 0:
                cv2.arrowedLine(self.img0, (int(self.ds_dich[0][0]),int(self.ds_dich[0][1])), (int(self.ds_dich[1][0]),int(self.ds_dich[1][1])), (0,0,255), 2,tipLength = 0.2)
            cv2.circle(self.img0,(int(self.ds_dich[0][0]),int(self.ds_dich[0][1])),5,(0,0,255),-1)
        if self.end_point[0] != 0:
            cv2.line(self.img0,(int(self.detect_lidar.x_goc),int(self.detect_lidar.y_goc)),(int(self.end_point[0]),int(self.end_point[1])),(0,0,255),1)
        # x = self.detect_lidar.x_goc
        # y = self.detect_lidar.y_goc
        # if x != 0 and y != 0:
        #     self.img0 = self.detect_lidar.img2[int(y - self.window_size_y):int(y + self.window_size_y),int(x-self.window_size_x):int(x+self.window_size_x)]
        h0,w0,_ = self.img0.shape
        w,h = self.update_img_frame("imgs_00","img0_img","img0",self.img0,w_goc=int(w0),h_goc=int(h0))
        self.ty_le_x = w0/w
        self.ty_le_y = h0/h
    def run_agv(self):
        if self.run == 1 and self.connect_plc == 1 and len(self.ds_dich) != 0:
            angle_deg = 0
            dk_van_toc = "off"
            distance = 0
            v0 = 2000
            angle = 0
            vt_trai = 0
            vt_phai = 0
            if self.upload_run == 1:
                self.upload_run = 0
                self.ds_duong_di_dich = self.ds_duong_di + [self.ds_dich[0]]
            if self.detect_lidar.rmse <= self.rmse1:
                if len(self.ds_duong_di_dich) >= 1:
                    start_point = [self.detect_lidar.x_goc,self.detect_lidar.y_goc]
                    end_point = self.ds_duong_di_dich[0]
                    self.end_point = end_point
                    robot_direction = [self.detect_lidar.huong_x, self.detect_lidar.huong_y]
                    if ((start_point[0] != end_point[0] or start_point[1] != end_point[1])):
                        distance, angle_deg = tim_duong_di.calculate_distance_and_angle(start_point, end_point, robot_direction)
                        if distance < 5:
                            del self.ds_duong_di_dich[0]
                            self.trang_thai_lui_phai = 0
                            self.trang_thai_lui_trai = 0
                    dk_van_toc = "on"

                elif len(self.ds_duong_di_dich) == 0 and self.done == 0:
                    start_point = [self.detect_lidar.x_goc,self.detect_lidar.y_goc]
                    robot_direction = [self.detect_lidar.huong_x, self.detect_lidar.huong_y]
                    A = np.array(self.ds_dich[0])
                    C = np.array(start_point)
                    B = np.array(self.ds_dich[1])
                
                    # Tính vector AC
                    AC = C - A
                    # Tịnh tiến điểm B theo vector AC
                    end_point = B + AC
                    self.end_point = end_point
                    distance, angle_deg = tim_duong_di.calculate_distance_and_angle(start_point, end_point, robot_direction)
                    if abs(angle_deg) <= 10:
                        self.done = 1
                    else:
                        dk_van_toc = "on"

                if self.done == 0:
                    if abs(angle_deg) >= 60:
                        self.trang_thai_tien_lui = "lui"
                    else:
                        if (self.trang_thai_goc > 0 and (-self.trang_thai_goc) > angle_deg) or\
                                                            (self.trang_thai_goc < 0 and (-self.trang_thai_goc) < angle_deg):
                            self.trang_thai_tien_lui = "tien"
                # thay doi trang thai tien lui
                number = 5
                if self.trang_thai_goc == 0:
                    if angle_deg > 0:
                        self.trang_thai_goc = number
                    elif angle_deg < 0:
                        self.trang_thai_goc = -number
                if self.trang_thai_goc == number and angle_deg < -number:
                    self.trang_thai_goc = -number
                    
                if self.trang_thai_goc == -number and angle_deg > number:
                    self.trang_thai_goc = number
                        
            if dk_van_toc == "on":
                if self.trang_thai_tien_lui == "tien":
                    self.trang_thai_lui_phai = 0
                    self.trang_thai_lui_trai = 0

                    number = 20
                    # angle = self.angle - angle_deg
                    angle_deg = angle_deg + self.angle
                    if angle_deg > 90:
                        angle_deg = 90
                    if angle_deg < -90:
                        angle_deg = -90
                    if angle_deg >= -20 or angle_deg <= 20:
                        vt_trai = v0 - v0*math.sin(angle_deg*np.pi/180)/2
                        vt_phai = v0 + v0*math.sin(angle_deg*np.pi/180)/2
                    else:
                        vt_trai = v0 - v0*math.sin(angle_deg*np.pi/180) 
                        vt_phai = v0 + v0*math.sin(angle_deg*np.pi/180)
                    # if self.angle > number:
                    #     vt_trai = 2*v0
                    #     vt_phai = 0
                    # if self.angle < -number:
                    #     vt_trai = 0
                    #     vt_phai = 2*v0
                    # data = self.plc.sent_data("tien",vt_trai = int(vt_trai),vt_phai = int(vt_phai))

                if self.trang_thai_tien_lui == "lui":
                    v0 = 1500
                    if angle_deg > 0 and self.trang_thai_lui_trai == 0:
                        vt_trai = 0
                        vt_phai = v0
                        self.trang_thai_lui_phai = 1
                        self.trang_thai_lui_trai = 0
                        
                    if angle_deg < 0 and self.trang_thai_lui_phai == 0:
                        vt_trai = v0
                        vt_phai = 0
                        self.trang_thai_lui_phai = 0
                        self.trang_thai_lui_trai = 1
                    if abs(self.angle) > 50:
                        vt_trai = v0
                        vt_phai = v0
                    # if len(self.ds_duong_di_dich) == 0:
                    #     if vt_trai > vt_phai:
                    #         vt_phai = 0
                    #     if vt_phai > vt_trai:
                    #         vt_trai = 0
                    # data = self.plc.sent_data("lui",vt_trai = int(vt_trai),vt_phai = int(vt_phai))
                # if angle_deg < 70 and angle_deg > - 70:
                #     data = self.plc.sent_data("tien",vt_trai = int(vt_trai),vt_phai = int(vt_phai))
                # else:
                # data = self.plc.sent_data(self.trang_thai_tien_lui,vt_trai = int(vt_phai),vt_phai = int(vt_trai))
                data = self.plc.sent_data(self.trang_thai_tien_lui,vt_trai = int(vt_trai),vt_phai = int(vt_phai))
            else:
                data = self.plc.sent_data("stop_agv")
            print(angle_deg,self.angle,self.trang_thai_lui_phai, self.trang_thai_lui_trai, vt_trai, vt_phai, self.trang_thai_tien_lui, self.trang_thai_goc, distance)

            for i in range(0,len(self.ds_duong_di_dich)): 
                if i == 0:
                    cv2.line(self.img0,(int(self.detect_lidar.x_goc),int(self.detect_lidar.y_goc)),(int(self.ds_duong_di_dich[i][0]),int(self.ds_duong_di_dich[i][1])),(0,200,100),2)
                else:
                    cv2.line(self.img0,(int(self.ds_duong_di_dich[i-1][0]),int(self.ds_duong_di_dich[i-1][1])),(int(self.ds_duong_di_dich[i][0]),int(self.ds_duong_di_dich[i][1])),(0,100,100),2)

























    def add_or_del_map(self):
        if self.them_map == 1:
            if os.path.exists(self.window.value("link_en_1")) == True:
                if self.update_map == 1:
                    self.update_map = 0
                    self.reset_lidar([],[])
            self.img0 = np.zeros((self.window_size_y , self.window_size_x , 3)).astype("uint8")
            if len(self.edit_x) != 0:
                for i in range(0,len(self.edit_x)): 
                    cv2.circle(self.img0,(int(self.edit_x[i]),int(self.edit_y[i])),3,(255,255,255),-1)
                x,y,x1,y1,_,_,_,_ = self.window.mouse_xy_label("img0")
                if x1 != 0 and y1 != 0:
                    x = x * self.ty_le_x
                    y = y * self.ty_le_y
                if x1 != 0 and y1 != 0:
                    cv2.rectangle(self.img0, (x1-10,y1-10), (x1+10,y1+10), (0,255,0), 1)
                    cv2.circle(self.img0,(x1,y1),3,(0,255,0),-1)
                    if x!= -1 and y != -1:
                        if self.window.get_radio_check_button("variable_4") == 1:
                            self.edit_x.append(x)
                            self.edit_y.append(y)
                        if self.window.get_radio_check_button("variable_4") == 2:
                            pass
        if self.xoa_map == 1:
            if os.path.exists(self.window.value("link_en_1")) == True:
                if self.update_map == 1:
                    self.update_map = 0
                    self.reset_lidar([],[])
            self.img0 = np.zeros((self.window_size_y , self.window_size_x , 3)).astype("uint8")
            if len(self.edit_x) != 0:
                for i in range(0,len(self.edit_x)): 
                    cv2.circle(self.img0,(int(self.edit_x[i]),int(self.edit_y[i])),3,(255,255,255),-1)
                x,y,x1,y1,_,_,_,_ = self.window.mouse_xy_label("img0")
                if x1 != 0 and y1 != 0:
                    x = x * self.ty_le_x
                    y = y * self.ty_le_y
                if x1 != 0 and y1 != 0:
                    cv2.rectangle(self.img0, (x1-10,y1-10), (x1+10,y1+10), (0,255,0), 1)
                    cv2.circle(self.img0,(x1,y1),3,(0,255,0),-1)

    def save_map_lidar(self):
        folder_save_map = self.window.value("link_en_map1")
        name_map = self.window.value("link_en_map2")
        if os.path.exists(folder_save_map) == True and name_map != "":
            name_map = str(name_map).split(".")[0]
            cv2.imwrite(folder_save_map+"/"+name_map + '.png', self.detect_lidar.map_all)
            np.save(folder_save_map+"/"+name_map, np.array([self.detect_lidar.x_goc,self.detect_lidar.y_goc,self.detect_lidar.rotation]))      
    def check_connect_COM(self,ds_com):
        output = 0
        com_connect = self.window.value("ds_com")
        for i in range(0,len(ds_com)):
            if com_connect == ds_com[i]:
                output = 1
        return output
    def thong_bao(self):
        if self.warning == 1:
            self.warning = 0
            reset_warning()
            convert.show_warning(self.name_warning)
        if self.error == 1:
            self.error = 0
            reset_warning()
            convert.show_error(self.name_error)
        
    def setup_line(self):
        x,y,x1,y1,_,_,_,_ = self.window.mouse_xy_label("img0")
        if x != -1 and y != -1:
            x = int(x * self.ty_le_x)
            y = int(y * self.ty_le_y)
            if self.chon_dich == 1:
                if x != -1 and y != -1:
                    self.ds_dich.append([x,y])
                    if len(self.ds_dich) > 1:
                        self.chon_dich = 0
                        self.window.text_in_button("chon_dich","Chọn đích đến","white")
                    text = ""
                    for i in range(0,len(self.ds_dich)):
                        if i == 0:
                            text = "1_"+str(self.ds_dich[0][0])+"_"+str(self.ds_dich[0][1])
                        else:
                            text = text + ",2_"+str(self.ds_dich[1][0])+"_"+str(self.ds_dich[1][1])
                    self.window.text_in_entry("toa_do_dich",text)
            if self.chon_duong_di == 1:
                if x >=0 and y >= 0:
                    self.ds_duong_di.append([x,y])
                    if len(self.ds_duong_di) > 0:
                        self.text_duong_di = "1_" + str(self.ds_duong_di[0][0]) +"_" +str(self.ds_duong_di[0][1])
                        for i in range(1,len(self.ds_duong_di)):
                            self.text_duong_di = self.text_duong_di + "," + str(i+1) + "_" + str(self.ds_duong_di[i][0]) + "_" + str(self.ds_duong_di[i][1])
                    self.window.text_in_entry("ds_toa_do",self.text_duong_di)
        self.text_duong_di_new = self.window.value("ds_toa_do")
        list_duong_di = self.text_duong_di_new.split(",")
        update_toa_do = 0
        self.ds_duong_di_new = []
        for i in range(0,len(list_duong_di)):
            list_toa_do = list_duong_di[i].split("_")
            if len(list_toa_do) >= 3:
                x = int(float(list_toa_do[1]))
                y = int(float(list_toa_do[2]))
                if x != self.ds_duong_di[i][0] or y != self.ds_duong_di[i][1]:
                    update_toa_do = 1
                self.ds_duong_di_new.append([x,y])
        if update_toa_do == 1:
            self.ds_duong_di = self.ds_duong_di_new
        
        self.text_dich_new = self.window.value("toa_do_dich")
        list_dich = self.text_dich_new.split(",")
        update_dich = 0
        self.ds_dich_new = []
        for i in range(0,len(list_dich)):
            list_dich_2 = list_dich[i].split("_")
            if len(list_dich_2) >= 3:
                x = int(float(list_dich_2[1]))
                y = int(float(list_dich_2[2]))
                if x != self.ds_dich[i][0] or y != self.ds_dich[i][1]:
                    update_dich = 1
                self.ds_dich_new.append([x,y])
        if update_dich == 1:
            self.ds_dich = self.ds_dich_new

    def update_img_frame(self,name_frame,name_img,name_label,img_input,w_goc=0,h_goc=0,const_w=0,const_h=0):
        if w_goc != 0 and h_goc != 0:
            w_img_1,h_img_1 = self.window.w_h_label(name_frame)
            if w_goc/h_goc > w_img_1/h_img_1:
                h_img_1 = int(int(w_img_1)*h_goc/w_goc)
            else:
                w_img_1 = int(int(h_img_1)*w_goc/h_goc)
            img = convert.img_resize_vid(img_input,w_img_1,h_img_1)
            self.window.label_img(str(name_img),str(name_label),img)
        if const_w != 0 and const_h != 0:
            w_img_1 = const_w
            h_img_1 = const_h
            img = convert.img_resize_vid(img_input,w_img_1,h_img_1)
            self.window.label_img(str(name_img),str(name_label),img)
        return w_img_1,h_img_1

    def load_input_8(self):
        self.input_8 = ket_noi_esp.input_8
        if self.input_8 == 1:
            angle,load_angle = self.load_angle_esp()
            if load_angle == 1:
                self.window.text_in_button("save_angle_0",text="goc = 0")
        else:
            angle,load_angle = self.load_angle_esp()
            if load_angle == 1:
                self.window.text_in_button("save_angle_0",text="goc != 0: " + str(int(angle*100)/100))

    def check_button(self):
        reset = 0
        if sent_data_main() == "reset_duong_di":
            reset = 1
            self.run = 0
            self.ds_duong_di = []
            self.ds_dich = []
            self.upload_run = 0
            self.ds_duong_di_dich = []
            self.chon_dich = 0
            self.chon_duong_di = 0
            self.window.text_in_button("chon_duong_di","Chọn đường đi","white")
            self.window.text_in_button("chon_dich","Chọn đích đến","white")
            self.window.text_in_button("run","Run","white")
            self.window.text_in_entry("ds_toa_do","")
            self.window.text_in_entry("toa_do_dich","")
            self.done = 0
            self.trang_thai_tien_lui = "tien"
            self.trang_thai_lui_trai = 0
            self.trang_thai_lui_phai = 0
            self.trang_thai_tien_trai = 0
            self.trang_thai_tien_phai = 0
            self.trang_thai_goc = 0
            self.end_point = [0,0]
        if sent_data_main() == "new_start_point":
            reset = 1
            if self.new_start_point == 0:
                self.new_start_point = 1
                self.window.text_in_button("new_start_point",color="yellow")
            else:
                self.new_start_point = 0
                self.window.text_in_button("new_start_point",color="white")
        if sent_data_main() == "save_angle_0":
            reset = 1
            angle,load_angle = ket_noi_esp.load_data_angle()
            if load_angle == 1:
                self.window.text_in_button("save_angle_0",color="white")
                self.ang_plc = 1
        if sent_data_main() == "save_map_edit":
            reset = 1
            if os.path.exists(self.window.value("link_en_1")) == True:
                link = self.window.value("link_en_1")
                print(link)
                edit_csv_tab.new_csv_replace(link,["0\t0\t0\t1\t2\t3\t4\t5"])
                edit_csv_tab.append_csv(link,["0\twindow_size_x\t"+str(self.window_size_x)])
                edit_csv_tab.append_csv(link,["0\twindow_size_y\t"+str(self.window_size_y)])
                edit_csv_tab.append_csv(link,["0\tscaling_factor\t"+str(self.scaling_factor)])
                # scaling_factor
                for i in range(0,len(self.edit_x)):
                    edit_csv_tab.append_csv(link,["4" + "\tdata\t" + str(int(self.edit_x[i])) + "\t" + str(int(self.edit_y[i]))])

        if sent_data_main() == "add_map":
            reset = 1
            if self.them_map == 0:
                self.them_map = 1
                self.window.text_in_button("add_map","Thêm map","yellow")
                self.window.text_in_button("del_map","Xóa map","white")
                self.xoa_map = 0
                time_0,time_1 = time_now()
                np.save(path_map_test_icp + "/" + str(time_1) + ".npy",self.scan)
            else:
                self.them_map = 0
                self.window.text_in_button("add_map","Thêm map","white")
        if sent_data_main() == "del_map":
            reset = 1
            if self.xoa_map == 0:
                self.xoa_map = 1
                self.window.text_in_button("del_map","Xóa map","yellow")
                self.window.text_in_button("add_map","Thêm map","white")
                self.them_map = 0
            else:
                self.xoa_map = 0
                self.window.text_in_button("del_map","Xóa map","white")

        if sent_data_main() == "run":
            reset = 1
            if self.run == 0:
                self.run = 1
                self.upload_run = 1
                self.window.text_in_button("run","Stop","red")
                self.chon_duong_di = 0
                self.window.text_in_button("chon_duong_di","Chọn đường đi","white")
                self.chon_dich = 0
                self.window.text_in_button("chon_dich","Chọn đích đến","white")

                
                
            else:
                self.run = 0
                self.window.text_in_button("run","Run","white")
                data = self.plc.sent_data("stop_agv")
                data = self.plc.sent_data("stop_agv")
        if sent_data_main() == "chon_duong_di":
            reset = 1
            if self.run == 0:
                if self.chon_duong_di == 0:
                    self.chon_duong_di = 1
                    self.window.text_in_button("chon_duong_di","Chọn đường đi","yellow")
                    self.chon_dich = 0
                    self.window.text_in_button("chon_dich","Chọn đích đến","white")
                else:
                    self.chon_duong_di = 0
                    self.window.text_in_button("chon_duong_di","Chọn đường đi","white")
        if sent_data_main() == "chon_dich":
            reset = 1
            if self.run == 0:
                if self.chon_dich == 0:
                    self.chon_dich = 1
                    self.window.text_in_button("chon_dich","Chọn đích đến","yellow")
                    self.chon_duong_di = 0
                    self.window.text_in_button("chon_duong_di","Chọn đường đi","white")
                else:
                    self.chon_dich = 0
                    self.window.text_in_button("chon_dich","Chọn đích đến","white")
        if sent_data_main() == "ba_cham_1":
            reset = 1
            link_file = load_link_csv()
            self.window.text_in_entry("link_en_1",link_file)
        if sent_data_main() == "ba_cham_map1":
            reset = 1
            link_folder = load_folder()
            self.window.text_in_entry("link_en_map1",link_folder)
        if sent_data_main() == "phai":
            reset = 1
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2:
                data = self.plc.sent_data("tien",vt_trai = "500",vt_phai = "0")
        if sent_data_main() == "trai":
            reset = 1
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2:
                data = self.plc.sent_data("tien",vt_trai = "0",vt_phai = "500")
        if sent_data_main() == "lui":
            reset = 1
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2:
                data = self.plc.sent_data("lui",vt_trai = "1000",vt_phai = "1000")
        if sent_data_main() == "tien":
            reset = 1
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2:
                data = self.plc.sent_data("tien",vt_trai = "1000",vt_phai = "1000")
        if sent_data_main() == "stop_agv":
            reset = 1
            if self.connect_plc == 1 and self.window.get_radio_check_button("variable_1") == 2:
                data = self.plc.sent_data("stop_agv")
        if sent_data_main() == "save_new_point":
            reset = 1
            self.new_map = 1
        if sent_data_main() == "reset_lidar":
            reset = 1
            self.window.text_in_entry("ds_toa_do","")
            self.window.text_in_entry("toa_do_dich","")
            self.reset_lidar()
        if sent_data_main() == "save_map":
            reset = 1
            self.save_map_lidar()
            # cv2.imwrite("map.png",self.detect_lidar.map_all)
            # np.save("arr_goc",self.detect_lidar.arr_goc0)
        if sent_data_main() == "connect_plc":
            reset = 1
            if self.window.value("link_en_2") != "" and self.window.value("link_en_3") != "":
                if self.connect_plc == 0:
                    self.connect_plc = 1
                    self.window.text_in_button("connect_plc","Disconnect PLC")
                    if self.window.value("link_en_2") != self.address or self.window.value("link_en_3") != self.port:
                        self.address = self.window.value("link_en_2")
                        self.port = int(self.window.value("link_en_3"))
                        edit_csv_tab.edit_csv(path_setting_plc,0,0,self.port)
                        edit_csv_tab.edit_csv(path_setting_plc,1,0,self.port)  
                    self.plc = connect_plc.sent_data_plc(self.address,self.port)
                else:
                    self.connect_plc = 0
                    self.window.text_in_button("connect_plc","Connect PLC")
            else:
                self.error = 1
                self.name_error = "Chưa chọn address và port cho PLC"
        if sent_data_main() == "connect_lidar":
            reset = 1
            if self.window.value("ds_com") != "" and self.window.value("ds_bau") != "":
                if self.connect_lidar == 0:
                    self.connect_lidar = 1
                    self.window.text_in_button("connect_lidar","Disconnect lidar")
                    if self.window.value("ds_com") != self.com_lidar or self.window.value("ds_bau") != self.bau_lidar:
                        self.com_lidar = self.window.value("ds_com")
                        self.bau_lidar = int(self.window.value("ds_bau")) 
                    threading.Thread(target=lambda: main_lidar(self.com_lidar ,self.bau_lidar)).start()
                else:
                    self.connect_lidar = 0
                    self.window.text_in_button("connect_lidar","Connect lidar")
                    disconnect_lidar()
            else:
                self.error = 1
                self.name_error = "Chưa chọn cổng com hoặc baudrate"
        if sent_data_main() == "update":
            reset = 1
            self.update_giao_dien = 1
            self.close_all()
        if sent_data_main() == "close_window":
            if os.path.exists(self.link3 + "/close_window") == True:
                shutil.copy(path_phan_mem + "/close.csv",self.link3 + "/close_window" + "/close.csv")
            reset = 1
            self.connect_window = False
        self.window.update(self.name_window)
        if reset == 1:
            reset_data()
    def close_all(self):
        ket_noi_esp.disconnect_esp()
        disconnect_lidar()
        remove.remove_all_file_in_folder(path_list_window)
        self.window.khai_bao_list_window()
        
    
                
                
            