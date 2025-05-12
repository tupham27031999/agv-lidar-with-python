from support_main.lib_main import remove, load_data_csv, edit_csv_tab, convert
# from support_main.connect_lidar import main_lidar
from support_main import process_lidar_driver, music, edit_file_json, connect_lidar_sick
import numpy as np
import cv2, os, time
import threading
import path
import A_star
from pynput import keyboard
from webserver import app
import webserver
# import ket_noi_esp



new_map = 1
x,y,angle = np.zeros(3)
anpha_scan = [130,200]
cong_esp32_1 = "COM7"
pause_esp32_1 = 256000
window_size = 500
window_size_all = 1000
scaling_factor = 0.03
rmse1 = 4
rmse2 = 2
run_while = True

# host = 'localhost'
host = "192.168.11.1"
port = 5000

def edit_path(input):
    output = ""
    for i in input:
        if i == "\\":
            output = output + "/"
        else:
            output = output + i
    return output

path_phan_mem = path.path_phan_mem

path_admin = path_phan_mem + "/setting/admin_window.csv"
if os.name == "nt":
    print("Hệ điều hành là Windows")
    # Đọc file cài đặt cho Windows
    path_admin = path_phan_mem + "/setting/admin_window.csv"
elif os.name == "posix":
    print("Hệ điều hành là Ubuntu (Linux)")
    # Đọc file cài đặt cho Ubuntu
    path_admin = path_phan_mem + "/setting/admin_ubuntu.csv"

data_admin = edit_csv_tab.load_all_stt(path_admin)
# PLC_connect = str(int("100000000", 2))
# PLC_disconnect = str(int("110000000", 2))
PLC_connect = "data#256"
PLC_disconnect = "data#384"
path_folder_scan_lidar = path_phan_mem + "/data_input_output/scan_lidar_2"
remove.tao_folder(path_folder_scan_lidar)


for i in range(0,len(data_admin)):
    if len(data_admin[i]) > 1:
        if data_admin[i][0] == "cong_esp32_1":
            cong_esp32_1 = data_admin[i][1]
            pause_esp32_1 = int(float(data_admin[i][2]))
        if data_admin[i][0] == "window_size":
            window_size = int(float(data_admin[i][1]))
        if data_admin[i][0] == "window_size_all":
            window_size_all = int(float(data_admin[i][1]))
        if data_admin[i][0] == "scaling_factor":
            # scaling_factor = float(data_admin[i][1])
            scaling_factor = 0.05
        if data_admin[i][0] == "rmse1":
            rmse1 = int(float(data_admin[i][1]))
        if data_admin[i][0] == "rmse2":
            rmse2 = int(float(data_admin[i][1]))
        if data_admin[i][0] == "cong_lidar":
            cong_lidar = data_admin[i][1]
            pause_lidar = int(float(data_admin[i][2]))
        if data_admin[i][0] == "rmse2":
            rmse2 = int(float(data_admin[i][1]))
        if data_admin[i][0] == "host":
            host = data_admin[i][1]
        if data_admin[i][0] == "port":
            port = int(float(data_admin[i][1]))
print(host, port, "ggg")

class support_main:
    def __init__(self,window_size,window_size_all,scaling_factor,rmse1,rmse2):
        # self.cap = cv2.VideoCapture(0)

        # self.scan_lidar = main_lidar(cong_lidar ,pause_lidar)
        # try:
        #     pass
        #     threading.Thread(target=ket_noi_esp.python_esp32).start() ######`##################
        # except OSError as e:
        #     print("khong ket noi duoc esp")
        #     pass

        # threading.Thread(target=ket_noi_esp.python_esp32).start() ######`##################
        # self.py_esp = ket_noi_esp.Python_Esp()
        # self.py_esp.khai_bao_serial()
        self.time_esp32 = time.time()

        self.window_size,self.window_size_all,self.scaling_factor,self.rmse1,self.rmse2 = [window_size,window_size_all,scaling_factor,rmse1,rmse2]
        self.detect_lidar = process_lidar_driver.process_data_lidar()
        print(self.window_size,self.window_size,self.window_size_all,self.window_size_all,
                                       self.scaling_factor,self.rmse1,self.rmse2)
        self.detect_lidar.setting_data(self.window_size,self.window_size,self.window_size_all,self.window_size_all,
                                       self.scaling_factor,self.rmse1,self.rmse2)
        self.connect_while = True

        self.manual_mode = False
        self.data_dk_tay = "stop"
        self.sent_data = ""
        self.key_states = {}
        self.tien, self.lui, self.trai, self.phai, self.stop = np.zeros(5)
        self.ss_dk = 0
        self.stt_scan = 0

        # Khởi động listener cho bàn phím
        listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        listener.start()

        self.time_dk_tay = 0
        self.stop_lidar = 0
        self.lidar_sick = connect_lidar_sick.LidarP()
        threading.Thread(target=self.lidar_sick.process_data).start()
    def main_loop(self):
        # self.scan_lidar.connect()
        # self.scan_lidar.time_close = time.time()
        # scan,check = self.scan_lidar.return_data()
        # if len(scan[0]) > 1:  # map goc
        #     self.detect_lidar.process_data_lidar(np.array(scan))
        #     # np.save(path_folder_scan_lidar + "/scan_" + str(self.stt_scan) + ".npy",scan)
        #     # self.stt_scan = self.stt_scan + 1

        # list_data = os.listdir(path_folder_scan_lidar)
        # if self.stt_scan < len(list_data):
        #     scan = np.load(path_folder_scan_lidar + "/scan_"+ str(self.stt_scan) +".npy")
        #     # print(scan)
        #     if self.stop_lidar == 0:
        #         self.stt_scan = self.stt_scan + 1
        # else:
        #     self.connect_while = False
        # if self.connect_while == True:
        #     if len(scan[0]) > 1:  # map goc
        #         self.detect_lidar.process_data_lidar(np.array(scan))

        

        scan = self.lidar_sick.get_data()
        if len(scan) != 0:
            if len(scan[0]) > 1:  # map goc
                self.detect_lidar.process_data_lidar(np.array(scan))

        # ket_noi_esp.while_esp()
        self.show_img()
        self.detect_lidar.main_loop()
        

    
    
    def show_img(self):
        data_sent_esp = ""
        img = self.detect_lidar.img2

        connect = True
        if self.detect_lidar.connect_driver == True:
            cv2.putText(img, "Driver:    connected", (400, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            cv2.putText(img, "Driver:    disconnected", (400, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            connect = False

        if connect == True or self.detect_lidar.dk_agv_thu_cong == 1:
            data_sent_esp = data_sent_esp + PLC_connect
        else:
            data_sent_esp = data_sent_esp + PLC_disconnect


        # cv2.putText(img, "Goc agv: " + str(self.detect_lidar.goc_agv) + " || " + str(int(self.detect_lidar.delta_distan)) + " || " + str(self.detect_lidar.delta_angle), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(img, str(self.detect_lidar.trang_thai_agv), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        cv2.putText(img, "Sai so: " + str(int(self.detect_lidar.rmse*100)/100), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        if self.manual_mode or webserver.dk_agv_thu_cong == 1:
            cv2.putText(img, "Dieu khien tay: ON", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
            self.detect_lidar.dk_agv_thu_cong = 1
            if webserver.dk_agv_thu_cong == 1:
                self.data_dk_tay = "stop"
                # {'tien': 1, 'lui': 0, 'trai': 0, 'phai': 0, 'stop': 0}
                data_dk = webserver.data_dk_tay

                if data_dk["tien"] == 1:
                    if data_dk["trai"] == 0 and data_dk["phai"] == 0:
                        self.data_dk_tay = "tien"
                    if data_dk["trai"] == 1:
                        self.data_dk_tay = "dich_tien_trai"
                    if data_dk["phai"] == 1:
                        self.data_dk_tay = "dich_tien_phai"
                if data_dk["lui"] == 1:
                    if data_dk["trai"] == 0 and data_dk["phai"] == 0:
                        self.data_dk_tay = "lui"
                    if data_dk["trai"] == 1:
                        self.data_dk_tay = "dich_lui_trai"
                    if data_dk["phai"] == 1:
                        self.data_dk_tay = "dich_lui_phai"
                if data_dk["tien"] == 0 and data_dk["lui"] == 0:
                    if data_dk["trai"] == 1:
                        self.data_dk_tay = "trai"
                    if data_dk["phai"] == 1:
                        self.data_dk_tay = "phai"
            # print(self.data_dk_tay)
            self.detect_lidar.data_dk_ban_phim = self.data_dk_tay
        else:
            self.detect_lidar.dk_agv_thu_cong = 0
            self.dedata_dk_tay = ""

        cv2.imshow("img_Astar",self.detect_lidar.image_new)
        cv2.imshow("map",img)
        # Xử lý sự kiện bàn phím
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            if self.stop_lidar == 0:
                self.stop_lidar = 1
            else:
                self.stop_lidar = 0

        
        
        # Xử lý sự kiện bàn phím
        if key == ord('s'):
            self.manual_mode = not self.manual_mode
        # Xử lý sự kiện bàn phím
        if self.key_states.get(keyboard.Key.up, False):  # tiến
            self.tien = 1
            self.time_dk_tay = time.time()
        else:
            self.tien = 0
        if self.key_states.get(keyboard.Key.down, False):  # lùi
            self.lui = 1
            self.time_dk_tay = time.time()
        else:
            self.lui = 0
        if self.key_states.get(keyboard.Key.left, False):  # trái
            self.trai = 1
            self.time_dk_tay = time.time()
        else:
            self.trai = 0
        if self.key_states.get(keyboard.Key.right, False):  # phải
            self.phai = 1
            self.time_dk_tay = time.time()
        else:
            self.phai = 0
        if self.tien == 0 and self.lui == 0 and self.trai == 0 and self.phai == 0 and (self.time_dk_tay == 0 or time.time() - self.time_dk_tay > 1):  # stop
            self.stop = 1
        
        if self.stop == 1:
            self.data_dk_tay = "stop"
        if self.tien == 1:
            if self.trai == 0 and self.phai == 0:
                self.data_dk_tay = "tien"
            if self.trai == 1:
                self.data_dk_tay = "dich_tien_trai"
            if self.phai == 1:
                self.data_dk_tay = "dich_tien_phai"
        if self.lui == 1:
            if self.trai == 0 and self.phai == 0:
                self.data_dk_tay = "lui"
            if self.trai == 1:
                self.data_dk_tay = "dich_lui_trai"
            if self.phai == 1:
                self.data_dk_tay = "dich_lui_phai"
        if self.tien == 0 and self.lui == 0:
            if self.trai == 1:
                self.data_dk_tay = "trai"
            if self.phai == 1:
                self.data_dk_tay = "phai"

        if key == ord('q') or run_while == False or cv2.getWindowProperty('map', cv2.WND_PROP_VISIBLE) < 1:
            music.disconnect_sound()
            # ket_noi_esp.close_serial()
            # self.scan_lidar.disconnect()
            self.lidar_sick.connect = False
            # self.disconnect_esp32()
            if type(self.detect_lidar.driver_motor) != type("str"):
                self.detect_lidar.driver_motor.disconnect()
            self.connect_while = False
            
    def on_press(self, key):
        try:
            self.key_states[key.char] = True
        except AttributeError:
            self.key_states[key] = True

    def on_release(self, key):
        try:
            self.key_states[key.char] = False
        except AttributeError:
            self.key_states[key] = False



# Hàm để chạy Flask trong một luồng riêng
def run_flask():
    app.run(host=host, port=port, debug=True, use_reloader=False)

# Tạo đối tượng detect
# detect = support_main(window_size, window_size_all, scaling_factor, 6, 4)
detect = support_main(window_size, window_size_all, scaling_factor, rmse1, rmse2)

if __name__ == "__main__":
    # Chạy Flask trong một luồng riêng
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    # Vòng lặp chính
    while detect.connect_while:
        detect.main_loop()
    
    
    
    
                
                
            
