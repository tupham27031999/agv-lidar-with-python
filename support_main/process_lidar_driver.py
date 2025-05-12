import numpy as np
import cv2, threading, time, math, shutil, os
from support_main.lib_main import edit_csv_tab, remove
from support_main import gicp_lidar, tim_duong_di, connect_driver, music, edit_file_json
import path, A_star
import crop_img_Atar
import webserver
# import ket_noi_esp
# import move_controller


def edit_path(input):
    output = ""
    for i in input:
        if i == "\\":
            output = output + "/"
        else:
            output = output + i
    return output

path_phan_mem = path.path_phan_mem

distan_scan_all = [0, 10000]
dis_min = 0
dis_max = 2000
anpha_scan = [130,200]
anpha_scan_an_toan_tien = [0,70,280,360]
anpha_scan_an_toan_re_phai = [50, 130, 50, 130]
anpha_scan_an_toan_re_trai =[200, 300, 200, 300]
path_admin = path_phan_mem + "/setting/admin_window.csv"
if os.name == "nt":
    print("Hệ điều hành là Windows")
    # Đọc file cài đặt cho Windows
    path_admin = path_phan_mem + "/setting/admin_window.csv"
    on_music = 1
elif os.name == "posix":
    print("Hệ điều hành là Ubuntu (Linux)")
    # Đọc file cài đặt cho Ubuntu
    path_admin = path_phan_mem + "/setting/admin_ubuntu.csv"
    on_music = 0
data_admin = edit_csv_tab.load_all_stt(path_admin)

for i in range(0,len(data_admin)):
    if len(data_admin[i]) > 1:
        if data_admin[i][0] == "khoang_cach_duong_di":
            khoang_cach_duong_di = int(float(data_admin[i][1]))
        if data_admin[i][0] == "khoang_cach_dich":
            khoang_cach_dich = int(float(data_admin[i][1]))
        if data_admin[i][0] == "anpha_scan_an_toan_tien":
            anpha_scan_an_toan_tien = [int(float(data_admin[i][1])), int(float(data_admin[i][2])),int(float(data_admin[i][3])), int(float(data_admin[i][4]))] 
        if data_admin[i][0] == "anpha_scan_an_toan_re_trai":
            anpha_scan_an_toan_re_trai = [int(float(data_admin[i][1])), int(float(data_admin[i][2])),int(float(data_admin[i][3])), int(float(data_admin[i][4]))] 
        if data_admin[i][0] == "anpha_scan_an_toan_re_phai":
            anpha_scan_an_toan_re_phai = [int(float(data_admin[i][1])), int(float(data_admin[i][2])),int(float(data_admin[i][3])), int(float(data_admin[i][4]))] 
        if data_admin[i][0] == "anpha_scan":
            anpha_scan = [int(float(data_admin[i][1])), int(float(data_admin[i][2]))] 
        if data_admin[i][0] == "khoang_canh_an_toan_tien":
            khoang_canh_an_toan_tien = [int(float(data_admin[i][1])), int(float(data_admin[i][2]))] 
        if data_admin[i][0] == "khoang_cach_tim_duoi_di":
            khoang_cach_tim_duoi_di = [int(float(data_admin[i][1])), int(float(data_admin[i][2]))] 
        if data_admin[i][0] == "khoang_cach_an_toan_lui":
            khoang_cach_an_toan_lui = int(float(data_admin[i][1]))
        if data_admin[i][0] == "alpha_star_scan_trai":
            alpha_star_scan_trai = [int(float(data_admin[i][1])), int(float(data_admin[i][2])),int(float(data_admin[i][3])), int(float(data_admin[i][4]))] 
        if data_admin[i][0] == "alpha_star_scan_phai":
            alpha_star_scan_phai = [int(float(data_admin[i][1])), int(float(data_admin[i][2])),int(float(data_admin[i][3])), int(float(data_admin[i][4]))] 
        if data_admin[i][0] == "khoang_cach_astar_scan":
            khoang_cach_astar_scan = int(float(data_admin[i][1]))
        if data_admin[i][0] == "distan_scan_all":
            distan_scan_all = [int(float(data_admin[i][1])), int(float(data_admin[i][2]))] 
        if data_admin[i][0] == "dis_min":
            dis_min = int(float(data_admin[i][1]))
        if data_admin[i][0] == "dis_max":
            dis_max = int(float(data_admin[i][1]))
print("distan_scan_all", distan_scan_all, "dis_min", dis_min, "dis_max", dis_max)
print(khoang_canh_an_toan_tien,khoang_cach_tim_duoi_di,khoang_cach_an_toan_lui)

print(anpha_scan, anpha_scan_an_toan_tien, anpha_scan_an_toan_re_trai, anpha_scan_an_toan_re_phai)
# Khởi tạo pygame mixer

def calculate_distance_and_angle(A, B, C, distan_can_vat_can_0,distan_can_vat_can_1,distan_can_vat_can_2, beta=90):
    output_0 = "OK"
    output_1 = "OK"
    output_2 = "OK"
    alpha_check_0 = math.atan(distan_can_vat_can_0[0]/distan_can_vat_can_0[1])*180/np.pi
    alpha_check_1 = math.atan(distan_can_vat_can_1[0]/distan_can_vat_can_1[1])*180/np.pi
    alpha_check_2 = math.atan(distan_can_vat_can_2[0]/distan_can_vat_can_2[1])*180/np.pi
    distance = 0
    # Tính vector AB và AC
    AB = np.array([B[0] - A[0], B[1] - A[1]])
    AC = np.array([C[0] - A[0], C[1] - A[1]])

    # Tính độ dài của vector AB và AC
    AB_length = np.linalg.norm(AB)
    AC_length = np.linalg.norm(AC)

    if A != B and A != C and B != C and C != [0,0]:
        # Tính góc alpha giữa AB và AC
        cos_alpha = np.dot(AB, AC) / (AB_length * AC_length)
        alpha = np.arccos(cos_alpha) * 180 / np.pi  # Chuyển đổi từ radian sang độ

        if abs(alpha) < abs(alpha_check_0):
            distance_check_0 = distan_can_vat_can_0[1]/np.cos(alpha*np.pi/180)
        else:
            distance_check_0 = distan_can_vat_can_0[0]/np.sin(alpha*np.pi/180)
        if abs(alpha) < abs(alpha_check_1):
            distance_check_1 = distan_can_vat_can_1[1]/np.cos(alpha*np.pi/180)
        else:
            distance_check_1 = distan_can_vat_can_1[0]/np.sin(alpha*np.pi/180)
        if abs(alpha) < abs(alpha_check_2):
            distance_check_2 = distan_can_vat_can_2[1]/np.cos(alpha*np.pi/180)
        else:
            distance_check_2 = distan_can_vat_can_2[0]/np.sin(alpha*np.pi/180)

        # print(distance_check_0, distance_check_1, distance_check_2, alpha_check_0,alpha_check_1, alpha_check_2, "------------")
        # Kiểm tra góc alpha có nằm trong dải [-55, 55] hay không
        if -beta <= alpha <= beta:
            # Tính khoảng cách AB * cos(alpha)
            distance = AB_length
            if abs(distance) < abs(distance_check_0):
                output_0 = "NG"
            if abs(distance) < abs(distance_check_1):
                output_1 = "NG"
            if abs(distance) < abs(distance_check_2):
                output_2 = "NG"
    return output_0,output_1,output_2
def callback_tien(x_goc, y_goc, px, py, distan_can_vat_can_0, distan_can_vat_can_1, distan_can_vat_can_2, huong_x, huong_y):
    A = [x_goc, y_goc]
    C = [huong_x,huong_y]
    point_vat_can_0 = []
    point_vat_can_1 = []
    point_vat_can_2 = []
    # print(distan_can_vat_can_0, distan_can_vat_can_1, distan_can_vat_can_2)
    for i in range(0, len(px)):
        B = [px[i], py[i]]
        kq_0,kq_1,kq_2 = calculate_distance_and_angle(A, B, C, distan_can_vat_can_0, distan_can_vat_can_1, distan_can_vat_can_2)
        if kq_0 == "NG":
            point_vat_can_0 = [px[i], py[i]]
        if kq_1 == "NG":
            point_vat_can_1 = [px[i], py[i]]
        if kq_2 == "NG":
            point_vat_can_2 = [px[i], py[i]]
    return point_vat_can_0, point_vat_can_1, point_vat_can_2
def callback_lui(x_goc, y_goc, px, py, distan_can_vat_can):
    min_dist = 1000
    closest_point = []
    point_vat_can = []
    for i in range(0, len(px)):
        dist = np.sqrt((px[i] - x_goc) ** 2 + (py[i] - y_goc) ** 2)
        if dist < min_dist:
            min_dist = dist
            closest_point = [px[i], py[i], min_dist, x_goc, y_goc]
    if len(closest_point) != 0:
        # Nếu khoảng cách nhỏ hơn 10 thì bật loa nói "có vật cản" trong một luồng riêng biệt
        if min_dist < distan_can_vat_can:
            point_vat_can = [closest_point[0], closest_point[1]]
    return point_vat_can
driver_motor_check = 1

class process_data_lidar:
    def __init__(self):
        if on_music == 1:
            threading.Thread(target=music.sound_speak).start()
        if driver_motor_check == 1:
            self.driver_motor = connect_driver.sent_data_driver()
        else:
            self.driver_motor = ""

        
        self.window_size_x = 400
        self.window_size_y = 400
        self.window_size_x_all = 1000
        self.window_size_y_all = 1000

        self.scaling_factor = 0.1

        self.scan = np.array([[0], [0], [0]])
        self.scan_an_toan_tien = np.array([[0], [0], [0]])
        self.scan_an_toan_re_trai = np.array([[0], [0], [0]])
        self.scan_an_toan_re_phai = np.array([[0], [0], [0]])
        self.arr_goc0 = np.array([])
        self.arr_goc = np.array([])

        self.rmse1 = 2
        self.rmse2 = 2
        self.rmse = 100
        self.stop_agv = 0
        self.rotation = 0

        self.x_goc = int(self.window_size_x_all/2)
        self.y_goc = int(self.window_size_x_all/2)
        self.x_goc_old = int(self.window_size_x_all/2)
        self.y_goc_old = int(self.window_size_x_all/2)
        self.vi_tri_x_agv, self.vi_tri_y_agv = self.translate_point(self.x_goc, self.y_goc, - self.rotation, distance = 15)
        
        
        self.update_vi_tri_agv_ban_dau = 1
        self.map_all = np.full((self.window_size_y_all, self.window_size_x_all, 4), (150, 150, 150, 0), np.uint8)
        self.map_all_px = []
        self.map_all_py = []
        self.img0 = np.ones((self.window_size_y, self.window_size_x, 4), np.uint8) * 150
        self.img1 = self.map_all.copy()
        self.window_size_img2 = 600
        self.number_img2 = int(self.window_size_img2/2)
        self.number_img3 = 20
        self.img2 = self.map_all.copy()[int(self.y_goc - self.number_img2):int(self.y_goc + self.number_img2),int(self.x_goc - self.number_img2):int(self.x_goc + self.number_img2),:]
        
        
        
        self.time_start = 0
        self.add_all_point = 1

        self.huong_x = 0
        self.huong_y = 0
        self.edit_img = self.map_all.copy()
        self.update_vi_tri_ok = 0

        self.update_vi_tri_agv = 0
        self.x_new_map = 0
        self.y_new_map = 0
        self.ang_new_map = 0
        
        self.reset_duong_di = 0

        self.dk_agv_thu_cong = 0

        # self.so_lan_lap = 0
        self.run_stop = "stop"

        self.data_run_agv0 = {"run_agv": 0,
                 "tien_max": 4000, "re_max": 1500, "grid_size": 5, "agv_size": 5, "loai_lap": "", "so_lan_lap": 0, "data_run": [],
                 "diem_1": {"point_name": "","point_coord": [0,0], "direction": "","alpha": ""}, 
                 "diem_2": {"point_name": "","point_coord": [0,0], "direction": "","alpha": ""},
                 "duong_di": {"ten_duong": "", "diem_1": "","diem_2": "","loai_duong": "", "C1": "", "C2": ""},
                 "tin_hieu": ["",""]}
        self.data_run_agv = self.data_run_agv0.copy()
        self.dict_data = {}
        self.convert_data_run_agv0 = {"tien_max": 2000, "re_max": 1000, "grid_size": 5, "agv_size": 5,
                        "diem_1": [], "diem_2": [], "diem_huong": [], "toa_do_agv": [], "diem_huong_agv": [], 
                        "run_diem_2": "NG", "run_huong": "NG"}
        self.convert_data_run_agv = self.convert_data_run_agv0.copy()
        self.done_sub = 0
        self.stt_sub = 0
        self.stt_sub_old = -1
        self.danh_sach_diem = webserver.danh_sach_diem
        self.danh_sach_duong = webserver.danh_sach_duong
        self.stt = 1
        self.point_old_tim_duong_di = []

        self.data_dk_ban_phim = ""

        # ktra vat can
        self.closest_point_0 = []
        self.closest_point_1 = []
        self.closest_point_2 = []

        self.trang_thai_tien_lui_an_toan = "tien"
        # self.trang_thai_tien_lui_an_toan = "re_phai"
        # self.trang_thai_tien_lui_an_toan = "re_trai"


        self.connect_driver = False
        self.trang_thai_agv = ""
        self.add_map = 0

        self.x_min_img2 = 0
        self.y_min_img2 = 0

        self.color_0 = [255, 255, 255]
        self.color_4 = [int(150 - 150*1.00),int(150 - 150*1.00),int(150 - 150*1.00)]

        self.connect_sound = True
        if self.connect_sound == False and on_music == 1:
            music.disconnect_sound()

        self.const_map_all = 0

        self.color_check = [0,0,0,255]
        self.color = [255,255,255,255]

        self.grid_size = int(float(webserver.data_cai_dat["grid_size"]))
        self.agv_size = int(float(webserver.data_cai_dat["agv_size"]))
        self.van_toc_max_tien = int(float(webserver.data_cai_dat["tien_max"]))
        self.van_toc_re_max = int(float(webserver.data_cai_dat["re_max"]))
        self.grid = np.zeros((self.map_all.shape[0] // self.grid_size, self.map_all.shape[1] // self.grid_size))

        self.img_controller = np.zeros((200,200,3),dtype=np.uint8)
        self.angle_controller = 90
        self.angle_camera = 90
        self.trang_thai_agv_controller = "none"
        self.v_controller = 0
        self.phan_tram_controller = 0

        self.auto_controller = 1
        self.delta_distan = 0
        self.delta_angle = 0

        self.star_trai = 0
        self.star_phai = 0
        self.star_scan_trai = np.array([[0], [0], [0]])
        self.star_scan_phai = np.array([[0], [0], [0]])
        self.point_star_scan = []
        self.point_start_star = []
        self.point_end_star = []
        self.point_new_star = []
        self.point_star_old = []
        self.point_star_new = []
        self.check_dis = 0
        self.stt_check_dis = 0
        self.list_point_star = []

        self.image_new = self.img2.copy()

        self.distance_old = 0
        self.check_distan_old = 0

        self.scan_dis = 0
        self.dis_min = dis_min
        self.dis_max = dis_max
        # try:
        #     pass
        #     threading.Thread(target=ket_noi_esp.python_esp32).start() ######`##################
        # except OSError as e:
        #     print("khong ket noi duoc esp")
        #     pass
        # self.input_esp = ket_noi_esp.input_esp
        self.input_esp = {"IN1":0,"IN2":0,"IN3":0,"IN4":0,"IN5":0,"IN6":0,"IN7":0,"IN8":0,"IN9":0,"IN10":0,"IN11":0,"IN12":0}
        
    def load_ds_di_dich_main(self,ds_diem,stt_main):
        ds_dich = []
        ds_duong_di = []
        for i in range(0,len(ds_diem)):
            if i >= (stt_main + 2):
                if ds_diem[i][0] != "diem_dich_1":
                    if i >= (stt_main + 2): # them diem thuong
                        ds_duong_di.append([ds_diem[i][1],ds_diem[i][2]])
                else:
                    if i == len(ds_diem) - 2: # den dem cuoi
                        stt_main = 0
                    else:
                        stt_main = i
                    ds_duong_di.append([ds_diem[i][1],ds_diem[i][2]])
                    ds_dich = [[ds_diem[i][1],ds_diem[i][2]],[ds_diem[i+1][1],ds_diem[i+1][2]]]
                    break
        return ds_dich,ds_duong_di,stt_main
    #################################################################################################################################################################
    #################################################################################################################################################################
    ###########################################################          main_loop         ##########################################################################
    #################################################################################################################################################################
    #################################################################################################################################################################
    def main_loop(self):
        self.input_esp = webserver.input_esp
        if self.auto_controller == 1 and driver_motor_check == 1:
            if self.driver_motor.quay_trai == 1:
                self.trang_thai_tien_lui_an_toan = "re_trai"
            if self.driver_motor.quay_phai == 1:
                self.trang_thai_tien_lui_an_toan = "re_phai"
            if self.driver_motor.quay_trai == 0 and self.driver_motor.quay_phai == 0:
                self.trang_thai_tien_lui_an_toan = "tien"
            if self.run_stop == "run" and self.rmse <= 4 and len(self.closest_point_0) == 0 and self.stop_agv == 0:
                print("run")
                if len(self.dict_data) == 0:
                    if webserver.data_text_box != "":
                        self.dict_data = edit_file_json.tach_du_lieu_dau_vao(webserver.data_text_box)
                self.run_agv()
            else:
                if on_music == 1:
                    if music.name_music != "co_vat_can":
                        music.name_music = "none"
                # print(int(float(self.convert_data_run_agv["tien_max"])), 0, 0, "distance", 1, self.closest_point_1)
                self.driver_motor.load_data_sent_drive(int(float(self.convert_data_run_agv["tien_max"])), 0, 0, "distance", 1, self.closest_point_1)
                # print(self.ds_diem, self.ds_dich_main, self.ds_duong_di_main)
        # else:
        #     # if self.run == 1:
        #     self.img_controller, angle, trang_thai_agv, v, phan_tram_controller = self.controller.detect(v0 = 1000)
        #     if abs(angle) >= 4:
        #         self.angle_controller = self.angle_camera - angle
        #     if self.angle_controller > 180:
        #         self.angle_controller = 180
        #     if self.angle_controller < 0:
        #         self.angle_controller = 0
        #     v_tien = v
        #     v_lui = 1000
        #     stop = 0
        #     chuyen_trang_thai = False
        #     if trang_thai_agv != "tien" or len(self.closest_point_0) != 0:
        #         chuyen_trang_thai = True
        #         stop = 1
        #     # print(v, angle, trang_thai_agv, phan_tram_controller,self.angle_controller)
        #     self.driver_motor.load_data_sent_plc(v_tien, v_lui, trang_thai_agv, distance = 200, angle = (self.angle_controller-90), 
        #                                 goc_banh_xe = self.goc_banh_xe, chuyen_trang_thai=chuyen_trang_thai,
        #                                 check_angle_distance = "none", stop = stop, check_an_toan = self.closest_point_1)
            
        if driver_motor_check == 1:
            self.driver_motor.connect_driver()
            if self.driver_motor.connect == True:
                self.connect_driver = True
            else:
                self.connect_driver = False
            self.trang_thai_agv = self.driver_motor.return_data()
        
        
        self.dk_ban_phim(self.data_dk_ban_phim)
        self.reset_duong_di_chuyen()
        # self.load_input_8()
        # self.load_goc_agv()
        self.agv_to_pc()
    def create_map(self, px, py, window_size_x_all, window_size_y_all):
        x_goc = int(window_size_x_all/2)
        y_goc = int(window_size_y_all/2)
        self.delta_distan = 0
        self.delta_angle = 0
        for i in range(0, px.shape[0]):
            # self.bresenham_line(self.map_all, int(self.x_goc), int(self.y_goc), 
            #                                 int(px[i]), int(py[i]), 
            #                                 50, color=self.color, color_check = self.color_check)
            cv2.line(self.map_all, (int(self.x_goc), int(self.y_goc)), (int(px[i]), int(py[i])), [255,255,255], 1)
            self.map_all[int(py[i]), int(px[i]),:] = self.color_check
            # grid_x = int(px[i] // self.grid_size)
            # grid_y = int(py[i] // self.grid_size)
            # self.grid[grid_y, grid_x] = 1
        h, w, _ = self.img0.shape
        self.img0 = self.map_all[int(self.y_goc - h/2):int(self.y_goc + h/2),
                                int(self.x_goc - w / 2):int(self.x_goc + w / 2), :]
        black_points = np.argwhere(np.all(self.img0[:, :, :3] == [0, 0, 0], axis=-1))
        px = black_points[:, 1]
        py = black_points[:, 0]
        px = px + x_goc - int(self.window_size_x / 2)
        py = py + y_goc - int(self.window_size_y / 2)
        px = np.append(px, np.array([int(x_goc)]))
        py = np.append(py, np.array([int(y_goc)]))
        arr_goc = np.vstack((px, py, np.zeros_like(px))).T  # Thêm chiều z = 0 để tạo PointCloud 3D
        return arr_goc

    def setting_data(self, window_size_x=400, window_size_y=400, window_size_x_all=2000, window_size_y_all=2000, scaling_factor=0.03, rmse1=4, rmse2=2):
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        self.window_size_x_all = window_size_x_all
        self.window_size_y_all = window_size_y_all
        self.scaling_factor = scaling_factor
        self.map_all = np.full((self.window_size_y_all, self.window_size_x_all, 4), (150, 150, 150, 0), np.uint8)
        # self.map_all_array = np.full((self.window_size_x_all, self.window_size_x_all, 4), (150, 150, 150, 0))
        # self.stt_map_all = 0
        # self.px_check = []
        # self.py_check = []
        # self.points_check = []
        self.img0 = np.ones((self.window_size_y, self.window_size_x, 3), np.uint8) *150
        self.img1 = self.map_all.copy()
        # self.grid = np.zeros((self.map_all.shape[0] // self.grid_size, self.map_all.shape[1] // self.grid_size))
        self.rmse1 = rmse1
        self.rmse2 = rmse2
        self.x_goc = int(self.window_size_x_all / 2)
        self.y_goc = int(self.window_size_y_all / 2)
        return int(self.window_size_x / 2), int(self.window_size_y / 2)

    def edit_points(self, image, angle, x, y):
        edit_img = image.copy()
        if x != 0 and y != 0:
            px = np.array(np.cos(self.scan[:, 1] / 180 * math.pi - angle / 180 * math.pi) * self.scan[:, 2] * self.scaling_factor + x)
            py = np.array(np.sin(self.scan[:, 1] / 180 * math.pi - angle / 180 * math.pi) * self.scan[:, 2] * self.scaling_factor + y)
            for i in range(0, px.shape[0]):
                cv2.circle(edit_img, (int(px[i]), int(py[i])), 1, (255, 0, 255), -1)
        return edit_img
    
    def translate_point(self, x, y, alpha, distance=5):
        """
        Dịch chuyển điểm (x, y) theo góc alpha và khoảng cách distance.
        
        Args:
            x (float): Tọa độ x của điểm đầu vào.
            y (float): Tọa độ y của điểm đầu vào.
            alpha (float): Góc alpha (đơn vị: radians).
            distance (float): Khoảng cách dịch chuyển (mặc định: 5 pixel).
        
        Returns:
            tuple: Tọa độ điểm mới (x_new, y_new).
        """
        x_new = x + distance * math.cos(alpha)
        y_new = y + distance * math.sin(alpha)
        return x_new, y_new
    
    #################################################################################################################################################################
    #################################################################################################################################################################
    ###########################################################          process_data_lidar         #################################################################
    #################################################################################################################################################################
    #################################################################################################################################################################

    def process_data_lidar(self, scan):
        x=self.x_new_map
        y= self.y_new_map
        angle=self.ang_new_map
        if int(float(distan_scan_all[1])) == 1:
            scan_all = scan[(scan[:, 2] < int(float(distan_scan_all[0])))]
        else:
            scan_all = scan
        if self.scan_dis == 1:
            # scan_all = scan[((scan[:, 1] < anpha_scan[0]) | (scan[:, 1] > anpha_scan[1])) & (scan[:, 2] > 700)  & (scan[:, 2] < 15000)]
            scan_all = scan[(scan[:, 2] > self.dis_min)  & (scan[:, 2] < self.dis_max)]

        self.scan_an_toan_tien = scan[(((scan[:, 1] >= anpha_scan_an_toan_tien[0]) & (scan[:, 1] <= anpha_scan_an_toan_tien[1])) | \
                                    ((scan[:, 1] >= anpha_scan_an_toan_tien[2]) & (scan[:, 1] <= anpha_scan_an_toan_tien[3]))) & \
                                        (scan[:, 2] < 1500)]
        self.scan_an_toan_re_trai = scan[(((scan[:, 1] > anpha_scan_an_toan_re_trai[0]) & (scan[:, 1] < anpha_scan_an_toan_re_trai[1])) | \
                                    ((scan[:, 1] > anpha_scan_an_toan_re_trai[2]) & (scan[:, 1] < anpha_scan_an_toan_re_trai[3]))) & \
                                       (scan[:, 2] < 500)]
        self.scan_an_toan_re_phai = scan[(((scan[:, 1] > anpha_scan_an_toan_re_phai[0]) & (scan[:, 1] < anpha_scan_an_toan_re_phai[1])) | \
                                    ((scan[:, 1] > anpha_scan_an_toan_re_phai[2]) & (scan[:, 1] < anpha_scan_an_toan_re_phai[3]))) & \
                                        (scan[:, 2] < 500)]
        
        if self.star_trai == 1:
            self.star_scan_trai = scan[(((scan[:, 1] > alpha_star_scan_trai[0]) & (scan[:, 1] < alpha_star_scan_trai[1])) | \
                                    ((scan[:, 1] > alpha_star_scan_trai[2]) & (scan[:, 1] < alpha_star_scan_trai[3]))) & \
                                       (scan[:, 2] < 1500)]
        if self.star_phai == 1:
            self.star_scan_phai = scan[(((scan[:, 1] > alpha_star_scan_phai[0]) & (scan[:, 1] < alpha_star_scan_phai[1])) | \
                                    ((scan[:, 1] > alpha_star_scan_phai[2]) & (scan[:, 1] < alpha_star_scan_phai[3]))) & \
                                       (scan[:, 2] < 1500)]

        self.scan = scan_all
        if self.scan.shape[1] != 1:
            if self.time_start == 0:
                self.time_start = time.time()
            self.img1 = self.map_all.copy()
            
            # dung ban do cu va cap nhat vi tri agv 
            if self.update_vi_tri_agv == 1:
                self.x_goc = x
                self.y_goc = y
                self.rotation = angle * np.pi / 180
                self.edit_img = self.edit_points(self.map_all.copy(), angle, x, y)
                self.update_vi_tri_ok = 1
                self.img1 = self.edit_img.copy()
                # self.update_vi_tri_agv = 0
            else:
                if self.update_vi_tri_ok == 1:
                    self.update_vi_tri_ok = 0
                    self.delta_distan = 0
                    self.delta_angle = 0
                    self.x_goc = x
                    self.y_goc = y
                    self.rotation = angle * np.pi / 180
                    self.update_vi_tri_agv_ban_dau = 0

                    h, w, _ = self.img0.shape
                    self.img0 = self.map_all[int(self.y_goc - h/2):int(self.y_goc + h/2),
                                int(self.x_goc - w / 2):int(self.x_goc + w / 2), :]
                    black_points = np.argwhere(np.all(self.img0[:, :, :3] == [0, 0, 0], axis=-1))
                    px = black_points[:, 1]
                    py = black_points[:, 0]

                    px = px + self.x_goc - int(self.window_size_x/2)
                    py = py + self.y_goc - int(self.window_size_y/2)

                    x_goc = self.arr_goc0[-1, 0]
                    y_goc = self.arr_goc0[-1, 1]
                    px = np.append(px, np.array([int(x_goc)]))
                    py = np.append(py, np.array([int(y_goc)]))
                    self.arr_goc0 = np.vstack((px, py, np.zeros_like(px))).T  # Thêm chiều z = 0 để tạo PointCloud 3D

                
                
                px_0 = np.array(np.cos(self.scan[:, 1] / 180 * math.pi - self.rotation) * self.scan[:, 2] * self.scaling_factor + self.x_goc)
                py_0 = np.array(np.sin(self.scan[:, 1] / 180 * math.pi - self.rotation) * self.scan[:, 2] * self.scaling_factor + self.y_goc)

                # px_0 = np.array(np.cos(self.scan[:, 0] / 180 * math.pi - self.rotation) * self.scan[:, 1] * self.scaling_factor + self.x_goc)
                # py_0 = np.array(np.sin(self.scan[:, 0] / 180 * math.pi - self.rotation) * self.scan[:, 1] * self.scaling_factor + self.y_goc)

                mask0 = (px_0 > 0) & (px_0 < self.window_size_x_all) & (py_0 > 0) & (py_0 < self.window_size_y_all)
                px0 = px_0[mask0]
                py0 = py_0[mask0]

                px_0_tien = np.array(np.cos(self.scan_an_toan_tien[:, 1] / 180 * math.pi - self.rotation) * self.scan_an_toan_tien[:, 2] * self.scaling_factor + self.x_goc)
                py_0_tien = np.array(np.sin(self.scan_an_toan_tien[:, 1] / 180 * math.pi - self.rotation) * self.scan_an_toan_tien[:, 2] * self.scaling_factor + self.y_goc)
                mask0_tien = (px_0_tien > 0) & (px_0_tien < self.window_size_x_all) & (py_0_tien > 0) & (py_0_tien < self.window_size_y_all)
                px0_tien = px_0_tien[mask0_tien]
                py0_tien = py_0_tien[mask0_tien]

                px_0_re_trai = np.array(np.cos(self.scan_an_toan_re_trai[:, 1] / 180 * math.pi - self.rotation) * self.scan_an_toan_re_trai[:, 2] * self.scaling_factor + self.x_goc)
                py_0_re_trai = np.array(np.sin(self.scan_an_toan_re_trai[:, 1] / 180 * math.pi - self.rotation) * self.scan_an_toan_re_trai[:, 2] * self.scaling_factor + self.y_goc)
                mask0_re_trai = (px_0_re_trai > 0) & (px_0_re_trai < self.window_size_x_all) & (py_0_re_trai > 0) & (py_0_re_trai < self.window_size_y_all)
                px0_re_trai = px_0_re_trai[mask0_re_trai]
                py0_re_trai = py_0_re_trai[mask0_re_trai]

                px_0_re_phai = np.array(np.cos(self.scan_an_toan_re_phai[:, 1] / 180 * math.pi - self.rotation) * self.scan_an_toan_re_phai[:, 2] * self.scaling_factor + self.x_goc)
                py_0_re_phai = np.array(np.sin(self.scan_an_toan_re_phai[:, 1] / 180 * math.pi - self.rotation) * self.scan_an_toan_re_phai[:, 2] * self.scaling_factor + self.y_goc)
                mask0_re_phai = (px_0_re_phai > 0) & (px_0_re_phai < self.window_size_x_all) & (py_0_re_phai > 0) & (py_0_re_phai < self.window_size_y_all)
                px0_re_phai = px_0_re_phai[mask0_re_phai]
                py0_re_phai = py_0_re_phai[mask0_re_phai]

                if self.star_trai == 1:
                    px_0_star_trai = np.array(np.cos(self.star_scan_trai[:, 1] / 180 * math.pi - self.rotation) * self.star_scan_trai[:, 2] * self.scaling_factor + self.x_goc)
                    py_0_star_trai = np.array(np.sin(self.star_scan_trai[:, 1] / 180 * math.pi - self.rotation) * self.star_scan_trai[:, 2] * self.scaling_factor + self.y_goc)
                    mask0_star_trai = (px_0_star_trai > 0) & (px_0_star_trai < self.window_size_x_all) & (py_0_star_trai > 0) & (py_0_star_trai < self.window_size_y_all)
                    px0_star_trai = px_0_star_trai[mask0_star_trai]
                    py0_star_trai = py_0_star_trai[mask0_star_trai]

                if self.star_phai == 1:
                    px_0_star_phai = np.array(np.cos(self.star_scan_phai[:, 1] / 180 * math.pi - self.rotation) * self.star_scan_phai[:, 2] * self.scaling_factor + self.x_goc)
                    py_0_star_phai = np.array(np.sin(self.star_scan_phai[:, 1] / 180 * math.pi - self.rotation) * self.star_scan_phai[:, 2] * self.scaling_factor + self.y_goc)
                    mask0_star_phai = (px_0_star_phai > 0) & (px_0_star_phai < self.window_size_x_all) & (py_0_star_phai > 0) & (py_0_star_phai < self.window_size_y_all)
                    px0_star_phai = px_0_star_phai[mask0_star_phai]
                    py0_star_phai = py_0_star_phai[mask0_star_phai]
                
                


                if self.trang_thai_tien_lui_an_toan == "tien":
                    self.closest_point_0, self.closest_point_1, self.closest_point_2 = callback_tien(self.x_goc, self.y_goc, 
                                                    px0_tien, py0_tien, khoang_canh_an_toan_tien,[khoang_cach_tim_duoi_di[0],khoang_cach_tim_duoi_di[1]+20],khoang_cach_tim_duoi_di,
                                                    self.huong_x,self.huong_y)
                if self.trang_thai_tien_lui_an_toan == "re_phai":
                    self.closest_point_0 = callback_lui(self.x_goc, self.y_goc, px0_re_phai, py0_re_phai, khoang_cach_an_toan_lui)
                    len(self.closest_point_0)
                if self.trang_thai_tien_lui_an_toan == "re_trai":
                    self.closest_point_0 = callback_lui(self.x_goc, self.y_goc, px0_re_trai, py0_re_trai, khoang_cach_an_toan_lui)

                if self.star_trai == 1:
                    self.point_star_scan = callback_lui(self.x_goc, self.y_goc, px0_star_trai, py0_star_trai, khoang_cach_astar_scan)
                if self.star_phai == 1:
                    self.point_star_scan = callback_lui(self.x_goc, self.y_goc, px0_star_phai, py0_star_phai, khoang_cach_astar_scan)
                if len(self.point_start_star) == 0:
                    self.star_trai = 0
                    self.star_phai = 0


                # print(len(self.point_star_scan))

                if on_music == 1:
                    if len(self.closest_point_0) != 0:
                        music.name_music = "co_vat_can"
                    else:
                        if music.name_music == "co_vat_can":
                            music.name_music = "none"
                if (self.update_vi_tri_agv_ban_dau == 1 and time.time() - self.time_start > 2):
                    if len(px0) > 60:  # map goc
                        self.rotation = 0
                        self.x_goc = int(self.window_size_x_all/2)
                        self.y_goc = int(self.window_size_y_all/2)
                        self.map_all = np.full((self.window_size_x_all, self.window_size_x_all, 4), (150, 150, 150, 0), np.uint8)
                        # self.map_all_array = np.full((self.window_size_x_all, self.window_size_x_all, 4), (150, 150, 150, 0))
                        # self.stt_map_all = 0
                        # self.px_check = []
                        # self.py_check = []
                        # self.points_check = []
                        self.img0 = np.ones((self.window_size_y, self.window_size_x, 3), np.uint8) * 150
                        self.img1 = self.map_all.copy()
                        # self.grid = np.zeros((self.map_all.shape[0] // self.grid_size, self.map_all.shape[1] // self.grid_size))
                        self.arr_goc0 = self.create_map(px0, py0, self.window_size_x_all, self.window_size_y_all)
                        # self.points_check = self.arr_goc0
                        self.arr_goc = self.arr_goc0
                        self.update_vi_tri_agv_ban_dau = 0
                        self.const_map_all = self.const_map_all + 1

                if self.update_vi_tri_agv_ban_dau == 0 and self.arr_goc0.shape[0] > 50:
                    h, w, _ = self.img0.shape
                    if self.scan_dis == 1:
                        h = int(h/2)
                        w = int(w/2)
                    # if self.add_all_point == 1:
                    self.img0 = self.map_all[int(self.y_goc - h/2):int(self.y_goc + h/2),
                                int(self.x_goc - w / 2):int(self.x_goc + w / 2), :]
                    black_points = np.argwhere(np.all(self.img0[:, :, :3] == [0, 0, 0], axis=-1))                       
                    px = black_points[:, 1]
                    py = black_points[:, 0] 
                    # else:
                    #     if self.load_map_lan_dau == 1:
                    #         self.black_points = np.argwhere(np.all(self.map_all[:, :, :3] == [0, 0, 0], axis=-1))
                    #         print("update black_points")
                    #     px, py = self.load_xy_map_all(self.black_points, int(self.x_goc - w / 2), int(self.y_goc - h/2), 
                                                                        # int(self.x_goc + w / 2), int(self.y_goc + h/2))

                    px = px + self.x_goc - int(self.window_size_x/2)
                    py = py + self.y_goc - int(self.window_size_y/2)

                    x_goc = self.arr_goc0[-1, 0]
                    y_goc = self.arr_goc0[-1, 1]
                    # px, py = self.KD_tree([px, py], 3, 3)
                    px = np.append(px, np.array([int(x_goc)]))
                    py = np.append(py, np.array([int(y_goc)]))
                    self.arr_goc0 = np.vstack((px, py, np.zeros_like(px))).T  # Thêm chiều z = 0 để tạo PointCloud 3D
                    
                    # ok3 3-5
                    # ok4 3-3
                    # px02, py02 = self.KD_tree([px0, py0], 3, 3)
                    # px02, py02 = self.filter_unreliable_points(px0, py0, 100)
                    # px02, py02 = self.KD_tree([px0, py0], 3, 3)
                    px02 = np.append(px0, np.array([int(self.x_goc)]))
                    py02 = np.append(py0, np.array([int(self.y_goc)]))
                    arr_test = np.vstack((px02, py02, np.zeros_like(px02))).T  # Thêm chiều z = 0 để tạo PointCloud 3D
                    
                    
                    rmse, r, t = gicp_lidar.gicp(arr_test, self.arr_goc0)
                    # rmse, r, t = NDT_lidar.fpfh_ransac_registration(arr_test, self.arr_goc0)

                    self.rmse = rmse
                    if rmse != 0:
                        
                        # chuyen arr_test ve vi tri self.arr_goc (test ngay lúc trc)
                        new_arr_ok = gicp_lidar.transform_points(arr_test, r, t) 
                        self.delta_distan = tim_duong_di.calculate_distance([self.x_goc, self.y_goc],[ new_arr_ok[-1,0], new_arr_ok[-1,1]])
                        self.delta_angle = int(abs(np.arcsin(r[0, 1])) * 180 / np.pi)
                        self.stop_agv = 0
                        # print(self.delta_distan, self.delta_angle)
                        if rmse < self.rmse1 and self.delta_distan < 50 and self.delta_angle <= 50:
                            
                            self.rotation = self.rotation + np.arcsin(r[0, 1])
                        
                            self.x_goc = new_arr_ok[-1,0]
                            self.y_goc = new_arr_ok[-1,1]
                            self.x_goc_old = self.x_goc
                            self.y_goc_old = self.y_goc
                        else:
                            if self.dk_agv_thu_cong == 0:
                                self.stop_agv = 1

                        h_img1,w_img1,_ = self.img1.shape
                        for ii in range(0, max(len(new_arr_ok), len(self.arr_goc[:, 0]), new_arr_ok.shape[0])):
                            # if ii < new_arr_ok.shape[0] - 1:
                            #     cv2.circle(self.img1, (int(new_arr_ok[ii, 0]), int(new_arr_ok[ii, 1])), 1, (0, 0, 255), -1)

                            if ii < len(new_arr_ok[:, 0]) - 1 and int(new_arr_ok[ii, 0]) < w_img1 and int(new_arr_ok[ii, 1]) < h_img1:
                                cv2.circle(self.img1, (int(new_arr_ok[ii, 0]), int(new_arr_ok[ii, 1])), 1, (255, 0, 255), -1)



                            if ii < len(new_arr_ok[:, 0]) - 1 and ii < len(new_arr_ok[:, 1]) - 1 and self.add_all_point == 1:
                                if (rmse < self.rmse2 or self.add_map == 1) and \
                                    int(new_arr_ok[ii, 1]) < self.window_size_y_all and int(new_arr_ok[ii, 1]) > 0 and \
                                    int(new_arr_ok[ii, 0]) < self.window_size_x_all and int(new_arr_ok[ii, 0]) > 0:

                                    
                                    if (self.map_all[int(new_arr_ok[ii, 1]), int(new_arr_ok[ii, 0]), :3].tolist() != self.color_0 or self.add_map == 1):
                                        
                                        if (self.map_all[int(new_arr_ok[ii, 1]), int(new_arr_ok[ii, 0]), :3].tolist() != self.color_4):
                                            # grid_x = int(new_arr_ok[ii, 0] // self.grid_size)
                                            # grid_y = int(new_arr_ok[ii, 1] // self.grid_size)
                                            # self.grid[grid_y, grid_x] = 1

                                            self.bresenham_line(self.map_all, int(self.x_goc), int(self.y_goc), 
                                                                int(new_arr_ok[ii, 0]), int(new_arr_ok[ii, 1]),  
                                                                30, color=self.color, color_check=self.color_check)
                                    else:
                                        self.bresenham_distan(self.map_all, int(self.x_goc), int(self.y_goc),
                                                            int(new_arr_ok[ii, 0]), int(new_arr_ok[ii, 1]),
                                                            4, color=self.color_check)
                                    # if self.map_all[int(new_arr_ok[ii, 1]), int(new_arr_ok[ii, 0]), :].tolist() == [255, 255, 255]:
                                    #     self.points_append_x = np.append(self.points_append_x, new_arr_ok[ii, 0])
                                    #     self.points_append_y = np.append(self.points_append_y, new_arr_ok[ii, 1])
                        self.add_map = 0
                        # if len(self.px_check) > 1000:
                        #     self.px_check = np.append(self.px_check, np.array([int(self.x_goc)]))
                        #     self.py_check = np.append(self.py_check, np.array([int(self.y_goc)]))
                        #     arr_test3 = np.vstack((self.px_check, self.py_check, np.zeros_like(self.px_check))).T
                        #     rmse3, r3, t3 = gicp_lidar.gicp(arr_test3, self.points_check)
                        #     new_arr_ok3 = gicp_lidar.transform_points(arr_test3, r, t) 

                        #     self.rotation = self.rotation + np.arcsin(r3[0, 1])
                        #     self.x_goc = new_arr_ok3[-1,0]
                        #     self.y_goc = new_arr_ok3[-1,1]
                        #     self.px_check = []
                        #     self.py_check = []
                        #     self.points_check = self.arr_goc0
                    self.vi_tri_x_agv, self.vi_tri_y_agv = self.translate_point(self.x_goc, self.y_goc, - self.rotation, distance=13)
                    cv2.circle(self.img1, (int(self.vi_tri_x_agv), int(self.vi_tri_y_agv)), 5, (255, 0, 0), -1)
                    self.huong_x = int(self.vi_tri_x_agv + 20 * math.cos(np.pi - self.rotation))
                    self.huong_y = int(self.vi_tri_y_agv + 20 * math.sin(np.pi - self.rotation))
                    cv2.arrowedLine(self.img1, (int(self.vi_tri_x_agv), int(self.vi_tri_y_agv)), (self.huong_x, self.huong_y), (255, 0, 0), 1, tipLength=0.2)
                    self.img2 = self.img1.copy()[int(self.y_goc - self.number_img2):int(self.y_goc + self.number_img2),int(self.x_goc - self.number_img2):int(self.x_goc + self.number_img2),:]
                    # self.x_min_img2 = int(self.x_goc - self.number_img2)
                    # self.y_min_img2 = int(self.y_goc - self.number_img2)
                    
    def find_matching_coordinate_fast(self, x, y, coordinates):
        coordinates_set = set(map(tuple, coordinates))
        return (x, y) in coordinates_set
    def find_opposite_point(self, x0, y0, x1, y1):
        x2 = 2 * x1 - x0
        y2 = 2 * y1 - y0
        return x2, y2
    def bresenham_distan(self,image, x0, y0, x1, y1, number, color = [0,0,0,255]):
        x_tg, y_tg = self.find_opposite_point(x0, y0, x1, y1)

        x0 = x1
        y0 = y1
        x1 = x_tg
        y1 = y_tg
        # kiem tra xem tu x0, y0 den x1, y1 co diem mau den nao trong khoang cach distan hay khong, co thi True, khong thi False
        xa = x0
        ya = y0
        
        dx = abs(x1 - xa)
        dy = abs(y1 - ya)
        sx = 1 if xa < x1 else -1
        sy = 1 if ya < y1 else -1
        err = dx - dy
        bien_dem = 0
        ok1 = False
        ok2 = True
        while True:
            if bien_dem <= number:
                if bien_dem <= int(number/2):
                    if ok1 == False:
                        if image[ya, xa, :].tolist() == color:
                            ok1 = True
                else:
                    if ok2 == True:
                        if image[ya, xa, :].tolist() == color:
                            ok2 = False
            else:
                if ok1 == True and ok2 == True:
                    image[y0, x0, :] = color
                    # grid_x = int(x0 // self.grid_size)
                    # grid_y = int(y0 // self.grid_size)
                    # self.grid[grid_y, grid_x] = 1
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                xa += sx
            if e2 < dx:
                err += dx
                ya += sy
            bien_dem = bien_dem + 1
    
    def bresenham_line(self, image, x0, y0, x1, y1, distan, color=[255, 255, 255, 255], color_check = [0, 0, 0, 255]):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        so_lan = 0
        start = 0
        bien_dem = 0
        point_check = []
        
        distan2 = tim_duong_di.calculate_distance([self.x_goc,self.y_goc],[x1,y1])
        
        while distan2 <= 170:

            if image[y0, x0, :].tolist() == color_check:
                start = 1
                point_check = [x0,y0]
                bien_dem = 0
                so_lan = so_lan + 1
            else:
                image[y0, x0, :] = color
            if start == 1:
                bien_dem = bien_dem + 1
            if bien_dem == 10:
                image[point_check[1], point_check[0], :] = color
                # grid_x = int(point_check[0] // self.grid_size)
                # grid_y = int(point_check[1] // self.grid_size)
                # self.grid[grid_y, grid_x] = 0
                point_check = 0

            if so_lan >= 2:
                break
            
            
            if x0 == x1 and y0 == y1:
                image[y1, x1, :] = color_check
                # grid_x = int(x0 // self.grid_size)
                # grid_y = int(y0 // self.grid_size)
                # self.grid[grid_y, grid_x] = 1
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy  
        return image
    def return_point(self,data):
        return [data[1],data[2]]
    def bresenham_line_grid(self, grid, x0, y0, x1, y1):
        output = True
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            if grid[y0, x0] == 1:
                output = False
                break
            if x0 == x1 and y0 == y1:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy  
        return output
    def check_grid(self,grid,points):
        output = True
        points_new = [self.x_goc,self.y_goc] + points
        for i in range(0,len(points_new)):
            output = self.bresenham_line_grid(grid, self.x_goc, self.y_goc, points_new[i][0], points_new[i][1])
        return output

    #################################################################################################################################################################
    #################################################################################################################################################################
    ###########################################################           run agv              ######################################################################
    #################################################################################################################################################################
    #################################################################################################################################################################

    # load loai lap
    def load_loai_lap(self, data_input):
        for sub_key, sub_value in data_input.items():
            if list(sub_key)[0] == "X":
                loai_lap = "so_luong"
                so_lan_lap = int(float(list(sub_key)[1]))
            else:
                loai_lap = "lien_tuc"
                so_lan_lap = 0
            data_run = data_input[sub_key]
            break
        return loai_lap, so_lan_lap, data_run
    def convert_tin_hieu(self, data_input = "NONE"):
        output = ["",""]
        data = data_input.split("_")
        if len(data) >= 2:
            output = [str(data[0]), str(data[1])]
        return output
    def get_point_info(self, point_name, ds_diem):
        if point_name == "START":
            return {"point_name": "START", "point_coord": [self.vi_tri_x_agv, self.vi_tri_y_agv], "direction": "", "alpha": ""}
        for key, value in ds_diem.items():
            if value["point_name"] == point_name:
                return value
        return None  # Trả về None nếu không tìm thấy điểm
    def get_duong_info(self, ten_duong, ds_duong):
        if ten_duong == "L0":
            return {"ten_duong": "L0", "diem_1": "START", "diem_2": "", "loai_duong": "line_type", "C1": "", "C2": ""}
        for key, value in ds_duong.items():
            if value["ten_duong"] == ten_duong:
                return value
        return None  # Trả về None nếu không tìm thấy đường
    def check_tin_hieu(self, data_check, data_input):
        output = False
        for key, value in data_input.items():
            if key == data_check[0] and str(value) == str(data_check[1]):
                output = True
                break
        return output
    def sub_agv_run(self):
        done_sub = 0
        check_angle_distance = "distance"
        stop = 0
        angle_deg_line = 0
        angle_deg = 0
        distance = 0

        self.convert_data_run_agv["tien_max"] = self.data_run_agv["tien_max"]
        self.convert_data_run_agv["re_max"] = self.data_run_agv["re_max"]
        self.convert_data_run_agv["grid_size"] = self.data_run_agv["grid_size"]
        self.convert_data_run_agv["agv_size"] = self.data_run_agv["agv_size"]
        self.convert_data_run_agv["diem_1"] = self.data_run_agv["diem_1"]["point_coord"]
        self.convert_data_run_agv["diem_2"] = self.data_run_agv["diem_2"]["point_coord"]
        self.convert_data_run_agv["tin_hieu"] = self.data_run_agv["tin_hieu"]

        if self.data_run_agv["diem_2"]["direction"] == "" or self.data_run_agv["diem_2"]["direction"] != "có hướng" or self.data_run_agv["diem_2"]["alpha"] is None or self.data_run_agv["diem_2"]["direction"] is None:
            self.convert_data_run_agv["diem_huong"] = []
        else:
            huong_x = int(self.convert_data_run_agv["diem_2"][0] + 20 * math.cos(-(float(self.data_run_agv["diem_2"]["alpha"])*math.pi/180)))
            huong_y = int(self.convert_data_run_agv["diem_2"][1] + 20 * math.sin(-(float(self.data_run_agv["diem_2"]["alpha"])*math.pi/180)))
            self.convert_data_run_agv["diem_huong"] = [huong_x, huong_y]
        self.convert_data_run_agv["toa_do_agv"] = [int(self.vi_tri_x_agv), int(self.vi_tri_y_agv)]
        self.convert_data_run_agv["diem_huong_agv"] = [int(self.huong_x), int(self.huong_y)]

        start_point = [int(self.vi_tri_x_agv), int(self.vi_tri_y_agv)]
        point_end_vat_can = self.convert_data_run_agv["diem_2"] 
        robot_direction = self.convert_data_run_agv["diem_huong_agv"]
        
        check, distance, angle_deg = tim_duong_di.calculate_distance_and_angle(start_point.copy(), point_end_vat_can, robot_direction)
        if distance > 80:
            img_Astar, max_point_Astar, x_min_Astar, y_min_Astar, x_max_Astar, y_max_Astar = crop_img_Atar.img_crop(self.img1.copy(), start_point.copy(), point_end_vat_can, distance = 80)
            end_point = [max_point_Astar[0],max_point_Astar[1]]
            robot_direction = self.convert_data_run_agv["diem_huong_agv"]
            point_old = self.convert_data_run_agv["diem_1"]
        else:
            end_point = self.convert_data_run_agv["diem_2"]
            robot_direction = self.convert_data_run_agv["diem_huong_agv"]
            point_old = self.convert_data_run_agv["diem_1"]
        # self.check_dis = len(self.list_point_star)

        # if len(self.closest_point_2) != 0 and self.check_dis == 0 and 1 == 2:
        #     self.driver_motor.load_data_sent_drive(int(float(self.convert_data_run_agv["tien_max"])), 0, 0, "distance", 1, self.closest_point_1)
        #     if len(self.point_start_star) == 0:
        #         self.point_start_star = start_point.copy()
        #     list_point_star = []

        #     check_closest, distance_closest, angle_deg_closest = tim_duong_di.calculate_distance_and_angle(start_point.copy(), point_end_vat_can, robot_direction)
        #     if check_closest == True:
        #         img_Astar, max_point_Astar, x_min_Astar, y_min_Astar, x_max_Astar, y_max_Astar = crop_img_Atar.img_crop(self.img1.copy(), start_point.copy(), point_end_vat_can, distance = 80)
        #         # qua gan, dang re, 
        #         print(len(max_point_Astar) , distance_closest , abs(angle_deg_closest))
        #         # kiem tra dieu khien xem gan den dich chua, co dang re hay khong
        #         if len(max_point_Astar) != 0 and distance_closest > 70 and (abs(angle_deg_closest) < 40 or self.check_dis != 0):
        #             point_start = start_point.copy()
        #             point_end = [max_point_Astar[0],max_point_Astar[1]]
                    
        #             self.image_new, list_points, self.grid = A_star.creat_gird(img_Astar, x_min_Astar, y_min_Astar, point_start, point_end,
        #                                                             grid_size = self.grid_size, agv_size = self.agv_size)
        #             # self.list_point_star = list_points
        #             for i in range(0,len(list_points)):
        #                 dis = tim_duong_di.calculate_distance(start_point.copy(),list_points[i])
        #                 if dis > 15:
        #                     list_point_star.append([list_points[i][0],list_points[i][1]])
        #     else:
        #         print("tim duong di: False")
            
        #     if len(list_point_star) != 0:
        #         self.list_point_star = list_point_star
        #         self.stt_check_dis = 0
        #         self.check_dis = len(self.list_point_star)
            
        # if len(self.closest_point_2) == 0 and len(self.point_star_scan) == 0:
        #     self.list_point_star = []
        #     self.stt_check_dis = 0
        #     self.check_dis = 0
        #     self.point_start_star = []
        #     self.star_trai = 0
        #     self.star_phai = 0
        #     self.point_new_star = []
        #     print("reset_tim duong di")
            
        # tinh toan dk agv
        # if self.check_dis == 0:
        #     end_point = self.convert_data_run_agv["diem_2"]
        #     robot_direction = self.convert_data_run_agv["diem_huong_agv"]
        #     point_old = self.convert_data_run_agv["diem_1"]
        # else:
        #     end_point = self.list_point_star[self.stt_check_dis]
        #     robot_direction = self.convert_data_run_agv["diem_huong_agv"]
        #     if self.stt_check_dis == 0:
        #         if len(self.point_star_old) == 0:
        #             self.point_star_old = start_point.copy()
        #     else:
        #         self.point_star_old = self.list_point_star[self.stt_check_dis - 1]
        #     point_old = self.point_star_old
        #     # point_old = self.point_old_tim_duong_di

        #     self.point_new_star = end_point 
        # 
        # 
        


        webserver.list_point_star = self.list_point_star
        
        # print("start_point.copy(), end_point, robot_direction", start_point.copy(), end_point, robot_direction)
        check, distance, angle_deg = tim_duong_di.calculate_distance_and_angle(start_point.copy(), end_point, robot_direction)
        check_line, distance_line, angle_deg_line = tim_duong_di.calculate_distance_and_angle(end_point, point_old, start_point.copy())
        # print("---------",self.point_new_star, self.point_start_star, len(self.list_point_star),self.list_point_star, start_point, self.stt_check_dis)
        self.point_end_star = self.convert_data_run_agv["diem_2"]
        if len(self.point_end_star) != 0 and len(self.point_new_star) != 0 and len(self.point_start_star) != 0:
            check_star, distance_star, angle_deg_star = tim_duong_di.calculate_distance_and_angle(self.point_end_star, self.point_start_star, self.point_new_star)
            if angle_deg_star > 0:
                self.star_phai = 1
            if angle_deg_line <= 0:
                self.star_trai = 1
            # print("angle_deg_star", angle_deg_star)
        # print(angle_deg_line, self.star_trai, self.star_phai) 
        if angle_deg_line > 90:
            angle_deg_line = 180 - angle_deg_line
        if angle_deg_line < -90:
            angle_deg_line = -180 - angle_deg_line

        # print("self.convert_data_run_agnd self.check_dis == 0", self.convert_data_run_agv["run_diem_2"] != "OK" and self.check_dis == 0)
        if self.convert_data_run_agv["run_diem_2"] != "OK":
            check_2, distance_diem_2, angle_deg = tim_duong_di.calculate_distance_and_angle(start_point.copy(), end_point, robot_direction)
            number = 3
            if (distance_diem_2 <= 2 or (distance_diem_2 < number and angle_deg > 20)  or (distance_diem_2 > self.distance_old and self.check_distan_old == 1)) and check_2 == True:
                self.convert_data_run_agv["run_diem_2"] = "OK"
                self.check_distan_old = 0
            if distance_diem_2 < number and distance_diem_2 > 2 and self.convert_data_run_agv["run_diem_2"] != "OK":
                self.check_distan_old = 1
                self.distance_old = distance_diem_2
            if len(self.convert_data_run_agv["diem_huong"]) != 0:
                if distance_diem_2 <= 80:
                    self.scan_dis = 1
        # kiem tra huong cua agv den diem huong
        if self.convert_data_run_agv["run_diem_2"] == "OK":
            self.scan_dis = 0
            if len(self.convert_data_run_agv["diem_huong"]) == 0:
                self.convert_data_run_agv["run_huong"] = "OK"
            else:
                print("angle_check",distance, angle_deg)
                check_angle_distance = "angle"
                start_point = [int(self.vi_tri_x_agv), int(self.vi_tri_y_agv)]
                robot_direction = self.convert_data_run_agv["diem_huong_agv"]
                A = np.array(self.convert_data_run_agv["diem_2"])
                C = np.array(start_point)
                B = np.array(self.convert_data_run_agv["diem_huong"])
                # Tính vector AC
                AC = C - A
                # Tịnh tiến điểm B theo vector AC
                end_point_angle = B + AC
                check_ang, distance_ang, angle_deg = tim_duong_di.calculate_distance_and_angle(start_point, end_point_angle, robot_direction)
                # print(angle_deg, start_point, end_point, robot_direction)
                if abs(angle_deg) <= 1 and check_ang == True:
                    self.convert_data_run_agv["run_huong"] = "OK"
        if self.convert_data_run_agv["tin_hieu"][0] != "":
            if self.check_tin_hieu(self.convert_data_run_agv["tin_hieu"], self.input_esp) != True:
                stop = 1
        if self.convert_data_run_agv["run_diem_2"] == "OK" and self.convert_data_run_agv["run_huong"] == "OK":
            # reset_data = 0
            # if self.convert_data_run_agv["tin_hieu"][0] != "":
            #     if self.check_tin_hieu(self.convert_data_run_agv["tin_hieu"], self.input_esp) == True:
            #         reset_data = 1
            #     else:
            #         stop = 1
            # else:
            reset_data = 1
            if self.check_dis > 0:
                # self.point_old_tim_duong_di = end_point
                self.stt_check_dis = self.stt_check_dis + 1
                if self.stt_check_dis > self.check_dis - 1:
                    self.list_point_star = []
                    self.stt_check_dis = 0
                    self.check_dis = 0
                    self.point_start_star = []
                    self.star_trai = 0
                    self.star_phai = 0
                    self.point_new_star = []
            else:
                if reset_data == 1:
                    done_sub = 1
                    self.list_point_star = []
                    self.stt_check_dis = 0
                    self.check_dis = 0
                    self.point_start_star = []
                    self.star_trai = 0
                    self.star_phai = 0
                    self.point_new_star = []
                else:
                    stop = 1
            if reset_data == 1 or self.check_dis > 0:
                self.convert_data_run_agv = self.convert_data_run_agv0.copy()
        if check_angle_distance == "distance":
            goc_quay_check = angle_deg - angle_deg_line
        else:
            goc_quay_check = angle_deg
        # print(angle_deg, angle_deg_line, goc_quay_check)
        # if goc_quay_check > 90:
        #     goc_quay_check = 180 - goc_quay_check
        # if goc_quay_check < -90:
        #     goc_quay_check = -180 - goc_quay_check
        if on_music == 1:
            if angle_deg < -60:
                music.name_music = "re_phai"
            else:
                if music.name_music == "re_phai":
                    music.name_music = "none"

            if angle_deg > 60:
                music.name_music = "re_trai"
            else:
                if music.name_music == "re_trai":
                    music.name_music = "none"
        # print("----------------- sent_data ---------------------")
        print(int(float(self.convert_data_run_agv["tien_max"])), distance, goc_quay_check, check_angle_distance, stop, self.closest_point_1, angle_deg)
        self.driver_motor.load_data_sent_drive(int(float(self.convert_data_run_agv["tien_max"])), 
                                               distance, goc_quay_check, 
                                               check_angle_distance, stop, self.closest_point_1, tim_duong = self.check_dis, v_re=self.van_toc_re_max)
        


        
        return done_sub
    def run_agv(self):
        # global data_run_agv0, data_run_agv, stt_sub, stt_sub_old, done_sub, ds_diem, ds_duong, dict_data, stt, convert_data_run_agv
        self.danh_sach_diem = webserver.danh_sach_diem
        self.danh_sach_duong = webserver.danh_sach_duong
        self.data_run_agv["tien_max"] = self.van_toc_max_tien
        self.data_run_agv["re_max"] = self.van_toc_re_max
        self.data_run_agv["grid_size"] = self.grid_size
        self.data_run_agv["agv_size"] = self.agv_size
        if self.stt < len(self.dict_data):
            self.data_run_agv["run_agv"] = 1
            data = self.dict_data[str(self.stt)] #{"X0": [["START","L0","P1","NONE"]]} ###########################################
            if self.data_run_agv["loai_lap"] == "":
                loai_lap, so_lan_lap, data_run = self.load_loai_lap(data)
                self.data_run_agv["loai_lap"] = loai_lap
                self.data_run_agv["so_lan_lap"] = so_lan_lap
                self.data_run_agv["data_run"] = data_run
            if self.stt_sub < len(self.data_run_agv["data_run"]):
                if self.stt_sub != self.stt_sub_old:
                    self.stt_sub_old = self.stt_sub
                    self.data_sub_run = self.data_run_agv["data_run"][self.stt_sub]
                    # Lấy thông tin điểm từ ds_diem
                    value_info_1 = self.get_point_info(self.data_sub_run[0], self.danh_sach_diem)
                    self.data_run_agv["diem_1"] = value_info_1
                    # Lấy thông tin điểm từ ds_diem
                    value_info_2 = self.get_point_info(self.data_sub_run[2], self.danh_sach_diem)
                    self.data_run_agv["diem_2"] = value_info_2
                    # Lấy thông tin đường từ ds_duong
                    value_info_3 = self.get_duong_info(self.data_sub_run[1], self.danh_sach_duong)
                    self.data_run_agv["duong_di"] = value_info_3
                    self.data_run_agv["tin_hieu"] = self.convert_tin_hieu(self.data_sub_run[3])

                ############### dk agv #####################
                
                self.done_sub = self.sub_agv_run()
                # print("kkk")
                ################################# dk agv #######################################

                # di đến điểm đích của từng phần tử trong list đường đi
                if self.done_sub == 1:
                    self.stt_sub = self.stt_sub + 1
                    self.done_sub = 0
                    self.scan_dis = 0
                
            else: # đã đi hết danh sách đường đi
                # nếu là lặp liên tục
                if self.stt_sub >= len(self.data_run_agv["data_run"]) and self.data_run_agv["loai_lap"] == "lien_tuc":
                    self.stt_sub = 0
                    self.stt_sub_old = -1
                    self.data_run_agv = self.data_run_agv0.copy()

                # nếu là lặp số lượng    
                if self.data_run_agv["so_lan_lap"] >= 1:
                    self.data_run_agv["so_lan_lap"] = self.data_run_agv["so_lan_lap"] - 1
                    self.stt_sub = 0
                    self.stt_sub_old = -1
                if self.data_run_agv["loai_lap"] == "so_luong" and self.data_run_agv["so_lan_lap"] == 0:
                    self.stt_sub = 0
                    self.stt_sub_old = -1
                    self.stt = self.stt + 1
                    self.data_run_agv = self.data_run_agv0.copy()
            
        else:
            
            self.data_run_agv = self.data_run_agv0.copy()
            self.data_run_agv["run_agv"] = 0
            # print(int(float(self.convert_data_run_agv["tien_max"])), 0, 0, "distance", 1, self.closest_point_1)
            self.driver_motor.load_data_sent_drive(int(float(self.convert_data_run_agv["tien_max"])), 0, 0, "distance", 1, self.closest_point_1)
    def dk_ban_phim(self,data_input):
        # print(self.dk_agv_thu_cong)
        if self.dk_agv_thu_cong == 1:
            if data_input != "":
                if self.connect_driver == True:
                    # print(data_input)
                    if data_input == "stop":
                        self.driver_motor.sent_data_controller(vt_trai = 0, vt_phai = 0)
                    if data_input == "tien":
                        self.driver_motor.sent_data_controller(vt_trai = self.van_toc_max_tien, vt_phai = self.van_toc_max_tien)
                    if data_input == "trai":
                        self.driver_motor.sent_data_controller(vt_trai = -int(self.van_toc_max_tien/4), vt_phai = int(self.van_toc_max_tien/4))
                    if data_input == "phai":
                        self.driver_motor.sent_data_controller(vt_trai = int(self.van_toc_max_tien/4), vt_phai = -int(self.van_toc_max_tien/4))
                    if data_input == "dich_tien_trai":
                        self.driver_motor.sent_data_controller(vt_trai = int((self.van_toc_max_tien/4)*3), vt_phai = self.van_toc_max_tien)
                    if data_input == "dich_tien_phai":
                        self.driver_motor.sent_data_controller(vt_trai = self.van_toc_max_tien, vt_phai = int((self.van_toc_max_tien/4)*3))

                    if data_input == "lui":
                        self.driver_motor.sent_data_controller(vt_trai = -self.van_toc_max_tien, vt_phai = -self.van_toc_max_tien)
                    if data_input == "dich_lui_trai":
                        self.driver_motor.sent_data_controller(vt_trai = -self.van_toc_max_tien, vt_phai = -(self.van_toc_max_tien/3))
                    if data_input == "dich_lui_phai":
                        self.driver_motor.sent_data_controller(vt_trai = -int(self.van_toc_max_tien/3), vt_phai = -int(self.van_toc_max_tien))
        
    def reset_duong_di_chuyen(self):
        if self.reset_duong_di == 1:
            self.reset_duong_di = 0

            # self.point_setup = []
            # self.loai_lap = []
            # self.so_lan_lap = 0
            self.run_stop = "stop"

            self.ds_dich_setup = []
            self.ds_duong_di_setup = []
            self.ds_duong_di_dich_setup = []
            self.trang_thai_tien_lui_setup = "tien"
            self.distan_setup = 1000
            self.point_old_setup = []
            self.upload_run_setup, self.trang_thai_lui_phai_setup, self.done_setup,\
                self.trang_thai_lui_trai_setup, self.trang_thai_goc_setup = np.zeros(5)
        
            self.ds_dich_main = []
            self.ds_duong_di_main = []
            self.ds_duong_di_dich_main = []
            self.trang_thai_tien_lui_main = "tien"
            self.distan_main = 1000
            self.point_old_main = []
            self.upload_run_main, self.trang_thai_lui_phai_main, self.done_main,\
                self.trang_thai_lui_trai_main, self.trang_thai_goc_main = np.zeros(5)
            self.stt_main = 0

            # self.trang_thai_tien_lui_an_toan = "tien"
        
            # print(self.goc_banh_xe)


    def load_xy_map_all(self, black_points, min_x = 0, min_y = 0, max_x = 0, max_y = 0, crop = 1):
        # Lọc các điểm có x > 500, y > 500 và x < 1000, y < 1000
        if crop == 1:
            filtered_points = black_points[(black_points[:, 1] > min_x) & (black_points[:, 0] > min_y) & 
                                            (black_points[:, 1] < max_x) & (black_points[:, 0] < max_y)]
        else:
            filtered_points = black_points

        map_all_px = filtered_points[:, 1]
        map_all_py = filtered_points[:, 0]
        return map_all_px, map_all_py
    
    def agv_to_pc(self):
        self.grid_size = int(float(webserver.data_cai_dat["grid_size"]))
        self.agv_size = int(float(webserver.data_cai_dat["agv_size"]))
        self.van_toc_max_tien = int(float(webserver.data_cai_dat["tien_max"]))
        self.van_toc_re_max = int(float(webserver.data_cai_dat["re_max"]))

        # data_chon_ban_do = {"update": 0, "map_file_path": "", "add_all_point": 0,"name_map": ""}
        # data_ban_do_moi = {"reset": 0, "start_stop": "stop", "path_new_map": "", "save": 0, "name_map": ""}
        # data_vi_tri_agv = {"x": 0, "y": 0, "angle": 0, "update": 0}
        if self.update_vi_tri_agv_ban_dau == 0:
            self.update_vi_tri_agv_ban_dau = int(float(webserver.data_ban_do_moi["reset"]))
        if self.update_vi_tri_agv_ban_dau == 1:
            self.add_all_point = 1

        # self.add_all_point thêm các điểm mới vào bản đồ đang có

        self.x_new_map = int(float(webserver.data_vi_tri_agv["x"]))
        self.y_new_map = int(float(webserver.data_vi_tri_agv["y"]))
        self.ang_new_map = float(webserver.data_vi_tri_agv["angle"])
        if int(float(webserver.data_vi_tri_agv["update_vi_tri_agv"])) != 0:
            self.update_vi_tri_agv = int(float(webserver.data_vi_tri_agv["update_vi_tri_agv"]))

        if int(float(webserver.data_vi_tri_agv["update"])) == 1:
            self.update_vi_tri_agv = 0
            webserver.data_vi_tri_agv["update"] = 0

        # lay map cu da luu
        if int(float(webserver.data_chon_ban_do["update"])) == 1: 
            self.map_all = np.load(webserver.data_chon_ban_do["map_file_path"])
            # self.black_points = np.argwhere(np.all(self.map_all[:, :, :3] == [0, 0, 0], axis=-1))
            # self.map_all_px, self.map_all_py = self.load_xy_map_all(self.black_points, crop = 0)

            self.add_all_point = int(float(webserver.data_chon_ban_do["add_all_point"]))

        self.run_stop = webserver.run_stop


        # gửi ảnh qua webserver
        webserver.map_all = self.map_all.copy()

        webserver.img1 = self.img1.copy()
        webserver.x_goc = int(self.vi_tri_x_agv)
        webserver.y_goc = int(self.vi_tri_y_agv)
        webserver.angle_goc = int(180 + self.rotation*180/np.pi)
        
    